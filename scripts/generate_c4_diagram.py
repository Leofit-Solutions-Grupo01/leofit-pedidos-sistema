import matplotlib.pyplot as plt
import matplotlib.patches as patches
import os

def create_c4_diagram():
    fig, ax = plt.subplots(figsize=(15, 10), dpi=300)
    ax.set_xlim(0, 15)
    ax.set_ylim(0, 10)
    ax.axis('off')
    fig.patch.set_facecolor('#F8FAFC')

    # Title Banner
    ax.text(7.5, 9.5, 'DIAGRAMA C4 - MODELO DE CONTENEDORES (LEVEL 2)', ha='center', va='center',
            fontsize=17, fontweight='bold', color='#0F172A')
    ax.text(7.5, 9.15, 'Sistema de Gestión de Pedidos & Control de Inventario - LeoFit Solutions (Estándar C4 / IcePanel)',
            ha='center', va='center', fontsize=11, color='#64748B')

    # Actors / Users
    # 1. Admin/Operator Person
    user_box = patches.FancyBboxPatch((0.5, 5.5), 3.2, 2.2, boxstyle="round,pad=0.2",
                                      fc='#08427B', ec='#052E56', lw=2)
    ax.add_patch(user_box)
    ax.text(2.1, 7.1, '[Person]', ha='center', va='center', fontsize=9, color='#94A3B8', fontweight='bold')
    ax.text(2.1, 6.6, 'Víctor / Operador', ha='center', va='center', fontsize=13, color='white', fontweight='bold')
    ax.text(2.1, 6.0, 'Personal de taller y ventas\nque gestiona pedidos y stock', ha='center', va='center',
            fontsize=8.5, color='#E2E8F0')

    # 2. End Client (WhatsApp)
    client_box = patches.FancyBboxPatch((0.5, 1.5), 3.2, 2.2, boxstyle="round,pad=0.2",
                                        fc='#475569', ec='#334155', lw=2)
    ax.add_patch(client_box)
    ax.text(2.1, 3.1, '[Person]', ha='center', va='center', fontsize=9, color='#CBD5E1', fontweight='bold')
    ax.text(2.1, 2.6, 'Cliente Final', ha='center', va='center', fontsize=13, color='white', fontweight='bold')
    ax.text(2.1, 2.0, 'Comprador de indumentaria\nque contacta por WhatsApp', ha='center', va='center',
            fontsize=8.5, color='#F1F5F9')

    # Main System Boundary (LeoFit System)
    sys_boundary = patches.FancyBboxPatch((4.5, 0.8), 7.0, 7.8, boxstyle="round,pad=0.3",
                                         fc='#FFFFFF', ec='#94A3B8', lw=1.5, ls='--')
    ax.add_patch(sys_boundary)
    ax.text(8.0, 8.3, 'Límite del Sistema: LeoFit Pedidos PWA', ha='center', va='center',
            fontsize=12, fontweight='bold', color='#1E293B')

    # Container 1: PWA Single Page Application
    pwa_box = patches.FancyBboxPatch((5.0, 5.2), 6.0, 2.6, boxstyle="round,pad=0.2",
                                    fc='#1168BD', ec='#0B4884', lw=2)
    ax.add_patch(pwa_box)
    ax.text(8.0, 7.3, '[Container: React 19 + TypeScript + Vite]', ha='center', va='center',
            fontsize=9, color='#BAE6FD', fontweight='bold')
    ax.text(8.0, 6.7, 'Single-Page Application (PWA)', ha='center', va='center',
            fontsize=13, color='white', fontweight='bold')
    ax.text(8.0, 5.9, 'Proporciona interfaz Mobile-First reactiva, modo offline,\ncontrol de privacidad y cálculo de fletes.',
            ha='center', va='center', fontsize=8.5, color='#F0F9FF')

    # Container 2: API REST Backend
    api_box = patches.FancyBboxPatch((5.0, 1.4), 6.0, 2.6, boxstyle="round,pad=0.2",
                                    fc='#1168BD', ec='#0B4884', lw=2)
    ax.add_patch(api_box)
    ax.text(8.0, 3.5, '[Container: Node.js + Express + Prisma ORM]', ha='center', va='center',
            fontsize=9, color='#BAE6FD', fontweight='bold')
    ax.text(8.0, 2.9, 'Backend REST API', ha='center', va='center',
            fontsize=13, color='white', fontweight='bold')
    ax.text(8.0, 2.1, 'Lógica transaccional ACID, autenticación JWT,\nreglas de negocio y endpoints JSON.',
            ha='center', va='center', fontsize=8.5, color='#F0F9FF')

    # External System / Database
    # Container 3: Relational Database
    db_box = patches.FancyBboxPatch((12.2, 1.4), 2.5, 2.6, boxstyle="round,pad=0.2",
                                    fc='#2B78E4', ec='#1A5BB8', lw=2)
    ax.add_patch(db_box)
    ax.text(13.45, 3.5, '[Database]', ha='center', va='center', fontsize=9, color='#E0E7FF', fontweight='bold')
    ax.text(13.45, 2.9, 'PostgreSQL\n/ MySQL', ha='center', va='center', fontsize=12, color='white', fontweight='bold')
    ax.text(13.45, 1.9, 'Esquema 3FN/BCNF\n8 tablas relacionales', ha='center', va='center', fontsize=8, color='#EEF2FF')

    # External System: Delivery Courier / WhatsApp Gateway
    ext_box = patches.FancyBboxPatch((12.2, 5.2), 2.5, 2.6, boxstyle="round,pad=0.2",
                                     fc='#64748B', ec='#475569', lw=2)
    ax.add_patch(ext_box)
    ax.text(13.45, 7.3, '[External System]', ha='center', va='center', fontsize=8.5, color='#E2E8F0', fontweight='bold')
    ax.text(13.45, 6.7, 'WhatsApp &\nMotorizado', ha='center', va='center', fontsize=11, color='white', fontweight='bold')
    ax.text(13.45, 5.8, 'Canal de mensajería\ny logística de entrega', ha='center', va='center', fontsize=8, color='#F8FAFC')

    # Relationship Arrows
    # User -> PWA
    ax.annotate('', xy=(5.0, 6.5), xytext=(3.7, 6.5),
                arrowprops=dict(arrowstyle="-|>", lw=2, color='#0F172A'))
    ax.text(4.35, 6.75, 'HTTPS / UI', ha='center', va='center', fontsize=8, fontweight='bold', color='#0F172A')

    # Client -> User
    ax.annotate('', xy=(2.1, 5.5), xytext=(2.1, 3.7),
                arrowprops=dict(arrowstyle="-|>", lw=1.5, ls=':', color='#475569'))
    ax.text(2.6, 4.6, 'Mensaje WhatsApp', ha='center', va='center', fontsize=8, color='#475569')

    # PWA -> API Backend
    ax.annotate('', xy=(8.0, 4.0), xytext=(8.0, 5.2),
                arrowprops=dict(arrowstyle="-|>", lw=2, color='#0F172A'))
    ax.text(8.7, 4.6, 'JSON / REST\nBearer JWT', ha='left', va='center', fontsize=8, fontweight='bold', color='#0F172A')

    # API Backend -> DB
    ax.annotate('', xy=(12.2, 2.7), xytext=(11.0, 2.7),
                arrowprops=dict(arrowstyle="-|>", lw=2, color='#0F172A'))
    ax.text(11.6, 3.0, 'SQL / TCP\nTransacciones', ha='center', va='center', fontsize=7.5, fontweight='bold', color='#0F172A')

    # PWA / User -> WhatsApp
    ax.annotate('', xy=(12.2, 6.5), xytext=(11.0, 6.5),
                arrowprops=dict(arrowstyle="-|>", lw=1.5, ls='--', color='#0F172A'))
    ax.text(11.6, 6.8, 'Notificación\nwa.me URL', ha='center', va='center', fontsize=7.5, fontweight='bold', color='#0F172A')

    # Footer note
    ax.text(7.5, 0.3, 'C4 Model Level 2 - Contenedores de Software | Conforme a Estándar IEEE 1471 / ISO 42010',
            ha='center', va='center', fontsize=9, style='italic', color='#64748B')

    os.makedirs('diagrams', exist_ok=True)
    out_path = 'diagrams/11_Arquitectura_C4_Model.png'
    plt.tight_layout()
    plt.savefig(out_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f'[OK] Diagrama C4 generado exitosamente en: {out_path}')

if __name__ == '__main__':
    create_c4_diagram()
