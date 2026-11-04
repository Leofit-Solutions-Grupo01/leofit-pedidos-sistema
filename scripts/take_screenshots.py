import subprocess, os, tempfile
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DIST_DIR = BASE_DIR / "frontend" / "dist"
ARTIFACT_DIR = BASE_DIR / "docs" / "auditoria_cierre"
ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)

EDGE_EXE = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
index_file = DIST_DIR / "index.html"
html_content = index_file.read_text(encoding="utf-8")

# 1. Preview Dashboard (Vista Superior Hero y KPIs)
inject_hero = """<script>
sessionStorage.setItem('leofit_session', 'token-mock-admin');
sessionStorage.setItem('leofit_user', JSON.stringify({ id: 1, name: 'Víctor L. Cárdenas F.', email: 'operador.demo@leofit.pe', role: 'ADMIN' }));
</script>"""
(DIST_DIR / "preview_hero.html").write_text(html_content.replace("<head>", f"<head>\n{inject_hero}"), encoding="utf-8")

# 2. Preview Performance Charts (Ventas & Caja enfocado al centro)
inject_charts = """<script>
sessionStorage.setItem('leofit_session', 'token-mock-admin');
sessionStorage.setItem('leofit_user', JSON.stringify({ id: 1, name: 'Víctor L. Cárdenas F.', email: 'operador.demo@leofit.pe', role: 'ADMIN' }));
</script>
<style>
/* Ocultar el hero superior para enfocar de inmediato el panel de rendimiento en la captura */
.space-y-4 > div:nth-child(2) { display: none !important; }
.space-y-4 > div:nth-child(3) { display: none !important; }
</style>
"""
(DIST_DIR / "preview_charts_focus.html").write_text(html_content.replace("<head>", f"<head>\n{inject_charts}"), encoding="utf-8")

# 3. Preview SLA & Stock (SLA enfocado)
inject_sla = """<script>
sessionStorage.setItem('leofit_session', 'token-mock-admin');
sessionStorage.setItem('leofit_user', JSON.stringify({ id: 1, name: 'Víctor L. Cárdenas F.', email: 'operador.demo@leofit.pe', role: 'ADMIN' }));
</script>
<style>
.space-y-4 > div:nth-child(2) { display: none !important; }
.space-y-4 > div:nth-child(3) { display: none !important; }
</style>
"""
(DIST_DIR / "preview_sla_focus.html").write_text(html_content.replace("<head>", f"<head>\n{inject_sla}"), encoding="utf-8")

def snap(file_name, out_png, width=390, height=844):
    file_path = DIST_DIR / file_name
    file_url = "file:///" + str(file_path).replace("\\", "/")
    cmd = [
        EDGE_EXE,
        "--headless",
        "--disable-gpu",
        "--no-sandbox",
        "--allow-file-access-from-files",
        "--disable-web-security",
        f"--window-size={width},{height}",
        f"--screenshot={out_png}",
        file_url,
    ]
    res = subprocess.run(cmd, capture_output=True, text=True, timeout=15)
    size = out_png.stat().st_size if out_png.exists() else 0
    print(f"Captured {out_png.name}: {size} bytes")

snap("preview_hero.html", ARTIFACT_DIR / "1_dashboard_hero.png", 390, 844)
snap("preview_charts_focus.html", ARTIFACT_DIR / "2_dashboard_performance_charts.png", 390, 844)
snap("preview_sla_focus.html", ARTIFACT_DIR / "3_dashboard_sla_operations.png", 390, 844)

print("Capturas finalizadas con éxito.")
