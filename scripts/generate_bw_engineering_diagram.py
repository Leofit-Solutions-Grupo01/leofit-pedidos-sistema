# -*- coding: utf-8 -*-
"""
@file generate_bw_engineering_diagram.py
@description Generador de Diagrama Técnico en Blanco y Negro Puro (Estilo ERwin / CAD Clásico)
             Base de Datos para Control de Inventario y Ventas (Modelo Lógico y Físico)
@project LeoFit Pedidos Sistema (UTP - Curso Integrador II)
@author Grupo 01 - UTP
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import Rectangle, Circle, Polygon
import os

def create_bw_diagram():
    print("Generando diagrams/Diagrama_Inventario_Ventas_BW.png...")
    
    # Lienzo de alta resolución (300 DPI)
    fig, ax = plt.subplots(figsize=(16, 14), dpi=300)
    fig.patch.set_facecolor('#FFFFFF')
    ax.set_facecolor('#FFFFFF')
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 14)
    ax.axis('off')

    # Línea divisoria o marco general
    border = Rectangle((0.4, 0.4), 15.2, 13.2, fill=False, edgecolor='#000000', linewidth=1.5)
    ax.add_patch(border)
    
    # Separador horizontal entre sección superior e inferior
    ax.plot([0.4, 15.6], [7.0, 7.0], color='#000000', linestyle='--', linewidth=1.0)

    # -------------------------------------------------------------
    # FUNCIONES AUXILIARES PARA DIBUJAR TABLAS Y PATA DE GALLO
    # -------------------------------------------------------------
    
    def draw_table(x, y, w, h, table_name, rows, is_physical=True):
        # Header (Negro sólido, texto blanco)
        header_h = 0.55
        h_rect = Rectangle((x, y + h - header_h), w, header_h, facecolor='#000000', edgecolor='#000000', linewidth=1.2)
        ax.add_patch(h_rect)
        ax.text(x + w/2, y + h - header_h/2, table_name, ha='center', va='center',
                color='#FFFFFF', fontsize=10, fontweight='bold', family='monospace')

        # Body (Blanco con borde negro)
        body_rect = Rectangle((x, y), w, h - header_h, facecolor='#FFFFFF', edgecolor='#000000', linewidth=1.2)
        ax.add_patch(body_rect)

        # Divisor de clave primaria si hay
        pk_count = sum(1 for r in rows if '(PK)' in r[0] or r[0].startswith('PK'))
        
        curr_y = y + h - header_h - 0.35
        for i, row in enumerate(rows):
            left_txt = row[0]
            right_txt = row[1] if len(row) > 1 else ""
            
            # Formato de texto
            is_pk = '(PK)' in left_txt or '(PK)' in right_txt
            is_fk = '(FK)' in left_txt or '(FK)' in right_txt
            
            font_weight = 'bold' if is_pk else 'normal'
            
            if is_physical:
                # Columna izquierda: nombre del campo
                ax.text(x + 0.15, curr_y, left_txt, ha='left', va='center',
                        color='#000000', fontsize=8.5, fontweight=font_weight, family='monospace')
                # Columna derecha: tipo de dato y restricciones
                if right_txt:
                    ax.text(x + w - 0.15, curr_y, right_txt, ha='right', va='center',
                            color='#000000', fontsize=8.5, fontweight=font_weight, family='monospace')
            else:
                # Modelo lógico
                full_text = f"{left_txt}  {right_txt}".strip()
                ax.text(x + 0.15, curr_y, full_text, ha='left', va='center',
                        color='#000000', fontsize=8.5, fontweight=font_weight, family='monospace')
                
            curr_y -= 0.38

    def draw_crows_foot_h(x1, x2, y, orientation='left_to_right'):
        """
        Dibuja una línea horizontal con notación Crow's Foot entre x1 y x2 a la altura y.
        orientation='left_to_right': Lado 1 en x1, Lado N en x2.
        orientation='right_to_left': Lado 1 en x2, Lado N en x1.
        """
        ax.plot([x1, x2], [y, y], color='#000000', linewidth=1.3)
        
        if orientation == 'left_to_right':
            # Lado 1 en x1 (dos barras verticales)
            ax.plot([x1 + 0.14, x1 + 0.14], [y - 0.16, y + 0.16], color='#000000', linewidth=1.3)
            ax.plot([x1 + 0.26, x1 + 0.26], [y - 0.16, y + 0.16], color='#000000', linewidth=1.3)
            
            # Lado N en x2 (Círculo de opcionalidad + Tridente hacia la derecha)
            circle = Circle((x2 - 0.42, y), 0.08, facecolor='#FFFFFF', edgecolor='#000000', linewidth=1.2, zorder=5)
            ax.add_patch(circle)
            ax.plot([x2 - 0.28, x2], [y, y + 0.18], color='#000000', linewidth=1.3)
            ax.plot([x2 - 0.28, x2], [y, y - 0.18], color='#000000', linewidth=1.3)
            
        elif orientation == 'right_to_left':
            # Lado 1 en x2 (dos barras verticales)
            ax.plot([x2 - 0.14, x2 - 0.14], [y - 0.16, y + 0.16], color='#000000', linewidth=1.3)
            ax.plot([x2 - 0.26, x2 - 0.26], [y - 0.16, y + 0.16], color='#000000', linewidth=1.3)
            
            # Lado N en x1 (Círculo de opcionalidad + Tridente hacia la izquierda)
            circle = Circle((x1 + 0.42, y), 0.08, facecolor='#FFFFFF', edgecolor='#000000', linewidth=1.2, zorder=5)
            ax.add_patch(circle)
            ax.plot([x1 + 0.28, x1], [y, y + 0.18], color='#000000', linewidth=1.3)
            ax.plot([x1 + 0.28, x1], [y, y - 0.18], color='#000000', linewidth=1.3)

    def draw_crows_foot_v(y_top, y_bottom, x):
        """
        Dibuja conexión vertical con Crow's foot: Lado 1 arriba en y_top, Lado N abajo en y_bottom
        """
        ax.plot([x, x], [y_top, y_bottom], color='#000000', linewidth=1.3)
        
        # Lado 1 arriba (dos barras horizontales)
        ax.plot([x - 0.16, x + 0.16], [y_top - 0.14, y_top - 0.14], color='#000000', linewidth=1.3)
        ax.plot([x - 0.16, x + 0.16], [y_top - 0.26, y_top - 0.26], color='#000000', linewidth=1.3)
        
        # Lado N abajo (Círculo de opcionalidad + Tridente hacia abajo)
        circle = Circle((x, y_bottom + 0.42), 0.08, facecolor='#FFFFFF', edgecolor='#000000', linewidth=1.2, zorder=5)
        ax.add_patch(circle)
        ax.plot([x, x - 0.18], [y_bottom + 0.28, y_bottom], color='#000000', linewidth=1.3)
        ax.plot([x, x + 0.18], [y_bottom + 0.28, y_bottom], color='#000000', linewidth=1.3)

    # =============================================================
    # 1. SECCIÓN SUPERIOR: MODELO LÓGICO
    # =============================================================
    ax.text(8.0, 13.2, "BASE DE DATOS PARA CONTROL DE INVENTARIO Y VENTAS (MODELO LOGICO)",
            ha='center', va='center', color='#000000', fontsize=12.5, fontweight='bold', family='monospace')
    
    # Cliente (Lógico - Semántico)
    draw_table(0.8, 10.3, 4.0, 2.2, "Cliente", [
        ("Codigo de cliente", ""),
        ("Nombre del cliente", ""),
        ("Telefono de contacto", "")
    ], is_physical=False)

    # Venta (Lógico - Semántico)
    draw_table(5.8, 10.3, 4.3, 2.2, "Venta", [
        ("Numero de venta", ""),
        ("Codigo de cliente (FK)", ""),
        ("Fecha de la venta", "")
    ], is_physical=False)

    # Detalle de Venta (Lógico - Semántico)
    draw_table(5.8, 7.3, 4.3, 2.4, "Detalle de Venta", [
        ("Codigo de detalle", ""),
        ("Numero de venta (FK)", ""),
        ("Codigo de producto (FK)", ""),
        ("Cantidad vendida", "")
    ], is_physical=False)

    # Producto (Lógico - Semántico)
    draw_table(11.0, 7.3, 4.2, 2.4, "Producto", [
        ("Codigo de producto", ""),
        ("Nombre de producto", ""),
        ("Stock disponible", ""),
        ("Precio unitario", "")
    ], is_physical=False)

    # Conexiones Modelo Lógico
    # Cliente (x=4.8) -> Venta (x=5.8) a y=11.3
    draw_crows_foot_h(4.8, 5.8, 11.3, orientation='left_to_right')
    
    # Venta (y=10.3) -> Detalle de Venta (y=9.7) a x=7.95
    draw_crows_foot_v(10.3, 9.7, 7.95)
    
    # Detalle de Venta (x=10.1) <- Producto (x=11.0) a y=8.5
    draw_crows_foot_h(10.1, 11.0, 8.5, orientation='right_to_left')


    # =============================================================
    # 2. SECCIÓN INFERIOR: MODELO FÍSICO
    # =============================================================
    ax.text(8.0, 6.4, "BASE DE DATOS PARA CONTROL DE INVENTARIO Y VENTAS (MODELO FISICO)",
            ha='center', va='center', color='#000000', fontsize=12.5, fontweight='bold', family='monospace')

    # CLIENTE (Fisico)
    draw_table(0.8, 3.8, 4.1, 2.2, "CLIENTE", [
        ("Cod_cli (PK)", "char(6)"),
        ("Nom_cli", "varchar(40)"),
        ("Telf_cli", "varchar(15)")
    ], is_physical=True)

    # VENTA (Fisico)
    draw_table(5.8, 3.8, 4.2, 2.2, "VENTA", [
        ("Id_venta (PK)", "char(6)"),
        ("Cod_cli (FK)", "char(6)"),
        ("Fecha_venta", "datetime")
    ], is_physical=True)

    # DETALLE_VENTA (Fisico)
    draw_table(5.8, 0.8, 4.2, 2.4, "DETALLE_VENTA", [
        ("Id_detalle (PK)", "char(6)"),
        ("Id_venta (FK)", "char(6)"),
        ("Cod_prod (FK)", "char(6)"),
        ("Cantidad", "int")
    ], is_physical=True)

    # PRODUCTO (Fisico)
    draw_table(10.9, 0.8, 4.3, 2.4, "PRODUCTO", [
        ("Cod_prod (PK)", "char(6)"),
        ("Nom_prod", "varchar(30)"),
        ("Stock_prod", "int"),
        ("Precio_prod", "decimal(10,2)")
    ], is_physical=True)

    # Conexiones Modelo Físico
    # CLIENTE (x=4.9) -> VENTA (x=5.8) a y=4.8
    draw_crows_foot_h(4.9, 5.8, 4.8, orientation='left_to_right')
    
    # VENTA (y=3.8) -> DETALLE_VENTA (y=3.2) a x=7.9
    draw_crows_foot_v(3.8, 3.2, 7.9)
    
    # DETALLE_VENTA (x=10.0) <- PRODUCTO (x=10.9) a y=2.0
    draw_crows_foot_h(10.0, 10.9, 2.0, orientation='right_to_left')

    out_path = 'diagrams/Diagrama_Inventario_Ventas_BW.png'
    plt.savefig(out_path, dpi=300, facecolor='#FFFFFF', bbox_inches='tight')
    plt.close()
    print(f"[OK] Generado exitosamente: {out_path}")

if __name__ == '__main__':
    create_bw_diagram()
