# -*- coding: utf-8 -*-
"""
Genera el Diagrama Entidad-Relación (ERD) completo de las 22 tablas y 2 vistas
desplegadas en Neon PostgreSQL (neondb) con tipografía grande, legible, espaciada y nítida.
"""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_DIR = os.path.join(REPO_ROOT, "docs", "04_diagramas_arquitectura_y_negocio")
OUT_PNG = os.path.join(OUT_DIR, "05_erd_bd.png")
OUT_MMD = os.path.join(OUT_DIR, "05_erd_bd.mmd")

MMD_CONTENT = """erDiagram
    categories ||--o{ products : "category_id"
    products ||--o{ product_variants : "product_id"
    sizes ||--o{ product_variants : "size_id"
    colors ||--o{ product_variants : "color_id"
    districts ||--o{ clients : "district_id"
    clients ||--o{ orders : "client_id"
    users ||--o{ orders : "user_id"
    payment_methods ||--o{ orders : "payment_method_id"
    orders ||--|{ order_items : "order_id"
    product_variants ||--o{ order_items : "variant_id"
    orders ||--o{ order_status_history : "order_id"
    users ||--o{ order_status_history : "user_id"
    orders ||--o{ order_state_transitions : "order_id"
    orders ||--o{ payments : "order_id"
    orders ||--o{ invoices : "order_id"
    orders ||--o{ invoice_queue : "order_id"
    users ||--o{ refresh_tokens : "user_id"
    users ||--o{ audit_log : "user_id"
"""

def draw_table(ax, x, y, w, title, header_color, rows):
    row_h = 0.38
    header_h = 0.56
    total_h = header_h + len(rows) * row_h + 0.12

    # Card shadow
    shadow = FancyBboxPatch(
        (x + 0.06, y - total_h - 0.06), w, total_h,
        boxstyle="round,pad=0.03,rounding_size=0.10",
        facecolor="#020617", edgecolor="none", alpha=0.45, zorder=2
    )
    ax.add_patch(shadow)

    # Card body
    body = FancyBboxPatch(
        (x, y - total_h), w, total_h,
        boxstyle="round,pad=0.03,rounding_size=0.10",
        facecolor="#1E293B", edgecolor=header_color, linewidth=2.0, zorder=3
    )
    ax.add_patch(body)

    # Header bar
    hdr = FancyBboxPatch(
        (x, y - header_h), w, header_h,
        boxstyle="round,pad=0.03,rounding_size=0.10",
        facecolor=header_color, edgecolor=header_color, linewidth=1.2, zorder=4
    )
    ax.add_patch(hdr)

    ax.text(
        x + w / 2, y - header_h / 2, title,
        color="#FFFFFF", fontsize=12.2, fontweight="bold",
        ha="center", va="center", family="DejaVu Sans Mono", zorder=5
    )

    for idx, (badge, col_name, col_type) in enumerate(rows):
        ry = y - header_h - (idx + 0.62) * row_h
        if idx % 2 == 1:
            stripe = FancyBboxPatch(
                (x + 0.03, ry - row_h * 0.44), w - 0.06, row_h * 0.92,
                boxstyle="square,pad=0",
                facecolor="#0F172A", edgecolor="none", alpha=0.50, zorder=3.5
            )
            ax.add_patch(stripe)

        badge_color = "#F59E0B" if "PK" in badge else ("#38BDF8" if "FK" in badge else "#94A3B8")
        if badge:
            ax.text(
                x + 0.15, ry, badge,
                color=badge_color, fontsize=10.2, fontweight="bold",
                ha="left", va="center", family="DejaVu Sans Mono", zorder=5
            )
        ax.text(
            x + 0.78, ry, col_name,
            color="#F8FAFC", fontsize=10.8, fontweight="bold" if "PK" in badge else "normal",
            ha="left", va="center", family="DejaVu Sans Mono", zorder=5
        )
        ax.text(
            x + w - 0.15, ry, col_type,
            color="#CBD5E1", fontsize=10.0,
            ha="right", va="center", family="DejaVu Sans Mono", zorder=5
        )

    return {
        "top": (x + w / 2, y),
        "bottom": (x + w / 2, y - total_h),
        "left": (x, y - total_h / 2),
        "right": (x + w, y - total_h / 2),
        "box": (x, y - total_h, w, total_h),
    }

def connect_orth(ax, p1, p2, color="#38BDF8", label="", mid_x=None, mid_y=None):
    x1, y1 = p1
    x2, y2 = p2
    if mid_x is not None:
        xs = [x1, mid_x, mid_x, x2]
        ys = [y1, y1, y2, y2]
        lx, ly = mid_x, (y1 + y2) / 2
    elif mid_y is not None:
        xs = [x1, x1, x2, x2]
        ys = [y1, mid_y, mid_y, y2]
        lx, ly = (x1 + x2) / 2, mid_y
    else:
        mx = (x1 + x2) / 2
        xs = [x1, mx, mx, x2]
        ys = [y1, y1, y2, y2]
        lx, ly = mx, (y1 + y2) / 2

    ax.plot(xs, ys, color=color, linewidth=1.8, linestyle="-", alpha=0.90, zorder=2.5)
    ax.scatter([x1, x2], [y1, y2], color=color, s=30, zorder=6)
    if label:
        ax.text(
            lx, ly + 0.10, label, color="#E2E8F0", fontsize=9.2, fontweight="bold",
            ha="center", va="bottom",
            bbox=dict(boxstyle="round,pad=0.20", facecolor="#0F172A", edgecolor=color, lw=1.2),
            zorder=7
        )

def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    with open(OUT_MMD, "w", encoding="utf-8") as f:
        f.write(MMD_CONTENT)

    fig, ax = plt.subplots(figsize=(27, 23.5), dpi=180)
    fig.patch.set_facecolor("#0B1120")
    ax.set_facecolor("#0B1120")
    ax.set_xlim(0, 27)
    ax.set_ylim(0, 23.5)
    ax.axis("off")

    # Title Banner
    banner = FancyBboxPatch(
        (0.40, 22.05), 26.2, 1.15,
        boxstyle="round,pad=0.03,rounding_size=0.14",
        facecolor="#1E3A8A", edgecolor="#3B82F6", linewidth=2.2, zorder=3
    )
    ax.add_patch(banner)
    ax.text(
        13.5, 22.75,
        "ESQUEMA ENTIDAD-RELACIÓN COMPLETO (BCNF + TRANSACCIONAL) — NEON POSTGRESQL (neondb)",
        color="#FFFFFF", fontsize=17.5, fontweight="bold", ha="center", va="center", zorder=5
    )
    ax.text(
        13.5, 22.32,
        "22 Tablas Relacionales + 2 Vistas Analíticas | 15 Migraciones Versionadas | Integridad Referencial ACID & Facturación Electrónica SUNAT",
        color="#BAE6FD", fontsize=12.2, ha="center", va="center", zorder=5
    )

    w = 4.80

    # COLUMN 1 (x=0.50): Catálogo & Dominios BCNF
    ax.text(0.50, 21.60, "DOMINIO 1: CATÁLOGO & LOOKUPS BCNF", color="#38BDF8", fontsize=12.5, fontweight="bold")
    t_cat = draw_table(ax, 0.50, 21.20, w, "categories", "#0284C7", [
        ("[PK]", "id", "SERIAL"),
        ("[UK]", "name", "VARCHAR(60)"),
        ("", "description", "TEXT"),
        ("", "created_at", "TIMESTAMPTZ"),
    ])
    t_prod = draw_table(ax, 0.50, 18.50, w, "products", "#0284C7", [
        ("[PK]", "id", "SERIAL"),
        ("[FK]", "category_id", "INT"),
        ("[UK]", "name", "VARCHAR(120)"),
        ("", "base_price", "NUMERIC(10,2)"),
        ("", "image_url", "VARCHAR(512)"),
        ("", "is_active", "BOOLEAN"),
        ("", "deleted_at", "TIMESTAMPTZ"),
    ])
    t_var = draw_table(ax, 0.50, 14.65, w, "product_variants", "#0284C7", [
        ("[PK]", "id", "SERIAL"),
        ("[FK]", "product_id", "INT"),
        ("[FK]", "size_id", "SMALLINT"),
        ("[FK]", "color_id", "SMALLINT"),
        ("[UK]", "sku", "VARCHAR(60)"),
        ("", "stock", "INT >= 0"),
        ("", "alert_threshold", "INT DEFAULT 3"),
    ])
    t_sizes = draw_table(ax, 0.50, 10.75, 2.30, "sizes", "#0369A1", [
        ("[PK]", "id", "SMALLSERIAL"),
        ("[UK]", "code", "VARCHAR(10)"),
        ("", "label", "VARCHAR(30)"),
    ])
    t_colors = draw_table(ax, 3.00, 10.75, 2.30, "colors", "#0369A1", [
        ("[PK]", "id", "SMALLSERIAL"),
        ("[UK]", "name", "VARCHAR(60)"),
        ("", "hex", "CHAR(7)"),
    ])
    t_dist = draw_table(ax, 0.50, 8.40, 2.30, "districts", "#0369A1", [
        ("[PK]", "id", "SMALLSERIAL"),
        ("[UK]", "name", "VARCHAR(80)"),
    ])
    t_pm = draw_table(ax, 3.00, 8.40, 2.30, "payment_methods", "#0369A1", [
        ("[PK]", "id", "SMALLSERIAL"),
        ("[UK]", "code", "VARCHAR(30)"),
        ("", "name", "VARCHAR(60)"),
    ])
    t_views = draw_table(ax, 0.50, 6.20, w, "VISTAS ANALÍTICAS (2)", "#0F766E", [
        ("[VW]", "vw_low_stock_alert", "stock <= threshold"),
        ("[VW]", "vw_orders_summary", "resumen BCNF"),
    ])

    # COLUMN 2 (x=5.70): Clientes & Núcleo de Pedidos
    ax.text(5.70, 21.60, "DOMINIO 2: CLIENTES & PEDIDOS (ACID)", color="#4ADE80", fontsize=12.5, fontweight="bold")
    t_cli = draw_table(ax, 5.70, 21.20, w, "clients", "#15803D", [
        ("[PK]", "id", "SERIAL"),
        ("", "full_name", "VARCHAR(120)"),
        ("[UK]", "phone", "VARCHAR(20)"),
        ("", "address", "TEXT"),
        ("[FK]", "district_id", "SMALLINT"),
        ("", "reference", "TEXT"),
    ])
    t_ord = draw_table(ax, 5.70, 17.75, w, "orders", "#15803D", [
        ("[PK]", "id", "SERIAL"),
        ("[UK]", "order_number", "VARCHAR(30)"),
        ("[FK]", "client_id", "INT"),
        ("[FK]", "user_id", "INT"),
        ("[FK]", "payment_method_id", "SMALLINT"),
        ("", "status", "order_status_enum"),
        ("", "estado", "VARCHAR(20)"),
        ("", "subtotal / shipping", "NUMERIC(10,2)"),
        ("", "total_amount", "NUMERIC(10,2)"),
        ("", "total_cents", "BIGINT"),
        ("", "shipping_type", "VARCHAR(20)"),
        ("", "tracking_number", "VARCHAR(50)"),
        ("", "notified_at", "TIMESTAMPTZ"),
        ("", "deleted_at", "TIMESTAMPTZ"),
    ])
    t_items = draw_table(ax, 5.70, 11.25, w, "order_items", "#15803D", [
        ("[PK]", "id", "SERIAL"),
        ("[FK]", "order_id", "INT [CASCADE]"),
        ("[FK]", "variant_id", "INT [RESTRICT]"),
        ("", "quantity", "INT > 0"),
        ("", "unit_price", "NUMERIC(10,2)"),
        ("", "subtotal", "NUMERIC(10,2)"),
    ])
    t_hist = draw_table(ax, 5.70, 7.80, w, "order_status_history", "#166534", [
        ("[PK]", "id", "SERIAL"),
        ("[FK]", "order_id", "INT [CASCADE]"),
        ("[FK]", "user_id", "INT"),
        ("", "previous_status", "order_status_enum"),
        ("", "new_status", "order_status_enum"),
        ("", "changed_at", "TIMESTAMPTZ"),
    ])
    t_ost = draw_table(ax, 5.70, 4.35, w, "order_state_transitions", "#166534", [
        ("[PK]", "id", "BIGSERIAL"),
        ("[FK]", "order_id", "INT [CASCADE]"),
        ("", "from_state / to_state", "VARCHAR(20)"),
        ("", "actor", "VARCHAR(50)"),
        ("", "metadata", "JSONB"),
    ])

    # COLUMN 3 (x=10.90): Pagos, Webhooks & Facturación SUNAT
    ax.text(10.90, 21.60, "DOMINIO 3: PAGOS & FACTURACIÓN SUNAT", color="#FB923C", fontsize=12.5, fontweight="bold")
    t_pay = draw_table(ax, 10.90, 21.20, w, "payments", "#C2410C", [
        ("[PK]", "id", "BIGSERIAL"),
        ("[FK]", "order_id", "INT [RESTRICT]"),
        ("[UK]", "provider_charge_id", "TEXT"),
        ("", "provider", "VARCHAR(30)"),
        ("", "amount_cents", "BIGINT > 0"),
        ("", "status", "VARCHAR(20)"),
        ("", "refunded_amount_cents", "BIGINT"),
        ("", "reconciled_at", "TIMESTAMPTZ"),
    ])
    t_web = draw_table(ax, 10.90, 17.00, w, "webhook_events", "#C2410C", [
        ("[PK]", "id", "BIGSERIAL"),
        ("[UK]", "provider + event_id", "VARCHAR"),
        ("", "status", "VARCHAR(20)"),
        ("", "payload", "JSONB"),
        ("", "attempts", "INT DEFAULT 0"),
        ("", "created_at", "TIMESTAMPTZ"),
        ("", "processed_at", "TIMESTAMPTZ"),
    ])
    t_inv = draw_table(ax, 10.90, 13.15, w, "invoices", "#B45309", [
        ("[PK]", "id", "SERIAL"),
        ("[FK]", "order_id", "INT [RESTRICT]"),
        ("[UK]", "tipo + serie + numero", "CHAR/INT"),
        ("", "cliente_numero_doc", "VARCHAR(20)"),
        ("", "cliente_denominacion", "VARCHAR(255)"),
        ("", "monto_subtotal / igv", "NUMERIC(12,2)"),
        ("", "monto_total", "NUMERIC(12,2)"),
        ("", "estado", "VARCHAR(20)"),
        ("", "hash_sunat / xml / cdr", "TEXT"),
        ("", "resumen_ticket", "TEXT"),
    ])
    t_invq = draw_table(ax, 10.90, 8.20, w, "invoice_queue", "#B45309", [
        ("[PK]", "id", "SERIAL"),
        ("[FK]", "order_id", "INT [CASCADE]"),
        ("", "tipo", "CHAR(2)"),
        ("", "estado", "VARCHAR(20)"),
        ("", "attempts / max", "INT"),
        ("", "next_attempt_at", "TIMESTAMPTZ"),
    ])
    t_invs = draw_table(ax, 10.90, 4.70, w, "invoice_series", "#B45309", [
        ("[PK]", "tipo + serie", "CHAR(2)+VARCHAR(4)"),
        ("", "last_number", "INT DEFAULT 0"),
    ])

    # COLUMN 4 (x=16.10): Seguridad, RBAC, Auditoría y Migraciones
    ax.text(16.10, 21.60, "DOMINIO 4: SEGURIDAD JWT & AUDITORÍA", color="#C084FC", fontsize=12.5, fontweight="bold")
    t_usr = draw_table(ax, 16.10, 21.20, w, "users", "#6D28D9", [
        ("[PK]", "id", "SERIAL"),
        ("[UK]", "email", "VARCHAR(150)"),
        ("", "name", "VARCHAR(100)"),
        ("", "password_hash", "VARCHAR(255)"),
        ("", "role", "user_role_enum"),
        ("", "is_active", "BOOLEAN"),
    ])
    t_ref = draw_table(ax, 16.10, 17.75, w, "refresh_tokens", "#6D28D9", [
        ("[PK]", "id", "BIGSERIAL"),
        ("[FK]", "user_id", "INT [CASCADE]"),
        ("[UK]", "token_hash", "CHAR(64)"),
        ("", "family_id", "UUID"),
        ("[FK]", "replaced_by", "BIGINT"),
        ("", "expires_at / revoked", "TIMESTAMPTZ"),
    ])
    t_aud = draw_table(ax, 16.10, 14.30, w, "audit_log", "#6D28D9", [
        ("[PK]", "id", "BIGSERIAL"),
        ("[FK]", "user_id", "INT [SET NULL]"),
        ("", "action", "VARCHAR(64)"),
        ("", "resource_type / id", "VARCHAR/TEXT"),
        ("", "before / after_state", "JSONB"),
        ("", "correlation_id", "TEXT"),
    ])
    t_idem = draw_table(ax, 16.10, 10.85, w, "idempotency_keys", "#4338CA", [
        ("[PK]", "id", "SERIAL"),
        ("[UK]", "user_id + key", "INT+VARCHAR(128)"),
        ("", "request_hash", "VARCHAR(64)"),
        ("", "status / status_code", "VARCHAR/INT"),
        ("", "response_body", "JSONB"),
        ("", "locked_until / expires", "TIMESTAMPTZ"),
    ])
    t_mig = draw_table(ax, 16.10, 7.40, w, "schema_migrations", "#4338CA", [
        ("[PK]", "version", "VARCHAR(64)"),
        ("", "name", "VARCHAR(255)"),
        ("", "applied_at", "TIMESTAMPTZ"),
    ])

    # COLUMN 5 (x=21.30): Resumen de Inventario de Objetos en Neon
    summary_box = FancyBboxPatch(
        (21.30, 2.40), 5.30, 19.30,
        boxstyle="round,pad=0.03,rounding_size=0.12",
        facecolor="#0F172A", edgecolor="#334155", linewidth=2.0, zorder=3
    )
    ax.add_patch(summary_box)
    ax.text(23.95, 21.10, "RESUMEN NEON DB", color="#38BDF8", fontsize=14.5, fontweight="bold", ha="center")
    ax.text(23.95, 20.60, "neondb (PostgreSQL 16/17)", color="#94A3B8", fontsize=11.5, ha="center")

    metrics = [
        ("Tablas Base (BCNF)", "22"),
        ("Vistas Analíticas", "2"),
        ("Tipos ENUM", "2"),
        ("Triggers Activos", "6"),
        ("Migraciones Aplicadas", "15 / 15"),
        ("Usuarios Semilla", "2"),
        ("Productos Activos", "8"),
        ("Variantes SKU", "23"),
        ("Clientes Registrados", "7"),
        ("Pedidos Iniciales", "6"),
        ("Series SUNAT", "4"),
    ]
    for i, (k, v) in enumerate(metrics):
        my = 19.65 - i * 0.95
        ax.text(21.65, my, k, color="#CBD5E1", fontsize=11.2, ha="left", va="center")
        ax.text(26.25, my, v, color="#4ADE80", fontsize=12.2, fontweight="bold", ha="right", va="center", family="DejaVu Sans Mono")

    ax.text(21.65, 8.60, "NOTACIÓN DE CLAVES:", color="#F8FAFC", fontsize=12.0, fontweight="bold")
    ax.text(21.65, 8.00, "[PK] Primary Key", color="#F59E0B", fontsize=11.0, family="DejaVu Sans Mono", fontweight="bold")
    ax.text(21.65, 7.40, "[FK] Foreign Key (1:N)", color="#38BDF8", fontsize=11.0, family="DejaVu Sans Mono", fontweight="bold")
    ax.text(21.65, 6.80, "[UK] Unique Constraint", color="#94A3B8", fontsize=11.0, family="DejaVu Sans Mono", fontweight="bold")
    ax.text(21.65, 6.20, "[VW] Analytical View", color="#2DD4BF", fontsize=11.0, family="DejaVu Sans Mono", fontweight="bold")
    ax.text(21.65, 4.80, "Host AWS US-West-2:\nep-young-lake-akgakejb\nSSL: require (TLS 1.3)\nCosto: $0.00 / S/ 0.00 perpetuo", color="#94A3B8", fontsize=10.6, linespacing=1.3)

    # Relationships (Foreign Keys)
    connect_orth(ax, t_cat["bottom"], t_prod["top"], color="#38BDF8", label="1:N")
    connect_orth(ax, t_prod["bottom"], t_var["top"], color="#38BDF8", label="1:N")
    connect_orth(ax, t_sizes["top"], (1.65, t_var["bottom"][1]), color="#38BDF8", mid_y=11.2)
    connect_orth(ax, t_colors["top"], (4.15, t_var["bottom"][1]), color="#38BDF8", mid_y=11.2)
    connect_orth(ax, t_dist["right"], (t_cli["left"][0], 8.50), color="#4ADE80", mid_x=5.40)
    connect_orth(ax, t_pm["right"], (t_ord["left"][0], 14.50), color="#4ADE80", mid_x=5.45)
    connect_orth(ax, t_cli["bottom"], t_ord["top"], color="#4ADE80", label="1:N")
    connect_orth(ax, t_ord["bottom"], t_items["top"], color="#4ADE80", label="1:N")
    connect_orth(ax, t_var["right"], (t_items["left"][0], 9.80), color="#38BDF8", mid_x=5.35, label="1:N")
    connect_orth(ax, t_items["bottom"], t_hist["top"], color="#4ADE80")
    connect_orth(ax, t_hist["bottom"], t_ost["top"], color="#4ADE80")

    connect_orth(ax, (t_ord["right"][0], 16.5), t_pay["left"], color="#FB923C", mid_x=10.60, label="1:N")
    connect_orth(ax, (t_ord["right"][0], 14.0), t_inv["left"], color="#FB923C", mid_x=10.65, label="1:N")
    connect_orth(ax, (t_ord["right"][0], 12.0), t_invq["left"], color="#FB923C", mid_x=10.55, label="1:N")

    connect_orth(ax, t_usr["bottom"], t_ref["top"], color="#C084FC", label="1:N")
    connect_orth(ax, t_ref["bottom"], t_aud["top"], color="#C084FC", label="1:N")
    connect_orth(ax, t_usr["left"], (t_ord["right"][0], 17.0), color="#C084FC", mid_x=15.75)

    # Footer
    ax.text(
        13.5, 0.90,
        "INFRAESTRUCTURA 100% GRATUITA (S/ 0.00 / MES):  Frontend PWA en Render Static + GitHub Pages ($0)   |   Backend API en Render Web Service Free ($0)   |   Base de Datos PostgreSQL en Neon Free Tier ($0 sin caducidad)",
        color="#94A3B8", fontsize=11.2, fontweight="bold", ha="center", va="center",
        bbox=dict(boxstyle="round,pad=0.35", facecolor="#0F172A", edgecolor="#334155", lw=1.5),
        zorder=5
    )

    plt.tight_layout(pad=0.3)
    plt.savefig(OUT_PNG, dpi=180, facecolor=fig.get_facecolor())
    plt.close(fig)
    print(f"Generated {OUT_PNG} ({os.path.getsize(OUT_PNG)} bytes)")

if __name__ == "__main__":
    main()
