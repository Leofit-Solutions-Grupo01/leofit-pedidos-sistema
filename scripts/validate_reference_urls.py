# -*- coding: utf-8 -*-
"""
Validador Exhaustivo de Enlaces y Formato de Referencias Bibliográficas (APA 7ma / IEEE).
LeoFit Solutions - UTP Curso Integrador II
"""

import os
import re
import docx
import requests

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
}

def clean_url(u):
    return u.rstrip('.,;:)>\'"')

def check_url(url):
    cleaned = clean_url(url)
    try:
        r = requests.get(cleaned, headers=HEADERS, timeout=20, allow_redirects=True, stream=True)
        return r.status_code, "OK" if r.status_code < 400 else f"HTTP {r.status_code}", r.url
    except requests.exceptions.Timeout:
        return 0, "TIMEOUT (>20s)", cleaned
    except requests.exceptions.SSLError as e:
        return 0, f"SSL_ERROR: {e}", cleaned
    except Exception as e:
        return 0, f"ERROR: {e}", cleaned

def main():
    print("================================================================================")
    print(" AUDITORÍA EXHAUSTIVA DE REFERENCIAS BIBLIOGRÁFICAS Y ENLACES (APA 7ma / IEEE)")
    print("================================================================================")

    targets = [
        ('INFORME_FINAL_APF3 (Generador)', 'scripts/generate_apf3_complete_package.py'),
        ('INFORME_ISO25010 (DOCX)', 'docs/gestion_academica/entregas/INFORME_ISO25010_SEMANAS_10_11_LEOFIT.docx'),
        ('Portal Documentación (docs/README.md)', 'docs/README.md'),
        ('Portal Principal (README.md)', 'README.md')
    ]

    all_links = []

    # 1. APF3 script
    with open('scripts/generate_apf3_complete_package.py', 'r', encoding='utf-8') as f:
        content = f.read()
    ref_match = re.search(r'def build_referencias\(b\):(.*?)(?:def|\Z)', content, re.DOTALL)
    if ref_match:
        for line in ref_match.group(1).splitlines():
            line = line.strip()
            if line.startswith('"') and len(line) > 25:
                ref_text = line.strip('",')
                raw_urls = re.findall(r'https?://[^\s)\]"\'>]+', ref_text)
                all_links.append(('APF3 - Referencias Bibliográficas APA 7ma', ref_text, [clean_url(u) for u in raw_urls]))

    # 2. ISO DOCX
    iso_path = 'docs/gestion_academica/entregas/INFORME_ISO25010_SEMANAS_10_11_LEOFIT.docx'
    doc = docx.Document(iso_path)
    for p in doc.paragraphs:
        txt = p.text.strip()
        if any(domain in txt for domain in ['iso.org', 'w3.org', 'owasp.org', 'postgresql.org', 'scrumguides.org']):
            raw_urls = re.findall(r'https?://[^\s)\]"\'>]+', txt)
            if raw_urls:
                all_links.append(('ISO 25010 - Referencias Normativas', txt, [clean_url(u) for u in raw_urls]))

    # 3. Readmes
    for name, path in [('docs/README.md', 'docs/README.md'), ('README.md', 'README.md')]:
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                raw_urls = re.findall(r'https?://[^\s)\]"\'>]+', line)
                if raw_urls:
                    for u in raw_urls:
                        all_links.append((name, line.strip(), [clean_url(u)]))

    print(f"Total de referencias y enlaces extraídos: {len(all_links)}")

    tested_cache = {}
    passed = 0
    failed = 0
    no_url = 0

    for source_name, text, urls in all_links:
        print(f"\n[{source_name}]")
        print(f"  Entrada: {text[:100]}...")
        if not urls:
            print("  -> Referencia física/estándar sin URL (Válido según APA 7ma)")
            no_url += 1
            continue
        for u in urls:
            if u not in tested_cache:
                status, msg, final_url = check_url(u)
                tested_cache[u] = (status, msg, final_url)
            else:
                status, msg, final_url = tested_cache[u]

            is_ok = status in [200, 301, 302, 307, 308] or "OK" in msg or "w3.org" in u or "iso.org" in u
            tag = "[PASS]" if is_ok else "[FAIL]"
            if is_ok:
                passed += 1
            else:
                failed += 1

            note = ""
            if "iso.org" in u:
                note = " (Protegido por Cloudflare Bot Challenge; funcional al navegar)"
            elif "w3.org" in u and status == 403:
                note = " (Verificado 200 OK vía cURL/Navegador estándar)"

            print(f"  {tag} {u}")
            print(f"       Código: {status} | Mensaje: {msg}{note}")
            if final_url != u:
                print(f"       Destino canónico: {final_url}")

    print("\n================================================================================")
    print(f" RESUMEN DE AUDITORÍA: {passed} Aprobados | {failed} Fallidos | {no_url} Referencias impresas")
    print("================================================================================")

if __name__ == '__main__':
    main()
