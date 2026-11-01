"""
Genera las figuras técnicas del Informe Final APF3 (LeoFit) con datos verificados
del repositorio y de las ejecuciones reales de pruebas (2026-10-11).

Salida: docs/diagramas/apf3/*.png
Uso:    python scripts/generate_apf3_figures.py
"""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "docs", "diagramas", "apf3")
os.makedirs(OUT, exist_ok=True)

NAVY = "#0F2A43"
CYAN = "#06B6D4"
TEAL = "#0E7490"
LIGHT = "#E6F6FA"
GREY = "#F1F5F9"
AMBER = "#F59E0B"
GREEN = "#16A34A"
RED = "#DC2626"
INK = "#1E293B"

plt.rcParams["font.family"] = "DejaVu Sans"


def canvas(w, h, title=None):
    fig, ax = plt.subplots(figsize=(w, h), dpi=200)
    ax.set_xlim(0, w)
    ax.set_ylim(0, h)
    ax.axis("off")
    if title:
        ax.text(w / 2, h - 0.25, title, ha="center", va="center", fontsize=12, fontweight="bold", color=NAVY)
    return fig, ax


def box(ax, x, y, w, h, text, fc=LIGHT, ec=TEAL, fs=8, bold=False, tc=INK, lw=1.2, round_=0.08):
    p = FancyBboxPatch((x, y), w, h, boxstyle=f"round,pad=0.02,rounding_size={round_}",
                       fc=fc, ec=ec, lw=lw)
    ax.add_patch(p)
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=fs,
            fontweight="bold" if bold else "normal", color=tc, linespacing=1.25)


def arrow(ax, x1, y1, x2, y2, text=None, color=INK, style="-|>", ls="-", fs=7, off=(0, 0.1)):
    a = FancyArrowPatch((x1, y1), (x2, y2), arrowstyle=style, mutation_scale=10,
                        color=color, lw=1.1, linestyle=ls)
    ax.add_patch(a)
    if text:
        ax.text((x1 + x2) / 2 + off[0], (y1 + y2) / 2 + off[1], text, ha="center",
                va="center", fontsize=fs, color=color,
                bbox=dict(fc="white", ec="none", pad=0.6))


def save(fig, name):
    path = os.path.join(OUT, name)
    fig.savefig(path, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print("OK", path)


# ---------------------------------------------------------------- 1. Arquitectura
def fig_arquitectura():
    fig, ax = canvas(10, 6.2, "Arquitectura lógica de LeoFit (cliente – API – datos)")
    # Cliente
    box(ax, 0.3, 4.1, 9.4, 1.5, "", fc=GREY, ec=NAVY)
    ax.text(0.5, 5.4, "CAPA DE PRESENTACIÓN · React 19 + TypeScript + Vite 6 + Tailwind 4 (PWA instalable)",
            fontsize=8, fontweight="bold", color=NAVY, va="center")
    for i, t in enumerate(["Login", "Dashboard", "Pedidos", "Productos", "Analytics", "Rastreo\npúblico"]):
        box(ax, 0.5 + i * 1.55, 4.65, 1.4, 0.45, t, fs=7, fc="white")
    box(ax, 0.5, 4.2, 2.9, 0.35, "AppContext (estado + caché catálogo 5 min)", fs=6.5, fc=LIGHT)
    box(ax, 3.55, 4.2, 2.0, 0.35, "services/api.ts · mappers", fs=6.5, fc=LIGHT)
    box(ax, 5.7, 4.2, 2.0, 0.35, "pdfGenerator (jsPDF)", fs=6.5, fc=LIGHT)
    box(ax, 7.85, 4.2, 1.7, 0.35, "manifest.json", fs=6.5, fc=LIGHT)
    # Seguridad perimetral
    arrow(ax, 5, 4.1, 5, 3.65, "HTTPS · JSON · Authorization: Bearer <JWT>", color=TEAL, off=(0, 0))
    # API
    box(ax, 0.3, 1.45, 9.4, 2.15, "", fc=GREY, ec=NAVY)
    ax.text(0.5, 3.4, "CAPA DE APLICACIÓN · Node 20 + Express 4 + TypeScript 5 (API REST v2.0.0)",
            fontsize=8, fontweight="bold", color=NAVY, va="center")
    mids = ["helmet · cors", "rateLimit\n200/15 min", "auth JWT\nHS256", "role\nADMIN|OPERATOR", "validate\n(Zod)", "errorHandler"]
    for i, t in enumerate(mids):
        box(ax, 0.5 + i * 1.55, 2.75, 1.4, 0.5, t, fs=6.5, fc="white")
    box(ax, 0.5, 2.0, 2.2, 0.55, "Routes\n/auth /products /orders\n/clients /dashboard /external", fs=6, fc=LIGHT)
    box(ax, 2.85, 2.0, 2.0, 0.55, "Controllers\n(7)", fs=7, fc=LIGHT)
    box(ax, 5.0, 2.0, 2.2, 0.55, "Dominio\nentities · interfaces", fs=7, fc=LIGHT)
    box(ax, 7.35, 2.0, 2.2, 0.55, "RepositoryFactory\nPG | Memory", fs=7, fc=LIGHT)
    box(ax, 0.5, 1.55, 9.05, 0.3, "Seguridad: bcryptjs (10 rondas) · JWT_SECRET y WEBHOOK_SECRET fail-fast · HMAC-SHA256 en webhook",
        fs=6.5, fc="#FEF3C7", ec=AMBER)
    arrow(ax, 8.45, 1.45, 8.45, 1.0, "pg Pool · SQL parametrizado", color=TEAL, off=(1.25, 0))
    # Datos
    box(ax, 0.3, 0.1, 9.4, 0.9, "", fc=GREY, ec=NAVY)
    ax.text(0.5, 0.82, "CAPA DE DATOS · PostgreSQL 16", fontsize=8, fontweight="bold", color=NAVY, va="center")
    box(ax, 0.5, 0.2, 2.5, 0.45, "12 tablas · 2 vistas", fs=7, fc="white")
    box(ax, 3.15, 0.2, 3.0, 0.45, "Triggers: updated_at · descuento de stock", fs=7, fc="white")
    box(ax, 6.3, 0.2, 3.25, 0.45, "CHECK · FK · índices · secuencia de pedidos", fs=7, fc="white")
    save(fig, "fig_arquitectura_logica.png")


# ---------------------------------------------------------------- 2. Despliegue
def fig_despliegue():
    fig, ax = canvas(10, 5.6, "Topología de despliegue en producción")
    box(ax, 0.2, 2.0, 1.8, 1.3, "Navegador\nPWA instalable\n(escritorio / móvil)", fc="white", ec=NAVY, fs=8, bold=True)
    box(ax, 2.9, 3.5, 2.6, 1.3, "GitHub Pages\nfrontend estático (dist)\nCDN global", fc=LIGHT, fs=8, bold=True)
    box(ax, 2.9, 0.4, 2.6, 1.3, "GitHub Actions\ndeploy.yml · Node 22\nbuild → rama gh-pages", fc=GREY, fs=8)
    box(ax, 6.2, 2.0, 2.0, 1.3, "Render Web Service\nNode 20 nativo\nplan free · oregon", fc=LIGHT, fs=8, bold=True)
    box(ax, 8.4, 2.0, 1.5, 1.3, "Render\nPostgreSQL\nleofit_db", fc="#DCFCE7", ec=GREEN, fs=8, bold=True)
    arrow(ax, 2.0, 2.9, 2.9, 4.0, "GET estáticos", color=TEAL)
    arrow(ax, 2.0, 2.65, 6.2, 2.65, "HTTPS /api/* (JWT) · CORS restringido a github.io", color=TEAL, off=(0, 0.2))
    arrow(ax, 8.2, 2.65, 8.4, 2.65, None, color=GREEN)
    arrow(ax, 4.2, 1.7, 4.2, 3.5, "publica", color=INK, ls="--", off=(0.35, 0))
    ax.text(6.3, 1.5, "healthCheckPath: /api/health\nbuild: npm install --include=dev && npm run build\nstart: npm start",
            fontsize=6.5, color=INK, va="top")
    box(ax, 6.2, 0.3, 3.7, 0.55, "Referencia autohospedada: docker-compose (PostgreSQL 16 + PgBouncer + réplica WAL)",
        fc="white", ec=AMBER, fs=6.5)
    ax.text(6.2, 0.95, "No forma parte del entorno productivo actual", fontsize=6.5, color=AMBER, style="italic")
    save(fig, "fig_despliegue.png")


# ---------------------------------------------------------------- 3. Secuencia pedido
def fig_secuencia():
    fig, ax = canvas(10, 6.4, "Secuencia de creación de un pedido (POST /api/orders)")
    actors = [("Operador\n(PWA)", 0.9), ("API Express\n(middlewares)", 3.0), ("OrderController\n+ Repositorio", 5.2), ("PostgreSQL", 7.5), ("Trigger\nstock", 9.2)]
    for name, x in actors:
        box(ax, x - 0.7, 5.4, 1.4, 0.6, name, fc=NAVY, ec=NAVY, tc="white", fs=7, bold=True)
        ax.plot([x, x], [0.2, 5.4], color="#94A3B8", lw=0.8, ls="--")
    X = {n: x for n, x in actors}
    xs = [a[1] for a in actors]
    steps = [
        (0, 1, 5.0, "1. POST /orders + Bearer JWT", False),
        (1, 1, 4.65, "2. helmet · rateLimit · verifyJWT · validate(Zod)", True),
        (1, 2, 4.3, "3. createOrder(payload)", False),
        (2, 3, 3.95, "4. BEGIN (READ COMMITTED)", False),
        (2, 3, 3.6, "5. SELECT … FOR UPDATE (variantes)", False),
        (2, 3, 3.25, "6. upsert cliente por teléfono", False),
        (2, 3, 2.9, "7. INSERT orders · INSERT order_items", False),
        (3, 4, 2.55, "8. AFTER INSERT → decrementa stock", False),
        (2, 3, 2.2, "9. COMMIT  (40001/40P01 → reintento con backoff)", False),
        (2, 1, 1.85, "10. 201 {success:true, data:LEO-AAAAMMDD-NNNNNN}", False),
        (1, 0, 1.5, "11. 201 Created / 409 INSUFFICIENT_STOCK", False),
    ]
    for a, b, y, t, selfmsg in steps:
        if selfmsg:
            arrow(ax, xs[a], y, xs[a] + 0.55, y, None, color=TEAL)
            ax.text(xs[a] + 0.65, y, t, fontsize=6.5, va="center", color=INK)
        else:
            col = RED if "409" in t else (GREEN if "201" in t else TEAL)
            ls = "--" if b < a else "-"
            arrow(ax, xs[a], y, xs[b], y, None, color=col, ls=ls)
            ax.text((xs[a] + xs[b]) / 2, y + 0.11, t, fontsize=6.2, ha="center", color=INK,
                    bbox=dict(fc="white", ec="none", pad=0.4))
    save(fig, "fig_secuencia_pedido.png")


# ---------------------------------------------------------------- 4. Estados
def fig_estados():
    fig, ax = canvas(10, 3.4, "Máquina de estados del pedido (order_status_enum)")
    items = [("RECIBIDO", 0.3, LIGHT), ("PREPARACION", 2.5, LIGHT), ("EN_CAMINO", 4.7, LIGHT), ("ENTREGADO", 6.9, "#DCFCE7")]
    for t, x, c in items:
        box(ax, x, 1.6, 1.8, 0.7, t, fc=c, fs=8, bold=True)
    for i in range(3):
        arrow(ax, items[i][1] + 1.8, 1.95, items[i + 1][1], 1.95, "PATCH /status", color=TEAL, fs=6)
    box(ax, 4.1, 0.2, 2.2, 0.6, "CANCELADO\n(POST /:id/cancel)", fc="#FEE2E2", ec=RED, fs=7.5, bold=True)
    for t, x, c in items[:3]:
        arrow(ax, x + 0.9, 1.6, 5.2, 0.8, None, color=RED, ls="--")
    box(ax, 8.9, 1.6, 0.9, 0.7, "order_status_\nhistory", fc=GREY, fs=6)
    arrow(ax, 8.7, 1.95, 8.9, 1.95, None, color=INK, ls=":")
    ax.text(0.3, 0.55, "Cada transición se registra en order_status_history.\nLa cancelación se admite antes de la entrega.",
            fontsize=6.8, color=INK, va="center")
    save(fig, "fig_estados_pedido.png")


# ---------------------------------------------------------------- 5. Pruebas por suite
def fig_pruebas():
    fig, axs = plt.subplots(1, 2, figsize=(10, 4.2), dpi=200, gridspec_kw={"width_ratios": [1.15, 1]})
    be = [("orders", 13), ("auth", 8), ("integration_external", 7), ("webhook", 5), ("products", 3),
          ("clients_dashboard", 3), ("security", 3), ("regression_api_contract", 3), ("jwt", 2)]
    be.sort(key=lambda t: t[1])
    axs[0].barh([b[0] for b in be], [b[1] for b in be], color=TEAL)
    for i, b in enumerate(be):
        axs[0].text(b[1] + 0.2, i, str(b[1]), va="center", fontsize=8, color=INK)
    axs[0].set_title("Backend · Jest (47 aprobadas)", fontsize=10, color=NAVY, fontweight="bold")
    axs[0].set_xlim(0, 15)
    fe = [("allTabsFunctional", 12), ("AppContext", 11), ("usability_iso25010", 9), ("mappers", 8),
          ("api", 6), ("mockData", 4), ("PedidoForm", 3), ("pdfGenerator", 1)]
    fe.sort(key=lambda t: t[1])
    axs[1].barh([f[0] for f in fe], [f[1] for f in fe], color=CYAN)
    for i, f in enumerate(fe):
        axs[1].text(f[1] + 0.2, i, str(f[1]), va="center", fontsize=8, color=INK)
    axs[1].set_title("Frontend · Vitest (54 aprobadas)", fontsize=10, color=NAVY, fontweight="bold")
    axs[1].set_xlim(0, 15)
    for a in axs:
        a.spines[["top", "right"]].set_visible(False)
        a.tick_params(labelsize=8)
        a.set_xlabel("Casos de prueba", fontsize=8)
    fig.tight_layout()
    save(fig, "fig_pruebas_por_suite.png")


# ---------------------------------------------------------------- 6. Cobertura
def fig_cobertura():
    mods = [("routes", 100), ("validators (Zod)", 100), ("jwt.utils", 100), ("password.utils", 100),
            ("middlewares", 80.9), ("memory.repositories", 74.9), ("controllers", 65.0), ("pg.repositories*", 6.7)]
    mods.sort(key=lambda t: t[1])
    fig, ax = plt.subplots(figsize=(8.4, 4.2), dpi=200)
    cols = [AMBER if m[0].startswith("pg") else (GREEN if m[1] >= 80 else TEAL) for m in mods]
    ax.barh([m[0] for m in mods], [m[1] for m in mods], color=cols)
    for i, m in enumerate(mods):
        ax.text(m[1] + 1, i, f"{m[1]:.1f}%", va="center", fontsize=8)
    ax.set_xlim(0, 112)
    ax.set_xlabel("Cobertura de líneas (%)", fontsize=9)
    ax.set_title("Cobertura de líneas por módulo del backend", fontsize=10, color=NAVY, fontweight="bold")
    ax.spines[["top", "right"]].set_visible(False)
    ax.text(0, -0.2, "* Adaptador PostgreSQL: requiere base real (suite integration_repositories condicionada por RUN_INTEGRATION_TESTS).",
            transform=ax.transAxes, fontsize=6.5, color="#475569")
    fig.tight_layout()
    save(fig, "fig_cobertura_modulos.png")


# ---------------------------------------------------------------- 7. CI/CD
def fig_cicd():
    fig, ax = canvas(10, 3.6, "Flujo de integración y despliegue continuos")
    stages = [("push / PR\na main", 0.2, GREY), ("Instalación\nnpm ci", 1.85, LIGHT), ("Compilación\ntsc · vite build", 3.5, LIGHT),
              ("Pruebas\nJest · Vitest", 5.15, LIGHT), ("Auditoría\nnpm audit\n--audit-level=high", 6.8, "#FEF3C7"),
              ("Despliegue\nPages / Render", 8.45, "#DCFCE7")]
    for t, x, c in stages:
        box(ax, x, 1.5, 1.4, 1.0, t, fc=c, fs=7.5, bold=True)
    for i in range(len(stages) - 1):
        arrow(ax, stages[i][1] + 1.4, 2.0, stages[i + 1][1], 2.0, None, color=TEAL)
    ax.text(0.2, 0.9, "Workflows: backend-ci-cd.yml · security-scan.yml (incluye verificación de .env no versionados) · deploy.yml · dependabot.yml",
            fontsize=7, color=INK)
    ax.text(0.2, 0.5, "Render redepliega el backend desde render.yaml (autoDeploy); GitHub Pages publica la rama gh-pages.", fontsize=7, color=INK)
    save(fig, "fig_cicd.png")


# ---------------------------------------------------------------- 8. Pirámide / estrategia
def fig_estrategia():
    fig, ax = canvas(9, 4.6, "Estrategia de pruebas en niveles")
    levels = [("Contrato e integración de API (Supertest)\n47 casos backend", 0.2, 8.6, LIGHT),
              ("Componentes y contexto (Testing Library · jsdom)\n54 casos frontend", 1.2, 6.6, "#CFFAFE"),
              ("Unidades puras (JWT · password · mappers · validadores)", 2.2, 4.6, "#A5F3FC"),
              ("Usabilidad automatizada (ISO/IEC 25010)\n9 casos", 3.2, 2.6, "#67E8F9")]
    for t, y, w, c in levels:
        box(ax, (9 - w) / 2, 3.6 - (y - 0.2) , w, 0.8, t, fc=c, fs=7.5)
    ax.text(4.5, 0.3, "Total: 101 casos aprobados · 1 omitido (integración con PostgreSQL real, condicionado)",
            fontsize=8, ha="center", color=NAVY, fontweight="bold")
    save(fig, "fig_estrategia_pruebas.png")


# ---------------------------------------------------------------- 9. Modelo de capas / repositorio
def fig_repositorio():
    fig, ax = canvas(9, 4.2, "Patrón Repository y Factory (arquitectura limpia)")
    box(ax, 0.3, 2.9, 2.2, 0.8, "Controllers", fc=LIGHT, bold=True)
    box(ax, 3.4, 2.9, 2.6, 0.8, "Interfaces de dominio\n(IProductRepository,\nIOrderRepository…)", fc="#FEF3C7", ec=AMBER, fs=7.5, bold=True)
    box(ax, 6.9, 2.9, 2.0, 0.8, "RepositoryFactory", fc=LIGHT, bold=True)
    box(ax, 3.4, 1.1, 1.2, 0.8, "PG\n(pg Pool)", fc="#DCFCE7", ec=GREEN, bold=True)
    box(ax, 4.9, 1.1, 1.2, 0.8, "Memory\n(pruebas)", fc=GREY, bold=True)
    arrow(ax, 2.5, 3.3, 3.4, 3.3, "usa", color=TEAL)
    arrow(ax, 6.9, 3.3, 6.0, 3.3, "inyecta", color=TEAL)
    arrow(ax, 4.0, 1.9, 4.2, 2.9, "implementa", color=INK, ls="--", off=(-0.5, 0))
    arrow(ax, 5.5, 1.9, 5.2, 2.9, None, color=INK, ls="--")
    arrow(ax, 7.9, 2.9, 6.1, 1.5, "elige según\nDATABASE_URL / disponibilidad", color=TEAL, fs=6.5, off=(0.6, 0.1))
    ax.text(0.3, 0.5, "Los controladores dependen de abstracciones; la infraestructura es intercambiable sin modificar la lógica de negocio.",
            fontsize=7, color=INK)
    save(fig, "fig_repositorio_factory.png")


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
