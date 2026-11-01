# -*- coding: utf-8 -*-
"""
Genera láminas dedicadas de ALTA ACCESIBILIDAD VISUAL (WCAG 2.1 AAA)
con fuentes gigantes (16pt a 26pt bold) y alto contraste:
- 15A_Flujo_Admin_Alta_Accesibilidad.png
- 15B_Flujo_Operador_Alta_Accesibilidad.png
"""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_DIR = os.path.join(REPO_ROOT, "docs", "04_diagramas_arquitectura_y_negocio")

def generate_admin_card():
    png_path = os.path.join(OUT_DIR, "15A_Flujo_Admin_Alta_Accesibilidad.png")
    fig, ax = plt.subplots(figsize=(14.0, 15.0), dpi=140)
    fig.patch.set_facecolor("#060B14")
    ax.set_facecolor("#060B14")
    ax.set_xlim(0, 14.0)
    ax.set_ylim(0, 15.0)
    ax.axis("off")

    # Banner
    hdr_box = FancyBboxPatch((0.5, 13.4), 13.0, 1.25, boxstyle="round,pad=0.04,rounding_size=0.14",
                             facecolor="#065F46", edgecolor="#10B981", linewidth=2.8, zorder=3)
    ax.add_patch(hdr_box)
    ax.text(7.0, 14.25, "PERFIL 1: ADMINISTRADOR (admin@leofit.pe)", color="#FFFFFF", fontsize=20.0, fontweight="bold", ha="center", va="center", zorder=5)
    ax.text(7.0, 13.72, "Rol: ADMIN  |  Control Total  |  100% de Llamadas Autorizadas (200 / 201)", color="#A7F3D0", fontsize=14.0, fontweight="bold", ha="center", va="center", zorder=5)

    calls = [
        ("200 OK", "GET /api/dashboard/metrics", "Ingresos totales, pedidos y alertas de stock", "Vistas vw_orders_summary + vw_low_stock"),
        ("201 CREATED", "POST /api/products", "Crea nueva prenda en el catálogo", "Inserta en tabla products + audit_log"),
        ("200 OK", "PATCH /api/products/variant/:id/stock", "Ajusta conteo físico de stock SKU", "Modifica product_variants + audit_log"),
        ("200 OK", "DELETE /api/products/:id", "Soft-delete de prenda en catálogo", "Marca deleted_at en products + audit_log"),
        ("201 CREATED", "POST /api/orders  [Idempotente]", "Transacción ACID con reserva de stock", "Bloquea FOR UPDATE y descuenta stock"),
        ("200 OK", "PATCH /api/orders/:id/status", "Avanza estado logístico del pedido", "Actualiza orders + order_status_history"),
        ("200 OK", "POST /api/orders/:id/cancel", "Cancela venta y restituye prendas a BD", "Restaura stock + emite Nota de Crédito"),
        ("201 CREATED", "POST /api/invoices/emit", "Emite comprobante electrónico a SUNAT", "Encola en invoice_queue + XML firmado"),
    ]

    y = 12.50
    for code, ep, desc, bd in calls:
        row = FancyBboxPatch((0.5, y - 0.95), 13.0, 1.05, boxstyle="round,pad=0.03,rounding_size=0.10",
                             facecolor="#0F1F38", edgecolor="#10B981", linewidth=1.8, zorder=3)
        ax.add_patch(row)

        badge = FancyBboxPatch((0.7, y - 0.78), 2.2, 0.70, boxstyle="round,pad=0.03,rounding_size=0.08",
                               facecolor="#15803D", edgecolor="none", zorder=4)
        ax.add_patch(badge)
        ax.text(1.80, y - 0.43, code, color="#FFFFFF", fontsize=14.0, fontweight="bold", ha="center", va="center", family="DejaVu Sans Mono", zorder=5)

        ax.text(3.15, y - 0.28, ep, color="#FFFFFF", fontsize=15.5, fontweight="bold", family="DejaVu Sans Mono", va="center", zorder=5)
        ax.text(3.15, y - 0.68, desc, color="#CBD5E1", fontsize=13.0, va="center", zorder=5)

        ax.text(13.25, y - 0.43, bd, color="#38BDF8", fontsize=13.0, fontweight="bold", ha="right", va="center", family="DejaVu Sans Mono", zorder=5)
        y -= 1.25

    # Footer
    ftr = FancyBboxPatch((0.5, 0.4), 13.0, 0.95, boxstyle="round,pad=0.03,rounding_size=0.10",
                         facecolor="#0B132B", edgecolor="#334155", linewidth=1.8, zorder=3)
    ax.add_patch(ftr)
    ax.text(7.0, 0.88, "INFRAESTRUCTURA GRATUITA: Render Web Service ($0)  -->  Neon PostgreSQL Oregon ($0 perpetuo)",
            color="#38BDF8", fontsize=13.0, fontweight="bold", ha="center", va="center", zorder=5)

    plt.tight_layout(pad=0.15)
    plt.savefig(png_path, dpi=140, facecolor=fig.get_facecolor())
    plt.close(fig)
    print("Generated", png_path)

def generate_operador_card():
    png_path = os.path.join(OUT_DIR, "15B_Flujo_Operador_Alta_Accesibilidad.png")
    fig, ax = plt.subplots(figsize=(14.0, 15.0), dpi=140)
    fig.patch.set_facecolor("#060B14")
    ax.set_facecolor("#060B14")
    ax.set_xlim(0, 14.0)
    ax.set_ylim(0, 15.0)
    ax.axis("off")

    # Banner
    hdr_box = FancyBboxPatch((0.5, 13.4), 13.0, 1.25, boxstyle="round,pad=0.04,rounding_size=0.14",
                             facecolor="#92400E", edgecolor="#F59E0B", linewidth=2.8, zorder=3)
    ax.add_patch(hdr_box)
    ax.text(7.0, 14.25, "PERFIL 2: OPERADOR LOGÍSTICO (operador@leofit.pe)", color="#FFFFFF", fontsize=20.0, fontweight="bold", ha="center", va="center", zorder=5)
    ax.text(7.0, 13.72, "Rol: OPERATOR  |  Mínimo Privilegio  |  Despacho Habilitado, Mutaciones Bloqueadas", color="#FDE68A", fontsize=13.5, fontweight="bold", ha="center", va="center", zorder=5)

    calls = [
        # Permitidas (Verde)
        ("200 OK", "GET /api/products & /alerts/low-stock", "Consulta catálogo de prendas y stock reposición", "SELECT en products y product_variants"),
        ("200 OK", "GET /api/orders & GET /api/orders/:id", "Visualiza pedidos para empaque y despacho", "SELECT en orders con filtros logísticos"),
        ("201 CREATED", "POST /api/orders  [Idempotente]", "Registra pedido de WhatsApp y reserva stock", "INSERT orders con Idempotency-Key"),
        ("200 OK", "PATCH /api/orders/:id/status", "Avanza despacho (Preparación -> En Camino)", "UPDATE orders + order_status_history"),
        ("200 OK", "GET /api/sunat/ruc/:numero", "Valida RUC/DNI para rotulado de paquetes", "Consulta servicio tributario externo"),
        # Bloqueadas (Rojo)
        ("403 FORBIDDEN", "POST / PUT / DELETE /api/products", "Intento de crear, alterar o borrar prendas", "BLOQUEADO por requireRole('ADMIN')"),
        ("403 FORBIDDEN", "PATCH /api/products/variant/:id/stock", "Intento de cambiar el conteo de stock manual", "BLOQUEADO por requireRole('ADMIN')"),
        ("403 FORBIDDEN", "POST /api/orders/:id/cancel | /refund", "Intento de anular ventas o hacer reembolsos", "BLOQUEADO por requireRole('ADMIN')"),
    ]

    y = 12.50
    for code, ep, desc, bd in calls:
        is_blocked = "403" in code
        row = FancyBboxPatch((0.5, y - 0.95), 13.0, 1.05, boxstyle="round,pad=0.03,rounding_size=0.10",
                             facecolor="#331414" if is_blocked else "#0F1F38",
                             edgecolor="#EF4444" if is_blocked else "#10B981", linewidth=1.8, zorder=3)
        ax.add_patch(row)

        badge = FancyBboxPatch((0.7, y - 0.78), 2.2, 0.70, boxstyle="round,pad=0.03,rounding_size=0.08",
                               facecolor="#B91C1C" if is_blocked else "#15803D", edgecolor="none", zorder=4)
        ax.add_patch(badge)
        ax.text(1.80, y - 0.43, code, color="#FFFFFF", fontsize=13.0 if is_blocked else 14.0, fontweight="bold", ha="center", va="center", family="DejaVu Sans Mono", zorder=5)

        ax.text(3.15, y - 0.28, ep, color="#FCA5A5" if is_blocked else "#FFFFFF", fontsize=15.5, fontweight="bold", family="DejaVu Sans Mono", va="center", zorder=5)
        ax.text(3.15, y - 0.68, desc, color="#FCA5A5" if is_blocked else "#CBD5E1", fontsize=13.0, va="center", zorder=5)

        ax.text(13.25, y - 0.43, bd, color="#EF4444" if is_blocked else "#38BDF8", fontsize=13.0, fontweight="bold", ha="right", va="center", family="DejaVu Sans Mono", zorder=5)
        y -= 1.25

    # Footer
    ftr = FancyBboxPatch((0.5, 0.4), 13.0, 0.95, boxstyle="round,pad=0.03,rounding_size=0.10",
                         facecolor="#0B132B", edgecolor="#334155", linewidth=1.8, zorder=3)
    ax.add_patch(ftr)
    ax.text(7.0, 0.88, "SEGURIDAD OWASP A01: El Operador no puede invocar rutas de Admin aunque use Postman o cURL",
            color="#F59E0B", fontsize=13.0, fontweight="bold", ha="center", va="center", zorder=5)

    plt.tight_layout(pad=0.15)
    plt.savefig(png_path, dpi=140, facecolor=fig.get_facecolor())
    plt.close(fig)
    print("Generated", png_path)

if __name__ == "__main__":
    generate_admin_card()
    generate_operador_card()
