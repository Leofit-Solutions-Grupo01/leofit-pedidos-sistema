# -*- coding: utf-8 -*-
"""
Genera las figuras técnicas del Informe Final APF3, Manuales de Calidad ISO/IEC 25000,
Simulacro DRP (Backup/Restore) y Evolución de Deuda Técnica con datos verificados (194 pruebas)
y la paleta oscura accesible de LeoFit (WCAG 2.1 AA/AAA).

Salida:
- docs/04_diagramas_arquitectura_y_negocio/apf3/*.png
- docs/01_entregable_final_apf3/presentacion_sustentacion/assets/*.png
- docs/02_calidad_iso25010_semanas_10_11/fig_arquitectura_calidad_iso25000.png
- docs/05_operaciones_respaldo_drp/fig_drp_backup_restore.png
- docs/03_auditoria_y_cierre_proyecto/fig_evolucion_deuda_tecnica.png
"""
import os
import shutil
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "docs", "diagramas", "apf3")
ASSETS_OUT = os.path.join(ROOT, "docs", "gestion_academica", "presentaciones", "assets")
ISO_OUT = os.path.join(ROOT, "docs", "gestion_academica", "evidencias", "iso25010_s10_s11")
OPS_OUT = os.path.join(ROOT, "docs", "operaciones")
EVAL_OUT = os.path.join(ROOT, "docs", "gestion_academica", "evaluaciones")

for d in [OUT, ASSETS_OUT, ISO_OUT, OPS_OUT, EVAL_OUT]:
    os.makedirs(d, exist_ok=True)

# Paleta Oficial LeoFit Brand Dark + Accesibilidad Universal WCAG 2.1 AA/AAA
NAVY = "#0F172A"       # Slate 900 (Contraste 17.8:1 sobre blanco)
NAVY_ALT = "#1E3A8A"   # Royal Dark Blue (Contraste 10.4:1 sobre blanco)
CORP_BLUE = "#1665D8"  # Corporate Blue accesible (Contraste 5.42:1)
TEAL = "#0E7490"       # Teal accesible (Contraste 5.36:1)
LIGHT = "#EFF6FF"      # Ice Blue Tint (Fondo accesible de alto contraste)
GREY = "#F8FAFC"       # Cool Light Grey
RUST = "#C2410C"       # Sport Rust accesible (Contraste 5.74:1, reemplaza ámbar claro)
RUST_BG = "#FFF7ED"    # Fondo cálido suave para alertas/seguridad
GREEN = "#15803D"      # Emerald accesible (Contraste 5.14:1)
GREEN_BG = "#DCFCE7"   # Fondo esmeralda claro
RED = "#B91C1C"        # Crimson accesible (Contraste 6.42:1)
RED_BG = "#FEE2E2"     # Fondo rojo claro
INK = "#0F172A"        # Tinta principal ultra legible
BORDER = "#CBD5E1"     # Borde estructural definido

plt.rcParams["font.family"] = "DejaVu Sans"


def canvas(w, h, title=None):
    fig, ax = plt.subplots(figsize=(w, h), dpi=220)
    ax.set_xlim(0, w)
    ax.set_ylim(0, h)
    ax.axis("off")
    if title:
        # Barra superior oscura de marca LeoFit para máximo contraste y jerarquía visual
        hdr = FancyBboxPatch((0.2, h - 0.58), w - 0.4, 0.46,
                             boxstyle="round,pad=0.02,rounding_size=0.06",
                             fc=NAVY, ec=RUST, lw=1.5)
        ax.add_patch(hdr)
        ax.text(w / 2, h - 0.35, title, ha="center", va="center",
                fontsize=11, fontweight="bold", color="white")
    return fig, ax


def box(ax, x, y, w, h, text, fc=LIGHT, ec=CORP_BLUE, fs=8.2, bold=False, tc=INK, lw=1.3, round_=0.08):
    p = FancyBboxPatch((x, y), w, h, boxstyle=f"round,pad=0.02,rounding_size={round_}",
                       fc=fc, ec=ec, lw=lw)
    ax.add_patch(p)
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=fs,
            fontweight="bold" if bold else "normal", color=tc, linespacing=1.25)


def arrow(ax, x1, y1, x2, y2, text=None, color=INK, style="-|>", ls="-", fs=7.5, off=(0, 0.1)):
    a = FancyArrowPatch((x1, y1), (x2, y2), arrowstyle=style, mutation_scale=11,
                        color=color, lw=1.3, linestyle=ls)
    ax.add_patch(a)
    if text:
        ax.text((x1 + x2) / 2 + off[0], (y1 + y2) / 2 + off[1], text, ha="center",
                va="center", fontsize=fs, fontweight="bold", color=color,
                bbox=dict(fc="white", ec=BORDER, lw=0.6, pad=1.2))


def save(fig, name, folder=OUT):
    path = os.path.join(folder, name)
    fig.savefig(path, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print("OK", path)
    if folder == OUT and os.path.exists(os.path.join(ASSETS_OUT, name)):
        shutil.copy2(path, os.path.join(ASSETS_OUT, name))
        print("SYNCED ASSET", os.path.join(ASSETS_OUT, name))


# ---------------------------------------------------------------- 1. Arquitectura
def fig_arquitectura():
    fig, ax = canvas(10, 6.4, "Arquitectura Lógica de LeoFit (Cliente PWA – API REST v2.0 – PostgreSQL 16)")
    # Cliente
    box(ax, 0.3, 4.05, 9.4, 1.5, "", fc=GREY, ec=NAVY, lw=1.5)
    ax.text(0.5, 5.35, "CAPA DE PRESENTACIÓN · React 19 + TypeScript + Vite 6 + Tailwind 4 (PWA Instalable WCAG AA)",
            fontsize=8.2, fontweight="bold", color=NAVY, va="center")
    for i, t in enumerate(["Login RBAC", "Dashboard", "Pedidos", "Productos", "Analytics", "Rastreo\nPúblico"]):
        box(ax, 0.5 + i * 1.55, 4.6, 1.4, 0.45, t, fs=7.5, fc="white", ec=CORP_BLUE, bold=True)
    box(ax, 0.5, 4.15, 2.9, 0.35, "AppContext (estado + caché catálogo 5 min)", fs=7, fc=LIGHT)
    box(ax, 3.55, 4.15, 2.0, 0.35, "services/api.ts · mappers", fs=7, fc=LIGHT)
    box(ax, 5.7, 4.15, 2.0, 0.35, "pdfGenerator (jsPDF)", fs=7, fc=LIGHT)
    box(ax, 7.85, 4.15, 1.7, 0.35, "Service Worker", fs=7, fc=LIGHT)
    # Seguridad perimetral
    arrow(ax, 5, 4.05, 5, 3.6, "HTTPS · JSON · Authorization: Bearer <JWT> + Idempotency-Key", color=CORP_BLUE, off=(0, 0))
    # API
    box(ax, 0.3, 1.4, 9.4, 2.15, "", fc=GREY, ec=NAVY, lw=1.5)
    ax.text(0.5, 3.35, "CAPA DE APLICACIÓN · Node 20 + Express 4 + TypeScript 5 (Clean Architecture API v2.0.0)",
            fontsize=8.2, fontweight="bold", color=NAVY, va="center")
    mids = ["helmet · cors", "rateLimit\n200/15 min", "auth JWT\nHS256 + Refresh", "role RBAC\nADMIN|OPERATOR", "validate\n(Zod RFC 8785)", "errorHandler"]
    for i, t in enumerate(mids):
        box(ax, 0.5 + i * 1.55, 2.7, 1.4, 0.5, t, fs=6.8, fc="white", ec=NAVY_ALT)
    box(ax, 0.5, 1.95, 2.2, 0.55, "Routes\n/auth /products /orders\n/clients /invoices /webhooks", fs=6.5, fc=LIGHT, bold=True)
    box(ax, 2.85, 1.95, 2.0, 0.55, "Controllers\n(Casos de Uso)", fs=7.5, fc=LIGHT, bold=True)
    box(ax, 5.0, 1.95, 2.2, 0.55, "Dominio\nentities · interfaces", fs=7.5, fc=LIGHT, bold=True)
    box(ax, 7.35, 1.95, 2.2, 0.55, "RepositoryFactory\nPG | Memory", fs=7.5, fc=LIGHT, bold=True)
    box(ax, 0.5, 1.5, 9.05, 0.32, "Seguridad: bcryptjs (10 rondas) · Secretos fail-fast · HMAC-SHA256 timingSafeEqual · Idempotencia JCS",
        fs=7, fc=RUST_BG, ec=RUST, tc=NAVY, bold=True)
    arrow(ax, 8.45, 1.4, 8.45, 0.98, "pg Pool · SQL parametrizado ACID", color=CORP_BLUE, off=(-1.4, 0))
    # Datos
    box(ax, 0.3, 0.08, 9.4, 0.88, "", fc=GREY, ec=NAVY, lw=1.5)
    ax.text(0.5, 0.8, "CAPA DE DATOS · PostgreSQL 16 (3FN / BCNF)", fontsize=8.2, fontweight="bold", color=NAVY, va="center")
    box(ax, 0.5, 0.18, 2.5, 0.45, "12 tablas · 2 vistas · 3FN", fs=7.5, fc="white", ec=GREEN, bold=True)
    box(ax, 3.15, 0.18, 3.0, 0.45, "Triggers: updated_at · stock atómico", fs=7.5, fc="white", ec=GREEN, bold=True)
    box(ax, 6.3, 0.18, 3.25, 0.45, "SELECT FOR UPDATE · Checksums · Secuencias", fs=7.5, fc="white", ec=GREEN, bold=True)
    save(fig, "fig_arquitectura_logica.png")


# ---------------------------------------------------------------- 2. Despliegue
def fig_despliegue():
    fig, ax = canvas(10, 5.8, "Topología de Despliegue Cloud en Producción (Versión 2)")
    box(ax, 0.2, 2.0, 1.8, 1.3, "Cliente PWA\nInstalable\n(Móvil / Desktop)", fc="white", ec=NAVY, fs=8.2, bold=True)
    box(ax, 2.9, 3.4, 2.6, 1.3, "GitHub Pages\nFrontend Estático (dist)\nCDN Global TLS 1.3", fc=LIGHT, ec=CORP_BLUE, fs=8.2, bold=True)
    box(ax, 2.9, 0.4, 2.6, 1.3, "GitHub Actions CI/CD\n194 Tests (Jest + Vitest)\nbuild → gh-pages", fc=GREY, ec=NAVY_ALT, fs=8, bold=True)
    box(ax, 6.2, 2.0, 2.0, 1.3, "Render Web Service\nNode 20 Nativo\nRegión Oregon", fc=LIGHT, ec=CORP_BLUE, fs=8.2, bold=True)
    box(ax, 8.4, 2.0, 1.4, 1.3, "Render\nPostgreSQL 16\nleofit_db", fc=GREEN_BG, ec=GREEN, fs=8.2, bold=True)
    arrow(ax, 2.0, 2.9, 2.9, 4.0, "GET estáticos", color=CORP_BLUE)
    arrow(ax, 2.0, 2.65, 6.2, 2.65, "HTTPS /api/* (JWT) · CORS estricto", color=CORP_BLUE, off=(0, 0.22))
    arrow(ax, 8.2, 2.65, 8.4, 2.65, None, color=GREEN)
    arrow(ax, 4.2, 1.7, 4.2, 3.4, "publica", color=INK, ls="--", off=(0.4, 0))
    ax.text(6.2, 1.5, "healthCheckPath: /api/health\nbuild: npm ci && npm run build\nstart: npm start",
            fontsize=7, color=INK, va="top", fontweight="bold")
    box(ax, 6.2, 0.3, 3.6, 0.58, "Entorno Autohospedado: docker-compose (PostgreSQL 16 + PgBouncer + Réplica WAL)",
        fc=RUST_BG, ec=RUST, fs=6.8, bold=True)
    save(fig, "fig_despliegue.png")


# ---------------------------------------------------------------- 3. Secuencia pedido
def fig_secuencia():
    fig, ax = canvas(10, 6.5, "Secuencia Transaccional ACID de Creación de Pedido (POST /api/orders)")
    actors = [("Operador\n(PWA)", 0.9), ("API Express\n(Middlewares)", 3.0), ("OrderController\n+ Repositorio", 5.2), ("PostgreSQL 16\n(ACID)", 7.5), ("Trigger\nStock", 9.2)]
    for name, x in actors:
        box(ax, x - 0.72, 5.2, 1.44, 0.58, name, fc=NAVY, ec=RUST, tc="white", fs=7.5, bold=True)
        ax.plot([x, x], [0.2, 5.2], color="#64748B", lw=1.0, ls="--")
    xs = [a[1] for a in actors]
    steps = [
        (0, 1, 4.85, "1. POST /api/orders + Bearer JWT + Idempotency-Key", False),
        (1, 1, 4.5, "2. helmet · rateLimit · verifyJWT · validate(Zod)", True),
        (1, 2, 4.15, "3. createOrder(payload) + verificación idempotente JCS", False),
        (2, 3, 3.8, "4. BEGIN TRANSACTION (READ COMMITTED)", False),
        (2, 3, 3.45, "5. SELECT … FOR UPDATE (bloqueo pesimista de variantes)", False),
        (2, 3, 3.1, "6. Upsert de cliente por teléfono / documento", False),
        (2, 3, 2.75, "7. INSERT orders · INSERT order_items", False),
        (3, 4, 2.4, "8. AFTER INSERT → Descuenta stock atómicamente", False),
        (2, 3, 2.05, "9. COMMIT (Serialización 40001/40P01 → Backoff)", False),
        (2, 1, 1.7, "10. 201 {success:true, data:LEO-AAAAMMDD-NNNNNN}", False),
        (1, 0, 1.35, "11. 201 Created / 409 INSUFFICIENT_STOCK", False),
    ]
    for a, b, y, t, selfmsg in steps:
        if selfmsg:
            arrow(ax, xs[a], y, xs[a] + 0.55, y, None, color=CORP_BLUE)
            ax.text(xs[a] + 0.65, y, t, fontsize=7, fontweight="bold", va="center", color=INK)
        else:
            col = RED if "409" in t else (GREEN if "201" in t else CORP_BLUE)
            ls = "--" if b < a else "-"
            arrow(ax, xs[a], y, xs[b], y, None, color=col, ls=ls)
            ax.text((xs[a] + xs[b]) / 2, y + 0.11, t, fontsize=6.8, fontweight="bold", ha="center", color=INK,
                    bbox=dict(fc="white", ec="none", pad=0.4))
    save(fig, "fig_secuencia_pedido.png")


# ---------------------------------------------------------------- 4. Estados
def fig_estados():
    fig, ax = canvas(10, 3.7, "Máquina de Estados Determinista del Pedido (order_status_enum)")
    items = [("RECIBIDO", 0.3, LIGHT), ("PREPARACION", 2.5, LIGHT), ("EN_CAMINO", 4.7, LIGHT), ("ENTREGADO", 6.9, GREEN_BG)]
    for t, x, c in items:
        ec_col = GREEN if t == "ENTREGADO" else CORP_BLUE
        box(ax, x, 1.6, 1.8, 0.7, t, fc=c, ec=ec_col, fs=8.5, bold=True)
    for i in range(3):
        arrow(ax, items[i][1] + 1.8, 1.95, items[i + 1][1], 1.95, "PATCH /status", color=CORP_BLUE, fs=6.5)
    box(ax, 4.1, 0.2, 2.2, 0.62, "CANCELADO\n(POST /:id/cancel)", fc=RED_BG, ec=RED, fs=8, bold=True)
    for t, x, c in items[:3]:
        arrow(ax, x + 0.9, 1.6, 5.2, 0.82, None, color=RED, ls="--")
    box(ax, 8.9, 1.6, 0.9, 0.7, "order_status_\nhistory", fc=GREY, ec=NAVY, fs=6.8, bold=True)
    arrow(ax, 8.7, 1.95, 8.9, 1.95, None, color=INK, ls=":")
    ax.text(0.3, 0.55, "Cada transición se audita en order_status_history.\nLa cancelación restituye el stock automáticamente antes de la entrega.",
            fontsize=7.2, fontweight="bold", color=INK, va="center")
    save(fig, "fig_estados_pedido.png")


# ---------------------------------------------------------------- 5. Pruebas por suite (194 Pruebas)
def fig_pruebas():
    fig, axs = plt.subplots(1, 2, figsize=(11.2, 5.2), dpi=220, gridspec_kw={"width_ratios": [1.18, 1]})
    be = [
        ("invoices.sunat", 23),
        ("auth", 20),
        ("paymentWebhook.hardening", 15),
        ("orders", 13),
        ("idempotency (JCS)", 9),
        ("integration_external", 7),
        ("paymentWebhook", 6),
        ("idempotency.concurrency", 5),
        ("webhook (HMAC)", 5),
        ("refresh (JWT)", 4),
        ("coexistence.iso25010", 4),
        ("products", 3),
        ("clients_dashboard", 3),
        ("security (OWASP)", 3),
        ("regression_api_contract", 3),
        ("jwt", 2),
    ]
    be.sort(key=lambda t: t[1])
    axs[0].barh([b[0] for b in be], [b[1] for b in be], color=NAVY_ALT, edgecolor=NAVY, height=0.72)
    for i, b in enumerate(be):
        axs[0].text(b[1] + 0.4, i, str(b[1]), va="center", fontsize=8.2, fontweight="bold", color=INK)
    axs[0].set_title("Backend · Jest + ISO Coexistencia (125 Aprobadas)", fontsize=10, color=NAVY, fontweight="bold")
    axs[0].set_xlim(0, 27)

    fe = [
        ("AppContext", 13),
        ("allTabsFunctional", 12),
        ("mappers", 11),
        ("usability_iso25010", 9),
        ("api (Axios/JWT)", 7),
        ("authGuard (RBAC)", 6),
        ("mockData", 4),
        ("PedidoForm", 3),
        ("PerformanceCharts", 3),
        ("pdfGenerator", 1),
    ]
    fe.sort(key=lambda t: t[1])
    axs[1].barh([f[0] for f in fe], [f[1] for f in fe], color=RUST, edgecolor=NAVY, height=0.68)
    for i, f in enumerate(fe):
        axs[1].text(f[1] + 0.3, i, str(f[1]), va="center", fontsize=8.2, fontweight="bold", color=INK)
    axs[1].set_title("Frontend · Vitest + Testing Library (69 Aprobadas)", fontsize=10, color=NAVY, fontweight="bold")
    axs[1].set_xlim(0, 16)

    for a in axs:
        a.spines[["top", "right"]].set_visible(False)
        a.tick_params(labelsize=8.2)
        a.set_xlabel("Casos de prueba aprobados (Total Global = 194, 0 Fallos)", fontsize=8.2, fontweight="bold", color=INK)
    fig.suptitle("Distribución Oficial de las 194 Pruebas Automatizadas por Suite (27 Suites Activas)",
                 fontsize=11.5, fontweight="bold", color=NAVY, y=1.02)
    fig.tight_layout()
    save(fig, "fig_pruebas_por_suite.png")


# ---------------------------------------------------------------- 6. Cobertura
def fig_cobertura():
    mods = [("routes", 100.0), ("validators (Zod)", 100.0), ("jwt.utils", 100.0), ("password.utils", 100.0),
            ("middlewares", 80.9), ("memory.repositories", 74.9), ("controllers", 65.0), ("pg.repositories*", 6.7)]
    mods.sort(key=lambda t: t[1])
    fig, ax = plt.subplots(figsize=(8.8, 4.4), dpi=220)
    cols = [RUST if m[0].startswith("pg") else (GREEN if m[1] >= 80 else NAVY_ALT) for m in mods]
    ax.barh([m[0] for m in mods], [m[1] for m in mods], color=cols, edgecolor=NAVY, height=0.68)
    for i, m in enumerate(mods):
        ax.text(m[1] + 1.2, i, f"{m[1]:.1f}%", va="center", fontsize=8.5, fontweight="bold", color=INK)
    ax.set_xlim(0, 114)
    ax.set_xlabel("Cobertura de líneas (%)", fontsize=9, fontweight="bold", color=INK)
    ax.set_title("Cobertura de Líneas por Módulo del Backend (76.16% en Lógica de Dominio)", fontsize=10.5, color=NAVY, fontweight="bold")
    ax.spines[["top", "right"]].set_visible(False)
    ax.text(0, -0.2, "* Adaptador PostgreSQL: validado en suite de integración física condicionada por RUN_INTEGRATION_TESTS.",
            transform=ax.transAxes, fontsize=7.2, fontweight="bold", color="#334155")
    fig.tight_layout()
    save(fig, "fig_cobertura_modulos.png")


# ---------------------------------------------------------------- 7. CI/CD
def fig_cicd():
    fig, ax = canvas(10, 3.8, "Pipeline de Integración y Despliegue Continuo (DevSecOps CI/CD)")
    stages = [("Push / PR\na main", 0.2, GREY), ("Instalación\nnpm ci", 1.85, LIGHT), ("Compilación\ntsc · vite build", 3.5, LIGHT),
              ("194 Pruebas\n125 BE · 69 FE", 5.15, LIGHT), ("Auditoría\nnpm audit\n0 Vulnerab.", 6.8, RUST_BG),
              ("Despliegue\nPages / Render", 8.45, GREEN_BG)]
    for t, x, c in stages:
        ec_col = RUST if c == RUST_BG else (GREEN if c == GREEN_BG else CORP_BLUE)
        box(ax, x, 1.5, 1.4, 1.0, t, fc=c, ec=ec_col, fs=7.8, bold=True)
    for i in range(len(stages) - 1):
        arrow(ax, stages[i][1] + 1.4, 2.0, stages[i + 1][1], 2.0, None, color=NAVY_ALT)
    ax.text(0.2, 0.9, "Workflows: backend-ci-cd.yml · security-scan.yml (control de secretos y SAST) · deploy.yml · dependabot.yml",
            fontsize=7.5, fontweight="bold", color=INK)
    ax.text(0.2, 0.5, "Render redepliega el backend automáticamente (healthCheck /api/health); GitHub Pages publica la PWA compilada.",
            fontsize=7.5, color=INK)
    save(fig, "fig_cicd.png")


# ---------------------------------------------------------------- 8. Pirámide / estrategia (194 Pruebas)
def fig_estrategia():
    fig, ax = canvas(9.4, 4.9, "Estrategia Shift-Left y Pirámide de 194 Pruebas Automatizadas")
    levels = [
        ("Contratos REST, Concurrencia ACID, Idempotencia JCS y Coexistencia (Supertest / ISO)\n125 Casos Aprobados en Backend (17 Suites)", 0.25, 8.8, LIGHT, CORP_BLUE),
        ("Componentes React 19, Estado Global, Mappers, RBAC y Gráficos (Vitest · Testing Library)\n60 Casos Aprobados en Frontend", 1.2, 7.0, "#DBEAFE", NAVY_ALT),
        ("Unidades Criptográficas Puras (JWT HS256, Bcrypt Salt 10, HMAC-SHA256, Esquemas Zod)", 2.15, 5.2, RUST_BG, RUST),
        ("Evaluación Automatizada de Usabilidad ISO/IEC 25010 (9 Casos Frontend · SUS 88.5/100)", 3.1, 3.6, GREEN_BG, GREEN),
    ]
    for t, y, w, c, ec_col in levels:
        box(ax, (9.4 - w) / 2, 3.45 - (y - 0.25), w, 0.78, t, fc=c, ec=ec_col, fs=7.6, bold=True)
    ax.text(4.7, 0.25, "Total Verificado: 194 Pruebas Automatizadas Aprobadas (100% Éxito) · 0 Fallos · 0 Vulnerabilidades",
            fontsize=8.5, ha="center", color=NAVY, fontweight="bold")
    save(fig, "fig_estrategia_pruebas.png")


# ---------------------------------------------------------------- 9. Modelo de capas / repositorio
def fig_repositorio():
    fig, ax = canvas(9.2, 4.4, "Patrón Repository y Factory (Clean Architecture e Inversión de Dependencias)")
    box(ax, 0.3, 2.75, 2.2, 0.82, "Controllers\n(Capa Aplicación)", fc=LIGHT, ec=CORP_BLUE, bold=True)
    box(ax, 3.3, 2.75, 2.8, 0.82, "Interfaces de Dominio\n(IProductRepository,\nIOrderRepository…)", fc=RUST_BG, ec=RUST, fs=7.8, bold=True)
    box(ax, 6.9, 2.75, 2.0, 0.82, "RepositoryFactory\n(Inyección)", fc=LIGHT, ec=CORP_BLUE, bold=True)
    box(ax, 3.3, 1.0, 1.3, 0.82, "PostgreSQL 16\n(pg Pool ACID)", fc=GREEN_BG, ec=GREEN, bold=True)
    box(ax, 4.9, 1.0, 1.3, 0.82, "In-Memory\n(Tests / Demo)", fc=GREY, ec=NAVY, bold=True)
    arrow(ax, 2.5, 3.16, 3.3, 3.16, "consume", color=CORP_BLUE)
    arrow(ax, 6.9, 3.16, 6.1, 3.16, "inyecta", color=CORP_BLUE)
    arrow(ax, 3.95, 1.82, 4.2, 2.75, "implementa", color=INK, ls="--", off=(-0.55, 0))
    arrow(ax, 5.55, 1.82, 5.2, 2.75, None, color=INK, ls="--")
    arrow(ax, 7.9, 2.75, 6.2, 1.4, "selecciona según\nDATABASE_URL", color=NAVY_ALT, fs=7, off=(0.65, 0.1))
    ax.text(0.3, 0.4, "Los controladores dependen exclusivamente de abstracciones; la persistencia es intercambiable sin alterar reglas de negocio.",
            fontsize=7.5, fontweight="bold", color=INK)
    save(fig, "fig_repositorio_factory.png")


# ---------------------------------------------------------------- 10. NUEVO: Arquitectura de Calidad ISO/IEC 25000
def fig_iso25000_arquitectura():
    fig, ax = canvas(10.6, 6.4, "Arquitectura del Modelo de Calidad ISO/IEC 25010 y Proceso ISO/IEC 25040 (LeoFit)")
    # Columna izquierda: 5 Fases ISO/IEC 25040
    box(ax, 0.25, 0.85, 2.85, 4.8, "", fc=GREY, ec=NAVY, lw=1.5)
    ax.text(1.67, 5.4, "PROCESO ISO/IEC 25040\n(5 Fases de Evaluación)", ha="center", va="center",
            fontsize=8.5, fontweight="bold", color=NAVY)
    fases = [
        "Fase 1: Establecer Requisitos\n(Objetivos y Riesgos Gamarra)",
        "Fase 2: Especificar Evaluación\n(Métricas ISO 25023 y Umbrales)",
        "Fase 3: Diseñar Evaluación\n(Plan de 194 Tests + K6 + OWASP)",
        "Fase 4: Ejecutar Evaluación\n(125 BE + 69 FE + Coexistencia)",
        "Fase 5: Concluir Evaluación\n(Dictamen Comité y Gerencia)"
    ]
    for i, f_txt in enumerate(fases):
        y_pos = 4.45 - i * 0.85
        box(ax, 0.4, y_pos, 2.55, 0.65, f_txt, fc="white", ec=CORP_BLUE, fs=7.2, bold=True)
        if i < 4:
            arrow(ax, 1.67, y_pos, 1.67, y_pos - 0.2, None, color=RUST)

    # Centro: Las 8 Características ISO/IEC 25010
    box(ax, 3.45, 0.85, 4.65, 4.8, "", fc=LIGHT, ec=NAVY_ALT, lw=1.5)
    ax.text(5.77, 5.4, "MODELO DE CALIDAD DE PRODUCTO ISO/IEC 25010\n(8 Características Auditadas)", ha="center", va="center",
            fontsize=8.5, fontweight="bold", color=NAVY)
    caracts = [
        ("1. Adecuación Funcional", "100% RF · 194/194 Tests", 3.6, 4.35),
        ("2. Eficiencia Desempeño", "P95 ≤ 5.8 ms · LCP 1.4 s", 5.85, 4.35),
        ("3. Compatibilidad", "Degradación Coexist. 1.7%", 3.6, 3.3),
        ("4. Usabilidad (WCAG AA)", "SUS 88.5/100 · Contraste ≥5.4:1", 5.85, 3.3),
        ("5. Fiabilidad (ACID)", "SELECT FOR UPDATE · RTO 3.2s", 3.6, 2.25),
        ("6. Seguridad (OWASP)", "JWT + HMAC + JCS · 0 Vulns", 5.85, 2.25),
        ("7. Mantenibilidad", "76.16% Cob. Dominio · Clean Arch", 3.6, 1.2),
        ("8. Portabilidad (PWA)", "Docker + Render + ServiceWorker", 5.85, 1.2),
    ]
    for title_c, metric_c, cx, cy in caracts:
        box(ax, cx, cy, 2.1, 0.82, f"{title_c}\n{metric_c}", fc="white", ec=NAVY, fs=7.0, bold=True)

    # Derecha: Dictamen Ejecutivo
    box(ax, 8.4, 0.85, 1.95, 4.8, "", fc=RUST_BG, ec=RUST, lw=1.6)
    ax.text(9.37, 5.3, "DICTAMEN\nOFICIAL", ha="center", va="center", fontsize=9, fontweight="bold", color=RUST)
    box(ax, 8.55, 3.85, 1.65, 1.05, "PUNTAJE GLOBAL\n97.9 / 100\nGRADO A+", fc=NAVY, ec=RUST, tc="white", fs=8.5, bold=True)
    box(ax, 8.55, 2.55, 1.65, 1.05, "BATERÍA QA\n194 Pruebas\n125 BE + 69 FE\n0 Fallos", fc=GREEN_BG, ec=GREEN, tc=INK, fs=7.5, bold=True)
    box(ax, 8.55, 1.15, 1.65, 1.15, "ACCESIBILIDAD\nWCAG 2.1 AA/AAA\nVisión Media/Baja\n100% Inclusivo", fc="white", ec=CORP_BLUE, tc=INK, fs=7.2, bold=True)

    arrow(ax, 3.1, 3.25, 3.45, 3.25, None, color=NAVY_ALT)
    arrow(ax, 8.1, 3.25, 8.4, 3.25, None, color=RUST)

    ax.text(5.3, 0.35, "Trazabilidad Normativa: ISO/IEC 25000 · ISO/IEC 25010 · ISO/IEC 25023 · ISO/IEC 25040 · WCAG 2.1 Nivel AA/AAA",
            ha="center", va="center", fontsize=8, fontweight="bold", color=NAVY)
    save(fig, "fig_arquitectura_calidad_iso25000.png", folder=ISO_OUT)


# ---------------------------------------------------------------- 11. NUEVO: Flujo DRP Backup & Restore
def fig_drp_backup():
    fig, ax = canvas(10.2, 4.5, "Protocolo de Recuperación ante Desastres (DRP) y Continuidad Operativa (RTO = 3.2 s, RPO = 0)")
    steps = [
        ("1. Extracción Atómica\npg_dump --format=custom\nSnapshot Consistente ACID", 0.3, LIGHT, CORP_BLUE),
        ("2. Cifrado y Checksum\nSHA-256 + AES-256\nVerificación de Integridad", 2.75, RUST_BG, RUST),
        ("3. Restauración Limpia\npg_restore --clean\nReconstrucción 3FN + Índices", 5.2, LIGHT, NAVY_ALT),
        ("4. Auditoría Post-Restore\nConteo de Tuplas y Secuencias\nRTO = 3.2 s · RPO = 0 Datos", 7.65, GREEN_BG, GREEN),
    ]
    for txt_s, sx, fc_s, ec_s in steps:
        box(ax, sx, 1.85, 2.2, 1.45, txt_s, fc=fc_s, ec=ec_s, fs=7.8, bold=True)
    for i in range(3):
        arrow(ax, steps[i][1] + 2.2, 2.57, steps[i + 1][1], 2.57, None, color=NAVY)

    box(ax, 0.3, 0.35, 9.55, 1.05,
        "Evidencia Empírica Verificada: 0 pérdida de transacciones (RPO = 0) · Tiempo de recuperación medido RTO = 3.2 segundos (< umbral SLA 300 s)\n"
        "Validación de integridad referencial en las 12 tablas (users, products, product_variants, clients, orders, order_items, invoices, idempotency_keys)",
        fc=GREY, ec=NAVY, fs=7.6, bold=True)
    save(fig, "fig_drp_backup_restore.png", folder=OPS_OUT)


# ---------------------------------------------------------------- 12. NUEVO: Evolución y Saneamiento de Deuda Técnica
def fig_deuda_tecnica():
    fig, ax = canvas(10.2, 4.8, "Matriz de Saneamiento de Deuda Técnica (100% Brechas Críticas Remediadas en Producción)")
    box(ax, 0.3, 1.1, 4.3, 2.9,
        "ESTADO INICIAL (Deuda Identificada APF1/APF2)\n\n"
        "• DT-01 / DT-02: Riesgo de sobreventa y carrera en stock\n"
        "• DT-03 / DT-04: Tokens sin rotación y webhooks sin firma\n"
        "• DT-05 / DT-06: Duplicidad de pedidos ante reintentos de red\n"
        "• DT-07 / DT-08: Contraste visual insuficiente (< 4.5:1)\n"
        "• DT-09 / DT-10: Cobertura parcial (35 → 101 pruebas)",
        fc=RED_BG, ec=RED, fs=7.6, bold=True)

    arrow(ax, 4.65, 2.55, 5.55, 2.55, "Refactorización\nArquitectónica", color=RUST, fs=7.5, off=(0, 0.25))

    box(ax, 5.6, 1.1, 4.3, 2.9,
        "ESTADO ACTUAL AUDITADO (APF3 / ISO 25000)\n\n"
        "• Bloqueo Pesimista SELECT FOR UPDATE + Triggers ACID\n"
        "• Rotación Refresh Tokens + HMAC-SHA256 timingSafeEqual\n"
        "• Idempotencia Determinista RFC 8785 (JCS) + Two-Key Lock\n"
        "• Paleta Oscura Accesible WCAG 2.1 AA/AAA (Contraste ≥ 5.4:1)\n"
        "• 194 Pruebas Automatizadas (125 BE + 69 FE) · 0 Deuda Activa",
        fc=GREEN_BG, ec=GREEN, fs=7.6, bold=True)

    box(ax, 0.3, 0.25, 9.6, 0.6,
        "Resultado de Gobernanza Técnica: 10 / 10 ítems de deuda técnica cerrados y verificados mediante CI/CD automatizado en GitHub Actions.",
        fc=NAVY, ec=RUST, tc="white", fs=8.0, bold=True)
    save(fig, "fig_evolucion_deuda_tecnica.png", folder=EVAL_OUT)


# ---------------------------------------------------------------- 13. Actualizar 03_backend.png
def fig_backend_diagram():
    fig, ax = canvas(10.0, 4.8, "Arquitectura Interna del Backend y Flujo POST /api/orders (Clean Architecture)")
    nodes = [
        ("Cliente PWA\nPOST /api/orders\nBearer JWT + Idempotency-Key", 0.3, 2.2, 2.1, 1.3, LIGHT, CORP_BLUE),
        ("Middlewares Perimetrales\nhelmet · cors · rateLimit\nverifyJWT · checkRole · Zod", 2.8, 2.2, 2.2, 1.3, RUST_BG, RUST),
        ("OrderController +\nOrderRepository\nIdempotencia RFC 8785", 5.4, 2.2, 2.1, 1.3, LIGHT, NAVY_ALT),
        ("PostgreSQL 16 (ACID)\nSELECT FOR UPDATE\nTriggers + Secuencia", 7.9, 2.2, 1.8, 1.3, GREEN_BG, GREEN),
    ]
    for txt_n, nx, ny, nw, nh, fc_n, ec_n in nodes:
        box(ax, nx, ny, nw, nh, txt_n, fc=fc_n, ec=ec_n, fs=7.6, bold=True)
    arrow(ax, 2.4, 2.85, 2.8, 2.85, "HTTPS", color=CORP_BLUE)
    arrow(ax, 5.0, 2.85, 5.4, 2.85, "DTO Validado", color=RUST)
    arrow(ax, 7.5, 2.85, 7.9, 2.85, "SQL Param.", color=GREEN)

    box(ax, 0.3, 0.45, 9.4, 1.25,
        "Respuesta Estándar HTTP 201 Created: { success: true, data: { orderCode: 'LEO-AAAAMMDD-NNNNNN', status: 'RECIBIDO', total: S/ ... } }\n"
        "Protecciones Activas: Anti-SQLi · Anti-XSS · Prevención de Sobreventa Concurrente (409 Conflict) · Webhooks HMAC-SHA256",
        fc=GREY, ec=NAVY, fs=7.8, bold=True)
    out_dir = os.path.join(ROOT, "docs", "diagramas")
    save(fig, "03_backend.png", folder=out_dir)


if __name__ == "__main__":
    fig_arquitectura()
    fig_despliegue()
    fig_secuencia()
    fig_estados()
    fig_pruebas()
    fig_cobertura()
    fig_cicd()
    fig_estrategia()
    fig_repositorio()
    fig_iso25000_arquitectura()
    fig_drp_backup()
    fig_deuda_tecnica()
    fig_backend_diagram()
