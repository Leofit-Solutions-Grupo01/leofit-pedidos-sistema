# -*- coding: utf-8 -*-
"""
Diagrama Vertical de Flujo RBAC: ADMIN vs. OPERADOR
Diseñado con ancho compacto (15 pulgadas) y tipografía grande (11-18pt)
para lectura directa y cómoda en cualquier monitor o visor de documentos sin necesidad de zoom.
"""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_DIR = os.path.join(REPO_ROOT, "docs", "04_diagramas_arquitectura_y_negocio")
OUT_PNG = os.path.join(OUT_DIR, "15_Flujo_RBAC_Admin_vs_Operador.png")

def main():
    os.makedirs(OUT_DIR, exist_ok=True)

    # Ancho contenido (15 pulgadas) x Alto generoso (25 pulgadas) para evitar el efecto de compresión horizontal
    fig, ax = plt.subplots(figsize=(15.5, 25.5), dpi=160)
    fig.patch.set_facecolor("#080D1A")
    ax.set_facecolor("#080D1A")
    ax.set_xlim(0, 15.5)
    ax.set_ylim(0, 25.5)
    ax.axis("off")

    # 1. ENCABEZADO PRINCIPAL (BANNER)
    hdr_box = FancyBboxPatch(
        (0.5, 23.8), 14.5, 1.35,
        boxstyle="round,pad=0.04,rounding_size=0.15",
        facecolor="#1E3A8A", edgecolor="#3B82F6", linewidth=2.5, zorder=3
    )
    ax.add_patch(hdr_box)
    ax.text(
        7.75, 24.65,
        "FLUJO END-TO-END RBAC: ADMINISTRADOR vs. OPERADOR",
        color="#FFFFFF", fontsize=17.5, fontweight="bold", ha="center", va="center", zorder=5
    )
    ax.text(
        7.75, 24.15,
        "Llamadas API, Compuertas de Seguridad y Respuestas en Base de Datos (Neon S/ 0.00)",
        color="#BAE6FD", fontsize=12.0, ha="center", va="center", zorder=5
    )

    # 2. BLOQUE CENTRAL: PIPELINE DE MIDDLEWARES Y COMPUERTA RBAC
    mw_card = FancyBboxPatch(
        (0.5, 20.3), 14.5, 3.2,
        boxstyle="round,pad=0.04,rounding_size=0.15",
        facecolor="#0F172A", edgecolor="#6366F1", linewidth=2.0, zorder=3
    )
    ax.add_patch(mw_card)
    ax.text(
        7.75, 23.15,
        "PIPELINE DE SEGURIDAD BACKEND (leofit-backend-api en Render)",
        color="#A5B4FC", fontsize=13.0, fontweight="bold", ha="center", va="center", zorder=5
    )

    # Pastillas horizontales de los middlewares
    mws = [
        ("1. Perímetro", "Helmet (HSTS/CSP)\nCORS Seguro", "#1E1B4B", "#4F46E5"),
        ("2. Tráfico", "RateLimiter\nIdempotency-Key", "#1E1B4B", "#4F46E5"),
        ("3. Autenticación", "authenticateToken\nVerifica firma JWT", "#1E3A8A", "#2563EB"),
        ("4. Compuerta RBAC", "requireRole('ADMIN')\n¿Es ADMIN?", "#7C2D12", "#EA580C"),
        ("5. Persistencia", "Motor Neon DB\nTransacciones ACID", "#064E3B", "#10B981"),
    ]
    for idx, (m_title, m_desc, m_bg, m_border) in enumerate(mws):
        bx = 0.8 + idx * 2.80
        bp = FancyBboxPatch(
            (bx, 20.6), 2.50, 2.15,
            boxstyle="round,pad=0.03,rounding_size=0.10",
            facecolor=m_bg, edgecolor=m_border, linewidth=1.8, zorder=4
        )
        ax.add_patch(bp)
        ax.text(bx + 1.25, 22.35, m_title, color="#FFFFFF", fontsize=11.0, fontweight="bold", ha="center", zorder=5)
        ax.text(bx + 1.25, 21.45, m_desc, color="#E2E8F0", fontsize=9.8, ha="center", va="center", zorder=5, linespacing=1.25)
        if idx < 4:
            ax.annotate("", xy=(bx + 2.75, 21.65), xytext=(bx + 2.55, 21.65),
                        arrowprops=dict(arrowstyle="-|>,head_width=0.25,head_length=0.30", color="#94A3B8", lw=1.8), zorder=6)

    # 3. SECCIÓN ADMINISTRADOR (role: ADMIN)
    adm_box = FancyBboxPatch(
        (0.5, 11.2), 14.5, 8.8,
        boxstyle="round,pad=0.04,rounding_size=0.15",
        facecolor="#0B132B", edgecolor="#10B981", linewidth=2.4, zorder=3
    )
    ax.add_patch(adm_box)

    # Header Admin
    adm_hdr = FancyBboxPatch(
        (0.5, 19.1), 14.5, 0.9,
        boxstyle="round,pad=0.04,rounding_size=0.15",
        facecolor="#065F46", edgecolor="#10B981", linewidth=1.5, zorder=4
    )
    ax.add_patch(adm_hdr)
    ax.text(0.9, 19.55, "PERFIL 1: ADMINISTRADOR", color="#FFFFFF", fontsize=14.0, fontweight="bold", va="center", zorder=5)
    ax.text(14.6, 19.55, "admin@leofit.pe  |  Rol: ADMIN  |  Acceso Total (100% Autorizado)", color="#A7F3D0", fontsize=11.2, fontweight="bold", ha="right", va="center", zorder=5)

    admin_calls = [
        ("200 OK", "GET /api/dashboard/metrics", "Consulta ingresos totales, pedidos por estado y prendas con stock critico", "Vistas vw_orders_summary + vw_low_stock_alert"),
        ("201 CREATED", "POST /api/products", "Crea nueva prenda deportiva en el catalogo con su categoria", "Inserta en tabla products y registra en audit_log"),
        ("200 OK", "PATCH /api/products/variant/:id/stock", "Ajusta fisicamente el stock de una talla/color (SET / INCREMENT)", "Modifica product_variants y registra en audit_log"),
        ("200 OK", "DELETE /api/products/:id", "Aplica Soft-Delete (deleted_at = NOW()) para retiro del catalogo", "Marca deleted_at en tabla products + audit_log"),
        ("201 CREATED", "POST /api/orders  [Idempotente]", "Crea pedido: SELECT FOR UPDATE -> valida stock -> descuenta unidades", "Transaccion ACID en orders, order_items y variants"),
        ("200 OK", "PATCH /api/orders/:id/status", "Transiciona estado: RECIBIDO -> PREPARACION -> EN_CAMINO -> ENTREGADO", "Actualiza orders e inserta en order_status_history"),
        ("200 OK", "POST /api/orders/:id/cancel", "Cancela pedido, restituye stock a product_variants y emite Nota Credito", "Restaura stock + emite comprobante SUNAT Cat. 09"),
        ("201 CREATED", "POST /api/invoices/emit", "Emite Comprobante Electronico oficial (Boleta BBB1 o Factura FFF1)", "Encola en invoice_queue y genera XML firmado + CDR"),
    ]

    y_adm = 18.55
    for status_code, endpoint, desc, bd_action in admin_calls:
        # Fila de llamada
        row_p = FancyBboxPatch(
            (0.8, y_adm - 0.72), 13.9, 0.78,
            boxstyle="round,pad=0.02,rounding_size=0.08",
            facecolor="#132238", edgecolor="#1E3A5F", linewidth=1.2, zorder=4
        )
        ax.add_patch(row_p)

        # Badge HTTP
        badge_p = FancyBboxPatch(
            (0.95, y_adm - 0.58), 1.65, 0.48,
            boxstyle="round,pad=0.02,rounding_size=0.06",
            facecolor="#15803D" if "200" in status_code or "201" in status_code else "#B91C1C",
            edgecolor="none", zorder=5
        )
        ax.add_patch(badge_p)
        ax.text(1.775, y_adm - 0.34, status_code, color="#FFFFFF", fontsize=10.5, fontweight="bold", ha="center", va="center", family="DejaVu Sans Mono", zorder=6)

        # Endpoint y Descripción
        ax.text(2.80, y_adm - 0.22, endpoint, color="#F8FAFC", fontsize=11.6, fontweight="bold", family="DejaVu Sans Mono", va="center", zorder=5)
        ax.text(2.80, y_adm - 0.52, desc, color="#94A3B8", fontsize=10.0, va="center", zorder=5)

        # Acción en Neon DB
        ax.text(14.5, y_adm - 0.36, bd_action, color="#38BDF8", fontsize=10.2, fontweight="bold", ha="right", va="center", family="DejaVu Sans Mono", zorder=5)

        y_adm -= 0.90

    # 4. SECCIÓN OPERADOR LOGÍSTICO (role: OPERATOR)
    opr_box = FancyBboxPatch(
        (0.5, 2.2), 14.5, 8.7,
        boxstyle="round,pad=0.04,rounding_size=0.15",
        facecolor="#151A28", edgecolor="#F59E0B", linewidth=2.4, zorder=3
    )
    ax.add_patch(opr_box)

    # Header Operador
    opr_hdr = FancyBboxPatch(
        (0.5, 10.0), 14.5, 0.9,
        boxstyle="round,pad=0.04,rounding_size=0.15",
        facecolor="#92400E", edgecolor="#F59E0B", linewidth=1.5, zorder=4
    )
    ax.add_patch(opr_hdr)
    ax.text(0.9, 10.45, "PERFIL 2: OPERADOR LOGÍSTICO", color="#FFFFFF", fontsize=14.0, fontweight="bold", va="center", zorder=5)
    ax.text(14.6, 10.45, "operador@leofit.pe  |  Rol: OPERATOR  |  Principio de Mínimo Privilegio", color="#FDE68A", fontsize=11.2, fontweight="bold", ha="right", va="center", zorder=5)

    oper_calls = [
        # Operaciones Permitidas
        ("200 OK", "GET /api/products & /alerts/low-stock", "Lee catálogo de prendas, tallas, colores y alertas de reposición", "Consulta SELECT directa en productos y variantes"),
        ("200 OK", "GET /api/orders & GET /api/orders/:id", "Visualiza lista de pedidos pendientes de empaque y seguimiento de rutas", "Consulta SELECT en tabla orders con filtros por estado"),
        ("201 CREATED", "POST /api/orders  [Idempotente]", "Registra pedidos de clientes y reserva stock físico automáticamente", "Crea pedido con Idempotency-Key y descuenta stock"),
        ("200 OK", "PATCH /api/orders/:id/status", "Actualiza despacho: RECIBIDO -> PREPARACION -> EN_CAMINO -> ENTREGADO", "Actualiza orders e inserta trazabilidad en historial"),
        ("200 OK", "GET /api/sunat/ruc/:numero", "Consulta datos de RUC/DNI para rotulado de paquetes y comprobantes", "Valida contribuyente ante el servicio tributario"),
        # Operaciones Bloqueadas por RBAC
        ("403 FORBIDDEN", "POST / PUT / DELETE /api/products", "Intento de crear, alterar precios o eliminar prendas del catálogo", "BLOQUEADO por requireRole('ADMIN') en Middleware 4"),
        ("403 FORBIDDEN", "PATCH /api/products/variant/:id/stock", "Intento de manipular el conteo de stock manual de variantes", "BLOQUEADO por requireRole('ADMIN') en Middleware 4"),
        ("403 FORBIDDEN", "POST /api/orders/:id/cancel | /refund", "Intento de cancelar ventas consolidadas o emitir reembolsos", "BLOQUEADO por requireRole('ADMIN') en Middleware 4"),
    ]

    y_opr = 9.45
    for status_code, endpoint, desc, bd_action in oper_calls:
        is_blocked = "403" in status_code
        row_p = FancyBboxPatch(
            (0.8, y_opr - 0.72), 13.9, 0.78,
            boxstyle="round,pad=0.02,rounding_size=0.08",
            facecolor="#2A1717" if is_blocked else "#132238",
            edgecolor="#7F1D1D" if is_blocked else "#1E3A5F",
            linewidth=1.4 if is_blocked else 1.2, zorder=4
        )
        ax.add_patch(row_p)

        badge_p = FancyBboxPatch(
            (0.95, y_opr - 0.58), 1.65, 0.48,
            boxstyle="round,pad=0.02,rounding_size=0.06",
            facecolor="#B91C1C" if is_blocked else "#15803D",
            edgecolor="none", zorder=5
        )
        ax.add_patch(badge_p)
        ax.text(1.775, y_opr - 0.34, status_code, color="#FFFFFF", fontsize=10.0, fontweight="bold", ha="center", va="center", family="DejaVu Sans Mono", zorder=6)

        ax.text(2.80, y_opr - 0.22, endpoint, color="#FCA5A5" if is_blocked else "#F8FAFC", fontsize=11.6, fontweight="bold", family="DejaVu Sans Mono", va="center", zorder=5)
        ax.text(2.80, y_opr - 0.52, desc, color="#FCA5A5" if is_blocked else "#94A3B8", fontsize=10.0, va="center", zorder=5)

        ax.text(14.5, y_opr - 0.36, bd_action, color="#EF4444" if is_blocked else "#38BDF8", fontsize=10.2, fontweight="bold", ha="right", va="center", family="DejaVu Sans Mono", zorder=5)

        y_opr -= 0.90

    # 5. PIE DE PÁGINA (COSTO S/ 0.00 Y TECNOLOGÍAS)
    ftr_box = FancyBboxPatch(
        (0.5, 0.4), 14.5, 1.4,
        boxstyle="round,pad=0.04,rounding_size=0.15",
        facecolor="#0F172A", edgecolor="#334155", linewidth=1.8, zorder=3
    )
    ax.add_patch(ftr_box)
    ax.text(
        7.75, 1.35,
        "ARQUITECTURA DE PRODUCCIÓN 100% OPERATIVA Y GRATUITA (COSTO: S/ 0.00 / MES)",
        color="#38BDF8", fontsize=12.0, fontweight="bold", ha="center", va="center", zorder=5
    )
    ax.text(
        7.75, 0.85,
        "Frontend: Render Static Site + GitHub Pages ($0)  |  Backend: Render Web Service ($0)  |  Base de Datos: Neon PostgreSQL Oregon ($0 perpetuo)",
        color="#94A3B8", fontsize=10.4, ha="center", va="center", zorder=5
    )

    plt.tight_layout(pad=0.20)
    plt.savefig(OUT_PNG, dpi=160, facecolor=fig.get_facecolor())
    plt.close(fig)
    print(f"Generated {OUT_PNG} ({os.path.getsize(OUT_PNG)} bytes)")

if __name__ == "__main__":
    main()
