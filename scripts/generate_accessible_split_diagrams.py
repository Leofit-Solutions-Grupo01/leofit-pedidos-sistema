# -*- coding: utf-8 -*-
"""
Genera diagramas con LETRAS GIGANTES (18pt a 28pt) de Máxima Visibilidad:
- Diseñado para usuarios con discapacidad visual media (WCAG 2.1 AAA).
- Calibrado a ~960px - 1020px de ancho para renderizado 1:1 en pantalla sin reducción.
- Espaciado matemático perfecto, sin solapamientos entre tarjetas, badges y footers.
"""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_DIR = os.path.join(REPO_ROOT, "docs", "04_diagramas_arquitectura_y_negocio")

def generate_super_large_cards():
    os.makedirs(OUT_DIR, exist_ok=True)

    # -------------------------------------------------------------
    # 1. ADMIN - OPERACIONES (Letras Gigantes)
    # -------------------------------------------------------------
    png_admin = os.path.join(OUT_DIR, "15A_Flujo_Admin_Alta_Accesibilidad.png")
    fig, ax = plt.subplots(figsize=(9.6, 19.2), dpi=100)
    fig.patch.set_facecolor("#040812")
    ax.set_facecolor("#040812")
    ax.set_xlim(0, 9.6)
    ax.set_ylim(0, 19.2)
    ax.axis("off")

    # Banner Título
    b_hdr = FancyBboxPatch((0.3, 17.4), 9.0, 1.45, boxstyle="round,pad=0.04,rounding_size=0.15",
                           facecolor="#065F46", edgecolor="#10B981", linewidth=3.0, zorder=3)
    ax.add_patch(b_hdr)
    ax.text(4.8, 18.25, "ADMINISTRADOR", color="#FFFFFF", fontsize=28.0, fontweight="bold", ha="center", va="center", zorder=5)
    ax.text(4.8, 17.70, "admin@leofit.pe  |  100% AUTORIZADO", color="#A7F3D0", fontsize=18.0, fontweight="bold", ha="center", va="center", zorder=5)

    admin_items = [
        ("200 OK", "GET /api/dashboard/metrics", "Ingresos, KPIs y stock crítico en Neon"),
        ("201 CREATED", "POST /api/products", "Crea prenda en catálogo + audit_log"),
        ("200 OK", "PATCH /api/products/variant/:id/stock", "Ajusta stock físico de variante SKU"),
        ("200 OK", "DELETE /api/products/:id", "Soft-delete de prenda en base de datos"),
        ("201 CREATED", "POST /api/orders  (Idempotente)", "Transacción ACID: descuenta stock"),
        ("200 OK", "PATCH /api/orders/:id/status", "Avanza estado y graba trazabilidad"),
        ("200 OK", "POST /orders/:id/cancel", "Anula pedido y devuelve stock a BD"),
        ("201 CREATED", "POST /api/invoices/emit", "Emite Factura / Boleta formal a SUNAT"),
    ]

    y_top = 17.0
    for code, ep, desc in admin_items:
        card = FancyBboxPatch((0.3, y_top - 1.60), 9.0, 1.60, boxstyle="round,pad=0.04,rounding_size=0.12",
                              facecolor="#0B1A30", edgecolor="#10B981", linewidth=2.4, zorder=3)
        ax.add_patch(card)

        # Badge Grande
        badge = FancyBboxPatch((0.5, y_top - 0.72), 2.8, 0.65, boxstyle="round,pad=0.03,rounding_size=0.08",
                               facecolor="#15803D", edgecolor="none", zorder=4)
        ax.add_patch(badge)
        ax.text(1.90, y_top - 0.40, code, color="#FFFFFF", fontsize=18.5, fontweight="bold", ha="center", va="center", family="DejaVu Sans Mono", zorder=5)

        # Endpoint Grande
        ax.text(3.50, y_top - 0.40, ep, color="#FFFFFF", fontsize=18.0, fontweight="bold", family="DejaVu Sans Mono", va="center", zorder=5)

        # Descripción
        ax.text(0.55, y_top - 1.18, desc, color="#38BDF8", fontsize=17.0, fontweight="bold", va="center", zorder=5)

        y_top -= 1.90

    # Footer
    b_ftr = FancyBboxPatch((0.3, 0.40), 9.0, 1.25, boxstyle="round,pad=0.04,rounding_size=0.12",
                           facecolor="#0F172A", edgecolor="#334155", linewidth=2.0, zorder=3)
    ax.add_patch(b_ftr)
    ax.text(4.8, 1.02, "Backend Render ($0)  -->  Neon PostgreSQL ($0)", color="#38BDF8", fontsize=18.0, fontweight="bold", ha="center", va="center", zorder=5)

    plt.tight_layout(pad=0.10)
    plt.savefig(png_admin, dpi=100, facecolor=fig.get_facecolor())
    plt.close(fig)
    print("Generated", png_admin)

    # -------------------------------------------------------------
    # 2. OPERADOR - OPERACIONES (Letras Gigantes)
    # -------------------------------------------------------------
    png_oper = os.path.join(OUT_DIR, "15B_Flujo_Operador_Alta_Accesibilidad.png")
    fig, ax = plt.subplots(figsize=(9.6, 19.2), dpi=100)
    fig.patch.set_facecolor("#040812")
    ax.set_facecolor("#040812")
    ax.set_xlim(0, 9.6)
    ax.set_ylim(0, 19.2)
    ax.axis("off")

    # Banner Título
    b_hdr = FancyBboxPatch((0.3, 17.4), 9.0, 1.45, boxstyle="round,pad=0.04,rounding_size=0.15",
                           facecolor="#92400E", edgecolor="#F59E0B", linewidth=3.0, zorder=3)
    ax.add_patch(b_hdr)
    ax.text(4.8, 18.25, "OPERADOR LOGÍSTICO", color="#FFFFFF", fontsize=28.0, fontweight="bold", ha="center", va="center", zorder=5)
    ax.text(4.8, 17.70, "operador@leofit.pe  |  MÍNIMO PRIVILEGIO", color="#FDE68A", fontsize=18.0, fontweight="bold", ha="center", va="center", zorder=5)

    oper_items = [
        # Permitidas (Verde)
        ("200 OK", "GET /api/products", "Consulta prendas y stock para reposición", True),
        ("200 OK", "GET /api/orders", "Visualiza pedidos para empaque y ruta", True),
        ("201 CREATED", "POST /api/orders", "Registra pedidos de clientes en Neon DB", True),
        ("200 OK", "PATCH /api/orders/:id/status", "Avanza despacho (Preparación -> En Camino)", True),
        ("200 OK", "GET /api/sunat/ruc/:numero", "Valida RUC/DNI para rotulado de paquetes", True),
        # Bloqueadas (Rojo)
        ("403 FORBIDDEN", "POST / PUT / DELETE /products", "BLOQUEADO: No puede crear o borrar prendas", False),
        ("403 FORBIDDEN", "PATCH /variant/:id/stock", "BLOQUEADO: No puede alterar stock manual", False),
        ("403 FORBIDDEN", "POST /orders/:id/cancel", "BLOQUEADO: Solo Admin puede anular ventas", False),
    ]

    y_top = 17.0
    for code, ep, desc, is_ok in oper_items:
        card = FancyBboxPatch((0.3, y_top - 1.60), 9.0, 1.60, boxstyle="round,pad=0.04,rounding_size=0.12",
                              facecolor="#0B1A30" if is_ok else "#2D1010",
                              edgecolor="#10B981" if is_ok else "#EF4444", linewidth=2.4, zorder=3)
        ax.add_patch(card)

        # Badge Grande
        badge = FancyBboxPatch((0.5, y_top - 0.72), 3.1 if not is_ok else 2.8, 0.65, boxstyle="round,pad=0.03,rounding_size=0.08",
                               facecolor="#15803D" if is_ok else "#B91C1C", edgecolor="none", zorder=4)
        ax.add_patch(badge)
        ax.text(2.05 if not is_ok else 1.90, y_top - 0.40, code, color="#FFFFFF", fontsize=17.5 if not is_ok else 18.5, fontweight="bold", ha="center", va="center", family="DejaVu Sans Mono", zorder=5)

        # Endpoint Grande
        ax.text(3.75 if not is_ok else 3.50, y_top - 0.40, ep, color="#FFFFFF" if is_ok else "#FCA5A5", fontsize=17.5, fontweight="bold", family="DejaVu Sans Mono", va="center", zorder=5)

        # Descripción
        ax.text(0.55, y_top - 1.18, desc, color="#38BDF8" if is_ok else "#F87171", fontsize=17.0, fontweight="bold", va="center", zorder=5)

        y_top -= 1.90

    # Footer
    b_ftr = FancyBboxPatch((0.3, 0.40), 9.0, 1.25, boxstyle="round,pad=0.04,rounding_size=0.12",
                           facecolor="#0F172A", edgecolor="#334155", linewidth=2.0, zorder=3)
    ax.add_patch(b_ftr)
    ax.text(4.8, 1.02, "Compuerta requireRole('ADMIN') protege la base de datos", color="#F59E0B", fontsize=17.5, fontweight="bold", ha="center", va="center", zorder=5)

    plt.tight_layout(pad=0.10)
    plt.savefig(png_oper, dpi=100, facecolor=fig.get_facecolor())
    plt.close(fig)
    print("Generated", png_oper)

    # -------------------------------------------------------------
    # 3. DIAGRAMA CONSOLIDADO 15_Flujo_RBAC_Admin_vs_Operador.png
    # -------------------------------------------------------------
    png_main = os.path.join(OUT_DIR, "15_Flujo_RBAC_Admin_vs_Operador.png")
    fig, ax = plt.subplots(figsize=(10.2, 21.6), dpi=100)
    fig.patch.set_facecolor("#040812")
    ax.set_facecolor("#040812")
    ax.set_xlim(0, 10.2)
    ax.set_ylim(0, 21.6)
    ax.axis("off")

    # Header General
    hdr = FancyBboxPatch((0.3, 19.8), 9.6, 1.45, boxstyle="round,pad=0.04,rounding_size=0.15",
                         facecolor="#1E3A8A", edgecolor="#3B82F6", linewidth=3.0, zorder=3)
    ax.add_patch(hdr)
    ax.text(5.1, 20.65, "FLUJO RBAC: ADMIN vs. OPERADOR", color="#FFFFFF", fontsize=26.0, fontweight="bold", ha="center", zorder=5)
    ax.text(5.1, 20.10, "Middlewares de Seguridad y Neon PostgreSQL (S/ 0.00)", color="#BAE6FD", fontsize=17.0, fontweight="bold", ha="center", zorder=5)

    # Bloque Admin
    b_adm = FancyBboxPatch((0.3, 10.6), 9.6, 8.8, boxstyle="round,pad=0.04,rounding_size=0.15",
                           facecolor="#06281E", edgecolor="#10B981", linewidth=2.8, zorder=3)
    ax.add_patch(b_adm)
    ax.text(0.6, 19.00, "PERFIL 1: ADMINISTRADOR", color="#10B981", fontsize=22.0, fontweight="bold", zorder=5)
    ax.text(0.6, 18.50, "admin@leofit.pe  |  Acceso Total (100% Autorizado)", color="#A7F3D0", fontsize=15.0, fontweight="bold", zorder=5)

    adm_summary = [
        ("200 OK", "GET /api/dashboard/metrics", "Ingresos, KPIs y stock crítico en Neon"),
        ("201 CREATED", "POST /api/products", "Crea prendas en catálogo + audit_log"),
        ("200 OK", "PATCH /variant/:id/stock", "Ajusta físicamente stock de SKU"),
        ("201 CREATED", "POST /api/orders", "Transacción ACID y reserva de stock"),
        ("200 OK", "POST /orders/:id/cancel", "Anula pedido y restituye stock"),
        ("201 CREATED", "POST /invoices/emit", "Emite comprobante oficial a SUNAT"),
    ]
    y_a = 18.0
    for code, ep, desc in adm_summary:
        r = FancyBboxPatch((0.5, y_a - 1.05), 9.2, 1.05, boxstyle="round,pad=0.03,rounding_size=0.08",
                           facecolor="#0A1E17", edgecolor="#10B981", linewidth=1.8, zorder=4)
        ax.add_patch(r)
        ax.text(0.7, y_a - 0.40, code, color="#4ADE80", fontsize=16.5, fontweight="bold", family="DejaVu Sans Mono", zorder=5)
        ax.text(3.1, y_a - 0.40, ep, color="#FFFFFF", fontsize=16.5, fontweight="bold", family="DejaVu Sans Mono", zorder=5)
        ax.text(0.7, y_a - 0.80, desc, color="#94A3B8", fontsize=14.5, fontweight="bold", zorder=5)
        y_a -= 1.20

    # Bloque Operador
    b_opr = FancyBboxPatch((0.3, 1.8), 9.6, 8.6, boxstyle="round,pad=0.04,rounding_size=0.15",
                           facecolor="#261A0C", edgecolor="#F59E0B", linewidth=2.8, zorder=3)
    ax.add_patch(b_opr)
    ax.text(0.6, 10.00, "PERFIL 2: OPERADOR LOGÍSTICO", color="#F59E0B", fontsize=22.0, fontweight="bold", zorder=5)
    ax.text(0.6, 9.50, "operador@leofit.pe  |  Mínimo Privilegio (Solo Despacho)", color="#FDE68A", fontsize=15.0, fontweight="bold", zorder=5)

    opr_summary = [
        ("200 OK", "GET /api/products & /orders", "Consulta catálogo y lista de despachos", True),
        ("201 CREATED", "POST /api/orders", "Crea pedidos de WhatsApp con stock", True),
        ("200 OK", "PATCH /orders/:id/status", "Avanza despacho (Preparación -> En Camino)", True),
        ("403 FORBIDDEN", "POST/PUT/DELETE /products", "BLOQUEADO por requireRole('ADMIN')", False),
        ("403 FORBIDDEN", "PATCH /variant/:id/stock", "BLOQUEADO por requireRole('ADMIN')", False),
        ("403 FORBIDDEN", "POST /orders/:id/cancel", "BLOQUEADO por requireRole('ADMIN')", False),
    ]
    y_o = 9.0
    for code, ep, desc, is_ok in opr_summary:
        r = FancyBboxPatch((0.5, y_o - 1.05), 9.2, 1.05, boxstyle="round,pad=0.03,rounding_size=0.08",
                           facecolor="#182718" if is_ok else "#351212",
                           edgecolor="#10B981" if is_ok else "#EF4444", linewidth=1.8, zorder=4)
        ax.add_patch(r)
        ax.text(0.7, y_o - 0.40, code, color="#4ADE80" if is_ok else "#F87171", fontsize=15.5, fontweight="bold", family="DejaVu Sans Mono", zorder=5)
        ax.text(3.3 if not is_ok else 3.1, y_o - 0.40, ep, color="#FFFFFF" if is_ok else "#FCA5A5", fontsize=16.0, fontweight="bold", family="DejaVu Sans Mono", zorder=5)
        ax.text(0.7, y_o - 0.80, desc, color="#94A3B8" if is_ok else "#EF4444", fontsize=14.0, fontweight="bold" if not is_ok else "normal", zorder=5)
        y_o -= 1.20

    # Footer
    ftr = FancyBboxPatch((0.3, 0.35), 9.6, 1.15, boxstyle="round,pad=0.04,rounding_size=0.12",
                         facecolor="#0F172A", edgecolor="#334155", linewidth=2.0, zorder=3)
    ax.add_patch(ftr)
    ax.text(5.1, 0.92, "Render Free ($0.00) + Neon PostgreSQL ($0.00)", color="#38BDF8", fontsize=17.0, fontweight="bold", ha="center", va="center", zorder=5)

    plt.tight_layout(pad=0.10)
    plt.savefig(png_main, dpi=100, facecolor=fig.get_facecolor())
    plt.close(fig)
    print("Generated", png_main)

if __name__ == "__main__":
    generate_super_large_cards()
