# -*- coding: utf-8 -*-
"""
Prueba objetiva de COEXISTENCIA - ISO/IEC 25010:2023 (Compatibilidad), Semana 11.

Protocolo (diapositivas 19-21 del curso):
  A. Ejecutar el servicio A (API LeoFit) solo y medir solicitudes de referencia.
  B. Ejecutar el servicio B (Reportes) con carga conocida y medir su línea base.
  C. Repetir las solicitudes de A mientras B está bajo carga (impacto B -> A).
  D. Repetir las solicitudes de B mientras A está bajo carga (impacto A -> B).
  E. Registrar latencias, tasa de error y CPU/RAM; calcular variación %.

Variación (%) = 100 x (simultáneo - base) / base. Si base = 0, se usa diferencia absoluta.

Requisitos previos:
  - API LeoFit (servicio A) ejecutándose en http://127.0.0.1:4000
  - Python: requests, psutil

Uso:
  python scripts/iso25010/run_coexistence_benchmark.py [--single-core]

Salida (evidencia reproducible):
  docs/gestion_academica/evidencias/iso25010_s10_s11/coexistencia/
    - coexistence_raw.csv       (cada solicitud medida)
    - coexistence_resources.csv (muestreo CPU/RAM cada 0.5 s)
    - coexistence_summary.json  (métricas consolidadas + entorno)
    - coexistence_log.txt       (bitácora legible de la ejecución)
"""
import argparse
import csv
import base64
import datetime as dt
import hashlib
import hmac
import json
import os
import platform
import statistics
import subprocess
import sys
import threading
import time
import uuid

import psutil
import requests

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
OUT_DIR = os.path.join(ROOT, 'docs', 'gestion_academica', 'evidencias', 'iso25010_s10_s11', 'coexistencia')
A_BASE = 'http://127.0.0.1:4000/api'
B_PORT = 4100
B_BASE = f'http://127.0.0.1:{B_PORT}'

# Umbrales definidos por el equipo ANTES de ejecutar (consignados en la Tabla 20 del informe)
THRESHOLD_LATENCY_PCT = 15.0      # variación máxima de latencia media aceptada
THRESHOLD_ERROR_PCT = 0.5         # tasa de error máxima aceptada (absoluta)
THRESHOLD_CPU_PCT = 70.0          # CPU pico máxima por proceso (% de un núcleo)
THRESHOLD_RAM_MB = 450.0          # RSS pico máximo por proceso

N_READS = 200
N_WRITES = 60
N_REPORTS = 100
BG_CONCURRENCY = 4

LOG_LINES = []


def log(msg):
    stamp = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    line = f'[{stamp}] {msg}'
    print(line, flush=True)
    LOG_LINES.append(line)


# ---------------------------------------------------------------------------
# JWT HS256 (misma configuración que backend/src/infrastructure/security/jwt.utils.ts)
# El secreto se lee de backend/.env y NUNCA se imprime ni se guarda en la evidencia.
# ---------------------------------------------------------------------------
def read_env_secret():
    env_path = os.path.join(ROOT, 'backend', '.env')
    with open(env_path, encoding='utf-8', errors='ignore') as fh:
        for line in fh:
            if line.strip().startswith('JWT_SECRET='):
                return line.strip().split('=', 1)[1].strip().strip('"').strip("'")
    raise RuntimeError('JWT_SECRET no definido en backend/.env')


def b64url(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b'=').decode()


def make_token(secret):
    now = int(time.time())
    header = {'alg': 'HS256', 'typ': 'JWT', 'kid': 'v1'}
    payload = {'userId': 1, 'id': 1, 'sub': 1, 'email': 'admin@leofit.pe', 'name': 'Benchmark Coexistencia',
               'role': 'ADMIN', 'iat': now, 'exp': now + 3600, 'iss': 'leofit', 'aud': 'leofit-app'}
    signing_input = f"{b64url(json.dumps(header, separators=(',', ':')).encode())}.{b64url(json.dumps(payload, separators=(',', ':')).encode())}"
    sig = hmac.new(secret.encode(), signing_input.encode(), hashlib.sha256).digest()
    return f'{signing_input}.{b64url(sig)}'


# ---------------------------------------------------------------------------
# Utilidades de medición
# ---------------------------------------------------------------------------
def pid_listening_on(port):
    for conn in psutil.net_connections(kind='tcp'):
        if conn.laddr and conn.laddr.port == port and conn.status == psutil.CONN_LISTEN and conn.pid:
            return conn.pid
    return None


def timed(method, url, expected, **kw):
    t0 = time.perf_counter()
    try:
        r = requests.request(method, url, timeout=15, **kw)
        ms = (time.perf_counter() - t0) * 1000
        return ms, r.status_code, r.status_code == expected, r
    except Exception as exc:  # timeout, conexión rechazada, etc.
        ms = (time.perf_counter() - t0) * 1000
        return ms, 0, False, exc


def summarize(samples):
    lat = [s['ms'] for s in samples]
    errors = sum(1 for s in samples if not s['ok'])
    lat_sorted = sorted(lat)
    p95 = lat_sorted[max(0, int(round(0.95 * len(lat_sorted))) - 1)]
    return {
        'n': len(samples),
        'mean_ms': round(statistics.mean(lat), 2),
        'median_ms': round(statistics.median(lat), 2),
        'p95_ms': round(p95, 2),
        'min_ms': round(min(lat), 2),
        'max_ms': round(max(lat), 2),
        'errors': errors,
        'error_pct': round(100.0 * errors / len(samples), 2),
    }


def variation(base, sim):
    if base == 0:
        return round(sim - base, 2), 'abs'
    return round(100.0 * (sim - base) / base, 2), 'pct'


class ResourceSampler(threading.Thread):
    """Muestrea CPU (% de un núcleo) y RSS (MB) de los procesos A y B cada 0.5 s."""

    def __init__(self, procs):
        super().__init__(daemon=True)
        self.procs = procs  # {'A': psutil.Process, 'B': psutil.Process}
        self.rows = []
        self.phase = 'init'
        self._stop = threading.Event()
        for p in procs.values():
            if p:
                p.cpu_percent(None)

    def run(self):
        while not self._stop.is_set():
            time.sleep(0.5)
            stamp = time.time()
            for name, p in self.procs.items():
                if not p:
                    continue
                try:
                    self.rows.append({'t': round(stamp, 3), 'phase': self.phase, 'service': name,
                                      'cpu_pct': p.cpu_percent(None),
                                      'rss_mb': round(p.memory_info().rss / 1048576, 1)})
                except psutil.Error:
                    pass

    def stop(self):
        self._stop.set()

    def stats(self, phase, service):
        rows = [r for r in self.rows if r['phase'] == phase and r['service'] == service]
        if not rows:
            return {'cpu_mean': 0, 'cpu_peak': 0, 'rss_mean_mb': 0, 'rss_peak_mb': 0}
        return {
            'cpu_mean': round(statistics.mean(r['cpu_pct'] for r in rows), 1),
            'cpu_peak': round(max(r['cpu_pct'] for r in rows), 1),
            'rss_mean_mb': round(statistics.mean(r['rss_mb'] for r in rows), 1),
            'rss_peak_mb': round(max(r['rss_mb'] for r in rows), 1),
        }


class DockerSampler(threading.Thread):
    """Muestrea CPU/RAM del contenedor PostgreSQL (si existe) con `docker stats --no-stream`."""

    def __init__(self, container='leofit_postgres'):
        super().__init__(daemon=True)
        self.container = container
        self.rows = []
        self.phase = 'init'
        self._stop = threading.Event()
        self.available = False
        try:
            out = subprocess.check_output(['docker', 'inspect', '-f', '{{.State.Running}}', container],
                                          text=True, stderr=subprocess.DEVNULL).strip()
            self.available = out == 'true'
        except Exception:
            self.available = False

    def run(self):
        while self.available and not self._stop.is_set():
            try:
                out = subprocess.check_output(
                    ['docker', 'stats', '--no-stream', '--format', '{{.CPUPerc}};{{.MemUsage}}', self.container],
                    text=True, stderr=subprocess.DEVNULL).strip()
                cpu, mem = out.split(';')
                used = mem.split('/')[0].strip()
                val = float(''.join(ch for ch in used if ch.isdigit() or ch == '.'))
                mb = val * 1024 if 'GiB' in used else (val / 1024 if 'KiB' in used else val)
                self.rows.append({'t': round(time.time(), 3), 'phase': self.phase, 'service': 'PostgreSQL',
                                  'cpu_pct': float(cpu.strip().rstrip('%')), 'rss_mb': round(mb, 1)})
            except Exception:
                time.sleep(0.5)

    def stop(self):
        self._stop.set()

    def stats(self, phase):
        rows = [r for r in self.rows if r['phase'] == phase]
        if not rows:
            return None
        return {
            'cpu_mean': round(statistics.mean(r['cpu_pct'] for r in rows), 1),
            'cpu_peak': round(max(r['cpu_pct'] for r in rows), 1),
            'rss_mean_mb': round(statistics.mean(r['rss_mb'] for r in rows), 1),
            'rss_peak_mb': round(max(r['rss_mb'] for r in rows), 1),
        }


class BackgroundLoad:
    """Carga conocida: BG_CONCURRENCY hilos repitiendo una solicitud hasta detenerse."""

    def __init__(self, fn, concurrency):
        self.fn = fn
        self.concurrency = concurrency
        self.stop_evt = threading.Event()
        self.count = 0
        self.errors = 0
        self.lock = threading.Lock()
        self.threads = []

    def _worker(self):
        while not self.stop_evt.is_set():
            ok = self.fn()
            with self.lock:
                self.count += 1
                if not ok:
                    self.errors += 1

    def __enter__(self):
        for _ in range(self.concurrency):
            t = threading.Thread(target=self._worker, daemon=True)
            t.start()
            self.threads.append(t)
        time.sleep(1.5)  # estabilizar la carga antes de medir
        return self

    def __exit__(self, *exc):
        self.stop_evt.set()
        for t in self.threads:
            t.join(timeout=20)


# ---------------------------------------------------------------------------
# Programa principal
# ---------------------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--single-core', action='store_true',
                        help='Fija A y B al mismo núcleo lógico para emular la vCPU compartida del host de producción')
    args = parser.parse_args()

    os.makedirs(OUT_DIR, exist_ok=True)
    started = dt.datetime.now()
    log('=== PRUEBA DE COEXISTENCIA ISO/IEC 25010 - LeoFit (Servicio A: API) vs Reportes (Servicio B) ===')

    # --- Servicio A ---
    health = requests.get(f'{A_BASE}/health', timeout=10).json()
    a_pid = pid_listening_on(4000)
    if not a_pid:
        sys.exit('No se encontró el proceso del servicio A escuchando en el puerto 4000')
    proc_a = psutil.Process(a_pid)
    log(f'Servicio A detectado: PID {a_pid} ({proc_a.name()}), health={json.dumps(health, ensure_ascii=False)[:300]}')

    token = make_token(read_env_secret())
    auth = {'Authorization': f'Bearer {token}'}

    # Preparar datos de escritura: variantes con stock suficiente
    prods = requests.get(f'{A_BASE}/products', timeout=10).json()
    plist = prods.get('data', prods) if isinstance(prods, dict) else prods
    if isinstance(plist, dict):
        plist = plist.get('products') or plist.get('items') or []
    candidates = []
    for p in plist:
        price = p.get('base_price') or p.get('price') or p.get('basePrice')
        for v in p.get('variants', []) or []:
            if (v.get('stock') or 0) >= 10 and price:
                candidates.append((v['id'], float(price), v['stock']))
    candidates.sort(key=lambda c: -c[2])
    if not candidates:
        sys.exit('No hay variantes con stock suficiente para las pruebas de escritura')
    candidates = candidates[:5]
    log(f'Catálogo: {len(plist)} productos; variantes usadas para escritura: {[c[0] for c in candidates]}')

    write_idx = {'i': 0}

    def replenish_stock():
        for vid, _, _ in candidates:
            try:
                requests.patch(f'{A_BASE}/products/variant/{vid}/stock', json={'quantityDelta': 500}, headers=auth, timeout=5)
            except Exception:
                pass
    replenish_stock()

    def do_read():
        return timed('GET', f'{A_BASE}/products', 200)

    def do_write():
        vid, price, _ = candidates[write_idx['i'] % len(candidates)]
        write_idx['i'] += 1
        body = {'clientId': 1, 'paymentMethod': 'YAPE', 'shippingCost': 0, 'shippingType': 'LIMA',
                'notes': 'Benchmark coexistencia ISO 25010 (dato sintetico)',
                'items': [{'variantId': vid, 'quantity': 1, 'unitPrice': price}]}
        use_idempotency = health.get('database', {}).get('status') != 'DEGRADED'
        headers = dict(auth)
        if use_idempotency:
            headers['Idempotency-Key'] = f'coex{uuid.uuid4().hex}'
        return timed('POST', f'{A_BASE}/orders', 201, json=body, headers=headers)

    def do_report():
        return timed('GET', f'{B_BASE}/report', 200)

    raw = []

    def series(phase, label, fn, n):
        out = []
        for i in range(n):
            ms, status, ok, resp = fn()
            row = {'phase': phase, 'request': label, 'seq': i + 1, 'ms': round(ms, 2), 'status': status, 'ok': ok}
            if not ok and len([r for r in out if not r['ok']]) < 3:
                detail = resp.text[:200] if hasattr(resp, 'text') else str(resp)[:200]
                log(f'  [{phase}] {label} #{i + 1} -> HTTP {status} (no esperado): {detail}')
            out.append(row)
            raw.append(row)
        s = summarize(out)
        log(f'  [{phase}] {label}: n={s["n"]} media={s["mean_ms"]} ms p95={s["p95_ms"]} ms errores={s["errors"]}')
        return s

    # Calentamiento A (descartado)
    for _ in range(10):
        do_read()
    do_write()

    # --- Iniciar servicio B ---
    b_proc = subprocess.Popen(['node', os.path.join(ROOT, 'scripts', 'iso25010', 'service_b_reportes.js'), str(B_PORT)],
                              stdout=subprocess.PIPE, stderr=subprocess.STDOUT, cwd=ROOT)
    for _ in range(40):
        try:
            if requests.get(f'{B_BASE}/health', timeout=1).ok:
                break
        except Exception:
            time.sleep(0.25)
    proc_b = psutil.Process(b_proc.pid)
    log(f'Servicio B iniciado: PID {b_proc.pid} (node service_b_reportes.js)')

    affinity_note = 'Sin restricción de afinidad (planificador del SO reparte núcleos)'
    if args.single_core:
        try:
            proc_a.cpu_affinity([0])
            proc_b.cpu_affinity([0])
            affinity_note = 'A y B fijados al núcleo lógico 0 (emulación de vCPU compartida)'
        except Exception as exc:
            affinity_note = f'No se pudo fijar afinidad: {exc}'
    log(f'Afinidad de CPU: {affinity_note}')

    for _ in range(5):
        do_report()

    sampler = ResourceSampler({'A': proc_a, 'B': proc_b})
    sampler.start()
    dsampler = DockerSampler()
    dsampler.start()
    log(f'Muestreo del contenedor PostgreSQL: {"activo" if dsampler.available else "no disponible"}')
    results = {}

    def set_phase(name):
        sampler.phase = name
        dsampler.phase = name

    # Fase 1: A solo (B iniciado pero sin carga)
    set_phase('F1_A_base')
    log('Fase 1 - Línea base del servicio A (B en reposo)')
    results['A_read_base'] = series('F1_A_base', 'A GET /api/products', do_read, N_READS)
    results['A_write_base'] = series('F1_A_base', 'A POST /api/orders', do_write, N_WRITES)

    # Fase 2: B solo (A en reposo)
    set_phase('F2_B_base')
    log('Fase 2 - Línea base del servicio B (A en reposo)')
    results['B_report_base'] = series('F2_B_base', 'B GET /report', do_report, N_REPORTS)

    # Fase 3: A medido con B bajo carga conocida
    replenish_stock()
    set_phase('F3_A_con_B')
    log(f'Fase 3 - Servicio A medido con B bajo carga ({BG_CONCURRENCY} clientes concurrentes en /report)')
    with BackgroundLoad(lambda: do_report()[2], BG_CONCURRENCY) as bg_b:
        results['A_read_sim'] = series('F3_A_con_B', 'A GET /api/products', do_read, N_READS)
        results['A_write_sim'] = series('F3_A_con_B', 'A POST /api/orders', do_write, N_WRITES)
    results['bg_B'] = {'requests': bg_b.count, 'errors': bg_b.errors}
    log(f'  Carga de fondo en B: {bg_b.count} solicitudes, {bg_b.errors} errores')

    # Fase 4: B medido con A bajo carga conocida
    set_phase('F4_B_con_A')
    log(f'Fase 4 - Servicio B medido con A bajo carga ({BG_CONCURRENCY} clientes concurrentes en /api/products)')
    with BackgroundLoad(lambda: do_read()[2], BG_CONCURRENCY) as bg_a:
        results['B_report_sim'] = series('F4_B_con_A', 'B GET /report', do_report, N_REPORTS)
    results['bg_A'] = {'requests': bg_a.count, 'errors': bg_a.errors}
    log(f'  Carga de fondo en A: {bg_a.count} solicitudes, {bg_a.errors} errores')

    sampler.stop()
    dsampler.stop()
    sampler.join(timeout=2)
    dsampler.join(timeout=5)
    b_proc.terminate()

    # --- Recursos por fase ---
    resources = {ph: {svc: sampler.stats(ph, svc) for svc in ('A', 'B')}
                 for ph in ('F1_A_base', 'F2_B_base', 'F3_A_con_B', 'F4_B_con_A')}
    for ph in resources:
        pg = dsampler.stats(ph)
        if pg:
            resources[ph]['PostgreSQL'] = pg
    sampler.rows.extend(dsampler.rows)

    # --- Comparaciones y dictamen ---
    def compare(key_base, key_sim, label):
        b, s = results[key_base], results[key_sim]
        var, kind = variation(b['mean_ms'], s['mean_ms'])
        err_var = round(s['error_pct'] - b['error_pct'], 2)
        ok = var <= THRESHOLD_LATENCY_PCT and s['error_pct'] <= THRESHOLD_ERROR_PCT
        return {'label': label, 'base_mean_ms': b['mean_ms'], 'sim_mean_ms': s['mean_ms'],
                'base_p95_ms': b['p95_ms'], 'sim_p95_ms': s['p95_ms'],
                'variation': var, 'variation_kind': kind,
                'base_error_pct': b['error_pct'], 'sim_error_pct': s['error_pct'], 'error_diff_abs': err_var,
                'verdict': 'APROBADA' if ok else 'NO CONFORME'}

    comparisons = [
        compare('A_read_base', 'A_read_sim', 'PC-01 Latencia A - GET /api/products (impacto B->A)'),
        compare('A_write_base', 'A_write_sim', 'PC-02 Latencia A - POST /api/orders (impacto B->A)'),
        compare('B_report_base', 'B_report_sim', 'PC-03 Latencia B - GET /report (impacto A->B)'),
    ]
    peak_cpu = max(resources[ph][svc]['cpu_peak'] for ph in resources for svc in ('A', 'B'))
    peak_ram = max(resources[ph][svc]['rss_peak_mb'] for ph in resources for svc in ('A', 'B'))
    comparisons.append({'label': 'PC-04 CPU / RAM pico por proceso (A y B)', 'peak_cpu_pct': peak_cpu,
                        'peak_rss_mb': peak_ram,
                        'verdict': 'APROBADA' if peak_cpu <= THRESHOLD_CPU_PCT and peak_ram <= THRESHOLD_RAM_MB else 'NO CONFORME'})

    for c in comparisons:
        log(f"DICTAMEN {c['label']}: {c['verdict']} | " + ', '.join(f'{k}={v}' for k, v in c.items() if k not in ('label', 'verdict')))

    # --- Entorno ---
    def cmd(c):
        try:
            return subprocess.check_output(c, shell=True, cwd=ROOT, text=True, stderr=subprocess.DEVNULL).strip()
        except Exception:
            return 'n/d'

    env = {
        'fecha_inicio': started.isoformat(timespec='seconds'),
        'fecha_fin': dt.datetime.now().isoformat(timespec='seconds'),
        'commit': cmd('git rev-parse --short HEAD'),
        'rama': cmd('git rev-parse --abbrev-ref HEAD'),
        'node': cmd('node --version'),
        'python': platform.python_version(),
        'so': f'{platform.system()} {platform.release()} ({platform.version()})',
        'cpu_logicos': psutil.cpu_count(logical=True),
        'cpu_fisicos': psutil.cpu_count(logical=False),
        'ram_total_gb': round(psutil.virtual_memory().total / 1073741824, 1),
        'persistencia_servicio_A': health,
        'afinidad_cpu': affinity_note,
        'parametros': {'n_lecturas': N_READS, 'n_escrituras': N_WRITES, 'n_reportes': N_REPORTS,
                       'concurrencia_carga_fondo': BG_CONCURRENCY,
                       'registros_por_reporte_B': 40000},
        'umbrales_predefinidos': {'latencia_var_max_pct': THRESHOLD_LATENCY_PCT, 'error_max_pct': THRESHOLD_ERROR_PCT,
                                  'cpu_pico_max_pct': THRESHOLD_CPU_PCT, 'rss_pico_max_mb': THRESHOLD_RAM_MB},
    }

    summary = {'entorno': env, 'resultados': results, 'recursos': resources, 'comparaciones': comparisons}
    with open(os.path.join(OUT_DIR, 'coexistence_summary.json'), 'w', encoding='utf-8') as fh:
        json.dump(summary, fh, ensure_ascii=False, indent=2)
    with open(os.path.join(OUT_DIR, 'coexistence_raw.csv'), 'w', newline='', encoding='utf-8') as fh:
        w = csv.DictWriter(fh, fieldnames=['phase', 'request', 'seq', 'ms', 'status', 'ok'])
        w.writeheader()
        w.writerows(raw)
    with open(os.path.join(OUT_DIR, 'coexistence_resources.csv'), 'w', newline='', encoding='utf-8') as fh:
        w = csv.DictWriter(fh, fieldnames=['t', 'phase', 'service', 'cpu_pct', 'rss_mb'])
        w.writeheader()
        w.writerows(sampler.rows)
    with open(os.path.join(OUT_DIR, 'coexistence_log.txt'), 'w', encoding='utf-8') as fh:
        fh.write('\n'.join(LOG_LINES) + '\n')
    log(f'Evidencia guardada en {OUT_DIR}')


if __name__ == '__main__':
    main()
