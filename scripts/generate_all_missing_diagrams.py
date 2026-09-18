# -*- coding: utf-8 -*-
"""
@file generate_all_missing_diagrams.py
@description Generador automático de diagramas de ingeniería en alta resolución (300 DPI) para LeoFit
@project LeoFit Pedidos Sistema (UTP - Curso Integrador II)
@author Lady Luz Loayza Rodriguez (@LadyyLuz) <168585420+luzylay@users.noreply.github.com>
@copyright (c) 2026 Grupo 01 - UTP. All rights reserved.
1. 06_Lean_Canvas.png
2. 07_Cronograma_Gantt.png
3. 08_Tablero_Kanban.png
4. 09_Wireframes_Baja_Fidelidad.png
5. 10_User_Flow_Navegacion.png
6. 12_Modelo_Entidad_Relacion.png
"""

import os
import textwrap
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, Rectangle

os.makedirs('diagrams', exist_ok=True)

def generate_lean_canvas():
    print("Generando diagrams/06_Lean_Canvas.png...")
    fig, ax = plt.subplots(figsize=(16, 10), dpi=300)
    fig.patch.set_facecolor('#0F172A') # Slate 900
    ax.set_facecolor('#0F172A')
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 7)
    ax.axis('off')
    
    # Title
    ax.text(5, 6.6, "LEAN CANVAS - MODELO DE NEGOCIO LEOFIT", 
            ha='center', va='center', color='#F8FAFC', fontsize=18, fontweight='bold', fontfamily='sans-serif')
    ax.text(5, 6.3, "Sistema Web PWA de Gestión y Toma de Pedidos Multicanal | Curso Integrador II - UTP Grupo 01", 
            ha='center', va='center', color='#F97316', fontsize=11, fontfamily='sans-serif')
    
    # Definición de los 9 bloques (x, y, w, h, title, [lines])
    blocks = [
        # Columna 1
        (0.2, 2.2, 1.85, 3.8, "1. PROBLEMA", 
         ["Gestion manual y reactiva", "por WhatsApp.", "", "Descoordinacion de stock", "real en almacen.", "", "Tiempos excesivos de", "atencion (25 min).", "", "Alternativas:", "Libreta fisica, chats, llamadas."]),
        # Columna 2 Arriba
        (2.15, 4.15, 1.85, 1.85, "4. SOLUCIÓN", 
         ["Catalogo interactivo PWA", "con fotos HD.", "Carrito reactivo con", "calculo automatico.", "Trazabilidad de 5 estados."]),
        # Columna 2 Abajo
        (2.15, 2.2, 1.85, 1.85, "8. MÉTRICAS CLAVE", 
         ["Ciclo de pedido: <= 3 min.", "Tasa conversion: +35%.", "Error despacho: < 1%.", "Uptime PWA: >= 99.5%."]),
        # Columna 3
        (4.1, 2.2, 1.8, 3.8, "3. PROPUESTA VALOR", 
         ["Plataforma Web PWA", "ultraligera que permite", "al cliente armar su pedido", "deportivo en 2 minutos con", "stock en tiempo real.", "", "Brinda al administrador", "control centralizado y", "despacho inmediato."]),
        # Columna 4 Arriba
        (6.0, 4.15, 1.85, 1.85, "9. VENTAJA INJUSTA", 
         ["Trato directo del fundador.", "PWA ultrarrapida (<1s).", "Integracion con pagos", "locales (Yape/Plin)."]),
        # Columna 4 Abajo
        (6.0, 2.2, 1.85, 1.85, "5. CANALES", 
         ["PWA Web responsive.", "Resumen orden via", "WhatsApp API.", "Panel web de administracion."]),
        # Columna 5
        (7.95, 2.2, 1.85, 3.8, "2. SEGMENTO CLIENTES", 
         ["Publico Objetivo:", "18-45 anos fitness en", "Lima Metropolitana.", "", "Early Adopters:", "Compradores habituales.", "", "Administrador:", "Dueño operador LeoFit."]),
        # Fila Inferior 1
        (0.2, 0.3, 4.75, 1.75, "7. ESTRUCTURA DE COSTOS", 
         ["Desarrollo y mantenimiento de software.", "Infraestructura Cloud / Edge CDN (GitHub Pages / Vercel).", "Adquisicion de inventario textil deportivo y empaque.", "Logistica motorizada tercerizada."]),
        # Fila Inferior 2
        (5.05, 0.3, 4.75, 1.75, "6. FLUJO DE INGRESOS", 
         ["Venta directa de indumentaria deportiva (margen 35-45%).", "Tarifas de delivery zonificadas por distrito.", "Venta cruzada de accesorios y suplementos en catalogo."])
    ]
    
    for x, y, w, h, title, lines in blocks:
        box = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.08,rounding_size=0.15",
                             facecolor='#1E293B', edgecolor='#334155', linewidth=1.5)
        ax.add_patch(box)
        
        # Header banner
        header_box = FancyBboxPatch((x, y + h - 0.45), w, 0.45, boxstyle="round,pad=0.04,rounding_size=0.08",
                                    facecolor='#0F172A', edgecolor='#F97316', linewidth=1.0)
        ax.add_patch(header_box)
        
        ax.text(x + w/2, y + h - 0.22, title, ha='center', va='center',
                color='#F97316', fontsize=10.5, fontweight='bold')
        
        content_text = "\n".join(lines)
        ax.text(x + 0.12, y + h - 0.65, content_text, ha='left', va='top',
                color='#E2E8F0', fontsize=8.0, linespacing=1.3)
                
    plt.tight_layout()
    plt.savefig('diagrams/06_Lean_Canvas.png', dpi=300, facecolor='#0F172A')
    plt.close()
    print("Guardado: diagrams/06_Lean_Canvas.png")

def generate_cronograma_gantt():
    print("Generando diagrams/07_Cronograma_Gantt.png...")
    fig, ax = plt.subplots(figsize=(15, 8), dpi=300)
    fig.patch.set_facecolor('#0F172A')
    ax.set_facecolor('#1E293B')
    
    tasks = [
        "Fase 1: Mapeo y Levantamiento AS-IS",
        "Fase 2: Project Charter y Requerimientos IEEE 830",
        "Fase 3: Wireframes y Mockups UI/UX",
        "Fase 4: Setup Repositorio, CI/CD y Vitest",
        "Sprint 1: Catalogo Interactivo y Modelos Base",
        "Sprint 2: Carrito Reactivo y Registro de Pedidos",
        "Sprint 3: Panel Admin y Trazabilidad de Estados",
        "Sprint 4: Optimizacion WPO, QA y Despliegue PWA",
        "Fase 5: Entrega y Sustentacion APF1"
    ]
    starts = [1, 3, 5, 6, 7, 9, 11, 13, 15]
    durations = [2, 2, 2, 2, 2, 2, 2, 2, 1]
    colors = ['#38BDF8', '#38BDF8', '#F59E0B', '#F59E0B', '#F97316', '#F97316', '#F97316', '#10B981', '#10B981']
    
    y_pos = range(len(tasks))
    
    for idx, (s, d, c) in enumerate(zip(starts, durations, colors)):
        ax.barh(idx, d, left=s, height=0.55, align='center', color=c, edgecolor='#FFFFFF', linewidth=1, alpha=0.9)
        ax.text(s + d/2, idx, f"{d*7} dias", ha='center', va='center', color='#0F172A', fontweight='bold', fontsize=9)
        
    ax.set_yticks(y_pos)
    ax.set_yticklabels(tasks, color='#F8FAFC', fontsize=10, fontweight='bold')
    ax.invert_yaxis()
    
    ax.set_xlabel("Semanas del Ciclo Academico 2026-II", color='#F8FAFC', fontsize=12, fontweight='bold', labelpad=10)
    ax.set_xlim(0, 17)
    ax.set_xticks(range(1, 17))
    ax.set_xticklabels([f"Sem {i}" for i in range(1, 17)], color='#94A3B8', fontsize=9.5)
    
    ax.grid(axis='x', color='#334155', linestyle='--', alpha=0.7)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color('#475569')
    ax.spines['bottom'].set_color('#475569')
    
    plt.title("CRONOGRAMA DE GANTT Y PLAN DE SPRINTS - PROYECTO LEOFIT (UTP)", 
              color='#F8FAFC', fontsize=14, fontweight='bold', pad=15)
              
    plt.tight_layout()
    plt.savefig('diagrams/07_Cronograma_Gantt.png', dpi=300, facecolor='#0F172A')
    plt.close()
    print("Guardado: diagrams/07_Cronograma_Gantt.png")

def generate_tablero_kanban():
    print("Generando diagrams/08_Tablero_Kanban.png...")
    fig, ax = plt.subplots(figsize=(16, 9), dpi=300)
    fig.patch.set_facecolor('#0F172A')
    ax.set_facecolor('#0F172A')
    ax.set_xlim(0, 15)
    ax.set_ylim(0, 9)
    ax.axis('off')
    
    ax.text(7.5, 8.5, "TABLERO KANBAN / SCRUM - FLUJO DE TRABAJO LEOFIT", 
            ha='center', va='center', color='#F8FAFC', fontsize=16, fontweight='bold')
    ax.text(7.5, 8.1, "Limites de Trabajo en Progreso (WIP Limits) y Transicion de Estados", 
            ha='center', va='center', color='#F97316', fontsize=10.5)
            
    cols = [
        ("BACKLOG", "Sin Limite", 0.4, 3),
        ("TO DO", "Limite: 8", 3.4, 3),
        ("IN PROGRESS", "WIP: 4", 6.4, 3),
        ("CODE REVIEW / QA", "WIP: 3", 9.4, 3),
        ("DONE (DoD)", "Sin Limite", 12.4, 3)
    ]
    
    cards_data = {
        0: ["HU-008: Reporte Ventas Excel", "HU-009: Factura PDF SUNAT", "HU-010: Notif. Push PWA"],
        1: ["HU-006: Editar Producto Admin", "HU-007: Modificar Precios", "T-14: Configurar Sentry"],
        2: ["HU-003: Registrar Pedido PWA", "HU-004: Cambiar Estado Orden"],
        3: ["HU-001: Filtro Catalogo React", "HU-002: Carrito Reactivo"],
        4: ["T-01: Ficha Identificacion", "T-02: BPMN AS-IS v2.0", "T-03: SAD Arquitectura 4+1", "T-04: Suite Vitest 4 Tests"]
    }
    
    for idx, (title, wip, x, w) in enumerate(cols):
        col_box = FancyBboxPatch((x, 0.4), 2.6, 7.3, boxstyle="round,pad=0.06,rounding_size=0.12",
                                 facecolor='#1E293B', edgecolor='#334155', linewidth=1.2)
        ax.add_patch(col_box)
        
        h_box = FancyBboxPatch((x, 7.0), 2.6, 0.65, boxstyle="round,pad=0.04,rounding_size=0.08",
                               facecolor='#0F172A', edgecolor='#38BDF8', linewidth=1.0)
        ax.add_patch(h_box)
        ax.text(x + 1.3, 7.42, title, ha='center', va='center', color='#38BDF8', fontsize=10, fontweight='bold')
        ax.text(x + 1.3, 7.15, wip, ha='center', va='center', color='#94A3B8', fontsize=8)
        
        card_y = 6.1
        for card_text in cards_data.get(idx, []):
            c_box = FancyBboxPatch((x + 0.12, card_y), 2.36, 0.75, boxstyle="round,pad=0.04,rounding_size=0.06",
                                   facecolor='#334155', edgecolor='#475569', linewidth=1.0)
            ax.add_patch(c_box)
            ax.text(x + 0.22, card_y + 0.38, card_text, ha='left', va='center', color='#F8FAFC', fontsize=8, fontweight='bold')
            card_y -= 0.95
            
    plt.tight_layout()
    plt.savefig('diagrams/08_Tablero_Kanban.png', dpi=300, facecolor='#0F172A')
    plt.close()
    print("Guardado: diagrams/08_Tablero_Kanban.png")

def generate_wireframes_overview():
    print("Generando diagrams/09_Wireframes_Baja_Fidelidad.png...")
    fig, axes = plt.subplots(2, 2, figsize=(14, 10), dpi=300)
    fig.patch.set_facecolor('#0F172A')
    
    titles = [
        "1. Wireframe: Autenticacion / Login Admin",
        "2. Wireframe: Catalogo Interactivo PWA",
        "3. Wireframe: Carrito y Registro de Pedido",
        "4. Wireframe: Dashboard y Gestion de Pedidos"
    ]
    
    for idx, (ax, t) in enumerate(zip(axes.flatten(), titles)):
        ax.set_facecolor('#1E293B')
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 8)
        ax.axis('off')
        
        box = FancyBboxPatch((0.2, 0.2), 9.6, 7.6, boxstyle="round,pad=0.05,rounding_size=0.1",
                             facecolor='#1E293B', edgecolor='#38BDF8', linewidth=1.2)
        ax.add_patch(box)
        
        h_box = FancyBboxPatch((0.2, 7.1), 9.6, 0.7, boxstyle="round,pad=0.02,rounding_size=0.05",
                               facecolor='#0F172A', edgecolor='#38BDF8', linewidth=1.0)
        ax.add_patch(h_box)
        ax.text(5, 7.45, t, ha='center', va='center', color='#38BDF8', fontsize=10, fontweight='bold')
        
        if idx == 0:
            ax.add_patch(Rectangle((2.5, 4.5), 5, 1.0, facecolor='#334155', edgecolor='#64748B'))
            ax.text(2.7, 5.0, "Usuario / Email: admin@leofit.pe", color='#94A3B8', fontsize=8.5)
            ax.add_patch(Rectangle((2.5, 3.0), 5, 1.0, facecolor='#334155', edgecolor='#64748B'))
            ax.text(2.7, 3.5, "Contrasena: **********", color='#94A3B8', fontsize=8.5)
            ax.add_patch(Rectangle((3.5, 1.4), 3, 0.9, facecolor='#F97316', edgecolor='#EA580C'))
            ax.text(5, 1.85, "INGRESAR AL SISTEMA", ha='center', va='center', color='#FFFFFF', fontsize=9, fontweight='bold')
        elif idx == 1:
            ax.add_patch(Rectangle((0.6, 5.8), 8.8, 0.9, facecolor='#334155', edgecolor='#64748B'))
            ax.text(0.8, 6.25, "[Buscar polo, short, licra...] | [Filtro Categoria]", color='#94A3B8', fontsize=8)
            for c_i in range(3):
                cx = 0.6 + c_i * 3.0
                ax.add_patch(Rectangle((cx, 1.2), 2.8, 4.2, facecolor='#334155', edgecolor='#475569'))
                ax.text(cx + 1.4, 4.2, "[Foto HD]", ha='center', color='#38BDF8', fontsize=8)
                ax.text(cx + 1.4, 3.2, f"Polo Dry-Fit 0{c_i+1}", ha='center', color='#FFFFFF', fontsize=8, fontweight='bold')
                ax.text(cx + 1.4, 2.5, "S/ 45.00 | Tallas: S,M,L", ha='center', color='#F59E0B', fontsize=7.5)
                ax.text(cx + 1.4, 1.7, "[+ Agregar al Carrito]", ha='center', color='#10B981', fontsize=7.5, fontweight='bold')
        elif idx == 2:
            ax.add_patch(Rectangle((0.6, 4.0), 8.8, 2.7, facecolor='#334155', edgecolor='#64748B'))
            ax.text(0.8, 6.2, "RESUMEN DE COMPRA (2 items) | Subtotal: S/ 90.00", color='#F8FAFC', fontsize=8.5, fontweight='bold')
            ax.text(0.8, 5.2, "- 1x Polo Oversize Black (Talla M) - S/ 45.00\n- 1x Short Deportivo Pro (Talla L) - S/ 45.00", color='#CBD5E1', fontsize=8)
            ax.add_patch(Rectangle((0.6, 0.8), 8.8, 2.8, facecolor='#334155', edgecolor='#64748B'))
            ax.text(0.8, 3.0, "DATOS DE ENVIO Y PAGO:", color='#F97316', fontsize=8.5, fontweight='bold')
            ax.text(0.8, 1.8, "Nombre: Juan Perez | Cel: 987654321\nDireccion: Av. Arequipa 1234, Lince | Pago: Yape", color='#E2E8F0', fontsize=8)
            ax.add_patch(Rectangle((6.2, 1.1), 3.0, 0.7, facecolor='#10B981', edgecolor='#059669'))
            ax.text(7.7, 1.45, "ENVIAR POR WHATSAPP", ha='center', color='#FFFFFF', fontsize=7.5, fontweight='bold')
        elif idx == 3:
            ax.add_patch(Rectangle((0.6, 5.0), 8.8, 1.7, facecolor='#334155', edgecolor='#64748B'))
            kpis = [("Total Pedidos", "24"), ("Pendientes", "5"), ("Ingresos Hoy", "S/ 1,450")]
            for ki, (kt, kv) in enumerate(kpis):
                kx = 0.8 + ki * 2.9
                ax.text(kx+1.05, 6.1, kt, ha='center', color='#38BDF8', fontsize=8)
                ax.text(kx+1.05, 5.5, kv, ha='center', color='#F8FAFC', fontsize=12, fontweight='bold')
            ax.add_patch(Rectangle((0.6, 0.5), 8.8, 4.1, facecolor='#334155', edgecolor='#64748B'))
            ax.text(0.8, 4.2, "BANDEJA DE PEDIDOS EN TIEMPO REAL", color='#F97316', fontsize=8.5, fontweight='bold')
            ax.text(0.8, 3.2, "ORD-2026-001 | Carlos Mendoza | S/ 140.00 | [ EN CAMINO ]\nORD-2026-002 | Valeria Alarcon | S/ 146.00 | [ PREPARACION ]\nORD-2026-003 | Rodrigo Quispe  | S/ 87.00  | [ RECIBIDO ]", color='#E2E8F0', fontsize=8, linespacing=1.4)
            
    plt.tight_layout()
    plt.savefig('diagrams/09_Wireframes_Baja_Fidelidad.png', dpi=300, facecolor='#0F172A')
    plt.close()
    print("Guardado: diagrams/09_Wireframes_Baja_Fidelidad.png")

def generate_user_flow():
    print("Generando diagrams/10_User_Flow_Navegacion.png...")
    fig, ax = plt.subplots(figsize=(15, 8), dpi=300)
    fig.patch.set_facecolor('#0F172A')
    ax.set_facecolor('#0F172A')
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 8)
    ax.axis('off')
    
    ax.text(8, 7.5, "USER FLOW - FLUJO DE NAVEGACIÓN E INTERACCIÓN DEL SISTEMA LEOFIT", 
            ha='center', va='center', color='#F8FAFC', fontsize=15, fontweight='bold')
            
    nodes = [
        (0.6, 4.5, 2.4, 1.4, "1. Acceso a Catalogo", "Cliente entra a la PWA\ny filtra prendas.", '#38BDF8'),
        (3.6, 4.5, 2.4, 1.4, "2. Seleccion & Carrito", "Selecciona talla/color\ny valida stock real.", '#38BDF8'),
        (6.6, 4.5, 2.4, 1.4, "3. Formulario Pedido", "Ingresa direccion, flete\ny metodo de pago.", '#F59E0B'),
        (9.6, 4.5, 2.4, 1.4, "4. Orden Confirmada", "Genera ID unico y\ndescuenta inventario.", '#10B981'),
        (12.6, 4.5, 2.4, 1.4, "5. Resumen WhatsApp", "Formato estructurado\npara mensaje rapido.", '#10B981'),
        
        (6.6, 1.2, 2.4, 1.4, "6. Panel Admin", "Victor visualiza orden\nen Dashboard.", '#F97316'),
        (9.6, 1.2, 2.4, 1.4, "7. Preparacion & Ruta", "Cambia estado a\n'En Preparacion/Camino'.", '#F97316'),
        (12.6, 1.2, 2.4, 1.4, "8. Despacho & Entrega", "Motorizado entrega y\nestado pasa a 'Entregado'.", '#10B981')
    ]
    
    for x, y, w, h, title, desc, color in nodes:
        box = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.06,rounding_size=0.1",
                             facecolor='#1E293B', edgecolor=color, linewidth=1.5)
        ax.add_patch(box)
        ax.text(x + w/2, y + h - 0.35, title, ha='center', va='center', color=color, fontsize=9.5, fontweight='bold')
        ax.text(x + w/2, y + 0.45, desc, ha='center', va='center', color='#E2E8F0', fontsize=8, linespacing=1.2)
        
    # Arrows
    arrow_props = dict(facecolor='#94A3B8', edgecolor='#94A3B8', width=2, headwidth=8, headlength=8)
    ax.annotate('', xy=(3.6, 5.2), xytext=(3.0, 5.2), arrowprops=arrow_props)
    ax.annotate('', xy=(6.6, 5.2), xytext=(6.0, 5.2), arrowprops=arrow_props)
    ax.annotate('', xy=(9.6, 5.2), xytext=(9.0, 5.2), arrowprops=arrow_props)
    ax.annotate('', xy=(12.6, 5.2), xytext=(12.0, 5.2), arrowprops=arrow_props)
    
    ax.annotate('', xy=(7.8, 2.6), xytext=(10.8, 4.5), arrowprops=dict(facecolor='#F97316', edgecolor='#F97316', width=2, headwidth=8))
    ax.annotate('', xy=(9.6, 1.9), xytext=(9.0, 1.9), arrowprops=arrow_props)
    ax.annotate('', xy=(12.6, 1.9), xytext=(12.0, 1.9), arrowprops=arrow_props)
    
    plt.tight_layout()
    plt.savefig('diagrams/10_User_Flow_Navegacion.png', dpi=300, facecolor='#0F172A')
    plt.close()
    print("Guardado: diagrams/10_User_Flow_Navegacion.png")

def generate_database_models():
    print("Delegando generación de Modelos Lógico y Físico CAD B&W...")
    import generate_leofit_db_models_bw
    generate_leofit_db_models_bw.generate_logical_model()
    generate_leofit_db_models_bw.generate_physical_model()

if __name__ == '__main__':
    generate_lean_canvas()
    generate_cronograma_gantt()
    generate_tablero_kanban()
    generate_wireframes_overview()
    generate_user_flow()
    generate_database_models()

