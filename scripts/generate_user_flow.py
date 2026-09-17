import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

# ==============================================================================
# CONFIGURACIÓN: USER FLOW UX DE ALTA LEGIBILIDAD (PROPORCIONES CALIBRADAS)
# ==============================================================================
fig, ax = plt.subplots(figsize=(20, 11.5), dpi=300)
fig.patch.set_facecolor('#FFFFFF')
ax.set_facecolor('#FFFFFF')
ax.set_xlim(0, 200)
ax.set_ylim(0, 115)
ax.axis('off')

# Paleta Ejecutiva
C_PRIMARY = '#0F172A'       # Slate 900
C_TEXT_SUB = '#334155'      # Slate 700
C_BORDER = '#94A3B8'
C_SCREEN_HEADER = '#1E293B'  # Slate 800
C_ACCENT_BLUE = '#0284C7'   # Sky 600
C_ACCENT_GREEN = '#059669'  # Emerald 600
C_ACCENT_AMBER = '#D97706'  # Amber 600
C_FLOW = '#0F172A'

# ==============================================================================
# 1. ENCABEZADO Y BADGES
# ==============================================================================
ax.text(6, 110, "LEOFIT PWA — USER FLOW & ARQUITECTURA DE NAVEGACIÓN (TO-BE)", 
        fontsize=20, fontweight='bold', color=C_PRIMARY, va='top', fontfamily='sans-serif')
ax.text(6, 105, "Flujo de Conversión del Cliente, Puntos de Decisión y Estados de Interfaz en la Progressive Web App", 
        fontsize=11.5, color='#475569', va='top', fontfamily='sans-serif')

def draw_ux_badge(x, y, w, h, text, icon="✓"):
    p = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.1,rounding_size=0.8", 
                       facecolor='#F1F5F9', edgecolor='#CBD5E1', linewidth=1.4)
    ax.add_patch(p)
    ax.text(x + 2.5, y + h/2, icon, fontsize=10.0, fontweight='bold', color=C_ACCENT_BLUE, va='center')
    ax.text(x + 5.0, y + h/2, text, fontsize=9.2, fontweight='bold', color=C_PRIMARY, va='center')

draw_ux_badge(120, 103.5, 34, 4.5, "Guest Checkout (Sin Login)")
draw_ux_badge(158, 103.5, 36, 4.5, "Cálculo Reactivo de Flete")

# ==============================================================================
# 2. CONTENEDORES DE ETAPAS (FASE 1, FASE 2, FASE 3)
# ==============================================================================
stages = [
    {"name": "FASE 1: DESCUBRIMIENTO & PRODUCTO", "x1": 5, "x2": 66, "color": '#F8FAFC'},
    {"name": "FASE 2: CONFIGURACIÓN & CHECKOUT", "x1": 69, "x2": 133, "color": '#FFFFFF'},
    {"name": "FASE 3: CONFIRMACIÓN & TRACKING", "x1": 136, "x2": 195, "color": '#F8FAFC'}
]

for st in stages:
    w = st["x2"] - st["x1"]
    bg = FancyBboxPatch((st["x1"], 8), w, 92, boxstyle="round,pad=0.2,rounding_size=1.2", 
                        facecolor=st["color"], edgecolor='#CBD5E1', linewidth=1.5)
    ax.add_patch(bg)
    ax.text(st["x1"] + w/2, 96.5, st["name"], fontsize=10.2, fontweight='bold', color='#475569', ha='center', va='center')

# ==============================================================================
# 3. FUNCIONES DE DIBUJO UI
# ==============================================================================
def draw_screen_card(x, y, w, h, screen_title, action_text, bullets, tag_num=None, border_color=C_BORDER):
    card = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.2,rounding_size=1.2",
                          facecolor='#FFFFFF', edgecolor=border_color, linewidth=1.6)
    ax.add_patch(card)
    
    # Barra de Título
    header = FancyBboxPatch((x, y + h - 4.2), w, 4.2, boxstyle="square,pad=0",
                            facecolor=C_SCREEN_HEADER, edgecolor=C_SCREEN_HEADER)
    ax.add_patch(header)
    
    if tag_num:
        ax.text(x + 1.8, y + h - 2.1, f"P{tag_num}", fontsize=9.2, fontweight='bold', color='#38BDF8', va='center')
        ax.text(x + 6.2, y + h - 2.1, screen_title, fontsize=9.5, fontweight='bold', color='#FFFFFF', va='center')
    else:
        ax.text(x + w/2, y + h - 2.1, screen_title, fontsize=9.5, fontweight='bold', color='#FFFFFF', ha='center', va='center')
        
    ax.text(x + 1.8, y + h - 6.5, f"Acción: {action_text}", fontsize=8.8, fontweight='bold', color=C_ACCENT_BLUE, va='center')
    
    curr_y = y + h - 9.8
    for b in bullets:
        ax.text(x + 1.8, curr_y, f"• {b}", fontsize=8.4, color=C_TEXT_SUB, va='center')
        curr_y -= 2.6

def draw_decision(x, y, size, label, question):
    diamond = patches.Polygon([[x, y + size], [x + size, y], [x, y - size], [x - size, y]],
                              facecolor='#FFFBEB', edgecolor=C_ACCENT_AMBER, linewidth=2.0)
    ax.add_patch(diamond)
    ax.text(x, y, "?", fontsize=13, fontweight='bold', color=C_ACCENT_AMBER, ha='center', va='center')
    ax.text(x, y + size + 1.8, label, fontsize=9.2, fontweight='bold', color=C_PRIMARY, ha='center', va='bottom')
    ax.text(x, y - size - 1.8, question, fontsize=8.2, color='#64748B', ha='center', va='top')

def draw_flow_arrow(x1, y1, x2, y2, label="", color=C_FLOW, style='solid'):
    ls = '--' if style == 'dashed' else '-'
    arrow = FancyArrowPatch((x1, y1), (x2, y2),
                            arrowstyle='-|>,head_length=5.0,head_width=3.6',
                            color=color, linewidth=1.6, linestyle=ls)
    ax.add_patch(arrow)
    if label:
        mx, my = (x1 + x2)/2, (y1 + y2)/2
        ax.text(mx, my + 1.4, label, fontsize=8.8, fontweight='bold', color=color, ha='center', va='bottom',
                bbox=dict(boxstyle="square,pad=0.15", facecolor="#FFFFFF", edgecolor="none", alpha=0.95))

def draw_ortho(points, label="", color=C_FLOW, style='solid', label_pos=0):
    ls = '--' if style == 'dashed' else '-'
    for i in range(len(points) - 2):
        p1, p2 = points[i], points[i+1]
        ax.plot([p1[0], p2[0]], [p1[1], p2[1]], color=color, linewidth=1.6, linestyle=ls)
    p_pen, p_last = points[-2], points[-1]
    arrow = FancyArrowPatch(p_pen, p_last,
                            arrowstyle='-|>,head_length=5.0,head_width=3.6',
                            color=color, linewidth=1.6, linestyle=ls)
    ax.add_patch(arrow)
    if label:
        p1, p2 = points[label_pos], points[label_pos+1]
        mx, my = (p1[0] + p2[0])/2, (p1[1] + p2[1])/2
        ax.text(mx + (0.8 if p1[0]==p2[0] else 0), my + (1.4 if p1[1]==p2[1] else 0), 
                label, fontsize=8.8, fontweight='bold', color=color,
                ha='left' if p1[0]==p2[0] else 'center', va='center' if p1[0]==p2[0] else 'bottom',
                bbox=dict(boxstyle="square,pad=0.15", facecolor="#FFFFFF", edgecolor="none", alpha=0.95))

# ==============================================================================
# 4. COLOCACIÓN DE PANTALLAS
# ==============================================================================

# --- FASE 1: DESCUBRIMIENTO ---
c_start = plt.Circle((10, 72), 3.2, facecolor='#ECFDF5', edgecolor=C_ACCENT_GREEN, linewidth=2.2)
ax.add_patch(c_start)
ax.text(10, 72, "▶", fontsize=11, color=C_ACCENT_GREEN, ha='center', va='center')
ax.text(10, 66.5, "Ingreso a PWA\n(Sin Registro)", fontsize=8.6, fontweight='bold', color=C_PRIMARY, ha='center', va='top')

# P1: Catálogo Digital
draw_screen_card(16, 56, 21, 32, "Catálogo Digital", "Filtra y Explora", 
                 ["Grid de prendas", "Filtros de Talla", "Filtro Categoría", "Stock en Tiempo Real"], 
                 tag_num="1", border_color='#0284C7')

# P2: Ficha de Producto
draw_screen_card(42, 56, 21, 32, "Ficha de Producto", "Selecciona Talla", 
                 ["Galería fotos HD", "Selector dinámico", "Guía de medidas", "CTA: 'Agregar'"], 
                 tag_num="2")

# Validación Stock en UI
draw_decision(52.5, 28, 4.0, "¿Hay Stock?", "Verificación UI")

# --- FASE 2: CONFIGURACIÓN & CHECKOUT ---
# P3: Carrito Drawer
draw_screen_card(72, 56, 21, 32, "Carrito Reactivo", "Revisa Selección", 
                 ["Resumen de prendas", "Ajuste de unidades (+/-)", "Cálculo reactivo total", "CTA: 'Continuar'"], 
                 tag_num="3")

# P4: Datos de Envío
draw_screen_card(97, 56, 21, 32, "Datos de Envío", "Ingresa Destino", 
                 ["Nombre y Teléfono", "Dirección / Referencia", "Selector de Distrito", "Cálculo Flete Zonal"], 
                 tag_num="4")

# P5: Método de Pago
draw_screen_card(108, 14, 21, 31, "Método de Pago", "Elige Yape / Plin", 
                 ["Opciones: Yape / Plin", "QR y Teléfono en pantalla", "Carga comprobante", "CTA: 'Confirmar'"], 
                 tag_num="5")

# --- FASE 3: CONFIRMACIÓN & TRACKING ---
# P6: Orden Exitosa
draw_screen_card(139, 56, 22, 32, "Orden Confirmada", "Código Único", 
                 ["ID: ORD-XXXX", "Resumen WhatsApp", "Botón envío 1-clic", "Enlace a Tracking"], 
                 tag_num="6", border_color=C_ACCENT_GREEN)

# P7: Tracking en Tiempo Real
draw_screen_card(167, 56, 22, 32, "Tracking en Vivo", "Consulta 24/7", 
                 ["Línea de 4 estados", "1. Recibido / 2. Prep.", "3. En Camino / 4. Entregado", "Detalle de Courier"], 
                 tag_num="7", border_color=C_ACCENT_BLUE)

# Fin: Pedido Entregado
c_end = plt.Circle((178, 22), 3.2, facecolor='#ECFDF5', edgecolor=C_ACCENT_GREEN, linewidth=2.2)
ax.add_patch(c_end)
ax.text(178, 22, "★", fontsize=12, color=C_ACCENT_GREEN, ha='center', va='center')
ax.text(178, 17.0, "Pedido Entregado\n(Cliente Satisfecho)", fontsize=8.6, fontweight='bold', color=C_PRIMARY, ha='center', va='top')

# ==============================================================================
# 5. CONEXIONES Y FLUJOS
# ==============================================================================
# Start -> P1
draw_flow_arrow(13.2, 72, 16, 72)

# P1 -> P2
draw_flow_arrow(37, 72, 42, 72, label="Selecciona Prenda")

# P2 -> Decisión Stock
draw_flow_arrow(52.5, 56, 52.5, 32)

# Decisión Stock -> SÍ -> P3 Carrito
draw_ortho([[56.5, 28], [64, 28], [64, 72], [72, 72]], label="SÍ: Añade", color=C_ACCENT_GREEN, label_pos=0)

# Decisión Stock -> NO -> P1 Catálogo
draw_ortho([[48.5, 28], [26.5, 28], [26.5, 56]], label="NO: Agotado", color='#DC2626', style='dashed', label_pos=0)

# P3 Carrito -> P4 Datos Envío
draw_flow_arrow(93, 72, 97, 72, label="Checkout")

# P4 -> P5 Pago
draw_ortho([[118, 72], [124, 72], [124, 45]], label="Valida Destino", label_pos=0)

# P5 Pago -> P6 Orden
draw_ortho([[129, 29.5], [134, 29.5], [134, 72], [139, 72]], label="Paga y Sube Voucher", color=C_ACCENT_GREEN, label_pos=0)

# P6 Orden -> P7 Tracking
draw_flow_arrow(161, 72, 167, 72, label="Ver Estado")

# P7 Tracking -> Fin Entregado
draw_flow_arrow(178, 56, 178, 25.2, label="Entrega Exitosa")

# Guardar figura
output_path = r'c:\Users\Loayza\Downloads\leofit-pedidos-sistema\diagrams\10_User_Flow_Navegacion.png'
plt.tight_layout()
plt.savefig(output_path, format='png', dpi=300, bbox_inches='tight', pad_inches=0.15)
plt.close()
print("User Flow de Alta Legibilidad generado en:", output_path)
