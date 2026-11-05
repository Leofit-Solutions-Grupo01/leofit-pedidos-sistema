# -*- coding: utf-8 -*-
"""
Diagrama de Flujo RBAC: ADMIN vs. OPERADOR
Optimizado con tipografía GRANDE Y CLARA (12-19pt), espacio horizontal amplio (15.0 pulgadas)
y márgenes generosos para CERO colisiones entre textos.
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

    # 15.0 pulgadas de ancho para que el texto de la izquierda y la derecha tengan 2 pulgadas de margen libre
    # 26.0 pulgadas de alto a 140 DPI
    fig, ax = plt.subplots(figsize=(15.0, 26.0), dpi=140)
    fig.patch.set_facecolor("#080D1A")
    ax.set_facecolor("#080D1A")
    ax.set_xlim(0, 15.0)
    ax.set_ylim(0, 26.0)
    ax.axis("off")

    # 1. ENCABEZADO PRINCIPAL (BANNER)
    hdr_box = FancyBboxPatch(
        (0.50, 24.10), 14.0, 1.45,
        boxstyle="round,pad=0.03,rounding_size=0.14",
        facecolor="#1E3A8A", edgecolor="#3B82F6", linewidth=2.5, zorder=3
    )
    ax.add_patch(hdr_box)
    ax.text(
        7.50, 25.00,
        "FLUJO RBAC: ADMINISTRADOR vs. OPERADOR",
        color="#FFFFFF", fontsize=19.0, fontweight="bold", ha="center", va="center", zorder=5
    )
    ax.text(
        7.50, 24.45,
        "Llamadas API, Middlewares de Seguridad y Acciones en Neon PostgreSQL (S/ 0.00)",
        color="#BAE6FD", fontsize=12.5, ha="center", va="center", zorder=5
    )

    # 2. PIPELINE DE SEGURIDAD BACKEND
    mw_card = FancyBboxPatch(
        (0.50, 21.05), 14.0, 2.75,
        boxstyle="round,pad=0.03,rounding_size=0.14",
        facecolor="#0F172A", edgecolor="#6366F1", linewidth=2.0, zorder=3
    )
    ax.add_patch(mw_card)
    ax.text(
        7.50, 23.40,
        "PIPELINE DE SEGURIDAD BACKEND (Express / Render Free)",
        color="#A5B4FC", fontsize=13.5, fontweight="bold", ha="center", va="center", zorder=5
    )

    mws = [
        ("1. Perímetro", "Helmet\nCORS Multi-Origen", "#1E1B4B", "#4F46E5"),
        ("2. Tráfico", "RateLimiter\nIdempotency-Key", "#1E1B4B", "#4F46E5"),
        ("3. Auth", "authenticateToken\nVerifica firma JWT", "#1E3A8A", "#2563EB"),
        ("4. RBAC", "requireRole('ADMIN')\n¿Es ADMIN?", "#7C2D12", "#EA580C"),
        ("5. Persistencia", "Motor Neon DB\nTransacciones ACID", "#064E3B", "#10B981"),
    ]
    for idx, (m_title, m_desc, m_bg, m_border) in enumerate(mws):
        bx = 0.75 + idx * 2.70
        bp = FancyBboxPatch(
            (bx, 21.30), 2.45, 1.75,
            boxstyle="round,pad=0.03,rounding_size=0.10",
            facecolor=m_bg, edgecolor=m_border, linewidth=2.0, zorder=4
        )
        ax.add_patch(bp)
        ax.text(bx + 1.225, 22.60, m_title, color="#FFFFFF", fontsize=12.2, fontweight="bold", ha="center", zorder=5)
        ax.text(bx + 1.225, 21.85, m_desc, color="#E2E8F0", fontsize=10.8, ha="center", va="center", zorder=5, linespacing=1.2)
        if idx < 4:
            ax.annotate("", xy=(bx + 2.65, 22.15), xytext=(bx + 2.50, 22.15),
                        arrowprops=dict(arrowstyle="-|>,head_width=0.30,head_length=0.35", color="#94A3B8", lw=2.0), zorder=6)

    # 3. SECCIÓN ADMINISTRADOR (role: ADMIN)
    adm_box = FancyBboxPatch(
        (0.50, 11.75), 14.0, 9.00,
        boxstyle="round,pad=0.03,rounding_size=0.14",
        facecolor="#0B132B", edgecolor="#10B981", linewidth=2.6, zorder=3
    )
    ax.add_patch(adm_box)

    # Header Admin
    adm_hdr = FancyBboxPatch(
        (0.50, 19.85), 14.0, 0.90,
        boxstyle="round,pad=0.03,rounding_size=0.14",
        facecolor="#065F46", edgecolor="#10B981", linewidth=1.5, zorder=4
    )
    ax.add_patch(adm_hdr)
    ax.text(0.85, 20.30, "PERFIL 1: ADMINISTRADOR", color="#FFFFFF", fontsize=15.0, fontweight="bold", va="center", zorder=5)
    ax.text(14.15, 20.30, "admin@leofit.pe  |  Rol: ADMIN  |  100% Autorizado", color="#A7F3D0", fontsize=12.0, fontweight="bold", ha="right", va="center", zorder=5)

    admin_calls = [
        ("200 OK", "GET /api/dashboard/metrics", "Ingresos totales, pedidos por estado y stock crítico", "Vistas vw_orders_summary + vw_low_stock"),
        ("201 CREATED", "POST /api/products", "Crea nueva prenda deportiva en el catálogo", "Inserta en tabla products + audit_log"),
        ("200 OK", "PATCH /api/products/variant/:id/stock", "Ajusta físicamente el conteo de stock de una talla", "Modifica product_variants + audit_log"),
        ("200 OK", "DELETE /api/products/:id", "Aplica Soft-Delete (deleted_at = NOW()) a la prenda", "Marca deleted_at en products + audit_log"),
        ("201 CREATED", "POST /api/orders  [Idempotente]", "Transacción ACID: valida stock y descuenta unidades", "Bloquea FOR UPDATE y descuenta stock"),
        ("200 OK", "PATCH /api/orders/:id/status", "Avanza estado: RECIBIDO -> PREPARACIÓN -> ENTREGADO", "Actualiza orders + order_status_history"),
        ("200 OK", "POST /api/orders/:id/cancel", "Cancela venta, restituye stock y emite Nota Crédito", "Restaura stock + emite Nota de Crédito"),
        ("201 CREATED", "POST /api/invoices/emit", "Emite comprobante electrónico oficial a SUNAT", "Encola en invoice_queue + XML firmado"),
    ]

    y_adm = 19.30
    for status_code, endpoint, desc, bd_action in admin_calls:
        row_p = FancyBboxPatch(
            (0.70, y_adm - 0.72), 13.6, 0.78,
            boxstyle="round,pad=0.02,rounding_size=0.08",
            facecolor="#132238", edgecolor="#1E3A5F", linewidth=1.4, zorder=4
        )
        ax.add_patch(row_p)

        badge_p = FancyBboxPatch(
            (0.85, y_adm - 0.58), 1.70, 0.50,
            boxstyle="round,pad=0.02,rounding_size=0.06",
            facecolor="#15803D", edgecolor="none", zorder=5
        )
        ax.add_patch(badge_p)
        ax.text(1.70, y_adm - 0.33, status_code, color="#FFFFFF", fontsize=11.2, fontweight="bold", ha="center", va="center", family="DejaVu Sans Mono", zorder=6)

        ax.text(2.75, y_adm - 0.20, endpoint, color="#F8FAFC", fontsize=12.8, fontweight="bold", family="DejaVu Sans Mono", va="center", zorder=5)
        ax.text(2.75, y_adm - 0.52, desc, color="#94A3B8", fontsize=11.2, va="center", zorder=5)

        ax.text(14.10, y_adm - 0.33, bd_action, color="#38BDF8", fontsize=11.4, fontweight="bold", ha="right", va="center", family="DejaVu Sans Mono", zorder=5)

        y_adm -= 0.94

    # 4. SECCIÓN OPERADOR LOGÍSTICO (role: OPERATOR)
    opr_box = FancyBboxPatch(
        (0.50, 2.35), 14.0, 9.00,
        boxstyle="round,pad=0.03,rounding_size=0.14",
        facecolor="#151A28", edgecolor="#F59E0B", linewidth=2.6, zorder=3
    )
    ax.add_patch(opr_box)

    # Header Operador
    opr_hdr = FancyBboxPatch(
        (0.50, 10.45), 14.0, 0.90,
        boxstyle="round,pad=0.03,rounding_size=0.14",
        facecolor="#92400E", edgecolor="#F59E0B", linewidth=1.5, zorder=4
    )
    ax.add_patch(opr_hdr)
    ax.text(0.85, 10.90, "PERFIL 2: OPERADOR LOGÍSTICO", color="#FFFFFF", fontsize=15.0, fontweight="bold", va="center", zorder=5)
    ax.text(14.15, 10.90, "operador@leofit.pe  |  Rol: OPERATOR  |  Mínimo Privilegio", color="#FDE68A", fontsize=12.0, fontweight="bold", ha="right", va="center", zorder=5)

    oper_calls = [
        # Operaciones Permitidas
        ("200 OK", "GET /api/products & /alerts/low-stock", "Consulta catálogo de prendas y stock para reposición", "SELECT en products y product_variants"),
        ("200 OK", "GET /api/orders & GET /api/orders/:id", "Visualiza lista de pedidos para empaque y despacho", "SELECT en orders con filtros logísticos"),
        ("201 CREATED", "POST /api/orders  [Idempotente]", "Registra pedido de cliente WhatsApp y reserva stock", "INSERT orders con Idempotency-Key"),
        ("200 OK", "PATCH /api/orders/:id/status", "Avanza despacho (Preparación -> En Camino -> Entregado)", "UPDATE orders + order_status_history"),
        ("200 OK", "GET /api/sunat/ruc/:numero", "Consulta datos de RUC/DNI para rotulado de paquetes", "Consulta servicio tributario externo"),
        # Operaciones Bloqueadas por RBAC
        ("403 FORBIDDEN", "POST / PUT / DELETE /api/products", "Intento de crear, cambiar precio o borrar prendas", "BLOQUEADO por requireRole('ADMIN')"),
        ("403 FORBIDDEN", "PATCH /api/products/variant/:id/stock", "Intento de manipular el conteo de stock manual", "BLOQUEADO por requireRole('ADMIN')"),
        ("403 FORBIDDEN", "POST /api/orders/:id/cancel | /refund", "Intento de anular ventas consolidadas o reembolsar", "BLOQUEADO por requireRole('ADMIN')"),
    ]

    y_opr = 9.90
    for status_code, endpoint, desc, bd_action in oper_calls:
        is_blocked = "403" in status_code
        row_p = FancyBboxPatch(
            (0.70, y_opr - 0.72), 13.6, 0.78,
            boxstyle="round,pad=0.02,rounding_size=0.08",
            facecolor="#2A1717" if is_blocked else "#132238",
            edgecolor="#7F1D1D" if is_blocked else "#1E3A5F",
            linewidth=1.5 if is_blocked else 1.4, zorder=4
        )
        ax.add_patch(row_p)

        badge_p = FancyBboxPatch(
            (0.85, y_opr - 0.58), 1.70, 0.50,
            boxstyle="round,pad=0.02,rounding_size=0.06",
            facecolor="#B91C1C" if is_blocked else "#15803D",
            edgecolor="none", zorder=5
        )
        ax.add_patch(badge_p)
        ax.text(1.70, y_opr - 0.33, status_code, color="#FFFFFF", fontsize=10.6, fontweight="bold", ha="center", va="center", family="DejaVu Sans Mono", zorder=6)

        ax.text(2.75, y_opr - 0.20, endpoint, color="#FCA5A5" if is_blocked else "#F8FAFC", fontsize=12.8, fontweight="bold", family="DejaVu Sans Mono", va="center", zorder=5)
        ax.text(2.75, y_opr - 0.52, desc, color="#FCA5A5" if is_blocked else "#94A3B8", fontsize=11.2, va="center", zorder=5)

        ax.text(14.10, y_opr - 0.33, bd_action, color="#EF4444" if is_blocked else "#38BDF8", fontsize=11.4, fontweight="bold", ha="right", va="center", family="DejaVu Sans Mono", zorder=5)

        y_opr -= 0.94

    # 5. PIE DE PÁGINA (COSTO S/ 0.00)
    ftr_box = FancyBboxPatch(
        (0.50, 0.45), 14.0, 1.50,
        boxstyle="round,pad=0.03,rounding_size=0.14",
        facecolor="#0F172A", edgecolor="#334155", linewidth=2.0, zorder=3
    )
    ax.add_patch(ftr_box)
    ax.text(
        7.50, 1.35,
        "ARQUITECTURA DE PRODUCCIÓN 100% OPERATIVA (COSTO: S/ 0.00 / MES)",
        color="#38BDF8", fontsize=13.5, fontweight="bold", ha="center", va="center", zorder=5
    )
    ax.text(
        7.50, 0.85,
        "Frontend: Render / GitHub Pages ($0)  |  Backend API: Render Free ($0)  |  Base de Datos: Neon PostgreSQL Oregon ($0 perpetuo)",
        color="#94A3B8", fontsize=11.2, ha="center", va="center", zorder=5
    )

    plt.tight_layout(pad=0.15)
    plt.savefig(OUT_PNG, dpi=140, facecolor=fig.get_facecolor())
    plt.close(fig)
    print(f"Generated {OUT_PNG} ({os.path.getsize(OUT_PNG)} bytes)")

if __name__ == "__main__":
    main()
