# -*- coding: utf-8 -*-
"""
Generador de Gráficos de Rendimiento y Coexistencia - ISO/IEC 25010:2023
Genera figuras en alta resolución (300 DPI) para el informe técnico de Calidad de Software.
"""

import json
import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
DATA_DIR = os.path.join(ROOT, 'docs', 'gestion_academica', 'evidencias', 'iso25010_s10_s11', 'coexistencia')
OUT_DIR = os.path.join(ROOT, 'docs', 'gestion_academica', 'evidencias', 'iso25010_s10_s11')

def generate_charts():
    summary_path = os.path.join(DATA_DIR, 'coexistence_summary.json')
    if not os.path.exists(summary_path):
        print(f"No se encontró {summary_path}")
        return

    with open(summary_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    res = data['resultados']
    comps = {c['label'].split()[0]: c for c in data['comparaciones']}

    # -------------------------------------------------------------------------
    # Gráfico 1: Comparativa de Latencia Media (Línea Base vs Carga Concurrente)
    # -------------------------------------------------------------------------
    labels = [
        'A: Lectura Catálogo\n(GET /api/products)',
        'A: Escritura Pedido\n(POST /api/orders)',
        'B: Generador Reportes\n(GET /report)'
    ]
    
    base_means = [
        res['A_read_base']['mean_ms'],
        res['A_write_base']['mean_ms'],
        res['B_report_base']['mean_ms']
    ]
    
    sim_means = [
        res['A_read_sim']['mean_ms'],
        res['A_write_sim']['mean_ms'],
        res['B_report_sim']['mean_ms']
    ]
    
    p95_base = [
        res['A_read_base']['p95_ms'],
        res['A_write_base']['p95_ms'],
        res['B_report_base']['p95_ms']
    ]

    p95_sim = [
        res['A_read_sim']['p95_ms'],
        res['A_write_sim']['p95_ms'],
        res['B_report_sim']['p95_ms']
    ]

    x = np.arange(len(labels))
    width = 0.32

    fig, ax = plt.subplots(figsize=(9, 5.2), dpi=300)
    
    rects1 = ax.bar(x - width/2, base_means, width, label='Línea Base (Servicio Aislado)', color='#1E3A8A', edgecolor='#0F172A', linewidth=1)
    rects2 = ax.bar(x + width/2, sim_means, width, label='Ejecución Simultánea (Bajo Carga Concurrente)', color='#0284C7', edgecolor='#0F172A', linewidth=1)

    ax.set_ylabel('Tiempo de Respuesta Promedio (milisegundos)', fontsize=10, fontweight='bold', color='#1E293B')
    ax.set_title('Evaluación de Coexistencia ISO/IEC 25010:2023 — Impacto Recíproco de Latencia (A ↔ B)', fontsize=11, fontweight='bold', pad=15, color='#0F172A')
    ax.set_xticks(x)
    ax.set_xticklabels(labels, fontsize=9.5, fontweight='semibold', color='#334155')
    ax.legend(frameon=True, facecolor='#F8FAFC', edgecolor='#CBD5E1', fontsize=9)
    ax.grid(axis='y', linestyle='--', alpha=0.5, color='#94A3B8')
    ax.set_axisbelow(True)

    # Etiquetas de valor sobre barras
    for rect in rects1:
        height = rect.get_height()
        ax.annotate(f'{height:.2f} ms',
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 3), textcoords="offset points",
                    ha='center', va='bottom', fontsize=8.5, fontweight='bold', color='#1E3A8A')

    for rect in rects2:
        height = rect.get_height()
        ax.annotate(f'{height:.2f} ms',
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 3), textcoords="offset points",
                    ha='center', va='bottom', fontsize=8.5, fontweight='bold', color='#0284C7')

    plt.tight_layout()
    chart1_path = os.path.join(OUT_DIR, 'fig_coexistencia_latencias.png')
    plt.savefig(chart1_path, dpi=300)
    plt.close()
    print(f"[OK] Gráfico 1 generado en: {chart1_path}")

    # -------------------------------------------------------------------------
    # Gráfico 2: Comparativa de Percentil 95 (P95 Tail Latency) y Variación
    # -------------------------------------------------------------------------
    fig, ax2 = plt.subplots(figsize=(9, 4.8), dpi=300)
    
    rects_p1 = ax2.bar(x - width/2, p95_base, width, label='Línea Base P95', color='#475569', edgecolor='#1E293B', linewidth=1)
    rects_p2 = ax2.bar(x + width/2, p95_sim, width, label='Simultáneo P95 (Tail Latency)', color='#EA580C', edgecolor='#7C2D12', linewidth=1)

    ax2.set_ylabel('Percentil 95 - p95 (milisegundos)', fontsize=10, fontweight='bold', color='#1E293B')
    ax2.set_title('Estabilidad y Latencia en Percentil 95 (P95) bajo Estrés de Coexistencia', fontsize=11, fontweight='bold', pad=15, color='#0F172A')
    ax2.set_xticks(x)
    ax2.set_xticklabels(labels, fontsize=9.5, fontweight='semibold', color='#334155')
    ax2.legend(frameon=True, facecolor='#F8FAFC', edgecolor='#CBD5E1', fontsize=9)
    ax2.grid(axis='y', linestyle='--', alpha=0.5, color='#94A3B8')
    ax2.set_axisbelow(True)

    for rect in rects_p1:
        height = rect.get_height()
        ax2.annotate(f'{height:.2f} ms',
                     xy=(rect.get_x() + rect.get_width() / 2, height),
                     xytext=(0, 3), textcoords="offset points",
                     ha='center', va='bottom', fontsize=8.5, fontweight='bold', color='#334155')

    for rect in rects_p2:
        height = rect.get_height()
        ax2.annotate(f'{height:.2f} ms',
                     xy=(rect.get_x() + rect.get_width() / 2, height),
                     xytext=(0, 3), textcoords="offset points",
                     ha='center', va='bottom', fontsize=8.5, fontweight='bold', color='#EA580C')

    plt.tight_layout()
    chart2_path = os.path.join(OUT_DIR, 'fig_coexistencia_p95.png')
    plt.savefig(chart2_path, dpi=300)
    plt.close()
    print(f"[OK] Gráfico 2 generado en: {chart2_path}")

if __name__ == '__main__':
    generate_charts()
