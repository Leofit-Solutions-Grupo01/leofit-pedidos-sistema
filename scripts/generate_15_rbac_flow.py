# -*- coding: utf-8 -*-
"""
Genera el Diagrama de Flujo End-to-End de Llamadas y Respuestas por Rol (RBAC):
Perfil ADMINISTRADOR (ADMIN) vs. Perfil OPERADOR (OPERATOR)
con tipografía grande, legible, alto contraste y optimizada para lectura en pantallas y documentos.
"""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_DIR = os.path.join(REPO_ROOT, "docs", "04_diagramas_arquitectura_y_negocio")
OUT_PNG = os.path.join(OUT_DIR, "15_Flujo_RBAC_Admin_vs_Operador.png")
OUT_MMD = os.path.join(OUT_DIR, "15_Flujo_RBAC_Admin_vs_Operador.mmd")

MMD_CONTENT = """flowchart LR
    subgraph ADMIN["PERFIL 1: ADMINISTRADOR (admin@leofit.pe | role: ADMIN)"]
        A1["Login PWA -> POST /api/auth/login\nRecibe JWT (role=ADMIN) + Cookie HttpOnly"]
        A2["GET /api/dashboard/metrics\n-> 200 OK (KPIs financieros S/ + Alertas Stock)"]
        A3["POST/PUT/DELETE /api/products & PATCH stock\n-> 200/201 OK (Muta products & product_variants + audit_log)"]
        A4["POST /api/orders/:id/cancel | /refund | /credit-note\n-> 200 OK (Restituye stock + Nota Crédito SUNAT + audit_log)"]
        A5["POST /api/orders & PATCH /api/orders/:id/status\n-> 201/200 OK (Flujo operativo completo)"]
    end

    subgraph PIPE["PIPELINE PERIMETRAL BACKEND (Render Free - S/ 0.00)"]
        M1["1. Helmet + CORS + Correlation-ID"]
        M2["2. RateLimiter + Idempotency-Key"]
        M3["3. authenticateToken (Verifica JWT HMAC-SHA256)"]
        M4{"4. requireRole('ADMIN')\nen rutas críticas"}
        M5["5. validateBody (Zod) + audit()"]
    end

    subgraph OPER["PERFIL 2: OPERADOR LOGÍSTICO (operador@leofit.pe | role: OPERATOR)"]
        O1["Login PWA -> POST /api/auth/login\nRecibe JWT (role=OPERATOR) | UI oculta botones destructivos"]
        O2["GET /api/products & GET /api/orders\n-> 200 OK (Consulta catálogo y cola de despacho)"]
        O3["POST /api/orders (Idempotency-Key)\n-> 201 Created (LOCK FOR UPDATE + Descuento Stock ACID)"]
        O4["PATCH /api/orders/:id/status\n(RECIBIDO -> PREPARACION -> EN_CAMINO -> ENTREGADO) -> 200 OK"]
        O5["Intento de POST/DELETE /api/products o /cancel o /refund\n-> 403 FORBIDDEN (Bloqueado en Middleware RBAC)"]
    end

    subgraph NEON["BASE DE DATOS NEON POSTGRESQL (neondb - S/ 0.00)"]
        DB1[("22 Tablas BCNF + 2 Vistas\norders, product_variants,\ninvoices, audit_log")]
    end

    A1 --> M1 --> M2 --> M3 --> M4
    O1 --> M1
    M4 -->|"role == ADMIN (PASA)"| M5 --> DB1
    M4 -->|"role == OPERATOR (BLOQUEA)"| O5
    M3 -->|"Rutas Operativas (ADMIN u OPERATOR)"| DB1
    DB1 --> A2 & A3 & A4 & A5
    DB1 --> O2 & O3 & O4
"""

def draw_card(ax, x, y, w, h, title, subtitle, bg_color, border_color, title_color="#FFFFFF", items=None):
    # Sombra
    shadow = FancyBboxPatch(
        (x + 0.06, y - 0.06), w, h,
        boxstyle="round,pad=0.03,rounding_size=0.12",
        facecolor="#020617", edgecolor="none", alpha=0.45, zorder=2
    )
    ax.add_patch(shadow)

    # Cuerpo de tarjeta
    box = FancyBboxPatch(
        (x, y), w, h,
        boxstyle="round,pad=0.03,rounding_size=0.12",
        facecolor=bg_color, edgecolor=border_color, linewidth=2.0, zorder=3
    )
    ax.add_patch(box)

    hdr_h = 0.58 if subtitle else 0.44
    hdr = FancyBboxPatch(
        (x, y + h - hdr_h), w, hdr_h,
        boxstyle="round,pad=0.03,rounding_size=0.12",
        facecolor=border_color, edgecolor=border_color, linewidth=1.2, zorder=4
    )
    ax.add_patch(hdr)

    ax.text(
        x + w / 2, y + h - (0.22 if subtitle else hdr_h / 2),
        title, color=title_color, fontsize=12.2, fontweight="bold",
        ha="center", va="center", zorder=5
    )
    if subtitle:
        ax.text(
            x + w / 2, y + h - 0.44,
            subtitle, color="#E2E8F0", fontsize=9.8,
            ha="center", va="center", zorder=5
        )

    if items:
        curr_y = y + h - hdr_h - 0.22
        row_step = (h - hdr_h - 0.30) / len(items)
        for badge, endpoint, desc, resp in items:
            badge_bg = "#15803D" if "200" in badge or "201" in badge else ("#B91C1C" if "403" in badge else "#1D4ED8")
            b_patch = FancyBboxPatch(
                (x + 0.16, curr_y - 0.20), 1.25, 0.32,
                boxstyle="round,pad=0.02,rounding_size=0.06",
                facecolor=badge_bg, edgecolor="none", zorder=5
            )
            ax.add_patch(b_patch)
            ax.text(
                x + 0.785, curr_y - 0.04, badge,
                color="#FFFFFF", fontsize=9.5, fontweight="bold",
                ha="center", va="center", family="DejaVu Sans Mono", zorder=6
            )
            ax.text(
                x + 1.55, curr_y - 0.02, endpoint,
                color="#F8FAFC", fontsize=10.6, fontweight="bold",
                ha="left", va="center", family="DejaVu Sans Mono", zorder=5
            )
            ax.text(
                x + 1.55, curr_y - 0.25, desc,
                color="#CBD5E1", fontsize=9.4,
                ha="left", va="center", zorder=5
            )
            ax.text(
                x + w - 0.20, curr_y - 0.13, resp,
                color="#38BDF8" if "403" not in badge else "#FCA5A5",
                fontsize=9.8, fontweight="bold",
                ha="right", va="center", family="DejaVu Sans Mono", zorder=5
            )
            curr_y -= row_step

def draw_arrow(ax, x1, y1, x2, y2, color="#38BDF8", label=""):
    ax.annotate(
        "", xy=(x2, y2), xytext=(x1, y1),
        arrowprops=dict(arrowstyle="-|>,head_width=0.30,head_length=0.45", lw=2.2, color=color),
        zorder=6
    )
    if label:
        mx, my = (x1 + x2) / 2, (y1 + y2) / 2
        ax.text(
            mx, my + 0.12, label, color="#F8FAFC", fontsize=9.2, fontweight="bold",
            ha="center", va="bottom",
            bbox=dict(boxstyle="round,pad=0.20", facecolor="#0F172A", edgecolor=color, lw=1.2),
            zorder=7
        )

def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    with open(OUT_MMD, "w", encoding="utf-8") as f:
        f.write(MMD_CONTENT)

    fig, ax = plt.subplots(figsize=(24, 15.5), dpi=180)
    fig.patch.set_facecolor("#0B1120")
    ax.set_facecolor("#0B1120")
    ax.set_xlim(0, 24)
    ax.set_ylim(0, 15.5)
    ax.axis("off")

    # Banner Superior de Título
    banner = FancyBboxPatch(
        (0.40, 14.10), 23.2, 1.10,
        boxstyle="round,pad=0.03,rounding_size=0.14",
        facecolor="#1E3A8A", edgecolor="#3B82F6", linewidth=2.2, zorder=3
    )
    ax.add_patch(banner)
    ax.text(
        12.0, 14.80,
        "FLUJO END-TO-END DE LLAMADAS Y RESPUESTAS POR PERFIL (RBAC): ADMIN vs. OPERADOR",
        color="#FFFFFF", fontsize=16.5, fontweight="bold", ha="center", va="center", zorder=5
    )
    ax.text(
        12.0, 14.36,
        "Arquitectura Funcional Real de Costo S/ 0.00: Frontend PWA (Render/GitHub Pages)  -->  API Node.js (Render Free)  -->  Neon PostgreSQL (neondb)",
        color="#BAE6FD", fontsize=11.2, ha="center", va="center", zorder=5
    )

    # 1A. PANEL IZQUIERDO ARRIBA: ADMINISTRADOR (role = ADMIN)
    draw_card(
        ax, 0.40, 7.80, 4.40, 6.00,
        "1A. PERFIL ADMINISTRADOR (PWA)",
        "admin@leofit.pe | Rol: ADMIN (Control Total)",
        "#1E293B", "#2563EB"
    )
    admin_steps = [
        ("PASO 1: Login e Identidad JWT",
         "POST /api/auth/login -> Valida hash bcrypt en users.\nRecibe Access Token (role='ADMIN', exp=15m) +\nCookie HttpOnly leofit_rt con rotación segura."),
        ("PASO 2: UI Completa Habilitada",
         "AppContext detecta role === 'ADMIN':\n- Muestra KPIs financieros y márgenes en Dashboard.\n- Habilita botones: + Nuevo Producto, Editar Stock,\n  Eliminar Prenda, Cancelar Pedido y Reembolsos."),
        ("PASO 3: Emisión de Peticiones",
         "apiFetch() inyecta automáticamente:\n- Authorization: Bearer <JWT_ADMIN>\n- Idempotency-Key: <UUIDv4> (en POST /orders)\n- X-Correlation-ID: <trace_id>"),
    ]
    sy = 12.80
    for st_title, st_body in admin_steps:
        ax.text(0.65, sy, st_title, color="#60A5FA", fontsize=10.4, fontweight="bold", zorder=5)
        ax.text(0.65, sy - 0.60, st_body, color="#F1F5F9", fontsize=9.4, va="center", zorder=5, linespacing=1.25)
        sy -= 1.82

    # 3A. RESPUESTAS ADMIN (DERECHA ARRIBA)
    draw_card(
        ax, 10.70, 7.80, 12.90, 6.00,
        "3A. RESPUESTAS OBTENIDAS POR EL ADMINISTRADOR EN CADA LLAMADA (100% AUTORIZADO)",
        "Todas las rutas operativas y administrativas pasan requireRole('ADMIN') y ejecutan en Neon PostgreSQL (neondb)",
        "#0F172A", "#15803D",
        items=[
            ("200 OK", "GET /api/dashboard/metrics", "Consulta vistas vw_orders_summary + vw_low_stock_alert + ingresos totales", "KPIs + Alertas Stock"),
            ("201 CREATED", "POST /api/products", "Crea nueva prenda en tabla products + registra auditoría en audit_log", "Prenda creada en BD"),
            ("200 OK", "PATCH /api/products/variant/:id/stock", "Actualiza stock físico de variante SKU (SET/INCREMENT/DECREMENT) + audit_log", "Stock actualizado"),
            ("200 OK", "DELETE /api/products/:id", "Ejecuta Soft-Delete (deleted_at = NOW()) en products + trazabilidad audit_log", "Baja lógica aplicada"),
            ("201 CREATED", "POST /api/orders (Idempotency-Key)", "Transacción ACID: SELECT FOR UPDATE -> INSERT order/items -> Descuenta stock", "Pedido #ORD creado"),
            ("200 OK", "PATCH /api/orders/:id/status", "Transiciona estado (RECIBIDO->PREPARACION->EN_CAMINO->ENTREGADO) + historial", "Estado actualizado"),
            ("200 OK", "POST /api/orders/:id/cancel | /refund", "Cancela pedido, restituye stock automáticamente y emite Nota de Crédito SUNAT", "Stock restituido + NC"),
            ("201 CREATED", "POST /api/invoices/emit", "Encola y emite Boleta (BBB1) o Factura (FFF1) electrónica UBL 2.1 con IGV 18%", "XML + CDR SUNAT"),
        ]
    )

    # 2. COLUMNA CENTRAL: PIPELINE BACKEND + MOTOR NEON DB
    draw_card(
        ax, 5.20, 1.25, 5.10, 12.55,
        "2. PIPELINE BACKEND & NEON DB",
        "leofit-backend-api (Render) + neondb (Neon)",
        "#1E1B4B", "#7C3AED"
    )
    pipe_boxes = [
        ("MW-1: Perímetro HTTP", "Helmet (CSP / HSTS) + CORS Multi-Origen\n+ X-Correlation-ID (AsyncLocalStorage)", "#312E81", "#6366F1", 11.60),
        ("MW-2: Control de Tráfico", "RateLimiter perimetral (anti-fuerza bruta)\n+ Idempotency Lock (tabla idempotency_keys)", "#312E81", "#6366F1", 9.95),
        ("MW-3: authenticateToken", "Valida firma JWT (HMAC-SHA256 + kid v1)\nExtrae req.user = { id, email, role }", "#1E3A8A", "#3B82F6", 8.30),
        ("MW-4: requireRole('ADMIN')", "Compuerta RBAC Estricta (OWASP A01):\n¿req.user.role === 'ADMIN'?\n- SÍ -> Pasa al Controlador y Neon DB\n- NO (OPERATOR) -> Corta con HTTP 403", "#7C2D12", "#F97316", 6.25),
        ("MW-5: Zod + audit()", "Valida esquema DTO estricto de entrada\ny graba before/after en tabla audit_log", "#14532D", "#22C55E", 4.60),
        ("MOTOR NEON POSTGRESQL", "Host: ep-young-lake-akgakejb (Oregon)\n22 Tablas BCNF + 2 Vistas Analíticas\nTransacciones ACID + Triggers Stock\nCosto: $0.00 / S/ 0.00 perpetuo", "#064E3B", "#10B981", 2.45),
    ]
    for p_title, p_desc, p_bg, p_bd, py in pipe_boxes:
        ph = 1.80 if "MW-4" in p_title or "NEON" in p_title else 1.40
        pb = FancyBboxPatch(
            (5.42, py), 4.66, ph,
            boxstyle="round,pad=0.03,rounding_size=0.09",
            facecolor=p_bg, edgecolor=p_bd, linewidth=1.8, zorder=4
        )
        ax.add_patch(pb)
        header_y = py + ph - 0.28
        body_y = py + (ph - 0.28) / 2
        ax.text(7.75, header_y, p_title, color="#FFFFFF", fontsize=10.6, fontweight="bold", ha="center", va="center", zorder=5)
        ax.text(7.75, body_y, p_desc, color="#F1F5F9", fontsize=9.2, ha="center", va="center", zorder=5, linespacing=1.2)

    # 1B. PANEL IZQUIERDO ABAJO: OPERADOR (role = OPERATOR)
    draw_card(
        ax, 0.40, 1.25, 4.40, 6.25,
        "1B. PERFIL OPERADOR (PWA)",
        "operador@leofit.pe | Rol: OPERATOR (Logística)",
        "#1E293B", "#0D9488"
    )
    oper_steps = [
        ("PASO 1: Login Operativo",
         "POST /api/auth/login -> Valida credenciales.\nRecibe Access Token con claim role='OPERATOR'."),
        ("PASO 2: Restricción Preventiva en UI",
         "AppContext detecta role === 'OPERATOR':\n- Oculta creación, edición y borrado de productos.\n- Oculta opción 'Cancelar Pedido' en el listado.\n- Enfoca la vista en despacho y seguimiento."),
        ("PASO 3: Defensa en Profundidad (API)",
         "Aunque intente invocar rutas de Admin vía\nPostman o cURL, el token lleva role='OPERATOR'\ny el middleware requireRole corta con 403."),
    ]
    osy = 6.70
    for st_title, st_body in oper_steps:
        ax.text(0.65, osy, st_title, color="#2DD4BF", fontsize=10.4, fontweight="bold", zorder=5)
        ax.text(0.65, osy - 0.60, st_body, color="#F1F5F9", fontsize=9.4, va="center", zorder=5, linespacing=1.25)
        osy -= 1.85

    # 3B. RESPUESTAS OPERADOR (DERECHA ABAJO)
    draw_card(
        ax, 10.70, 1.25, 12.90, 6.25,
        "3B. RESPUESTAS OBTENIDAS POR EL OPERADOR EN CADA LLAMADA (PERMITIDAS vs. BLOQUEADAS POR RBAC)",
        "Principio de Mínimo Privilegio (ISO/IEC 25010 Seguridad): Opera despacho completo pero no puede alterar precios ni anular ventas",
        "#0F172A", "#0D9488",
        items=[
            ("200 OK", "GET /api/products & /alerts/low-stock", "Lee catálogo de prendas, tallas, colores y alertas de stock bajo desde Neon", "Catálogo en vivo"),
            ("200 OK", "GET /api/orders & GET /api/orders/:id", "Consulta cola de pedidos pendientes de empaque y despacho ( Lima / Provincia )", "Lista de pedidos"),
            ("201 CREATED", "POST /api/orders (Idempotency-Key)", "Registra nuevo pedido de cliente WhatsApp y descuenta stock atómicamente en Neon", "Pedido #ORD creado"),
            ("200 OK", "PATCH /api/orders/:id/status", "Avanza estado logístico: RECIBIDO -> PREPARACION -> EN_CAMINO -> ENTREGADO", "Estado + Historial"),
            ("200 OK", "GET /api/sunat/ruc/:numero", "Consulta validez de RUC/DNI para despacho con guía o comprobante", "Datos contribuyente"),
            ("403 FORBIDDEN", "POST / PUT / DELETE /api/products", "Bloqueado por requireRole('ADMIN'): Operador no puede crear ni borrar prendas", "Error: FORBIDDEN"),
            ("403 FORBIDDEN", "PATCH /api/products/variant/:id/stock", "Bloqueado por requireRole('ADMIN'): Operador no puede alterar stock manualmente", "Error: FORBIDDEN"),
            ("403 FORBIDDEN", "POST /api/orders/:id/cancel | /refund", "Bloqueado por requireRole('ADMIN'): Solo Admin puede anular pedidos o reembolsar", "Error: FORBIDDEN"),
        ]
    )

    # Conectores y Flechas
    draw_arrow(ax, 4.80, 10.80, 5.20, 10.80, color="#60A5FA", label="JWT (ADMIN)")
    draw_arrow(ax, 4.80, 4.40, 5.20, 4.40, color="#2DD4BF", label="JWT (OPERATOR)")
    draw_arrow(ax, 10.30, 10.80, 10.70, 10.80, color="#4ADE80", label="200 / 201 OK")
    draw_arrow(ax, 10.30, 5.20, 10.70, 5.20, color="#2DD4BF", label="200 OK (Operativas)")
    draw_arrow(ax, 10.30, 2.60, 10.70, 2.60, color="#F87171", label="403 FORBIDDEN")

    # Pie de Página Explicativo
    ax.text(
        12.0, 0.45,
        "INFRAESTRUCTURA 100% GRATUITA (S/ 0.00 / MES):  Frontend PWA en Render Static + GitHub Pages ($0)   |   Backend API en Render Web Service Free ($0)   |   Base de Datos PostgreSQL en Neon Free Tier ($0 sin caducidad)",
        color="#94A3B8", fontsize=10.2, fontweight="bold", ha="center", va="center",
        bbox=dict(boxstyle="round,pad=0.35", facecolor="#0F172A", edgecolor="#334155", lw=1.4),
        zorder=5
    )

    plt.tight_layout(pad=0.25)
    plt.savefig(OUT_PNG, dpi=180, facecolor=fig.get_facecolor())
    plt.close(fig)
    print(f"Generated {OUT_PNG} ({os.path.getsize(OUT_PNG)} bytes)")

if __name__ == "__main__":
    main()
