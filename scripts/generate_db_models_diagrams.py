# -*- coding: utf-8 -*-
"""
@file generate_db_models_diagrams.py
@description Generador de Diagramas de Modelo Lógico y Modelo Físico de Base de Datos para LeoFit Solutions en 300 DPI
@project LeoFit Pedidos Sistema (UTP - Curso Integrador II)
@author Grupo 01 - UTP
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch
import os

def generate_logical_model():
    print("Generando diagrams/12_Modelo_Logico_BD.png...")
    fig, ax = plt.subplots(figsize=(18, 11), dpi=300)
    fig.patch.set_facecolor('#0F172A')
    ax.set_facecolor('#0F172A')
    ax.set_xlim(0, 18)
    ax.set_ylim(0, 11)
    ax.axis('off')

    # Main Title Banner
    ax.text(9.0, 10.5, "MODELO LÓGICO DE BASE DE DATOS (DER CONCEPTUAL-LÓGICO)", 
            ha='center', va='center', color='#F8FAFC', fontsize=17, fontweight='bold')
    ax.text(9.0, 10.05, "Sistema de Gestión de Pedidos e Inventario Multicanal — LeoFit Solutions (Grupo 01)", 
            ha='center', va='center', color='#38BDF8', fontsize=11)
    ax.text(9.0, 9.7, "Entidades de Dominio, Atributos Lógicos de Negocio y Cardinalidades (Crow's Foot / Chen)", 
            ha='center', va='center', color='#94A3B8', fontsize=9.5)

    # 8 Logical Entities
    # Format: (x, y, w, h, entity_name, tag_color, [attributes])
    entities = [
        # Columna 1
        (0.6, 5.2, 3.8, 3.8, "CATEGORIAS", "#38BDF8", [
            ("PK", "id_categoria", "Identificador único"),
            ("ATTR", "nombre", "Nombre comercial de categoría"),
            ("ATTR", "descripcion", "Detalle de línea deportiva"),
            ("ATTR", "estado", "Activo / Inactivo")
        ]),
        (0.6, 0.7, 3.8, 4.0, "PRODUCTOS", "#38BDF8", [
            ("PK", "id_producto", "Código único de prenda"),
            ("FK", "id_categoria", "Categoría asociada"),
            ("ATTR", "nombre_producto", "Nombre comercial"),
            ("ATTR", "descripcion_corte", "Material / Confección"),
            ("ATTR", "precio_base", "Precio de lista en Soles"),
            ("ATTR", "imagen_catalogo", "URL fotografía de catálogo"),
            ("ATTR", "disponible_venta", "Bandera de visibilidad")
        ]),

        # Columna 2
        (4.9, 5.2, 4.0, 3.8, "VARIANTES_PRENDA", "#06B6D4", [
            ("PK", "id_variante", "Identificador de variante"),
            ("FK", "id_producto", "Prenda base asociada"),
            ("ATTR", "talla", "Talla (S, M, L, XL, XXL)"),
            ("ATTR", "color", "Color / Tono específico"),
            ("ATTR", "sku_inventario", "Código único de SKU"),
            ("ATTR", "stock_disponible", "Unidades físicas en almacén"),
            ("ATTR", "alerta_minimo", "Umbral mínimo de reposición")
        ]),
        (4.9, 0.7, 4.0, 4.0, "ITEMS_PEDIDO", "#06B6D4", [
            ("PK", "id_item", "Identificador de línea de venta"),
            ("FK", "id_pedido", "Pedido al que pertenece"),
            ("FK", "id_variante", "Variante específica solicitada"),
            ("ATTR", "cantidad_prendas", "Número de unidades"),
            ("ATTR", "precio_pactado", "Precio congelado al vender"),
            ("ATTR", "subtotal_linea", "Importe calculado de la prenda")
        ]),

        # Columna 3
        (9.4, 5.2, 3.8, 3.8, "USUARIOS", "#F59E0B", [
            ("PK", "id_usuario", "Identificador de colaborador"),
            ("ATTR", "nombre_completo", "Nombre y apellidos"),
            ("ATTR", "correo_acceso", "Email corporativo (Único)"),
            ("ATTR", "clave_segura", "Hash de credenciales"),
            ("ATTR", "rol_sistema", "Administrador / Operador")
        ]),
        (9.4, 0.7, 3.8, 4.0, "PEDIDOS", "#F59E0B", [
            ("PK", "id_pedido", "Identificador del pedido"),
            ("ATTR", "numero_orden", "Código visible (LFT-xxxx)"),
            ("FK", "id_cliente", "Cliente que solicita"),
            ("FK", "id_usuario", "Operador que gestiona"),
            ("ATTR", "estado_actual", "Recibido / En Camino / Entregado"),
            ("ATTR", "metodo_pago", "Yape, Plin, Transferencia"),
            ("ATTR", "costo_envio", "Flete Lima / Provincia"),
            ("ATTR", "monto_total", "Importe final liquidado")
        ]),

        # Columna 4
        (13.7, 5.2, 3.7, 3.8, "CLIENTES", "#10B981", [
            ("PK", "id_cliente", "Identificador del cliente"),
            ("ATTR", "nombre_completo", "Nombre y apellidos del cliente"),
            ("ATTR", "telefono_whatsapp", "Celular de contacto y aviso"),
            ("ATTR", "direccion_entrega", "Dirección y distrito"),
            ("ATTR", "referencia_ubicacion", "Puntos de referencia"),
            ("ATTR", "tipo_destino", "Lima Metropolitana / Provincia")
        ]),
        (13.7, 0.7, 3.7, 4.0, "HISTORIAL_ESTADOS", "#10B981", [
            ("PK", "id_historial", "Identificador de evento"),
            ("FK", "id_pedido", "Pedido auditado"),
            ("FK", "id_usuario", "Colaborador que cambió estado"),
            ("ATTR", "estado_anterior", "Estado previo del flujo"),
            ("ATTR", "estado_nuevo", "Nuevo estado asignado"),
            ("ATTR", "fecha_hora_cambio", "Timestamp exacto del cambio"),
            ("ATTR", "observaciones", "Notas de despacho / N° Guía")
        ])
    ]

    for x, y, w, h, name, color, attrs in entities:
        # Card Body
        box = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.04,rounding_size=0.09",
                             facecolor='#1E293B', edgecolor=color, linewidth=1.4)
        ax.add_patch(box)

        # Entity Header
        header = FancyBboxPatch((x, y + h - 0.52), w, 0.52, boxstyle="round,pad=0.02,rounding_size=0.07",
                                facecolor='#0F172A', edgecolor=color, linewidth=1.1)
        ax.add_patch(header)
        ax.text(x + w/2, y + h - 0.26, f"«Entidad» {name}", ha='center', va='center',
                color=color, fontsize=10, fontweight='bold')

        # Attributes list
        curr_y = y + h - 0.82
        for kind, attr_name, desc in attrs:
            if kind == "PK":
                badge_bg = '#38BDF8'
                badge_fg = '#0F172A'
                ax.text(x + 0.2, curr_y, "[PK]", color=badge_bg, fontsize=7.5, fontweight='bold', family='monospace')
                ax.text(x + 0.75, curr_y, attr_name, color='#F8FAFC', fontsize=8, fontweight='bold', family='monospace')
            elif kind == "FK":
                badge_bg = '#F97316'
                ax.text(x + 0.2, curr_y, "[FK]", color=badge_bg, fontsize=7.5, fontweight='bold', family='monospace')
                ax.text(x + 0.75, curr_y, attr_name, color='#FDBA74', fontsize=8, family='monospace')
            else:
                ax.text(x + 0.2, curr_y, "  •", color='#94A3B8', fontsize=7.5, fontweight='bold')
                ax.text(x + 0.75, curr_y, attr_name, color='#E2E8F0', fontsize=8, family='sans-serif')
            
            # Subtle description
            ax.text(x + w - 0.15, curr_y, desc, ha='right', va='center', color='#64748B', fontsize=6.8, style='italic')
            curr_y -= 0.44

    # Connectors & Semantic Relations
    def draw_logical_rel(p1, p2, label, card1="1", card2="N", color="#94A3B8"):
        ax.plot([p1[0], p2[0]], [p1[1], p2[1]], color=color, linestyle='-', linewidth=1.6)
        mid_x = (p1[0] + p2[0]) / 2
        mid_y = (p1[1] + p2[1]) / 2
        # Semantic label
        ax.text(mid_x, mid_y, label, ha='center', va='center', fontsize=7.5, color='#F8FAFC', fontweight='bold',
                bbox=dict(boxstyle='round,pad=0.2', facecolor='#0F172A', edgecolor=color, linewidth=0.9))
        # Cardinalities
        ax.text(p1[0], p1[1] + (0.18 if p1[1] <= p2[1] else -0.18), card1,
                ha='center', va='center', color='#38BDF8', fontsize=8.5, fontweight='bold')
        ax.text(p2[0], p2[1] + (0.18 if p2[1] <= p1[1] else -0.18), card2,
                ha='center', va='center', color='#38BDF8', fontsize=8.5, fontweight='bold')

    # 1. CATEGORIAS -> PRODUCTOS
    draw_logical_rel((2.5, 5.2), (2.5, 4.7), "Clasifica", "1", "1..*", "#38BDF8")

    # 2. PRODUCTOS -> VARIANTES_PRENDA
    draw_logical_rel((4.4, 2.7), (4.9, 7.0), "Posee", "1", "1..*", "#06B6D4")

    # 3. VARIANTES_PRENDA -> ITEMS_PEDIDO
    draw_logical_rel((6.9, 5.2), (6.9, 4.7), "Incluida en", "1", "0..*", "#06B6D4")

    # 4. PEDIDOS -> ITEMS_PEDIDO
    draw_logical_rel((9.4, 2.7), (8.9, 2.7), "Contiene", "1", "1..*", "#F59E0B")

    # 5. USUARIOS -> PEDIDOS
    draw_logical_rel((11.3, 5.2), (11.3, 4.7), "Gestiona", "1", "0..*", "#F59E0B")

    # 6. CLIENTES -> PEDIDOS
    draw_logical_rel((13.7, 7.0), (13.2, 2.7), "Realiza", "1", "0..*", "#10B981")

    # 7. PEDIDOS -> HISTORIAL_ESTADOS
    draw_logical_rel((13.2, 1.8), (13.7, 1.8), "Genera", "1", "1..*", "#10B981")

    # 8. USUARIOS -> HISTORIAL_ESTADOS
    draw_logical_rel((13.2, 6.2), (15.5, 4.7), "Audita", "1", "0..*", "#94A3B8")

    # Legend / Info Footer
    legend_box = FancyBboxPatch((0.6, 0.08), 16.8, 0.45, boxstyle="round,pad=0.02,rounding_size=0.04",
                                facecolor='#1E293B', edgecolor='#334155', linewidth=1.0)
    ax.add_patch(legend_box)
    ax.text(0.9, 0.3, "LEYENDA LÓGICA:", color='#F8FAFC', fontsize=8, fontweight='bold', va='center')
    ax.text(2.8, 0.3, "[PK] Clave Primaria", color='#38BDF8', fontsize=7.5, fontweight='bold', va='center')
    ax.text(4.8, 0.3, "[FK] Clave Foránea de Asociación", color='#F97316', fontsize=7.5, fontweight='bold', va='center')
    ax.text(8.0, 0.3, "Cardinalidades: 1 (Uno) | 1..* (Uno a Muchos) | 0..* (Cero a Muchos)", color='#E2E8F0', fontsize=7.5, va='center')
    ax.text(14.8, 0.3, "Modelado en 3FN / BCNF", color='#10B981', fontsize=7.5, fontweight='bold', va='center')

    out_path = 'diagrams/12_Modelo_Logico_BD.png'
    plt.savefig(out_path, dpi=300, bbox_inches='tight', facecolor='#0F172A')
    plt.close()
    print(f"[OK] Guardado exitosamente: {out_path}")


def generate_physical_model():
    print("Generando diagrams/13_Modelo_Fisico_BD.png...")
    fig, ax = plt.subplots(figsize=(19, 12), dpi=300)
    fig.patch.set_facecolor('#0B1120')
    ax.set_facecolor('#0B1120')
    ax.set_xlim(0, 19)
    ax.set_ylim(0, 12)
    ax.axis('off')

    # Main Title Banner
    ax.text(9.5, 11.5, "MODELO FÍSICO DE BASE DE DATOS (ESQUEMA DDL RELACIONAL)", 
            ha='center', va='center', color='#F8FAFC', fontsize=17, fontweight='bold')
    ax.text(9.5, 11.05, "Implementación RDBMS (PostgreSQL / MySQL InnoDB) — Conforme a database/schema.sql", 
            ha='center', va='center', color='#F97316', fontsize=11)
    ax.text(9.5, 10.7, "Tipos de Datos SQL Exactos, Constraints, Claves Primarias/Foráneas, Índices y Motores de Transacción ACID", 
            ha='center', va='center', color='#94A3B8', fontsize=9.5)

    # 8 Physical Tables
    # Format: (x, y, w, h, table_name, [columns_with_types])
    tables = [
        # Columna 1
        (0.6, 5.8, 4.0, 4.4, "categories", [
            ("PK", "id", "INT AUTO_INCREMENT"),
            ("UK", "name", "VARCHAR(60) NOT NULL"),
            ("COL", "description", "TEXT NULL"),
            ("IDX", "idx_cat_name", "INDEX (name)")
        ]),
        (0.6, 0.8, 4.0, 4.6, "products", [
            ("PK", "id", "INT AUTO_INCREMENT"),
            ("FK", "category_id", "INT NOT NULL [FK]"),
            ("COL", "name", "VARCHAR(120) NOT NULL"),
            ("COL", "description", "TEXT NULL"),
            ("COL", "base_price", "DECIMAL(10,2) CHECK > 0"),
            ("COL", "image_url", "VARCHAR(255) NULL"),
            ("COL", "is_active", "BOOLEAN DEFAULT TRUE"),
            ("COL", "created_at", "TIMESTAMP DEFAULT NOW()"),
            ("IDX", "idx_prod_cat", "INDEX (category_id)")
        ]),

        # Columna 2
        (5.1, 5.8, 4.2, 4.4, "product_variants", [
            ("PK", "id", "INT AUTO_INCREMENT"),
            ("FK", "product_id", "INT NOT NULL [FK]"),
            ("COL", "size", "VARCHAR(10) NOT NULL"),
            ("COL", "color", "VARCHAR(50) NOT NULL"),
            ("UK", "sku", "VARCHAR(50) UNIQUE NOT NULL"),
            ("COL", "stock", "INT NOT NULL CHECK >= 0"),
            ("COL", "alert_threshold", "INT DEFAULT 3"),
            ("IDX", "idx_var_prod", "INDEX (product_id)")
        ]),
        (5.1, 0.8, 4.2, 4.6, "order_items", [
            ("PK", "id", "INT AUTO_INCREMENT"),
            ("FK", "order_id", "INT NOT NULL [FK ON DELETE CASCADE]"),
            ("FK", "variant_id", "INT NOT NULL [FK]"),
            ("COL", "quantity", "INT NOT NULL CHECK > 0"),
            ("COL", "unit_price", "DECIMAL(10,2) NOT NULL"),
            ("COL", "subtotal", "DECIMAL(10,2) NOT NULL"),
            ("IDX", "idx_items_order", "INDEX (order_id)")
        ]),

        # Columna 3
        (9.8, 5.8, 4.1, 4.4, "users", [
            ("PK", "id", "INT AUTO_INCREMENT"),
            ("COL", "name", "VARCHAR(100) NOT NULL"),
            ("UK", "email", "VARCHAR(150) UNIQUE NOT NULL"),
            ("COL", "password_hash", "VARCHAR(255) NOT NULL"),
            ("COL", "role", "ENUM('ADMIN', 'OPERATOR')"),
            ("COL", "created_at", "TIMESTAMP DEFAULT NOW()")
        ]),
        (9.8, 0.8, 4.1, 4.6, "orders", [
            ("PK", "id", "INT AUTO_INCREMENT"),
            ("UK", "order_number", "VARCHAR(30) UNIQUE NOT NULL"),
            ("FK", "client_id", "INT NOT NULL [FK]"),
            ("FK", "user_id", "INT NULL [FK]"),
            ("COL", "status", "ENUM('RECIBIDO','PREPARACION',...)"),
            ("COL", "payment_method", "ENUM('YAPE','PLIN',...)"),
            ("COL", "subtotal", "DECIMAL(10,2) NOT NULL"),
            ("COL", "shipping_cost", "DECIMAL(10,2) DEFAULT 0.00"),
            ("COL", "total_amount", "DECIMAL(10,2) NOT NULL"),
            ("IDX", "idx_ord_stat_date", "INDEX (status, created_at)")
        ]),

        # Columna 4
        (14.4, 5.8, 4.0, 4.4, "clients", [
            ("PK", "id", "INT AUTO_INCREMENT"),
            ("COL", "full_name", "VARCHAR(120) NOT NULL"),
            ("COL", "phone", "VARCHAR(20) NOT NULL"),
            ("COL", "address", "TEXT NOT NULL"),
            ("COL", "district", "VARCHAR(80) NOT NULL"),
            ("COL", "reference", "TEXT NULL"),
            ("COL", "created_at", "TIMESTAMP DEFAULT NOW()"),
            ("IDX", "idx_client_phone", "INDEX (phone)")
        ]),
        (14.4, 0.8, 4.0, 4.6, "order_status_history", [
            ("PK", "id", "INT AUTO_INCREMENT"),
            ("FK", "order_id", "INT NOT NULL [FK ON DELETE CASCADE]"),
            ("FK", "user_id", "INT NULL [FK]"),
            ("COL", "previous_status", "VARCHAR(30) NULL"),
            ("COL", "new_status", "VARCHAR(30) NOT NULL"),
            ("COL", "changed_at", "TIMESTAMP DEFAULT NOW()"),
            ("COL", "comments", "TEXT NULL"),
            ("IDX", "idx_hist_order", "INDEX (order_id)")
        ])
    ]

    for x, y, w, h, tname, cols in tables:
        # Table Container Box
        box = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.03,rounding_size=0.07",
                             facecolor='#1E293B', edgecolor='#38BDF8', linewidth=1.3)
        ax.add_patch(box)

        # Table Header
        header = FancyBboxPatch((x, y + h - 0.50), w, 0.50, boxstyle="round,pad=0.02,rounding_size=0.05",
                                facecolor='#0F172A', edgecolor='#F97316', linewidth=1.2)
        ax.add_patch(header)
        ax.text(x + w/2, y + h - 0.25, f"TABLE: {tname}", ha='center', va='center',
                color='#F97316', fontsize=10.5, fontweight='bold', family='monospace')

        # Columns
        curr_y = y + h - 0.78
        for kind, col_name, sql_type in cols:
            if kind == "PK":
                badge_bg = '#E11D48'
                badge_lbl = "PK"
                color_name = '#F8FAFC'
                ax.text(x + 0.18, curr_y, badge_lbl, color=badge_bg, fontsize=7.5, fontweight='bold', family='monospace')
                ax.text(x + 0.75, curr_y, col_name, color=color_name, fontsize=8, fontweight='bold', family='monospace')
            elif kind == "FK":
                badge_bg = '#F59E0B'
                badge_lbl = "FK"
                color_name = '#FDE047'
                ax.text(x + 0.18, curr_y, badge_lbl, color=badge_bg, fontsize=7.5, fontweight='bold', family='monospace')
                ax.text(x + 0.75, curr_y, col_name, color=color_name, fontsize=8, family='monospace')
            elif kind == "UK":
                badge_bg = '#A855F7'
                badge_lbl = "UK"
                color_name = '#E9D5FF'
                ax.text(x + 0.18, curr_y, badge_lbl, color=badge_bg, fontsize=7.5, fontweight='bold', family='monospace')
                ax.text(x + 0.75, curr_y, col_name, color=color_name, fontsize=8, family='monospace')
            elif kind == "IDX":
                badge_bg = '#06B6D4'
                badge_lbl = "IDX"
                color_name = '#67E8F9'
                ax.text(x + 0.18, curr_y, badge_lbl, color=badge_bg, fontsize=7, fontweight='bold', family='monospace')
                ax.text(x + 0.75, curr_y, col_name, color=color_name, fontsize=7.5, style='italic', family='monospace')
            else:
                ax.text(x + 0.25, curr_y, "•", color='#94A3B8', fontsize=7.5, fontweight='bold')
                ax.text(x + 0.75, curr_y, col_name, color='#E2E8F0', fontsize=8, family='monospace')

            # SQL Type
            ax.text(x + w - 0.15, curr_y, sql_type, ha='right', va='center', color='#94A3B8', fontsize=7.2, family='monospace')
            curr_y -= 0.38

    # Foreign Key Connectors with Stepped Orthogonal Lines
    def draw_fk_line(points, label="FK 1:N", color="#38BDF8"):
        xs = [p[0] for p in points]
        ys = [p[1] for p in points]
        ax.plot(xs, ys, color=color, linestyle='-', linewidth=1.7)
        mid_idx = len(points) // 2
        lx = (points[mid_idx-1][0] + points[mid_idx][0]) / 2
        ly = (points[mid_idx-1][1] + points[mid_idx][1]) / 2
        ax.text(lx, ly, label, ha='center', va='center', fontsize=7.5, color='#F8FAFC', fontweight='bold',
                bbox=dict(boxstyle='round,pad=0.18', facecolor='#0F172A', edgecolor=color, linewidth=0.9))

    # 1. categories (Col 1 Top) -> products (Col 1 Bottom)
    draw_fk_line([(2.6, 5.8), (2.6, 5.4)], "FK: category_id", "#38BDF8")

    # 2. products (Col 1 Bottom) -> product_variants (Col 2 Top)
    draw_fk_line([(4.6, 3.6), (4.85, 3.6), (4.85, 8.0), (5.1, 8.0)], "FK: product_id", "#38BDF8")

    # 3. product_variants (Col 2 Top) -> order_items (Col 2 Bottom)
    draw_fk_line([(7.2, 5.8), (7.2, 5.4)], "FK: variant_id", "#38BDF8")

    # 4. orders (Col 3 Bottom) -> order_items (Col 2 Bottom)
    draw_fk_line([(9.8, 3.0), (9.3, 3.0)], "FK: order_id", "#F59E0B")

    # 5. users (Col 3 Top) -> orders (Col 3 Bottom)
    draw_fk_line([(11.8, 5.8), (11.8, 5.4)], "FK: user_id", "#F59E0B")

    # 6. clients (Col 4 Top) -> orders (Col 3 Bottom)
    draw_fk_line([(14.4, 8.0), (14.15, 8.0), (14.15, 4.4), (13.9, 4.4)], "FK: client_id", "#10B981")

    # 7. orders (Col 3 Bottom) -> order_status_history (Col 4 Bottom)
    draw_fk_line([(13.9, 2.5), (14.4, 2.5)], "FK: order_id", "#10B981")

    # 8. users (Col 3 Top) -> order_status_history (Col 4 Bottom)
    draw_fk_line([(13.9, 7.0), (14.15, 7.0), (14.15, 1.5), (14.4, 1.5)], "FK: user_id", "#94A3B8")

    # Physical DB Legend & Engine Notes
    legend_box = FancyBboxPatch((0.6, 0.12), 17.8, 0.48, boxstyle="round,pad=0.02,rounding_size=0.04",
                                facecolor='#1E293B', edgecolor='#334155', linewidth=1.0)
    ax.add_patch(legend_box)
    ax.text(0.9, 0.36, "CONVENCIONES FÍSICAS DDL:", color='#F8FAFC', fontsize=8, fontweight='bold', va='center')
    ax.text(3.4, 0.36, "PK: PRIMARY KEY (Clave Primaria)", color='#E11D48', fontsize=7.5, fontweight='bold', va='center')
    ax.text(7.0, 0.36, "FK: FOREIGN KEY (Integridad Referencial)", color='#F59E0B', fontsize=7.5, fontweight='bold', va='center')
    ax.text(11.2, 0.36, "UK: UNIQUE KEY (Restricción Única)", color='#A855F7', fontsize=7.5, fontweight='bold', va='center')
    ax.text(14.7, 0.36, "IDX: B-TREE INDEX (Optimización O(log N))", color='#06B6D4', fontsize=7.5, fontweight='bold', va='center')

    out_path = 'diagrams/13_Modelo_Fisico_BD.png'
    plt.savefig(out_path, dpi=300, bbox_inches='tight', facecolor='#0B1120')
    plt.close()
    print(f"[OK] Guardado exitosamente: {out_path}")


if __name__ == '__main__':
    os.makedirs('diagrams', exist_ok=True)
    generate_logical_model()
    generate_physical_model()
