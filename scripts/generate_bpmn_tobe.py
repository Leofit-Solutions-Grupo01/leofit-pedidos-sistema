import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

# ==============================================================================
# CONFIGURACIÓN: BPMN 2.0 TO-BE - MÁXIMA LEGIBILIDAD EJECUTIVA
# ==============================================================================
# Proporciones óptimas para visualización panorámica y lectura directa
fig, ax = plt.subplots(figsize=(20, 11.5), dpi=300)
fig.patch.set_facecolor('#FFFFFF')
ax.set_facecolor('#FFFFFF')
ax.set_xlim(0, 200)
ax.set_ylim(0, 115)
ax.axis('off')

# Paleta Cromática Minimalista de Alto Contraste
C_PRIMARY = '#0F172A'       # Slate 900
C_HEADER_BG = '#1E293B'     # Slate 800
C_LANE_TXT = '#FFFFFF'
C_BOX_BG = '#FFFFFF'
C_BOX_BORDER = '#475569'    # Slate 600
C_ACCENT_BLUE = '#0284C7'   # Sky 600
C_ACCENT_GREEN = '#059669'  # Emerald 600
C_ACCENT_AMBER = '#D97706'  # Amber 600
C_ACCENT_RED = '#DC2626'    # Red 600
C_TEXT_MAIN = '#0F172A'
C_TEXT_SUB = '#334155'      # Slate 700
C_GRID_LINE = '#CBD5E1'
C_FLOW_LINE = '#0F172A'
C_FLOW_DATA = '#0284C7'

# ==============================================================================
# 1. ENCABEZADO Y TARJETAS DE KPIS EJECUTIVAS
# ==============================================================================
# Título Principal
ax.text(5, 110, "LEOFIT INDUMENTARIA DEPORTIVA — MODELO TO-BE", 
        fontsize=20, fontweight='bold', color=C_PRIMARY, va='top', fontfamily='sans-serif')
ax.text(5, 105.5, "Diagrama BPMN 2.0 Rediseñado: Automatización Transaccional, Sincronización de Stock y Despacho en Tiempo Real", 
        fontsize=11.0, fontweight='medium', color='#475569', va='top', fontfamily='sans-serif')

# Función para Tarjetas KPI estilo Dashboard Ejecutivo
def draw_kpi_card(x, y, w, h, title, to_be_val, as_is_val, badge_text, badge_color='#059669', badge_bg='#ECFDF5'):
    card = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.2,rounding_size=1.0", 
                          facecolor='#F8FAFC', edgecolor='#CBD5E1', linewidth=1.4)
    ax.add_patch(card)
    
    # Título superior
    ax.text(x + 2.0, y + h - 1.8, title.upper(), fontsize=8.2, fontweight='bold', color='#64748B', va='top')
    
    # Valor principal TO-BE
    ax.text(x + 2.0, y + 3.8, to_be_val, fontsize=12.0, fontweight='bold', color=C_PRIMARY, va='center')
    
    # Valor anterior AS-IS
    ax.text(x + 2.0, y + 1.6, f"AS-IS: {as_is_val}", fontsize=8.0, color='#64748B', va='center')
    
    # Badge de Impacto (Derecha)
    b_w = len(badge_text) * 0.95 + 3.2
    badge = FancyBboxPatch((x + w - b_w - 1.5, y + h/2 - 1.8), b_w, 3.6, 
                           boxstyle="round,pad=0.1,rounding_size=0.6", facecolor=badge_bg, edgecolor='#A7F3D0', linewidth=1)
    ax.add_patch(badge)
    ax.text(x + w - b_w/2 - 1.5, y + h/2, badge_text, fontsize=8.2, fontweight='bold', color=badge_color, ha='center', va='center')

draw_kpi_card(122, 101.5, 24, 11.5, "Tiempo Ciclo", "≤ 2 min", "25 min", "-92%", badge_color='#059669', badge_bg='#ECFDF5')
draw_kpi_card(148, 101.5, 25, 11.5, "Tasa Errores", "< 0.5%", "18.0%", "-97%", badge_color='#059669', badge_bg='#ECFDF5')
draw_kpi_card(175, 101.5, 23, 11.5, "Capacidad", "80+ ped.", "15 ped.", "+433%", badge_color='#0284C7', badge_bg='#F0F9FF')

# ==============================================================================
# 2. DEFINICIÓN DE CARRILES (SWIMLANES)
# ==============================================================================
lanes = [
    {"name": "CLIENTE\n(PWA Frontend)", "sub": "Autoservicio Omnicanal 24/7", "y_top": 98, "y_bot": 75, "color": '#0F172A'},
    {"name": "MOTOR CORE & DB\n(Transaccional)", "sub": "Validación Atómica y Reglas", "y_top": 75, "y_bot": 52, "color": '#1E293B'},
    {"name": "ADMINISTRADOR\n(Almacén / Picking)", "sub": "Tablero Kanban y Picking", "y_top": 52, "y_bot": 29, "color": '#334155'},
    {"name": "LOGÍSTICA COURIER\n(Última Milla)", "sub": "Despacho y Entrega en Destino", "y_top": 29, "y_bot": 6, "color": '#475569'}
]

lane_header_w = 23
x_start = 5
x_end = 198

for i, l in enumerate(lanes):
    y_h = l["y_top"] - l["y_bot"]
    bg_c = '#FFFFFF' if i % 2 == 0 else '#F8FAFC'
    lane_bg = patches.Rectangle((x_start + lane_header_w, l["y_bot"]), x_end - (x_start + lane_header_w), y_h,
                                facecolor=bg_c, edgecolor=C_GRID_LINE, linewidth=1.3)
    ax.add_patch(lane_bg)
    
    header_box = FancyBboxPatch((x_start, l["y_bot"]), lane_header_w, y_h,
                                boxstyle="square,pad=0", facecolor=l["color"], edgecolor=l["color"])
    ax.add_patch(header_box)
    
    ax.text(x_start + lane_header_w/2, l["y_bot"] + y_h/2 + 2.5, l["name"], 
            color=C_LANE_TXT, fontsize=9.2, fontweight='bold', ha='center', va='center', multialignment='center')
    ax.text(x_start + lane_header_w/2, l["y_bot"] + y_h/2 - 5.5, l["sub"], 
            color='#94A3B8', fontsize=7.6, ha='center', va='center')

# ==============================================================================
# 3. FUNCIONES DE DIBUJO DE NODOS Y ELEMENTOS
# ==============================================================================
def draw_task(x, y, w, h, title, subtitle="", tag=None, border_color=C_BOX_BORDER, bg_color=C_BOX_BG):
    box = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.2,rounding_size=1.2",
                         facecolor=bg_color, edgecolor=border_color, linewidth=1.5)
    ax.add_patch(box)
    
    if tag:
        tag_box = FancyBboxPatch((x + 1.0, y + h - 2.8), 5.8, 2.0, boxstyle="round,pad=0.1,rounding_size=0.5",
                                 facecolor=C_PRIMARY, edgecolor=C_PRIMARY)
        ax.add_patch(tag_box)
        ax.text(x + 3.9, y + h - 1.8, tag, fontsize=7.2, fontweight='bold', color='#FFFFFF', ha='center', va='center')
        
    y_title = y + h/2 + (0.8 if subtitle else 0)
    ax.text(x + w/2, y_title, title, fontsize=8.8, fontweight='bold', color=C_TEXT_MAIN,
            ha='center', va='center', multialignment='center')
    if subtitle:
        ax.text(x + w/2, y + 2.2, subtitle, fontsize=7.5, fontweight='medium', color=C_TEXT_SUB,
                ha='center', va='center', multialignment='center')

def draw_event(x, y, r, label, event_type="start"):
    if event_type == "start":
        c = plt.Circle((x, y), r, facecolor='#ECFDF5', edgecolor=C_ACCENT_GREEN, linewidth=2.2)
        ax.add_patch(c)
        ax.text(x, y, "▶", fontsize=11, color=C_ACCENT_GREEN, ha='center', va='center')
    elif event_type == "end":
        c1 = plt.Circle((x, y), r, facecolor='#FEF2F2', edgecolor='#DC2626', linewidth=2.0)
        c2 = plt.Circle((x, y), r*0.72, facecolor='#DC2626', edgecolor='#DC2626', linewidth=1.2)
        ax.add_patch(c1)
        ax.add_patch(c2)
    ax.text(x, y - r - 2.2, label, fontsize=8.0, fontweight='bold', color=C_PRIMARY, ha='center', va='top')

def draw_gateway(x, y, size, label=""):
    diamond = patches.Polygon([[x, y + size], [x + size, y], [x, y - size], [x - size, y]],
                              facecolor='#FFFBEB', edgecolor=C_ACCENT_AMBER, linewidth=1.8)
    ax.add_patch(diamond)
    ax.text(x, y, "✕", fontsize=12, fontweight='bold', color=C_ACCENT_AMBER, ha='center', va='center')
    if label:
        ax.text(x, y + size + 1.8, label, fontsize=8.2, fontweight='bold', color=C_PRIMARY, ha='center', va='bottom')

def draw_arrow(x1, y1, x2, y2, label="", color=C_FLOW_LINE, style='solid', rad=0.0):
    ls = '--' if style == 'dashed' else '-'
    arrow = FancyArrowPatch((x1, y1), (x2, y2),
                            connectionstyle=f"arc3,rad={rad}",
                            arrowstyle='-|>,head_length=4.5,head_width=3.2',
                            color=color, linewidth=1.5, linestyle=ls)
    ax.add_patch(arrow)
    if label:
        mx, my = (x1 + x2)/2, (y1 + y2)/2
        ax.text(mx, my + 1.1, label, fontsize=7.8, fontweight='bold', color=color, ha='center', va='bottom',
                bbox=dict(boxstyle="square,pad=0.15", facecolor="#FFFFFF", edgecolor="none", alpha=0.95))

def draw_ortho_arrow(points, label="", color=C_FLOW_LINE, style='solid', label_pos=0, label_side='right'):
    ls = '--' if style == 'dashed' else '-'
    for i in range(len(points) - 2):
        p1, p2 = points[i], points[i+1]
        ax.plot([p1[0], p2[0]], [p1[1], p2[1]], color=color, linewidth=1.5, linestyle=ls)
    p_pen, p_last = points[-2], points[-1]
    arrow = FancyArrowPatch(p_pen, p_last,
                            arrowstyle='-|>,head_length=4.5,head_width=3.2',
                            color=color, linewidth=1.5, linestyle=ls)
    ax.add_patch(arrow)
    if label:
        p1, p2 = points[label_pos], points[label_pos+1]
        mx, my = (p1[0] + p2[0])/2, (p1[1] + p2[1])/2
        if p1[0] == p2[0]:
            x_offset = 1.0 if label_side == 'right' else -1.0
            ha_align = 'left' if label_side == 'right' else 'right'
            ax.text(mx + x_offset, my, label, fontsize=7.8, fontweight='bold', color=color, 
                    ha=ha_align, va='center',
                    bbox=dict(boxstyle="square,pad=0.15", facecolor="#FFFFFF", edgecolor="none", alpha=0.95))
        else:
            ax.text(mx, my + 1.1, label, fontsize=7.8, fontweight='bold', color=color, 
                    ha='center', va='bottom',
                    bbox=dict(boxstyle="square,pad=0.15", facecolor="#FFFFFF", edgecolor="none", alpha=0.95))

# ==============================================================================
# 4. COLOCACIÓN DE ACTIVIDADES
# ==============================================================================

# --- CARRIL 1: CLIENTE (Y: 75 a 98, Centro Y=86.5) ---
draw_event(33, 86.5, 3.2, "Inicio:\nPWA", "start")
draw_task(40, 79.5, 20, 14, "Explorar Catálogo\nInteractivo", "Filtros en vivo", tag="1.1")
draw_task(64, 79.5, 19, 14, "Configurar Carrito\nde Compras", "Cantidades y talla", tag="1.2")
draw_task(87, 79.5, 19, 14, "Completar Datos\ny Checkout", "Destino y Yape/Plin", tag="1.3")
draw_task(110, 79.5, 19, 14, "Confirmar y\nEmitir Orden", "Genera orden digital", tag="1.4")
draw_task(153, 79.5, 20, 14, "Monitoreo en Vivo\nde Tracking", "Consulta con ORD-ID", tag="1.5", border_color=C_ACCENT_BLUE)
draw_task(177, 79.5, 17, 14, "Recepción\nConforme", "Prendas recibidas", tag="1.6")
draw_event(197, 86.5, 3.0, "Fin del\nProceso", "end")

# --- CARRIL 2: MOTOR TRANSACCIONAL & DB (Y: 52 a 75, Centro Y=63.5) ---
draw_task(40, 56.5, 20, 14, "Sincronización\nde Inventario", "Consulta instantánea BD", tag="2.1", bg_color='#F0FDF4', border_color=C_ACCENT_GREEN)
draw_task(87, 56.5, 19, 14, "Cálculo Flete\ny Total Final", "Liquidación zonal", tag="2.2", bg_color='#F0F9FF', border_color=C_ACCENT_BLUE)
draw_gateway(119.5, 63.5, 4.2, "¿Stock Válido?")
draw_task(130, 56.5, 20, 14, "Reserva Atómica &\nGenera Orden", "Asigna ORD-XXXX", tag="2.3", bg_color='#F0F9FF', border_color=C_ACCENT_BLUE)

# --- CARRIL 3: ADMINISTRADOR & ALMACÉN (Y: 29 a 52, Centro Y=40.5) ---
draw_task(130, 33.5, 20, 14, "Recepción en Panel\nTablero Kanban", "Alerta push de pedido", tag="3.1")
draw_task(153, 33.5, 20, 14, "Picking & Packing\nDigital Asistido", "Validación y empaque", tag="3.2")

# --- CARRIL 4: LOGÍSTICA COURIER (Y: 6 a 29, Centro Y=17.5) ---
draw_task(153, 10.5, 20, 14, "Rotulado y Despacho\na Motorizado", "Hoja de ruta digital", tag="4.1")
draw_task(177, 10.5, 17, 14, "Distribución y\nEntrega Cliente", "Notificación final", tag="4.2")

# ==============================================================================
# 5. CONECTORES Y FLUJOS LÓGICOS
# ==============================================================================
# 1. Start -> 1.1 Catálogo
draw_arrow(36.2, 86.5, 40, 86.5)

# 2. Catálogo <-> Sincronía Stock BD
draw_ortho_arrow([(46.5, 79.5), (46.5, 70.5)], label="Consulta", color=C_ACCENT_GREEN, style='dashed', label_side='left')
draw_ortho_arrow([(53.5, 70.5), (53.5, 79.5)], label="Stock OK", color=C_ACCENT_GREEN, label_side='right')

# 3. 1.1 Catálogo -> 1.2 Carrito
draw_arrow(60, 86.5, 64, 86.5)

# 4. 1.2 Carrito -> 1.3 Checkout
draw_arrow(83, 86.5, 87, 86.5)

# 5. 1.3 Checkout <-> Cálculo Flete
draw_ortho_arrow([(92.5, 79.5), (92.5, 70.5)], label="Zona", color=C_ACCENT_BLUE, label_side='left')
draw_ortho_arrow([(100.5, 70.5), (100.5, 79.5)], label="Total", color=C_ACCENT_BLUE, label_side='right')

# 6. 1.3 Checkout -> 1.4 Emitir Orden
draw_arrow(106, 86.5, 110, 86.5)

# 7. 1.4 Emitir Orden -> Gateway Validación Stock
draw_ortho_arrow([(119.5, 79.5), (119.5, 67.7)], label="Validar", label_side='right')

# 8. Gateway -> [NO] Quiebre de Stock
draw_ortho_arrow([(119.5, 59.3), (119.5, 54.5), (73.5, 54.5), (73.5, 79.5)], 
                 label="[No] Quiebre Stock", color=C_ACCENT_RED, style='dashed', label_pos=1)

# 9. Gateway -> [SÍ] Conforme
draw_arrow(123.7, 63.5, 130, 63.5, label="[Sí] OK", color=C_ACCENT_GREEN)

# 10. Reserva -> Notificación Panel Kanban Admin
draw_ortho_arrow([(140, 56.5), (140, 47.5)], label="RECIBIDO", color=C_ACCENT_BLUE, label_side='right')

# 11. Confirmación inmediata hacia Tracking Cliente
draw_ortho_arrow([(147, 70.5), (147, 75.0), (153, 79.5)], label="ORD-XXXX", color=C_ACCENT_BLUE, style='dashed', label_side='right')

# 12. 3.1 Kanban -> 3.2 Picking & Packing
draw_arrow(150, 40.5, 153, 40.5)
ax.text(151.5, 43.0, "PREPARACIÓN", fontsize=7.2, fontweight='bold', color=C_ACCENT_AMBER, ha='center')

# 13. Sync Picking en vivo -> Tracking Cliente
draw_ortho_arrow([(163, 47.5), (163, 79.5)], label="Sync en Vivo", color=C_ACCENT_BLUE, style='dashed', label_side='right')

# 14. 3.2 Picking -> 4.1 Despacho Courier
draw_ortho_arrow([(163, 33.5), (163, 24.5)], label="EN CAMINO", color=C_ACCENT_BLUE, label_side='right')

# 15. 4.1 Despacho -> 4.2 Entrega Courier
draw_arrow(173, 17.5, 177, 17.5)

# 16. 4.2 Entrega Courier -> 1.6 Recepción Cliente
draw_ortho_arrow([(185.5, 24.5), (185.5, 79.5)], label="ENTREGADO", color=C_ACCENT_GREEN, label_side='right')

# 17. 1.6 Recepción -> Fin del Proceso
draw_arrow(194, 86.5, 197 - 3.0, 86.5)

# ==============================================================================
# 6. BARRA DE ESTADOS Y LEYENDA TÉCNICA (INFERIOR)
# ==============================================================================
leg_box = FancyBboxPatch((28, 1.5), 170, 4.2, boxstyle="round,pad=0.2,rounding_size=0.6",
                         facecolor='#F8FAFC', edgecolor='#CBD5E1', linewidth=1.2)
ax.add_patch(leg_box)

ax.text(30, 3.6, "ESTADOS:", fontsize=8.5, fontweight='bold', color=C_PRIMARY, va='center')

def draw_status_pill(x, y, text, bg, fg):
    p = FancyBboxPatch((x, y-1.1), 16, 2.2, boxstyle="round,pad=0.1,rounding_size=0.6", facecolor=bg, edgecolor=bg)
    ax.add_patch(p)
    ax.text(x + 8, y, text, fontsize=7.6, fontweight='bold', color=fg, ha='center', va='center')

draw_status_pill(62, 3.6, "1. RECIBIDO", "#E0F2FE", "#0369A1")
draw_status_pill(80, 3.6, "2. EN PREPARACIÓN", "#FEF3C7", "#92400E")
draw_status_pill(98, 3.6, "3. EN CAMINO", "#EDE9FE", "#6D28D9")
draw_status_pill(116, 3.6, "4. ENTREGADO", "#D1FAE5", "#065F46")

ax.text(138, 3.6, "LÍNEAS:", fontsize=8.5, fontweight='bold', color=C_PRIMARY, va='center')
ax.plot([148, 154], [3.6, 3.6], color=C_FLOW_LINE, linewidth=1.5)
ax.text(156, 3.6, "Flujo Secuencial", fontsize=7.8, color=C_TEXT_SUB, va='center')

ax.plot([174, 180], [3.6, 3.6], color=C_FLOW_DATA, linewidth=1.5, linestyle='--')
ax.text(182, 3.6, "WebSocket / API", fontsize=7.8, color=C_TEXT_SUB, va='center')

# Guardar figura
output_path = r'c:\Users\Loayza\Downloads\leofit-pedidos-sistema\diagrams\01_BPMN_TO-BE.png'
plt.tight_layout()
plt.savefig(output_path, format='png', dpi=300, bbox_inches='tight', pad_inches=0.15)
plt.close()
print("Diagrama TO-BE de Alta Legibilidad generado exitosamente en:", output_path)
