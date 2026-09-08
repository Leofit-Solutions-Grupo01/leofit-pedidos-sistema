import matplotlib.pyplot as plt
import matplotlib.patches as patches
import os

def create_c4_diagram():
    fig, ax = plt.subplots(figsize=(16, 11), dpi=300)
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 11)
    ax.axis('off')
    fig.patch.set_facecolor('#F8FAFC')

    # Title Banner
    ax.text(8.0, 10.4, 'DIAGRAMA C4 - MODELO DE CONTENEDORES (LEVEL 2)', ha='center', va='center',
            fontsize=17, fontweight='bold', color='#0F172A')
    ax.text(8.0, 10.0, 'Sistema de Gestión de Pedidos, Envíos Locales y Encomiendas Nacionales - LeoFit Solutions',
            ha='center', va='center', fontsize=11, color='#64748B')

    # Actors / Users
    # 1. Admin/Operator Person (Victor)
    user_box = patches.FancyBboxPatch((0.5, 6.2), 3.2, 2.6, boxstyle="round,pad=0.2",
                                      fc='#08427B', ec='#052E56', lw=2)
    ax.add_patch(user_box)
    ax.text(2.1, 8.2, '[Person: Administrador]', ha='center', va='center', fontsize=8.5, color='#94A3B8', fontweight='bold')
    ax.text(2.1, 7.6, 'Víctor / Operador', ha='center', va='center', fontsize=12, color='white', fontweight='bold')
    ax.text(2.1, 6.8, 'Gestiona pedidos, stock,\ndespecho local en Lima y\nremisión a agencias.', ha='center', va='center',
            fontsize=8.5, color='#E2E8F0')

    # 2. End Client (WhatsApp & Tracking)
    client_box = patches.FancyBboxPatch((0.5, 1.8), 3.2, 2.6, boxstyle="round,pad=0.2",
                                        fc='#475569', ec='#334155', lw=2)
    ax.add_patch(client_box)
    ax.text(2.1, 3.8, '[Person: Cliente Final]', ha='center', va='center', fontsize=8.5, color='#CBD5E1', fontweight='bold')
    ax.text(2.1, 3.2, 'Cliente Final', ha='center', va='center', fontsize=12, color='white', fontweight='bold')
    ax.text(2.1, 2.4, 'Realiza compras por WhatsApp\ny consulta el tracking en vivo\nde su paquete (Lima/Provincia).', ha='center', va='center',
            fontsize=8.5, color='#F1F5F9')

    # Main System Boundary (LeoFit System)
    sys_boundary = patches.FancyBboxPatch((4.4, 0.8), 7.2, 8.8, boxstyle="round,pad=0.3",
                                         fc='#FFFFFF', ec='#94A3B8', lw=1.5, ls='--')
    ax.add_patch(sys_boundary)
    ax.text(8.0, 9.2, 'Límite del Sistema: LeoFit Pedidos & Envíos PWA', ha='center', va='center',
            fontsize=12, fontweight='bold', color='#1E293B')

    # Container 1: PWA Single Page Application
    pwa_box = patches.FancyBboxPatch((4.9, 5.8), 6.2, 2.9, boxstyle="round,pad=0.2",
                                    fc='#1168BD', ec='#0B4884', lw=2)
    ax.add_patch(pwa_box)
    ax.text(8.0, 8.2, '[Container: React 19 + TypeScript + Vite PWA]', ha='center', va='center',
            fontsize=8.5, color='#BAE6FD', fontweight='bold')
    ax.text(8.0, 7.6, 'Single-Page Application (PWA)', ha='center', va='center',
            fontsize=13, color='white', fontweight='bold')
    ax.text(8.0, 6.7, 'Módulos: Dashboard, Gestión de Pedidos, Catálogo,\nPortal de Rastreo de Envíos en Vivo (Tracking)\ny Control de Encomiendas Nacionales.',
            ha='center', va='center', fontsize=8.5, color='#F0F9FF')

    # Container 2: API REST Backend
    api_box = patches.FancyBboxPatch((4.9, 1.5), 6.2, 2.8, boxstyle="round,pad=0.2",
                                    fc='#1168BD', ec='#0B4884', lw=2)
    ax.add_patch(api_box)
    ax.text(8.0, 3.8, '[Container: Node.js + Express + Prisma ORM]', ha='center', va='center',
            fontsize=8.5, color='#BAE6FD', fontweight='bold')
    ax.text(8.0, 3.2, 'Backend REST API & Tracking Hub', ha='center', va='center',
            fontsize=13, color='white', fontweight='bold')
    ax.text(8.0, 2.3, 'Lógica transaccional ACID, correlativos LFT,\nmotor de estados (Local / Agencia Encomienda)\ny autenticación JWT.',
            ha='center', va='center', fontsize=8.5, color='#F0F9FF')

    # External Systems / DB
    # Container 3: Relational Database
    db_box = patches.FancyBboxPatch((12.6, 1.5), 2.9, 2.8, boxstyle="round,pad=0.2",
                                    fc='#2B78E4', ec='#1A5BB8', lw=2)
    ax.add_patch(db_box)
    ax.text(14.05, 3.8, '[Database]', ha='center', va='center', fontsize=8.5, color='#E0E7FF', fontweight='bold')
    ax.text(14.05, 3.2, 'PostgreSQL\n/ MySQL', ha='center', va='center', fontsize=12, color='white', fontweight='bold')
    ax.text(14.05, 2.3, 'Esquema relacional 3FN\nTablas de pedidos, guías,\nencomiendas e ítems', ha='center', va='center', fontsize=8, color='#EEF2FF')

    # External System 1: WhatsApp & Delivery Local Lima
    ext_local = patches.FancyBboxPatch((12.6, 7.0), 2.9, 1.8, boxstyle="round,pad=0.2",
                                       fc='#64748B', ec='#475569', lw=2)
    ax.add_patch(ext_local)
    ax.text(14.05, 8.4, '[External System: Lima]', ha='center', va='center', fontsize=8, color='#E2E8F0', fontweight='bold')
    ax.text(14.05, 7.8, 'WhatsApp & Reparto Local', ha='center', va='center', fontsize=10.5, color='white', fontweight='bold')
    ax.text(14.05, 7.3, 'Entrega directa con Víctor / Motorizado', ha='center', va='center', fontsize=7.5, color='#F8FAFC')

    # External System 2: Agencias de Encomienda (Provincias)
    ext_prov = patches.FancyBboxPatch((12.6, 4.8), 2.9, 1.9, boxstyle="round,pad=0.2",
                                      fc='#334155', ec='#1E293B', lw=2)
    ax.add_patch(ext_prov)
    ax.text(14.05, 6.3, '[External System: Provincias]', ha='center', va='center', fontsize=8, color='#E2E8F0', fontweight='bold')
    ax.text(14.05, 5.7, 'Agencias Encomienda\n(Shalom / Olva / Marvisur)', ha='center', va='center', fontsize=10, color='white', fontweight='bold')
    ax.text(14.05, 5.1, 'Transporte nacional con N° Guía', ha='center', va='center', fontsize=7.5, color='#F8FAFC')

    # Relationship Arrows
    # User -> PWA
    ax.annotate('', xy=(4.9, 7.4), xytext=(3.7, 7.4),
                arrowprops=dict(arrowstyle="-|>", lw=2, color='#0F172A'))
    ax.text(4.3, 7.65, 'HTTPS / UI', ha='center', va='center', fontsize=8, fontweight='bold', color='#0F172A')

    # Client -> PWA (Tracking en vivo)
    ax.annotate('', xy=(4.9, 6.2), xytext=(3.7, 3.2),
                arrowprops=dict(arrowstyle="-|>", lw=1.5, ls='--', color='#2563EB'))
    ax.text(4.0, 4.8, 'Rastreo LFT\nen Vivo', ha='center', va='center', fontsize=8, fontweight='bold', color='#2563EB')

    # Client -> User (WhatsApp)
    ax.annotate('', xy=(2.1, 6.2), xytext=(2.1, 4.4),
                arrowprops=dict(arrowstyle="-|>", lw=1.5, ls=':', color='#475569'))
    ax.text(2.6, 5.3, 'Pedido WhatsApp', ha='center', va='center', fontsize=8, color='#475569')

    # PWA -> API Backend
    ax.annotate('', xy=(8.0, 4.3), xytext=(8.0, 5.8),
                arrowprops=dict(arrowstyle="-|>", lw=2, color='#0F172A'))
    ax.text(8.7, 5.0, 'JSON / REST\nBearer JWT', ha='left', va='center', fontsize=8, fontweight='bold', color='#0F172A')

    # API Backend -> DB
    ax.annotate('', xy=(12.6, 2.9), xytext=(11.1, 2.9),
                arrowprops=dict(arrowstyle="-|>", lw=2, color='#0F172A'))
    ax.text(11.85, 3.2, 'SQL / TCP\nTransacciones', ha='center', va='center', fontsize=7.5, fontweight='bold', color='#0F172A')

    # PWA -> Local Courier
    ax.annotate('', xy=(12.6, 7.8), xytext=(11.1, 7.4),
                arrowprops=dict(arrowstyle="-|>", lw=1.5, ls='--', color='#0F172A'))
    ax.text(11.85, 7.85, 'Notificación\nwa.me URL', ha='center', va='center', fontsize=7.5, fontweight='bold', color='#0F172A')

    # PWA -> Encomiendas
    ax.annotate('', xy=(12.6, 5.7), xytext=(11.1, 6.6),
                arrowprops=dict(arrowstyle="-|>", lw=1.5, ls='--', color='#0F172A'))
    ax.text(11.85, 6.35, 'N° Guía / Tracking\nNacional', ha='center', va='center', fontsize=7.5, fontweight='bold', color='#0F172A')

    # Footer note
    ax.text(8.0, 0.3, 'C4 Model Level 2 - Contenedores de Software | Conforme a Estándar IEEE 1471 / ISO 42010 | LeoFit Multi-Carrier Dispatch',
            ha='center', va='center', fontsize=9, style='italic', color='#64748B')

    os.makedirs('diagrams', exist_ok=True)
    out_path = 'diagrams/11_Arquitectura_C4_Model.png'
    plt.tight_layout()
    plt.savefig(out_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f'[OK] Diagrama C4 actualizado exitosamente en: {out_path}')

if __name__ == '__main__':
    create_c4_diagram()
