# -*- coding: utf-8 -*-
"""
Generador automático de diagramas de ingeniería en alta resolución (300 DPI)
para el proyecto LeoFit usando matplotlib:
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
    
    for ax, t in zip(axes.flatten(), titles):
        ax.set_facecolor('#1E293B')
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 8)
        ax.axis('off')
        
        # Frame
        frame = FancyBboxPatch((0.2, 0.2), 9.6, 7.6, boxstyle="round,pad=0.06,rounding_size=0.1",
                               facecolor='#1E293B', edgecolor='#475569', linewidth=1.5)
        ax.add_patch(frame)
        
        # Header bar
        header = Rectangle((0.2, 7.0), 9.6, 0.8, facecolor='#0F172A', edgecolor='#334155')
        ax.add_patch(header)
        ax.text(5, 7.4, t, ha='center', va='center', color='#F97316', fontsize=11, fontweight='bold')
        
        # Wireframe elements
        if "Login" in t:
            card = Rectangle((3, 2), 4, 4, facecolor='#334155', edgecolor='#94A3B8', linestyle='--')
            ax.add_patch(card)
            ax.text(5, 5.2, "[ LOGO LEOFIT ]", ha='center', color='#94A3B8', fontsize=10)
            ax.add_patch(Rectangle((3.5, 4.0), 3, 0.5, facecolor='#1E293B', edgecolor='#64748B'))
            ax.text(3.7, 4.25, "Usuario / Email", color='#64748B', fontsize=8)
            ax.add_patch(Rectangle((3.5, 3.2), 3, 0.5, facecolor='#1E293B', edgecolor='#64748B'))
            ax.text(3.7, 3.45, "Contraseña", color='#64748B', fontsize=8)
            ax.add_patch(Rectangle((3.5, 2.3), 3, 0.5, facecolor='#F97316', edgecolor='#EA580C'))
            ax.text(5, 2.55, "INGRESAR AL SISTEMA", ha='center', color='#FFFFFF', fontsize=8.5, fontweight='bold')
        elif "Catalogo" in t or "Catálogo" in t:
            ax.add_patch(Rectangle((0.6, 6.2), 8.8, 0.5, facecolor='#334155', edgecolor='#64748B'))
            ax.text(0.8, 6.45, "Buscar prenda por nombre o categoria...", color='#94A3B8', fontsize=8)
            for gx in [0.6, 3.6, 6.6]:
                for gy in [3.3, 0.5]:
                    ax.add_patch(Rectangle((gx, gy), 2.6, 2.5, facecolor='#334155', edgecolor='#64748B', linestyle='--'))
                    ax.add_patch(Rectangle((gx+0.2, gy+0.8), 2.2, 1.5, facecolor='#1E293B'))
                    ax.text(gx+1.3, gy+1.55, "[ FOTO HD ]", ha='center', color='#64748B', fontsize=8)
                    ax.text(gx+0.3, gy+0.5, "Prenda Dry-Fit\nS/ 45.00", color='#F8FAFC', fontsize=7.5)
        elif "Carrito" in t:
            ax.add_patch(Rectangle((0.6, 0.5), 4.5, 6.2, facecolor='#334155', edgecolor='#64748B', linestyle='--'))
            ax.text(0.8, 6.3, "ITEMS EN CARRITO (2)", color='#38BDF8', fontsize=9, fontweight='bold')
            ax.text(0.8, 5.5, "* Camiseta Oversize (M) x 1 -> S/ 65.00\n* Short 2-en-1 (L) x 1 -> S/ 55.00", color='#E2E8F0', fontsize=8, linespacing=1.4)
            ax.text(0.8, 4.4, "------------------------------------", color='#64748B', fontsize=8)
            ax.text(0.8, 3.8, "Subtotal: S/ 120.00\nDelivery: S/ 10.00\nTOTAL: S/ 130.00", color='#38BDF8', fontsize=8.5, fontweight='bold', linespacing=1.3)
            
            ax.add_patch(Rectangle((5.3, 0.5), 4.1, 6.2, facecolor='#334155', edgecolor='#64748B'))
            ax.text(5.5, 6.3, "DATOS DE ENTREGA", color='#F97316', fontsize=9, fontweight='bold')
            ax.add_patch(Rectangle((5.5, 5.3), 3.7, 0.45, facecolor='#1E293B'))
            ax.text(5.7, 5.5, "Nombre: Juan Perez", color='#94A3B8', fontsize=8)
            ax.add_patch(Rectangle((5.5, 4.6), 3.7, 0.45, facecolor='#1E293B'))
            ax.text(5.7, 4.8, "Telefono: 987654321", color='#94A3B8', fontsize=8)
            ax.add_patch(Rectangle((5.5, 3.9), 3.7, 0.45, facecolor='#1E293B'))
            ax.text(5.7, 4.1, "Direccion: Av. Lima 123", color='#94A3B8', fontsize=8)
            ax.add_patch(Rectangle((5.5, 1.0), 3.7, 0.6, facecolor='#10B981'))
            ax.text(7.35, 1.3, "CONFIRMAR PEDIDO", ha='center', color='#FFFFFF', fontsize=9, fontweight='bold')
        elif "Dashboard" in t:
            for kx, kt, kv in [(0.6, "PEDIDOS HOY", "12"), (2.9, "VENTAS (S/)", "1,450.00"), (5.2, "STOCK BAJO", "3"), (7.5, "ENTREGADOS", "9")]:
                ax.add_patch(Rectangle((kx, 5.0), 2.1, 1.6, facecolor='#334155', edgecolor='#38BDF8'))
                ax.text(kx+1.05, 6.2, kt, ha='center', color='#94A3B8', fontsize=7.5, fontweight='bold')
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

def generate_database_erd():
    print("Generando diagrams/12_Modelo_Entidad_Relacion.png...")
    fig, ax = plt.subplots(figsize=(16, 9.5), dpi=300)
    fig.patch.set_facecolor('#0F172A')
    ax.set_facecolor('#0F172A')
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 9.5)
    ax.axis('off')
    
    ax.text(8, 9.1, "MODELO ENTIDAD-RELACIÓN (DER) RELACIONAL - LEOFIT (3FN / BCNF)", 
            ha='center', va='center', color='#F8FAFC', fontsize=16, fontweight='bold')
    ax.text(8, 8.7, "Esquema de 8 Tablas Relacionales Conforme a database/schema.sql y Standard Codd", 
            ha='center', va='center', color='#F97316', fontsize=10.5)
            
    # Structured 4-column layout:
    # Col 1: CATEGORIES (top), PRODUCTS (bottom)
    # Col 2: PRODUCT_VARIANTS (top), ORDER_ITEMS (bottom)
    # Col 3: USERS (top), ORDERS (bottom)
    # Col 4: CLIENTS (top), ORDER_STATUS_HISTORY (bottom)
    tables = [
        # (x, y, w, h, table_name, [attributes])
        (0.5, 5.2, 3.4, 3.0, "CATEGORIES", ["PK id : INT", "   name : VARCHAR(60) (UK)", "   description : TEXT"]),
        (0.5, 0.8, 3.4, 3.8, "PRODUCTS", ["PK id : INT", "FK category_id : INT", "   name : VARCHAR(120)", "   description : TEXT", "   base_price : DECIMAL(10,2)", "   image_url : VARCHAR(255)", "   is_active : BOOLEAN"]),
        
        (4.4, 5.2, 3.5, 3.2, "PRODUCT_VARIANTS", ["PK id : INT", "FK product_id : INT", "   size : ENUM(S,M,L,XL)", "   color : VARCHAR(50)", "   sku : VARCHAR(50) (UK)", "   stock : INT", "   alert_threshold : INT"]),
        (4.4, 0.8, 3.5, 3.8, "ORDER_ITEMS", ["PK id : INT", "FK order_id : INT", "FK variant_id : INT", "   quantity : INT", "   unit_price : DECIMAL(10,2)", "   subtotal : DECIMAL(10,2)"]),
        
        (8.3, 5.2, 3.4, 3.0, "USERS", ["PK id : INT", "   name : VARCHAR(100)", "   email : VARCHAR(150) (UK)", "   password_hash : VARCHAR(255)", "   role : ENUM(ADMIN,OPERATOR)"]),
        (8.3, 0.8, 3.4, 3.8, "ORDERS", ["PK id : INT", "   order_number : VARCHAR(30) (UK)", "FK client_id : INT", "FK user_id : INT", "   status : ENUM(5 ESTADOS)", "   subtotal : DECIMAL(10,2)", "   shipping_cost : DECIMAL(10,2)", "   total_amount : DECIMAL(10,2)"]),
        
        (12.1, 5.2, 3.4, 3.2, "CLIENTS", ["PK id : INT", "   full_name : VARCHAR(120)", "   phone : VARCHAR(20)", "   address : TEXT", "   district : VARCHAR(80)", "   reference : TEXT"]),
        (12.1, 0.8, 3.4, 3.8, "ORDER_STATUS_HISTORY", ["PK id : INT", "FK order_id : INT", "FK user_id : INT", "   previous_status : VARCHAR(30)", "   new_status : VARCHAR(30)", "   changed_at : TIMESTAMP", "   comments : TEXT"])
    ]
    
    for x, y, w, h, t_name, attrs in tables:
        box = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.04,rounding_size=0.08",
                             facecolor='#1E293B', edgecolor='#38BDF8', linewidth=1.3)
        ax.add_patch(box)
        
        # Table Header
        h_box = FancyBboxPatch((x, y + h - 0.45), w, 0.45, boxstyle="round,pad=0.02,rounding_size=0.06",
                               facecolor='#0F172A', edgecolor='#F97316', linewidth=1.0)
        ax.add_patch(h_box)
        ax.text(x + w/2, y + h - 0.22, t_name, ha='center', va='center', color='#F97316', fontsize=9.5, fontweight='bold')
        
        # Attributes
        attr_y = y + h - 0.72
        for a in attrs:
            color = '#38BDF8' if 'PK' in a else ('#F59E0B' if 'FK' in a else '#E2E8F0')
            ax.text(x + 0.12, attr_y, a, ha='left', va='center', color=color, fontsize=7.5, fontfamily='monospace')
            attr_y -= 0.40
            
    # Connector Lines with Stepped/Orthogonal paths & labels
    def draw_orthogonal_rel(points, label="1:N", label_pos=None):
        xs = [p[0] for p in points]
        ys = [p[1] for p in points]
        ax.plot(xs, ys, color='#94A3B8', linestyle='-', linewidth=1.5)
        if label_pos:
            lx, ly = label_pos
        else:
            mid_idx = len(points) // 2
            lx, ly = (points[mid_idx-1][0] + points[mid_idx][0]) / 2, (points[mid_idx-1][1] + points[mid_idx][1]) / 2 + 0.15
        ax.text(lx, ly, label, color='#38BDF8', fontsize=8, ha='center', va='center', fontweight='bold',
                bbox=dict(boxstyle='round,pad=0.15', facecolor='#0F172A', edgecolor='#38BDF8', linewidth=0.8))

    # 1. Categories (Col 1 Top) -> Products (Col 1 Bottom)
    draw_orthogonal_rel([(2.2, 5.2), (2.2, 4.6)], "1:N", (2.2, 4.9))
    
    # 2. Products (Col 1 Bottom) -> Product Variants (Col 2 Top)
    draw_orthogonal_rel([(3.9, 3.5), (4.15, 3.5), (4.15, 6.8), (4.4, 6.8)], "1:N", (4.15, 5.1))
    
    # 3. Product Variants (Col 2 Top) -> Order Items (Col 2 Bottom)
    draw_orthogonal_rel([(6.1, 5.2), (6.1, 4.6)], "1:N", (6.1, 4.9))
    
    # 4. Orders (Col 3 Bottom) -> Order Items (Col 2 Bottom)
    draw_orthogonal_rel([(8.3, 2.7), (7.9, 2.7)], "1:N", (8.1, 2.9))
    
    # 5. Users (Col 3 Top) -> Orders (Col 3 Bottom)
    draw_orthogonal_rel([(10.0, 5.2), (10.0, 4.6)], "1:N", (10.0, 4.9))
    
    # 6. Clients (Col 4 Top) -> Orders (Col 3 Bottom)
    draw_orthogonal_rel([(12.1, 6.8), (11.85, 6.8), (11.85, 4.2), (11.7, 4.2)], "1:N", (11.85, 5.5))
    
    # 7. Orders (Col 3 Bottom) -> Order Status History (Col 4 Bottom)
    draw_orthogonal_rel([(11.7, 2.7), (12.1, 2.7)], "1:N", (11.9, 2.9))
    
    # 8. Users (Col 3 Top) -> Order Status History (Col 4 Bottom)
    draw_orthogonal_rel([(11.7, 5.5), (11.9, 5.5), (11.9, 1.5), (12.1, 1.5)], "1:N", (11.9, 3.5))

    plt.tight_layout()
    plt.savefig('diagrams/12_Modelo_Entidad_Relacion.png', dpi=300, facecolor='#0F172A')
    plt.close()
    print("Guardado: diagrams/12_Modelo_Entidad_Relacion.png")

if __name__ == '__main__':
    generate_lean_canvas()
    generate_cronograma_gantt()
    generate_tablero_kanban()
    generate_wireframes_overview()
    generate_user_flow()
    generate_database_erd()
