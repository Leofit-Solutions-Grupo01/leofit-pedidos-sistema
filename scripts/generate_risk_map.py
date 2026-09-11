import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch

# ==============================================================================
# CONFIGURACIÓN: MAPA DE RIESGOS 5X5 - TABLA CON TIPOGRAFÍA MAXIMIZADA
# ==============================================================================
fig, ax = plt.subplots(figsize=(21, 12.5), dpi=300)
fig.patch.set_facecolor('#FFFFFF')
ax.set_facecolor('#FFFFFF')
ax.set_xlim(0, 210)
ax.set_ylim(0, 125)
ax.axis('off')

# Colores Ejecutivos de Alto Contraste
C_DARK = '#0F172A'       # Slate 900
C_HEADER = '#1E293B'     # Slate 800
C_TEXT_MUTED = '#1E293B' # Slate 800 (oscuro para máxima lectura del plan)
C_BORDER = '#94A3B8'

# Zonas de Severidad del Heatmap
COLOR_CRIT_BG = '#FEE2E2'   # Red 100
COLOR_CRIT_TXT = '#991B1B'  # Red 800
COLOR_MEDH_BG = '#FFEDD5'   # Orange 100
COLOR_MEDH_TXT = '#9A3412'  # Orange 800
COLOR_MED_BG = '#FEF3C7'    # Amber 100
COLOR_MED_TXT = '#92400E'   # Amber 800
COLOR_LOW_BG = '#DCFCE7'    # Emerald 100
COLOR_LOW_TXT = '#166534'   # Emerald 800

# ==============================================================================
# 1. ENCABEZADO PRINCIPAL
# ==============================================================================
ax.text(6, 120, "LEOFIT — MATRIZ DE GESTIÓN DE RIESGOS (5 × 5)", 
        fontsize=25, fontweight='bold', color=C_DARK, va='top', fontfamily='sans-serif')
ax.text(6, 114, "Mapa de Calor Probabilidad × Impacto (P × I) y Catálogo de Mitigación de los 8 Riesgos", 
        fontsize=13.5, fontweight='medium', color='#475569', va='top', fontfamily='sans-serif')

# ==============================================================================
# 2. HEATMAP MATRIZ 5X5 (SECTOR IZQUIERDO: X: 28 a 98, Y: 28 a 98)
# ==============================================================================
m_x0 = 28.0
m_y0 = 28.0
cell_size = 14.0  # 5 celdas = 70.0 unidades de lado

def get_zone_info(p, i):
    score = p * i
    if score >= 15:
        return COLOR_CRIT_BG, COLOR_CRIT_TXT, "Crítico"
    elif score >= 12:
        return COLOR_MEDH_BG, COLOR_MEDH_TXT, "Medio-Alto"
    elif score >= 8:
        return COLOR_MED_BG, COLOR_MED_TXT, "Medio"
    else:
        return COLOR_LOW_BG, COLOR_LOW_TXT, "Bajo"

# Dibujar las 25 celdas
for p in range(1, 6):
    for i in range(1, 6):
        cx = m_x0 + (p - 1) * cell_size
        cy = m_y0 + (i - 1) * cell_size
        bg_col, txt_col, _ = get_zone_info(p, i)
        
        # Celda
        rect = FancyBboxPatch((cx, cy), cell_size, cell_size, boxstyle="square,pad=0",
                              facecolor=bg_col, edgecolor='#FFFFFF', linewidth=3.0)
        ax.add_patch(rect)
        
        # Puntuación P × I grande
        score = p * i
        ax.text(cx + 1.8, cy + cell_size - 1.8, f"{score}", 
                fontsize=12.0, fontweight='bold', color=txt_col, alpha=0.7, ha='left', va='top')

# Borde exterior matriz
mat_border = FancyBboxPatch((m_x0, m_y0), cell_size * 5, cell_size * 5, boxstyle="square,pad=0",
                            facecolor='none', edgecolor=C_DARK, linewidth=2.5)
ax.add_patch(mat_border)

# Eje X: Probabilidad
prob_labels = ["1\nMuy Baja", "2\nBaja", "3\nMedia", "4\nAlta", "5\nMuy Alta"]
for idx, lbl in enumerate(prob_labels):
    cx = m_x0 + idx * cell_size + cell_size / 2
    ax.text(cx, m_y0 - 2.5, lbl, fontsize=11.5, fontweight='bold', color=C_DARK, ha='center', va='top')

# Título Eje X
ax.text(m_x0 + (cell_size * 5) / 2, 14.0, "PROBABILIDAD (1 - 5)", 
        fontsize=14.0, fontweight='bold', color=C_DARK, ha='center', va='center')

# Eje Y: Impacto
impact_labels = ["1  Insignificante", "2  Menor", "3  Moderado", "4  Mayor", "5  Catastrófico"]
for idx, lbl in enumerate(impact_labels):
    cy = m_y0 + idx * cell_size + cell_size / 2
    ax.text(m_x0 - 2.5, cy, lbl, fontsize=11.5, fontweight='bold', color=C_DARK, ha='right', va='center')

# Título Eje Y
ax.text(6.5, m_y0 + (cell_size * 5) / 2, "IMPACTO (1 - 5)", 
        fontsize=14.0, fontweight='bold', color=C_DARK, ha='center', va='center', rotation=90)

# Tokens de Riesgo dentro del Heatmap
def draw_map_token(cx, cy, r_id, bg_color='#0F172A', size=3.8, font_sz=12.0):
    c = plt.Circle((cx, cy), size, facecolor=bg_color, edgecolor='#FFFFFF', linewidth=2.2, zorder=6)
    ax.add_patch(c)
    ax.text(cx, cy, r_id, fontsize=font_sz, fontweight='bold', color='#FFFFFF', ha='center', va='center', zorder=7)

# Posicionamiento de los 8 Riesgos en el Heatmap
draw_map_token(m_x0 + 0.5*cell_size, m_y0 + 4.5*cell_size, "R5", bg_color='#16A34A', size=4.0, font_sz=12.5)
draw_map_token(m_x0 + 1.5*cell_size, m_y0 + 4.5*cell_size, "R4", bg_color='#D97706', size=4.0, font_sz=12.5)
draw_map_token(m_x0 + 1.5*cell_size, m_y0 + 3.5*cell_size, "R7", bg_color='#D97706', size=4.0, font_sz=12.5)

draw_map_token(m_x0 + 2.5*cell_size - 3.5, m_y0 + 3.5*cell_size, "R1", bg_color='#EA580C', size=3.8, font_sz=12.0)
draw_map_token(m_x0 + 2.5*cell_size + 3.5, m_y0 + 3.5*cell_size, "R3", bg_color='#EA580C', size=3.8, font_sz=12.0)

draw_map_token(m_x0 + 1.5*cell_size - 3.5, m_y0 + 2.5*cell_size - 2.5, "R2", bg_color='#16A34A', size=3.6, font_sz=11.5)
draw_map_token(m_x0 + 1.5*cell_size + 3.5, m_y0 + 2.5*cell_size - 2.5, "R6", bg_color='#16A34A', size=3.6, font_sz=11.5)
draw_map_token(m_x0 + 1.5*cell_size, m_y0 + 2.5*cell_size + 3.5, "R8", bg_color='#16A34A', size=3.6, font_sz=11.5)

# Leyenda de Zonas de Severidad (Debajo)
def draw_legend_pill(x, y, w, h, label, bg, fg):
    b = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.2,rounding_size=0.8", 
                        facecolor=bg, edgecolor=fg, linewidth=1.6)
    ax.add_patch(b)
    ax.text(x + w/2, y + h/2, label, fontsize=11.0, fontweight='bold', color=fg, ha='center', va='center')

draw_legend_pill(m_x0, 4.0, 16.5, 4.5, "Bajo (1-6)", COLOR_LOW_BG, COLOR_LOW_TXT)
draw_legend_pill(m_x0 + 18.0, 4.0, 16.5, 4.5, "Medio (8-10)", COLOR_MED_BG, COLOR_MED_TXT)
draw_legend_pill(m_x0 + 36.0, 4.0, 18.0, 4.5, "Medio-Alto (12)", COLOR_MEDH_BG, COLOR_MEDH_TXT)
draw_legend_pill(m_x0 + 55.5, 4.0, 14.5, 4.5, "Crítico (15-25)", COLOR_CRIT_BG, COLOR_CRIT_TXT)

# ==============================================================================
# 3. TABLA EJECUTIVA DE TRATAMIENTO DE LOS 8 RIESGOS (LETRAS AMPLIADAS)
# ==============================================================================
# Sector derecho: X: 104 a 204 (Ancho = 100.0 unidades)
t_x0 = 104.0
t_y0 = 4.0
t_w = 100.0
t_h = 98.0

# Contenedor General
table_bg = FancyBboxPatch((t_x0, t_y0), t_w, t_h, boxstyle="round,pad=0.2,rounding_size=1.2",
                          facecolor='#F8FAFC', edgecolor='#CBD5E1', linewidth=2.0)
ax.add_patch(table_bg)

# Encabezado de la Tabla
t_header_h = 7.5
t_header = FancyBboxPatch((t_x0, t_y0 + t_h - t_header_h), t_w, t_header_h, boxstyle="square,pad=0",
                          facecolor=C_HEADER, edgecolor=C_HEADER)
ax.add_patch(t_header)

ax.text(t_x0 + t_w/2, t_y0 + t_h - t_header_h/2, "MATRIZ DE TRATAMIENTO Y MITIGACIÓN (R1 - R8)", 
        fontsize=14.5, fontweight='bold', color='#FFFFFF', ha='center', va='center')

# Catálogo estructurado de los 8 riesgos
risk_catalog = [
    {
        "id": "R1", "title": "Disponibilidad del Stakeholder", "cat": "Operacional",
        "pxi": "P:3 × I:4 = 12", "level": "MEDIO-ALTO", "badge_bg": "#FFEDD5", "badge_fg": "#9A3412",
        "action": "Minutas asíncronas, demos grabadas y sesiones semanales de 30 min."
    },
    {
        "id": "R3", "title": "Scope Creep (Exceso de Alcance)", "cat": "Alcance",
        "pxi": "P:3 × I:4 = 12", "level": "MEDIO-ALTO", "badge_bg": "#FFEDD5", "badge_fg": "#9A3412",
        "action": "Congelamiento estricto de MVP y priorización MoSCoW documentada."
    },
    {
        "id": "R4", "title": "Cálculo de Stock Concurrente", "cat": "Calidad",
        "pxi": "P:2 × I:5 = 10", "level": "MEDIO", "badge_bg": "#FEF3C7", "badge_fg": "#92400E",
        "action": "Bloqueo atómico transaccional en BD y pruebas Vitest de concurrencia."
    },
    {
        "id": "R7", "title": "Tiempo de Carga por Imágenes", "cat": "Rendimiento",
        "pxi": "P:2 × I:4 = 8", "level": "MEDIO", "badge_bg": "#FEF3C7", "badge_fg": "#92400E",
        "action": "Compresión WebP automática, almacenamiento en CDN y Lazy Loading."
    },
    {
        "id": "R2", "title": "Curva Técnica TypeScript/PWA", "cat": "Técnico",
        "pxi": "P:2 × I:3 = 6", "level": "BAJO", "badge_bg": "#DCFCE7", "badge_fg": "#166534",
        "action": "Pair programming diario, plantillas base y linters estrictos."
    },
    {
        "id": "R6", "title": "Compatibilidad PWA Móviles Antiguos", "cat": "Despliegue",
        "pxi": "P:2 × I:3 = 6", "level": "BAJO", "badge_bg": "#DCFCE7", "badge_fg": "#166534",
        "action": "Degradación progresiva y polyfills de compatibilidad para WebKit."
    },
    {
        "id": "R8", "title": "Conflictos en Repositorio Git", "cat": "Gestión",
        "pxi": "P:2 × I:3 = 6", "level": "BAJO", "badge_bg": "#DCFCE7", "badge_fg": "#166534",
        "action": "Flujo Trunk-Based con Pull Requests cortos e integración CI diaria."
    },
    {
        "id": "R5", "title": "Exposición de Datos de Contacto", "cat": "Seguridad",
        "pxi": "P:1 × I:5 = 5", "level": "BAJO", "badge_bg": "#DCFCE7", "badge_fg": "#166534",
        "action": "Sanitización en backend, políticas CORS y variables de entorno seguras."
    }
]

# Renderizar cada tarjeta con tipografía grande y clara
card_height = 10.6
start_y = t_y0 + t_h - t_header_h - card_height - 0.7

for r in risk_catalog:
    # Tarjeta base
    row_patch = FancyBboxPatch((t_x0 + 1.2, start_y), t_w - 2.4, card_height - 0.7,
                               boxstyle="round,pad=0.1,rounding_size=0.6",
                               facecolor='#FFFFFF', edgecolor='#E2E8F0', linewidth=1.4)
    ax.add_patch(row_patch)
    
    # Token ID circular a la izquierda
    b_cx = t_x0 + 5.5
    b_cy = start_y + (card_height - 0.7) / 2
    draw_map_token(b_cx, b_cy, r["id"], bg_color=r["badge_fg"], size=3.7, font_sz=12.5)
    
    # LÍNEA SUPERIOR: Título del riesgo + Categoría (Izquierda) - FUENTE GRANDE
    ax.text(t_x0 + 10.8, start_y + 6.8, f"{r['title']}  •  [{r['cat']}]", 
            fontsize=12.0, fontweight='bold', color=C_DARK, va='center')
    
    # LÍNEA SUPERIOR: Severidad y Nivel (Derecha) - FUENTE GRANDE
    ax.text(t_x0 + t_w - 3.5, start_y + 6.8, f"{r['pxi']} ({r['level']})", 
            fontsize=11.5, fontweight='bold', color=r["badge_fg"], ha='right', va='center')
    
    # LÍNEA INFERIOR: Acción Preventiva / Plan de Mitigación - FUENTE GRANDE Y CLARA
    ax.text(t_x0 + 10.8, start_y + 2.8, f"Plan: {r['action']}", 
            fontsize=10.5, fontweight='medium', color=C_TEXT_MUTED, va='center')
    
    start_y -= card_height

# Guardar figura en alta resolución (300 DPI)
output_path = r'c:\Users\Loayza\Downloads\leofit-pedidos-sistema\diagrams\02_Mapa_Riesgos.png'
plt.tight_layout()
plt.savefig(output_path, format='png', dpi=300, bbox_inches='tight', pad_inches=0.2)
plt.close()
print("Mapa de Riesgos con tabla agrandada generado exitosamente en:", output_path)
