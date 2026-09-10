# -*- coding: utf-8 -*-
"""
Generador automatico de diagramas de ingenieria en alta resolucion (300 DPI)
para el proyecto LeoFit usando matplotlib y PIL:
1. 06_Lean_Canvas.png
2. 07_Cronograma_Gantt.png
3. 08_Tablero_Kanban.png
4. 09_Wireframes_Baja_Fidelidad.png
5. 10_User_Flow_Navegacion.png
6. 12_Modelo_Entidad_Relacion.png
"""

import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, Rectangle, Arrow

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
    
    # Definición de los 9 bloques (x, y, w, h, title, content)
    blocks = [
        # Columna 1
        (0.2, 2.2, 1.85, 3.8, "1. PROBLEMA", 
         "• Gestión manual y reactiva por WhatsApp.\n• Descoordinación de stock real en almacén.\n• Tiempos excesivos de atención (25 min).\n\nAlternativas:\nLibreta física, llamadas, chats."),
        # Columna 2 Arriba
        (2.15, 4.15, 1.85, 1.85, "4. SOLUCIÓN", 
         "• Catálogo interactivo PWA con fotos HD.\n• Carrito reactivo con cálculo automático.\n• Módulo de trazabilidad (5 estados)."),
        # Columna 2 Abajo
        (2.15, 2.2, 1.85, 1.85, "8. MÉTRICAS CLAVE", 
         "• Ciclo de pedido: ≤ 3 min.\n• Tasa conversión: +35%.\n• Error despacho: < 1%.\n• Uptime PWA: ≥ 99.5%."),
        # Columna 3
        (4.1, 2.2, 1.8, 3.8, "3. PROPUESTA VALOR", 
         "Plataforma Web PWA ultraligera que permite al cliente armar su pedido deportivo en 2 minutos con stock en tiempo real y brinda al administrador control y despacho inmediato."),
        # Columna 4 Arriba
        (6.0, 4.15, 1.85, 1.85, "9. VENTAJA INJUSTA", 
         "• Trato directo del fundador.\n• PWA ultrarrápida (<1s).\n• Integración directa con pagos locales (Yape/Plin)."),
        # Columna 4 Abajo
        (6.0, 2.2, 1.85, 1.85, "5. CANALES", 
         "• PWA Web responsive (móvil/PC).\n• Resumen orden vía WhatsApp API.\n• Panel web de administración."),
        # Columna 5
        (7.95, 2.2, 1.85, 3.8, "2. SEGMENTO CLIENTES", 
         "• Público Objetivo: 18-45 años fitness en Lima Metropolitana.\n\n• Early Adopters: Compradores habituales por redes.\n\n• Administrador: Dueño operador de LeoFit."),
        # Fila Inferior 1
        (0.2, 0.3, 4.75, 1.75, "7. ESTRUCTURA DE COSTOS", 
         "• Desarrollo y mantenimiento de software.\n• Infraestructura Cloud / Edge CDN (GitHub Pages / Vercel).\n• Adquisición de inventario deportivo y empaque.\n• Logística motorizada tercerizada."),
        # Fila Inferior 2
        (5.05, 0.3, 4.75, 1.75, "6. FLUJO DE INGRESOS", 
         "• Venta directa de indumentaria deportiva (margen 35-45%).\n• Tarifas de delivery zonificadas.\n• Venta cruzada de suplementos y accesorios en catálogo.")
    ]
    
    for x, y, w, h, title, content in blocks:
        box = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.08,rounding_size=0.15",
                             facecolor='#1E293B', edgecolor='#334155', linewidth=1.5)
        ax.add_patch(box)
        
        # Header banner
        header_box = FancyBboxPatch((x, y + h - 0.45), w, 0.45, boxstyle="round,pad=0.04,rounding_size=0.08",
                                    facecolor='#0F172A', edgecolor='#F97316', linewidth=1.0)
        ax.add_patch(header_box)
        
        ax.text(x + w/2, y + h - 0.22, title, ha='center', va='center',
                color='#F97316', fontsize=10.5, fontweight='bold')
        
        ax.text(x + 0.1, y + h - 0.65, content, ha='left', va='top',
                color='#E2E8F0', fontsize=8.5, linespacing=1.35, wrap=True)
                
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
        "Sprint 1: Catálogo Interactivo y Modelos Base",
        "Sprint 2: Carrito Reactivo y Registro de Pedidos",
        "Sprint 3: Panel Admin y Trazabilidad de Estados",
        "Sprint 4: Optimización WPO, QA y Despliegue PWA",
        "Fase 5: Entrega y Sustentación APF1"
    ]
    starts = [1, 3, 5, 6, 7, 9, 11, 13, 15]
    durations = [2, 2, 2, 2, 2, 2, 2, 2, 1]
    colors = ['#38BDF8', '#38BDF8', '#F59E0B', '#F59E0B', '#F97316', '#F97316', '#F97316', '#10B981', '#10B981']
    
    y_pos = range(len(tasks))
    
    for idx, (s, d, c) in enumerate(zip(starts, durations, colors)):
        ax.barh(idx, d, left=s, height=0.55, align='center', color=c, edgecolor='#FFFFFF', linewidth=1, alpha=0.9)
        ax.text(s + d/2, idx, f"{d*7} días", ha='center', va='center', color='#0F172A', fontweight='bold', fontsize=9)
        
    ax.set_yticks(y_pos)
    ax.set_yticklabels(tasks, color='#F8FAFC', fontsize=10, fontweight='bold')
    ax.invert_yaxis()
    
    ax.set_xlabel("Semanas del Ciclo Académico 2026-II", color='#F8FAFC', fontsize=12, fontweight='bold', labelpad=10)
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
    ax.text(7.5, 8.1, "Límites de Trabajo en Progreso (WIP Limits) y Transición de Estados", 
            ha='center', va='center', color='#F97316', fontsize=10.5)
            
    cols = [
        ("BACKLOG", "Sin Límite", 0.4, 3),
        ("TO DO", "Límite: 8", 3.4, 3),
        ("IN PROGRESS", "WIP: 4", 6.4, 3),
        ("CODE REVIEW / QA", "WIP: 3", 9.4, 3),
        ("DONE (DoD)", "Sin Límite", 12.4, 3)
    ]
    
    cards_data = {
        0: ["HU-008: Reporte Ventas Excel", "HU-009: Factura PDF SUNAT", "HU-010: Notif. Push PWA"],
        1: ["HU-006: Editar Producto Admin", "HU-007: Modificar Precios", "T-14: Configurar Sentry"],
        2: ["HU-003: Registrar Pedido PWA", "HU-004: Cambiar Estado Orden"],
        3: ["HU-001: Filtro Catálogo React", "HU-002: Carrito Reactivo"],
        4: ["T-01: Ficha Identificación", "T-02: BPMN AS-IS v2.0", "T-03: SAD Arquitectura 4+1", "T-04: Suite Vitest 4 Tests"]
    }
    
    for idx, (title, wip, x, w) in enumerate(cols):
        # Column background
        col_box = FancyBboxPatch((x, 0.4), 2.6, 7.3, boxstyle="round,pad=0.06,rounding_size=0.12",
                                 facecolor='#1E293B', edgecolor='#334155', linewidth=1.2)
        ax.add_patch(col_box)
        
        # Column header
        h_box = FancyBboxPatch((x, 7.0), 2.6, 0.65, boxstyle="round,pad=0.04,rounding_size=0.08",
                               facecolor='#0F172A', edgecolor='#38BDF8', linewidth=1.0)
        ax.add_patch(h_box)
        ax.text(x + 1.3, 7.42, title, ha='center', va='center', color='#38BDF8', fontsize=10, fontweight='bold')
        ax.text(x + 1.3, 7.15, wip, ha='center', va='center', color='#94A3B8', fontsize=8)
        
        # Cards
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
        "1. Wireframe: Autenticación / Login Admin",
        "2. Wireframe: Catálogo Interactivo PWA",
        "3. Wireframe: Carrito y Registro de Pedido",
        "4. Wireframe: Dashboard y Gestión de Pedidos"
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
        
        # Wireframe elements (Blueprint sketch)
        if "Login" in t:
            # Login card
            card = Rectangle((3, 2), 4, 4, facecolor='#334155', edgecolor='#94A3B8', linestyle='--')
            ax.add_patch(card)
            ax.text(5, 5.2, "[ LOGO LEOFIT ]", ha='center', color='#94A3B8', fontsize=10)
            ax.add_patch(Rectangle((3.5, 4.0), 3, 0.5, facecolor='#1E293B', edgecolor='#64748B'))
            ax.text(3.7, 4.25, "Usuario / Email", color='#64748B', fontsize=8)
            ax.add_patch(Rectangle((3.5, 3.2), 3, 0.5, facecolor='#1E293B', edgecolor='#64748B'))
            ax.text(3.7, 3.45, "Contraseña", color='#64748B', fontsize=8)
            ax.add_patch(Rectangle((3.5, 2.3), 3, 0.5, facecolor='#F97316', edgecolor='#EA580C'))
            ax.text(5, 2.55, "INGRESAR AL SISTEMA", ha='center', color='#FFFFFF', fontsize=8.5, fontweight='bold')
        elif "Catálogo" in t:
            # Search bar
            ax.add_patch(Rectangle((0.6, 6.2), 8.8, 0.5, facecolor='#334155', edgecolor='#64748B'))
            ax.text(0.8, 6.45, "🔍 Buscar prenda por nombre o categoría...", color='#94A3B8', fontsize=8)
            # Products grid
            for gx in [0.6, 3.6, 6.6]:
                for gy in [3.3, 0.5]:
                    ax.add_patch(Rectangle((gx, gy), 2.6, 2.5, facecolor='#334155', edgecolor='#64748B', linestyle='--'))
                    ax.add_patch(Rectangle((gx+0.2, gy+0.8), 2.2, 1.5, facecolor='#1E293B'))
                    ax.text(gx+1.3, gy+1.55, "[ FOTO HD ]", ha='center', color='#64748B', fontsize=8)
                    ax.text(gx+0.3, gy+0.5, "Prenda Dry-Fit\nS/ 45.00", color='#F8FAFC', fontsize=7.5)
        elif "Carrito" in t:
            # Items list
            ax.add_patch(Rectangle((0.6, 3.5), 4.5, 3.2, facecolor='#334155', edgecolor='#64748B', linestyle='--'))
            ax.text(0.8, 6.3, "ITEMS EN CARRITO (2)", color='#38BDF8', fontsize=9, fontweight='bold')
            ax.text(0.8, 5.4, "• Camiseta Dry-Fit (Talla M) x 1 -> S/ 45.00\n• Short Deportivo (Talla L) x 1 -> S/ 35.00\n------------------------------------\nSubtotal: S/ 80.00 | Delivery: S/ 10.00\nTOTAL: S/ 90.00", color='#E2E8F0', fontsize=8, linespacing=1.3)
            # Form
            ax.add_patch(Rectangle((5.3, 0.5), 4.1, 6.2, facecolor='#334155', edgecolor='#64748B'))
            ax.text(5.5, 6.3, "DATOS DE ENTREGA", color='#F97316', fontsize=9, fontweight='bold')
            ax.add_patch(Rectangle((5.5, 5.3), 3.7, 0.45, facecolor='#1E293B'))
            ax.text(5.7, 5.5, "Nombre: Juan Pérez", color='#94A3B8', fontsize=8)
            ax.add_patch(Rectangle((5.5, 4.6), 3.7, 0.45, facecolor='#1E293B'))
            ax.text(5.7, 4.8, "Teléfono: 987654321", color='#94A3B8', fontsize=8)
            ax.add_patch(Rectangle((5.5, 3.9), 3.7, 0.45, facecolor='#1E293B'))
            ax.text(5.7, 4.1, "Dirección: Av. Lima 123", color='#94A3B8', fontsize=8)
            ax.add_patch(Rectangle((5.5, 1.0), 3.7, 0.6, facecolor='#10B981'))
            ax.text(7.35, 1.3, "CONFIRMAR PEDIDO", ha='center', color='#FFFFFF', fontsize=9, fontweight='bold')
        elif "Dashboard" in t:
            # Metrics cards
            for kx, kt, kv in [(0.6, "PEDIDOS HOY", "12"), (2.9, "VENTAS (S/)", "1,450.00"), (5.2, "STOCK BAJO", "3"), (7.5, "ENTREGADOS", "9")]:
                ax.add_patch(Rectangle((kx, 5.0), 2.1, 1.6, facecolor='#334155', edgecolor='#38BDF8'))
                ax.text(kx+1.05, 6.2, kt, ha='center', color='#94A3B8', fontsize=7.5, fontweight='bold')
                ax.text(kx+1.05, 5.5, kv, ha='center', color='#F8FAFC', fontsize=12, fontweight='bold')
            # Table sketch
            ax.add_patch(Rectangle((0.6, 0.5), 8.8, 4.1, facecolor='#334155', edgecolor='#64748B'))
            ax.text(0.8, 4.2, "BANDEJA DE PEDIDOS EN TIEMPO REAL", color='#F97316', fontsize=8.5, fontweight='bold')
            ax.text(0.8, 3.2, "PED-001 | Juan Pérez   | S/ 90.00 | [ EN CAMINO ]\nPED-002 | María Gómez  | S/ 45.00 | [ RECIBIDO ]\nPED-003 | Carlos Ruiz  | S/ 130.00| [ ENTREGADO ]", color='#E2E8F0', fontsize=8, linespacing=1.4)
            
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
        (0.6, 4.5, 2.4, 1.4, "1. Acceso a Catálogo", "Cliente entra a la PWA\ny filtra prendas.", '#38BDF8'),
        (3.6, 4.5, 2.4, 1.4, "2. Selección & Carrito", "Selecciona talla/color\ny valida stock real.", '#38BDF8'),
        (6.6, 4.5, 2.4, 1.4, "3. Formulario Pedido", "Ingresa dirección, flete\ny método de pago.", '#F59E0B'),
        (9.6, 4.5, 2.4, 1.4, "4. Orden Confirmada", "Genera ID único y\ndescuenta inventario.", '#10B981'),
        (12.6, 4.5, 2.4, 1.4, "5. Resumen WhatsApp", "Formato estructurado\npara mensaje rápido.", '#10B981'),
        
        (6.6, 1.2, 2.4, 1.4, "6. Panel Admin", "Víctor visualiza orden\nen Dashboard.", '#F97316'),
        (9.6, 1.2, 2.4, 1.4, "7. Preparación & Ruta", "Cambia estado a\n'En Preparación/Camino'.", '#F97316'),
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
    # 1 -> 2 -> 3 -> 4 -> 5
    ax.annotate('', xy=(3.6, 5.2), xytext=(3.0, 5.2), arrowprops=arrow_props)
    ax.annotate('', xy=(6.6, 5.2), xytext=(6.0, 5.2), arrowprops=arrow_props)
    ax.annotate('', xy=(9.6, 5.2), xytext=(9.0, 5.2), arrowprops=arrow_props)
    ax.annotate('', xy=(12.6, 5.2), xytext=(12.0, 5.2), arrowprops=arrow_props)
    
    # 4 -> 6 (Down)
    ax.annotate('', xy=(7.8, 2.6), xytext=(10.8, 4.5), arrowprops=dict(facecolor='#F97316', edgecolor='#F97316', width=2, headwidth=8))
    # 6 -> 7 -> 8
    ax.annotate('', xy=(9.6, 1.9), xytext=(9.0, 1.9), arrowprops=arrow_props)
    ax.annotate('', xy=(12.6, 1.9), xytext=(12.0, 1.9), arrowprops=arrow_props)
    
    plt.tight_layout()
    plt.savefig('diagrams/10_User_Flow_Navegacion.png', dpi=300, facecolor='#0F172A')
    plt.close()
    print("Guardado: diagrams/10_User_Flow_Navegacion.png")

def generate_database_erd():
    print("Generando diagrams/12_Modelo_Entidad_Relacion.png...")
    fig, ax = plt.subplots(figsize=(16, 9), dpi=300)
    fig.patch.set_facecolor('#0F172A')
    ax.set_facecolor('#0F172A')
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 9)
    ax.axis('off')
    
    ax.text(8, 8.5, "MODELO ENTIDAD-RELACIÓN (DER) RELACIONAL - LEOFIT (3FN / BCNF)", 
            ha='center', va='center', color='#F8FAFC', fontsize=16, fontweight='bold')
            
    tables = [
        # (x, y, w, h, table_name, [attributes])
        (0.6, 5.0, 3.2, 2.8, "ROLES", ["PK id_rol : INT", "   nombre_rol : VARCHAR(50)"]),
        (0.6, 1.0, 3.2, 3.4, "USUARIOS", ["PK id_usuario : INT", "   nombre : VARCHAR(100)", "   email : VARCHAR(100)", "   password_hash : VARCHAR(255)", "FK id_rol : INT"]),
        (4.4, 5.0, 3.4, 2.8, "CATEGORIAS", ["PK id_categoria : INT", "   nombre_categoria : VARCHAR(100)", "   descripcion : TEXT"]),
        (4.4, 0.8, 3.4, 3.6, "PRODUCTOS", ["PK id_producto : VARCHAR(50)", "   nombre : VARCHAR(150)", "FK id_categoria : INT", "   precio : DECIMAL(10,2)", "   stock : INT", "   talla : VARCHAR(20)", "   color : VARCHAR(50)"]),
        (8.5, 0.8, 3.5, 4.0, "DETALLE_PEDIDOS", ["PK/FK id_pedido : VARCHAR(50)", "PK/FK id_producto : VARCHAR(50)", "      cantidad : INT", "      precio_unitario : DECIMAL(10,2)"]),
        (12.4, 0.8, 3.2, 4.5, "PEDIDOS", ["PK id_pedido : VARCHAR(50)", "   cliente_nombre : VARCHAR(150)", "   cliente_telefono : VARCHAR(20)", "   cliente_direccion : TEXT", "   subtotal : DECIMAL(10,2)", "   costo_envio : DECIMAL(10,2)", "   total : DECIMAL(10,2)", "   metodo_pago : VARCHAR(50)", "FK id_estado : INT"]),
        (12.4, 6.0, 3.2, 2.0, "ESTADOS_PEDIDO", ["PK id_estado : INT", "   nombre_estado : VARCHAR(50)"])
    ]
    
    for x, y, w, h, t_name, attrs in tables:
        box = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.04,rounding_size=0.08",
                             facecolor='#1E293B', edgecolor='#38BDF8', linewidth=1.2)
        ax.add_patch(box)
        
        # Table Header
        h_box = FancyBboxPatch((x, y + h - 0.45), w, 0.45, boxstyle="round,pad=0.02,rounding_size=0.06",
                               facecolor='#0F172A', edgecolor='#F97316', linewidth=1.0)
        ax.add_patch(h_box)
        ax.text(x + w/2, y + h - 0.22, t_name, ha='center', va='center', color='#F97316', fontsize=9.5, fontweight='bold')
        
        # Attributes
        attr_y = y + h - 0.75
        for a in attrs:
            color = '#38BDF8' if 'PK' in a else ('#F59E0B' if 'FK' in a else '#E2E8F0')
            ax.text(x + 0.15, attr_y, a, ha='left', va='center', color=color, fontsize=8, fontfamily='monospace')
            attr_y -= 0.45
            
    # Connector Lines
    def draw_rel(x1, y1, x2, y2, label="1:N"):
        ax.plot([x1, x2], [y1, y2], color='#94A3B8', linestyle='-', linewidth=1.5)
        ax.text((x1+x2)/2, (y1+y2)/2 + 0.15, label, color='#94A3B8', fontsize=7.5, ha='center')
        
    draw_rel(2.2, 5.0, 2.2, 4.4, "1:N") # Roles -> Usuarios
    draw_rel(6.1, 5.0, 6.1, 4.4, "1:N") # Categorias -> Productos
    draw_rel(7.8, 2.5, 8.5, 2.5, "1:N") # Productos -> Detalle_Pedidos
    draw_rel(12.0, 2.5, 12.4, 2.5, "1:N") # Detalle_Pedidos <- Pedidos
    draw_rel(14.0, 6.0, 14.0, 5.3, "1:N") # Estados -> Pedidos
    
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
