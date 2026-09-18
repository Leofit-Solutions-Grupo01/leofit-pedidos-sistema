# -*- coding: utf-8 -*-
"""
@file generate_leofit_db_models_bw.py
@description Generador de Diagramas Oficiales de Base de Datos para LeoFit Solutions:
             1. Modelo Lógico de Dominio (DER Conceptual-Lógico en B&W)
             2. Modelo Físico Relacional (Esquema DDL SQL en B&W)
             Diseño CAD de Alta Precisión:
             - Conexiones ortogonales directas campo a campo (PK -> FK).
             - Cero cruces de líneas, cero colisiones de texto o cabeceras.
             - Notación Crow's Foot pura y perfectamente dimensionada.
@project LeoFit Pedidos Sistema (UTP - Curso Integrador II)
@author Grupo 01 - UTP
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import Rectangle, Circle
import os

os.makedirs('diagrams', exist_ok=True)

# ----------------------------------------------------------------------
# FUNCIONES DE DIBUJO DE NOTACIÓN CROW'S FOOT CAD
# ----------------------------------------------------------------------
def draw_orthogonal_relation_h(ax, x_start, y_start, x_mid, y_end, x_end):
    """
    Conecta de forma ortogonal horizontal:
    (x_start, y_start) -> (x_mid, y_start) -> (x_mid, y_end) -> (x_end, y_end)
    Lado 1 (Padre) en (x_start, y_start): Barras ||
    Lado N (Hijo) en (x_end, y_end): Círculo ○ y Pata de Gallo <
    """
    if x_start == x_end and y_start == y_end:
        return
    
    if abs(y_start - y_end) < 1e-4:
        # Línea recta pura
        ax.plot([x_start, x_end], [y_start, y_end], color='#000000', linewidth=1.3, zorder=2)
    else:
        # Escalón ortogonal
        ax.plot([x_start, x_mid, x_mid, x_end], [y_start, y_start, y_end, y_end], color='#000000', linewidth=1.3, zorder=2)

    # Lado 1 (Padre): ||
    direction_start = 1 if x_mid >= x_start else -1
    b1_x = x_start + direction_start * 0.16
    b2_x = x_start + direction_start * 0.28
    ax.plot([b1_x, b1_x], [y_start - 0.16, y_start + 0.16], color='#000000', linewidth=1.3, zorder=4)
    ax.plot([b2_x, b2_x], [y_start - 0.16, y_start + 0.16], color='#000000', linewidth=1.3, zorder=4)

    # Lado N (Hijo): ○<
    direction_end = 1 if x_end >= x_mid else -1
    # Círculo de opcionalidad
    c_x = x_end - direction_end * 0.42
    circle = Circle((c_x, y_end), 0.09, facecolor='#FFFFFF', edgecolor='#000000', linewidth=1.2, zorder=5)
    ax.add_patch(circle)
    # Tridente / Pata de gallo
    ax.plot([x_end - direction_end * 0.30, x_end], [y_end, y_end + 0.16], color='#000000', linewidth=1.3, zorder=4)
    ax.plot([x_end - direction_end * 0.30, x_end], [y_end, y_end - 0.16], color='#000000', linewidth=1.3, zorder=4)


def draw_orthogonal_relation_v(ax, x_start, y_start, y_mid, x_end, y_end):
    """
    Conecta verticalmente con escalón:
    (x_start, y_start) -> (x_start, y_mid) -> (x_end, y_mid) -> (x_end, y_end)
    Lado 1 (Padre) en (x_start, y_start): Barras ==
    Lado N (Hijo) en (x_end, y_end): Círculo ○ y Pata de Gallo <
    """
    if abs(x_start - x_end) < 1e-4:
        ax.plot([x_start, x_end], [y_start, y_end], color='#000000', linewidth=1.3, zorder=2)
    else:
        ax.plot([x_start, x_start, x_end, x_end], [y_start, y_mid, y_mid, y_end], color='#000000', linewidth=1.3, zorder=2)

    # Lado 1 (Padre arriba): ==
    b1_y = y_start - 0.15
    b2_y = y_start - 0.27
    ax.plot([x_start - 0.16, x_start + 0.16], [b1_y, b1_y], color='#000000', linewidth=1.3, zorder=4)
    ax.plot([x_start - 0.16, x_start + 0.16], [b2_y, b2_y], color='#000000', linewidth=1.3, zorder=4)

    # Lado N (Hijo abajo): ○<
    c_y = y_end + 0.40
    circle = Circle((x_end, c_y), 0.09, facecolor='#FFFFFF', edgecolor='#000000', linewidth=1.2, zorder=5)
    ax.add_patch(circle)
    ax.plot([x_end, x_end - 0.16], [y_end + 0.28, y_end], color='#000000', linewidth=1.3, zorder=4)
    ax.plot([x_end, x_end + 0.16], [y_end + 0.28, y_end], color='#000000', linewidth=1.3, zorder=4)


# ======================================================================
# 1. MODELO LÓGICO DE BASE DE DATOS
# ======================================================================
def generate_logical_model():
    print("Generando diagrams/12_Modelo_Logico_BD.png...")
    fig, ax = plt.subplots(figsize=(24, 15.5), dpi=300)
    fig.patch.set_facecolor('#FFFFFF')
    ax.set_facecolor('#FFFFFF')
    ax.set_xlim(0, 24)
    ax.set_ylim(0, 15.5)
    ax.axis('off')

    # Marco de ingeniería
    border = Rectangle((0.5, 0.5), 23.0, 14.5, fill=False, edgecolor='#000000', linewidth=1.6)
    ax.add_patch(border)

    # Encabezado
    ax.text(12.0, 14.70, "SISTEMA DE GESTIÓN DE PEDIDOS E INVENTARIO LEOFIT — MODELO LÓGICO DE DATOS",
            ha='center', va='center', color='#000000', fontsize=15.5, fontweight='bold', family='monospace')
    ax.text(12.0, 14.30, "Diagrama Entidad-Relación Conceptual-Lógico de Dominio (3FN / BCNF) — Notación Crow's Foot",
            ha='center', va='center', color='#000000', fontsize=10.5, family='monospace')
    ax.plot([0.5, 23.5], [14.00, 14.00], color='#000000', linewidth=1.2)

    # Rótulos de Dominio / Capas
    ax.text(0.8, 13.65, "DOMINIO 1: CATÁLOGO Y PRODUCTOS", color='#000000', fontsize=9.0, fontweight='bold', family='monospace')
    ax.text(0.8, 8.85, "DOMINIO 2: VENTAS Y PEDIDOS", color='#000000', fontsize=9.0, fontweight='bold', family='monospace')
    ax.text(0.8, 4.05, "DOMINIO 3: CONTROL DE ACCESO Y AUDITORÍA", color='#000000', fontsize=9.0, fontweight='bold', family='monospace')

    def draw_entity(x, y_top, w, name, attrs):
        header_h = 0.46
        row_h = 0.32
        padding_b = 0.12
        total_h = header_h + (len(attrs) * row_h) + padding_b
        y_bot = y_top - total_h

        # Cabecera
        h_rect = Rectangle((x, y_top - header_h), w, header_h, facecolor='#000000', edgecolor='#000000', linewidth=1.2, zorder=3)
        ax.add_patch(h_rect)
        ax.text(x + w/2, y_top - header_h/2, name, ha='center', va='center',
                color='#FFFFFF', fontsize=9.2, fontweight='bold', family='monospace', zorder=4)

        # Cuerpo
        b_rect = Rectangle((x, y_bot), w, total_h - header_h, facecolor='#FFFFFF', edgecolor='#000000', linewidth=1.2, zorder=3)
        ax.add_patch(b_rect)

        # Atributos y registro de posiciones Y exactas
        row_y_map = {}
        curr_y = y_top - header_h - 0.20
        for i, attr in enumerate(attrs):
            is_pk = '(PK)' in attr
            font_weight = 'bold' if is_pk else 'normal'
            ax.text(x + 0.14, curr_y, attr, ha='left', va='center',
                    color='#000000', fontsize=8.0, fontweight=font_weight, family='monospace', zorder=4)
            row_y_map[i] = curr_y
            curr_y -= row_h

        return {
            'x_left': x,
            'x_right': x + w,
            'x_center': x + w/2,
            'y_top': y_top,
            'y_bottom': y_bot,
            'width': w,
            'height': total_h,
            'rows': row_y_map
        }

    # -------------------------------------------------------------
    # FILA 1: CATÁLOGO (Y_TOP = 13.35)
    # -------------------------------------------------------------
    cat = draw_entity(0.8, 13.35, 5.0, "CATEGORIAS", [
        "id_categoria (PK)",          # row 0
        "nombre_categoria",           # row 1
        "descripcion_linea",          # row 2
        "estado_categoria"            # row 3
    ])

    prod = draw_entity(9.5, 13.35, 5.0, "PRODUCTOS", [
        "id_producto (PK)",           # row 0
        "id_categoria (FK)",          # row 1
        "nombre_prenda",              # row 2
        "descripcion_confeccion",     # row 3
        "precio_base_lista",          # row 4
        "fotografia_catalogo",        # row 5
        "disponible_para_venta"       # row 6
    ])

    var = draw_entity(18.2, 13.35, 5.0, "VARIANTES_PRODUCTO", [
        "id_variante (PK)",           # row 0
        "id_producto (FK)",           # row 1
        "talla_prenda",               # row 2
        "color_prenda",               # row 3
        "sku_inventario",             # row 4
        "stock_disponible",           # row 5
        "alerta_stock_minimo"         # row 6
    ])

    # -------------------------------------------------------------
    # FILA 2: VENTAS (Y_TOP = 8.55)
    # -------------------------------------------------------------
    cli = draw_entity(0.8, 8.55, 5.0, "CLIENTES", [
        "id_cliente (PK)",            # row 0
        "nombre_completo",            # row 1
        "telefono_whatsapp",          # row 2
        "direccion_despacho",         # row 3
        "distrito_entrega",           # row 4
        "referencia_ubicacion"        # row 5
    ])

    ped = draw_entity(9.5, 8.55, 5.0, "PEDIDOS", [
        "id_pedido (PK)",             # row 0
        "numero_orden_compra",        # row 1
        "id_cliente (FK)",            # row 2
        "id_usuario (FK)",            # row 3
        "estado_pedido",              # row 4
        "metodo_pago",                # row 5
        "costo_flete_envio",          # row 6
        "monto_total_orden",          # row 7
        "notas_indicaciones"          # row 8
    ])

    item = draw_entity(18.2, 8.55, 5.0, "ITEMS_PEDIDO", [
        "id_item_pedido (PK)",        # row 0
        "id_pedido (FK)",             # row 1
        "id_variante (FK)",           # row 2
        "cantidad_prendas",           # row 3
        "precio_unitario_venta",      # row 4
        "subtotal_calculado"          # row 5
    ])

    # -------------------------------------------------------------
    # FILA 3: USUARIOS Y AUDITORÍA (Y_TOP = 3.75)
    # -------------------------------------------------------------
    usr = draw_entity(0.8, 3.75, 5.0, "USUARIOS", [
        "id_usuario (PK)",            # row 0
        "nombre_completo",            # row 1
        "correo_corporativo",         # row 2
        "clave_acceso_hash",          # row 3
        "rol_sistema"                 # row 4
    ])

    hist = draw_entity(9.5, 3.75, 5.0, "HISTORIAL_ESTADOS", [
        "id_historial (PK)",          # row 0
        "id_pedido (FK)",             # row 1
        "id_usuario (FK)",            # row 2
        "estado_anterior",            # row 3
        "nuevo_estado",               # row 4
        "fecha_hora_cambio",          # row 5
        "observaciones_guia"          # row 6
    ])

    # =============================================================
    # CONEXIONES PRECISAS CAMPO A CAMPO (PK -> FK)
    # =============================================================

    # 1. CATEGORIAS.id_categoria (PK, row 0) -> PRODUCTOS.id_categoria (FK, row 1)
    draw_orthogonal_relation_h(ax,
                               x_start=cat['x_right'], y_start=cat['rows'][0],
                               x_mid=7.65,
                               y_end=prod['rows'][1], x_end=prod['x_left'])

    # 2. PRODUCTOS.id_producto (PK, row 0) -> VARIANTES_PRODUCTO.id_producto (FK, row 1)
    draw_orthogonal_relation_h(ax,
                               x_start=prod['x_right'], y_start=prod['rows'][0],
                               x_mid=16.35,
                               y_end=var['rows'][1], x_end=var['x_left'])

    # 3. VARIANTES_PRODUCTO (1) -> ITEMS_PEDIDO (N) [Vertical directo]
    draw_orthogonal_relation_v(ax,
                               x_start=var['x_center'], y_start=var['y_bottom'],
                               y_mid=item['y_top'] + 0.45,
                               x_end=item['x_center'], y_end=item['y_top'])

    # 4. CLIENTES.id_cliente (PK, row 0) -> PEDIDOS.id_cliente (FK, row 2)
    draw_orthogonal_relation_h(ax,
                               x_start=cli['x_right'], y_start=cli['rows'][0],
                               x_mid=7.20,
                               y_end=ped['rows'][2], x_end=ped['x_left'])

    # 5. PEDIDOS.id_pedido (PK, row 0) -> ITEMS_PEDIDO.id_pedido (FK, row 1)
    draw_orthogonal_relation_h(ax,
                               x_start=ped['x_right'], y_start=ped['rows'][0],
                               x_mid=16.35,
                               y_end=item['rows'][1], x_end=item['x_left'])

    # 6. PEDIDOS (1) -> HISTORIAL_ESTADOS (N) [Vertical directo]
    draw_orthogonal_relation_v(ax,
                               x_start=ped['x_center'], y_start=ped['y_bottom'],
                               y_mid=hist['y_top'] + 0.45,
                               x_end=hist['x_center'], y_end=hist['y_top'])

    # 7. USUARIOS.id_usuario (PK, row 0) -> HISTORIAL_ESTADOS.id_usuario (FK, row 2)
    draw_orthogonal_relation_h(ax,
                               x_start=usr['x_right'], y_start=usr['rows'][0] - 0.08,
                               x_mid=7.65,
                               y_end=hist['rows'][2], x_end=hist['x_left'])

    # 8. USUARIOS.id_usuario (PK, row 0) -> PEDIDOS.id_usuario (FK, row 3)
    draw_orthogonal_relation_h(ax,
                               x_start=usr['x_right'], y_start=usr['rows'][0] + 0.08,
                               x_mid=8.10,
                               y_end=ped['rows'][3], x_end=ped['x_left'])

    # Leyenda inferior
    ax.plot([0.5, 23.5], [1.00, 1.00], color='#000000', linewidth=1.2)
    ax.text(12.0, 0.72, "NOTACIÓN CROW'S FOOT:  || Uno obligatorio (Mandatory One)    ○< Cero a muchos (Optional Many)    (PK) Primary Key    (FK) Foreign Key",
            ha='center', va='center', color='#000000', fontsize=9.0, family='monospace', fontweight='bold')

    plt.savefig('diagrams/12_Modelo_Logico_BD.png', dpi=300, facecolor='#FFFFFF', bbox_inches='tight')
    plt.close()
    print("[OK] Modelo Lógico guardado: diagrams/12_Modelo_Logico_BD.png")


# ======================================================================
# 2. MODELO FÍSICO DE BASE DE DATOS (ESQUEMA DDL SQL)
# ======================================================================
def generate_physical_model():
    print("Generando diagrams/13_Modelo_Fisico_BD.png...")
    fig, ax = plt.subplots(figsize=(24, 15.5), dpi=300)
    fig.patch.set_facecolor('#FFFFFF')
    ax.set_facecolor('#FFFFFF')
    ax.set_xlim(0, 24)
    ax.set_ylim(0, 15.5)
    ax.axis('off')

    # Marco de ingeniería
    border = Rectangle((0.5, 0.5), 23.0, 14.5, fill=False, edgecolor='#000000', linewidth=1.6)
    ax.add_patch(border)

    # Encabezado
    ax.text(12.0, 14.70, "BASE DE DATOS RELACIONAL LEOFIT SOLUTIONS — MODELO FÍSICO DDL",
            ha='center', va='center', color='#000000', fontsize=15.5, fontweight='bold', family='monospace')
    ax.text(12.0, 14.30, "Especificación Técnica RDBMS (PostgreSQL / MySQL) — Tipos de Datos y Restricciones de Integridad",
            ha='center', va='center', color='#000000', fontsize=10.5, family='monospace')
    ax.plot([0.5, 23.5], [14.00, 14.00], color='#000000', linewidth=1.2)

    # Rótulos de Dominio / Capas
    ax.text(0.8, 13.65, "DOMINIO 1: CATÁLOGO Y PRODUCTOS", color='#000000', fontsize=9.0, fontweight='bold', family='monospace')
    ax.text(0.8, 8.85, "DOMINIO 2: VENTAS Y PEDIDOS", color='#000000', fontsize=9.0, fontweight='bold', family='monospace')
    ax.text(0.8, 4.05, "DOMINIO 3: CONTROL DE ACCESO Y AUDITORÍA", color='#000000', fontsize=9.0, fontweight='bold', family='monospace')

    def draw_table(x, y_top, w, name, cols):
        header_h = 0.46
        row_h = 0.32
        padding_b = 0.12
        total_h = header_h + (len(cols) * row_h) + padding_b
        y_bot = y_top - total_h

        # Cabecera
        h_rect = Rectangle((x, y_top - header_h), w, header_h, facecolor='#000000', edgecolor='#000000', linewidth=1.2, zorder=3)
        ax.add_patch(h_rect)
        ax.text(x + w/2, y_top - header_h/2, f"TABLE: {name}", ha='center', va='center',
                color='#FFFFFF', fontsize=9.2, fontweight='bold', family='monospace', zorder=4)

        # Cuerpo
        b_rect = Rectangle((x, y_bot), w, total_h - header_h, facecolor='#FFFFFF', edgecolor='#000000', linewidth=1.2, zorder=3)
        ax.add_patch(b_rect)

        # Columnas y registro de posiciones Y exactas
        row_y_map = {}
        curr_y = y_top - header_h - 0.20
        for i, (tag, col_name, col_type) in enumerate(cols):
            font_weight = 'bold' if tag == 'PK' else 'normal'
            tag_str = f"[{tag}]" if tag else "    "
            # Izquierda: Tag + Nombre Columna
            ax.text(x + 0.14, curr_y, f"{tag_str} {col_name}", ha='left', va='center',
                    color='#000000', fontsize=7.8, fontweight=font_weight, family='monospace', zorder=4)
            # Derecha: Tipo SQL
            ax.text(x + w - 0.14, curr_y, col_type, ha='right', va='center',
                    color='#000000', fontsize=7.8, fontweight=font_weight, family='monospace', zorder=4)
            row_y_map[i] = curr_y
            curr_y -= row_h

        return {
            'x_left': x,
            'x_right': x + w,
            'x_center': x + w/2,
            'y_top': y_top,
            'y_bottom': y_bot,
            'width': w,
            'height': total_h,
            'rows': row_y_map
        }

    # -------------------------------------------------------------
    # FILA 1: CATÁLOGO (Y_TOP = 13.35)
    # -------------------------------------------------------------
    cat = draw_table(0.8, 13.35, 5.0, "categories", [
        ("PK", "id", "int"),                  # row 0
        ("UK", "name", "varchar(60)"),         # row 1
        ("", "description", "text"),          # row 2
        ("", "created_at", "timestamp")       # row 3
    ])

    prod = draw_table(9.5, 13.35, 5.0, "products", [
        ("PK", "id", "int"),                  # row 0
        ("FK", "category_id", "int"),         # row 1
        ("", "name", "varchar(120)"),         # row 2
        ("", "description", "text"),          # row 3
        ("", "base_price", "decimal(10,2)"),  # row 4
        ("", "image_url", "varchar(255)"),    # row 5
        ("", "is_active", "boolean"),         # row 6
        ("", "created_at", "timestamp")       # row 7
    ])

    var = draw_table(18.2, 13.35, 5.0, "product_variants", [
        ("PK", "id", "int"),                  # row 0
        ("FK", "product_id", "int"),          # row 1
        ("", "size", "varchar(10)"),          # row 2
        ("", "color", "varchar(50)"),         # row 3
        ("UK", "sku", "varchar(50)"),         # row 4
        ("", "stock", "int"),                 # row 5
        ("", "alert_threshold", "int"),       # row 6
        ("", "created_at", "timestamp")       # row 7
    ])

    # -------------------------------------------------------------
    # FILA 2: VENTAS (Y_TOP = 8.55)
    # -------------------------------------------------------------
    cli = draw_table(0.8, 8.55, 5.0, "clients", [
        ("PK", "id", "int"),                  # row 0
        ("", "full_name", "varchar(120)"),    # row 1
        ("", "phone", "varchar(20)"),         # row 2
        ("", "address", "text"),              # row 3
        ("", "district", "varchar(80)"),      # row 4
        ("", "reference", "text"),            # row 5
        ("", "created_at", "timestamp")       # row 6
    ])

    ped = draw_table(9.5, 8.55, 5.0, "orders", [
        ("PK", "id", "int"),                  # row 0
        ("UK", "order_number", "varchar(30)"),# row 1
        ("FK", "client_id", "int"),           # row 2
        ("FK", "user_id", "int"),             # row 3
        ("", "status", "varchar(30)"),        # row 4
        ("", "payment_method", "varchar(30)"),# row 5
        ("", "subtotal", "decimal(10,2)"),    # row 6
        ("", "shipping_cost", "decimal(10,2)"),# row 7
        ("", "total_amount", "decimal(10,2)"),# row 8
        ("", "created_at", "timestamp")       # row 9
    ])

    item = draw_table(18.2, 8.55, 5.0, "order_items", [
        ("PK", "id", "int"),                  # row 0
        ("FK", "order_id", "int [CASCADE]"),  # row 1
        ("FK", "variant_id", "int"),          # row 2
        ("", "quantity", "int"),              # row 3
        ("", "unit_price", "decimal(10,2)"),  # row 4
        ("", "subtotal", "decimal(10,2)")     # row 5
    ])

    # -------------------------------------------------------------
    # FILA 3: USUARIOS Y AUDITORÍA (Y_TOP = 3.75)
    # -------------------------------------------------------------
    usr = draw_table(0.8, 3.75, 5.0, "users", [
        ("PK", "id", "int"),                  # row 0
        ("", "name", "varchar(100)"),         # row 1
        ("UK", "email", "varchar(150)"),      # row 2
        ("", "password_hash", "varchar(255)"),# row 3
        ("", "role", "varchar(20)"),          # row 4
        ("", "created_at", "timestamp")       # row 5
    ])

    hist = draw_table(9.5, 3.75, 5.0, "order_status_history", [
        ("PK", "id", "int"),                  # row 0
        ("FK", "order_id", "int [CASCADE]"),  # row 1
        ("FK", "user_id", "int"),             # row 2
        ("", "previous_status", "varchar(30)"),# row 3
        ("", "new_status", "varchar(30)"),    # row 4
        ("", "changed_at", "timestamp"),      # row 5
        ("", "comments", "text")              # row 6
    ])

    # =============================================================
    # CONEXIONES FÍSICAS DDL (PK -> FK)
    # =============================================================

    # 1. categories.id (PK, row 0) -> products.category_id (FK, row 1)
    draw_orthogonal_relation_h(ax,
                               x_start=cat['x_right'], y_start=cat['rows'][0],
                               x_mid=7.65,
                               y_end=prod['rows'][1], x_end=prod['x_left'])

    # 2. products.id (PK, row 0) -> product_variants.product_id (FK, row 1)
    draw_orthogonal_relation_h(ax,
                               x_start=prod['x_right'], y_start=prod['rows'][0],
                               x_mid=16.35,
                               y_end=var['rows'][1], x_end=var['x_left'])

    # 3. product_variants (1) -> order_items (N) [Vertical directo]
    draw_orthogonal_relation_v(ax,
                               x_start=var['x_center'], y_start=var['y_bottom'],
                               y_mid=item['y_top'] + 0.45,
                               x_end=item['x_center'], y_end=item['y_top'])

    # 4. clients.id (PK, row 0) -> orders.client_id (FK, row 2)
    draw_orthogonal_relation_h(ax,
                               x_start=cli['x_right'], y_start=cli['rows'][0],
                               x_mid=7.20,
                               y_end=ped['rows'][2], x_end=ped['x_left'])

    # 5. orders.id (PK, row 0) -> order_items.order_id (FK, row 1)
    draw_orthogonal_relation_h(ax,
                               x_start=ped['x_right'], y_start=ped['rows'][0],
                               x_mid=16.35,
                               y_end=item['rows'][1], x_end=item['x_left'])

    # 6. orders (1) -> order_status_history (N) [Vertical directo]
    draw_orthogonal_relation_v(ax,
                               x_start=ped['x_center'], y_start=ped['y_bottom'],
                               y_mid=hist['y_top'] + 0.45,
                               x_end=hist['x_center'], y_end=hist['y_top'])

    # 7. users.id (PK, row 0) -> order_status_history.user_id (FK, row 2)
    draw_orthogonal_relation_h(ax,
                               x_start=usr['x_right'], y_start=usr['rows'][0] - 0.08,
                               x_mid=7.65,
                               y_end=hist['rows'][2], x_end=hist['x_left'])

    # 8. users.id (PK, row 0) -> orders.user_id (FK, row 3)
    draw_orthogonal_relation_h(ax,
                               x_start=usr['x_right'], y_start=usr['rows'][0] + 0.08,
                               x_mid=8.10,
                               y_end=ped['rows'][3], x_end=ped['x_left'])

    # Leyenda inferior
    ax.plot([0.5, 23.5], [1.00, 1.00], color='#000000', linewidth=1.2)
    ax.text(12.0, 0.72, "CONVENCIONES FÍSICAS RDBMS:  [PK] PRIMARY KEY    [FK] FOREIGN KEY    [UK] UNIQUE KEY    ON DELETE CASCADE en order_items y order_status_history",
            ha='center', va='center', color='#000000', fontsize=9.0, family='monospace', fontweight='bold')

    plt.savefig('diagrams/13_Modelo_Fisico_BD.png', dpi=300, facecolor='#FFFFFF', bbox_inches='tight')
    plt.close()
    print("[OK] Modelo Físico guardado: diagrams/13_Modelo_Fisico_BD.png")


if __name__ == '__main__':
    generate_logical_model()
    generate_physical_model()
