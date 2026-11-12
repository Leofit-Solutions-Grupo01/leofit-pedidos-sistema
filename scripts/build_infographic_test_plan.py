# -*- coding: utf-8 -*-
"""
@file build_infographic_test_plan.py
@description Genera los 3 gráficos infográficos de alta resolución (300 DPI) y compila el
             Plan de Pruebas de Software Ejecutivo-Visual (Formato Infografía Formal Compacta)
             en Word (.docx), PDF (.pdf) y HTML (.html) en la menor cantidad de hojas posible (4 páginas A4).
@project LeoFit Solutions - Sistema de Gestión de Pedidos (ISO/IEC/IEEE 29119-3 & 29119-4)
"""

import os
import sys
import shutil
import fitz  # PyMuPDF
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DOCS_PLAN_DIR = os.path.join(BASE_DIR, "docs", "02_CALIDAD_Y_AUDITORIA", "01_plan_de_pruebas_iso29119")
ASSETS_DIR = os.path.join(DOCS_PLAN_DIR, "assets")
PROYECTO_LOCAL_DIR = os.path.join(BASE_DIR, "_PROYECTO_FINAL_LOCAL", "02_ENTREGABLES_UTP")
DOCX_LOCAL_DIR = os.path.join(PROYECTO_LOCAL_DIR, "01_DOCX")
HTML_LOCAL_DIR = os.path.join(PROYECTO_LOCAL_DIR, "00_HTML")

os.makedirs(DOCS_PLAN_DIR, exist_ok=True)
os.makedirs(ASSETS_DIR, exist_ok=True)
os.makedirs(DOCX_LOCAL_DIR, exist_ok=True)
os.makedirs(HTML_LOCAL_DIR, exist_ok=True)

# Paleta Corporativa LeoFit (Alto Contraste WCAG AA/AAA)
NAVY = "#0F172A"
NAVY_MID = "#1E293B"
ROYAL = "#1E3A8A"
BLUE = "#1665D8"
BLUE_LIGHT = "#EFF6FF"
TEAL = "#0E7490"
GREEN = "#15803D"
GREEN_LIGHT = "#F0FDF4"
RUST = "#C2410C"
RUST_LIGHT = "#FFF7ED"
RED = "#B91C1C"
RED_LIGHT = "#FEF2F2"
SLATE_BG = "#F8FAFC"
SLATE_BORDER = "#CBD5E1"
SLATE_TEXT = "#334155"

plt.rcParams["font.family"] = "DejaVu Sans"


def draw_rounded_box(ax, x, y, w, h, fc, ec, lw=1.2, radius=0.06):
    patch = FancyBboxPatch(
        (x, y), w, h,
        boxstyle=f"round,pad=0.01,rounding_size={radius}",
        fc=fc, ec=ec, lw=lw
    )
    ax.add_patch(patch)
    return patch


# ==============================================================================
# FIGURA 1: DASHBOARD EJECUTIVO DE QA, PIRÁMIDE SHIFT-LEFT Y SUITES (194 TESTS)
# ==============================================================================
def generate_fig1_dashboard_piramide():
    fig = plt.figure(figsize=(11.0, 5.0), dpi=300, facecolor="white")
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, 11.0)
    ax.set_ylim(0, 5.0)
    ax.axis("off")

    # Banner Superior
    draw_rounded_box(ax, 0.15, 4.44, 10.7, 0.44, fc=NAVY, ec=BLUE, lw=1.5, radius=0.05)
    ax.text(5.5, 4.66, "FIGURA 1 — PANEL EJECUTIVO DE CALIDAD: PIRÁMIDE SHIFT-LEFT Y DISTRIBUCIÓN DE 194 PRUEBAS",
            ha="center", va="center", fontsize=9.5, fontweight="bold", color="white")

    # 5 KPI Cards
    kpis = [
        ("194 / 194", "PRUEBAS APROBADAS", "100% Pass Rate · 0 Fallos", GREEN_LIGHT, GREEN, GREEN),
        ("125 BE + 69 FE", "COBERTURA FULL-STACK", "27 Suites Activas (Jest/Vitest)", BLUE_LIGHT, BLUE, BLUE),
        ("97.9 / 100", "CALIDAD ISO/IEC 25010", "Grado A+ Auditado en Comité", BLUE_LIGHT, ROYAL, ROYAL),
        ("342 ms", "LATENCIA P95 BAJO CARGA", "Meta SLA <= 800 ms (50 VUs)", RUST_LIGHT, RUST, RUST),
        ("RTO 3.2 s", "CONTINUIDAD DRP NEON", "RPO = 0 s · Cero Pérdida Datos", GREEN_LIGHT, TEAL, TEAL),
    ]
    card_w = 2.02
    gap = 0.15
    start_x = 0.15
    for i, (big, title, sub, bg, border_c, txt_c) in enumerate(kpis):
        cx = start_x + i * (card_w + gap)
        draw_rounded_box(ax, cx, 3.52, card_w, 0.78, fc=bg, ec=border_c, lw=1.3, radius=0.05)
        ax.text(cx + card_w / 2, 4.08, big, ha="center", va="center", fontsize=12.0, fontweight="bold", color=txt_c)
        ax.text(cx + card_w / 2, 3.82, title, ha="center", va="center", fontsize=6.9, fontweight="bold", color=NAVY)
        ax.text(cx + card_w / 2, 3.64, sub, ha="center", va="center", fontsize=6.2, color=SLATE_TEXT)

    # Panel Izquierdo: Pirámide de Pruebas Shift-Left
    draw_rounded_box(ax, 0.15, 0.15, 5.20, 3.24, fc=SLATE_BG, ec=SLATE_BORDER, lw=1.0, radius=0.06)
    ax.text(2.75, 3.20, "PIRÁMIDE DE AUTOMATIZACIÓN SHIFT-LEFT (ISO 29119-2)",
            ha="center", va="center", fontsize=8.2, fontweight="bold", color=NAVY)

    levels = [
        (2.48, 3.55, 0.54, "NIVEL 4: SISTEMA, E2E Y USABILIDAD WCAG AA (9 Tests)",
         "Flujo Compra E2E · Accesibilidad Visual · SUS 88.5/100", GREEN_LIGHT, GREEN, GREEN),
        (1.80, 4.00, 0.58, "NIVEL 3: COMPONENTES UI Y ESTADO REACT 19 (60 Tests)",
         "AppContext · Carrito · Checkout Modal · AuthGuard RBAC · Gráficos", BLUE_LIGHT, BLUE, ROYAL),
        (1.06, 4.45, 0.64, "NIVEL 2: INTEGRACIÓN API REST Y PERSISTENCIA ACID (85 Tests)",
         "Supertest · SELECT FOR UPDATE · Idempotencia JCS · Webhooks Culqi · OSE", RUST_LIGHT, RUST, RUST),
        (0.28, 4.90, 0.68, "NIVEL 1: UNIDADES PURAS DE DOMINIO Y CRIPTOGRAFÍA (40 Tests)",
         "Esquemas Zod · JWT HS256 · Bcrypt Salt 10 · HMAC timingSafeEqual · Decimal.js IGV", "#EEF2FF", NAVY, NAVY),
    ]
    for ly, lw_box, lh, ltitle, ldesc, lfc, lec, ltc in levels:
        lx = 2.75 - lw_box / 2
        draw_rounded_box(ax, lx, ly, lw_box, lh, fc=lfc, ec=lec, lw=1.3, radius=0.04)
        ax.text(2.75, ly + lh * 0.64, ltitle, ha="center", va="center", fontsize=6.9, fontweight="bold", color=ltc)
        ax.text(2.75, ly + lh * 0.28, ldesc, ha="center", va="center", fontsize=6.2, color=SLATE_TEXT)

    # Panel Derecho: Distribución por Suites Activas
    draw_rounded_box(ax, 5.55, 0.15, 5.30, 3.24, fc=SLATE_BG, ec=SLATE_BORDER, lw=1.0, radius=0.06)
    ax.text(8.20, 3.20, "DISTRIBUCIÓN POR MÓDULO Y SUITE DE PRUEBA (194 CASOS)",
            ha="center", va="center", fontsize=8.2, fontweight="bold", color=NAVY)

    suites = [
        ("Facturación SUNAT (Nubefact/CPE)", 23, BLUE),
        ("Seguridad & Webhooks HMAC Culqi", 26, BLUE),
        ("Autenticación JWT, Refresh & RBAC", 26, BLUE),
        ("Órdenes, Estados & Idempotencia JCS", 27, BLUE),
        ("Catálogo, Clientes, Salud & Coexist.", 23, BLUE),
        ("Frontend: Contexto, Tabs & Mappers", 36, RUST),
        ("Frontend: API, AuthGuard & Forms", 24, RUST),
        ("Frontend: Usabilidad ISO 25010 & PDF", 9, GREEN),
    ]
    base_y = 0.34
    row_h = 0.33
    bar_x0 = 7.90
    max_bar_w = 2.15
    max_val = 36.0

    for idx, (label, count, color) in enumerate(reversed(suites)):
        ry = base_y + idx * row_h
        ax.text(7.80, ry + 0.11, label, ha="right", va="center", fontsize=6.6, fontweight="bold", color=NAVY_MID)
        bw = (count / max_val) * max_bar_w
        rect = FancyBboxPatch((bar_x0, ry + 0.02), bw, 0.19,
                              boxstyle="round,pad=0.005,rounding_size=0.02",
                              fc=color, ec=color, lw=0.5)
        ax.add_patch(rect)
        ax.text(bar_x0 + bw + 0.08, ry + 0.11, f"{count} tests", ha="left", va="center",
                fontsize=6.6, fontweight="bold", color=color)

    out_path = os.path.join(ASSETS_DIR, "infog_qa_01_dashboard_piramide.png")
    fig.savefig(out_path, dpi=300, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    return out_path


# ==============================================================================
# FIGURA 2: ARQUITECTURA 3-CAPAS + TÉCNICAS ISO 29119-4 + MÁQUINA DE ESTADOS
# ==============================================================================
def generate_fig2_arquitectura_estados():
    fig = plt.figure(figsize=(11.0, 5.1), dpi=300, facecolor="white")
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, 11.0)
    ax.set_ylim(0, 5.1)
    ax.axis("off")

    # Banner Superior
    draw_rounded_box(ax, 0.15, 4.54, 10.7, 0.44, fc=NAVY, ec=BLUE, lw=1.5, radius=0.05)
    ax.text(5.5, 4.76, "FIGURA 2 — MAPA ARQUITECTÓNICO DE TÉCNICAS ISO/IEC/IEEE 29119-4 Y MÁQUINA DE ESTADOS",
            ha="center", va="center", fontsize=9.5, fontweight="bold", color="white")

    # Bloque Superior: 4 Columnas de Capas del SUT
    cols = [
        ("1. CAPA PRESENTACIÓN PWA", "React 19 · Vite 6 · Tailwind 4",
         "TÉCNICA ISO 29119-4:\n• Scenario Testing (Cl. 7.7)\n• Combinatorial UI Testing",
         "VERIFICACIÓN REAL:\n• Recorrido Catálogo -> Pago\n• Carrito Reactivo y Mappers\n• Accesibilidad WCAG 2.1 AA",
         BLUE_LIGHT, BLUE),
        ("2. CAPA API & MIDDLEWARES", "Node 20 · Express 4.19 · Zod",
         "TÉCNICA ISO 29119-4:\n• Branch Testing (Cl. 8.2)\n• Error Guessing (Cl. 9.1)",
         "VERIFICACIÓN REAL:\n• Ramas JWT 401 / RBAC 403\n• Firma HMAC timingSafeEqual\n• Rechazo Payload >100kb / 415",
         RUST_LIGHT, RUST),
        ("3. SERVICIOS DE DOMINIO", "Culqi API v2 · Nubefact OSE",
         "TÉCNICA ISO 29119-4:\n• Equivalence Part. (Cl. 7.2)\n• Decision Table (Cl. 7.4)",
         "VERIFICACIÓN REAL:\n• Clases DNI (8) y RUC (11)\n• Tabla Boleta BBB1 vs Factura FFF1\n• IGV 18% Exacto (Decimal.js)",
         "#EEF2FF", ROYAL),
        ("4. PERSISTENCIA ACID 3FN", "PostgreSQL 16 (Neon Cloud)",
         "TÉCNICA ISO 29119-4:\n• Boundary Value (Cl. 7.3)\n• Concurrency & DRP Drill",
         "VERIFICACIÓN REAL:\n• Fronteras Stock: -1, 0, 1, Max, Max+1\n• Bloqueo SELECT FOR UPDATE\n• Trigger trg_decrement_stock",
         GREEN_LIGHT, GREEN),
    ]

    col_w = 2.52
    col_gap = 0.20
    for i, (ctitle, csub, ctech, cverif, cbg, cec) in enumerate(cols):
        cx = 0.15 + i * (col_w + col_gap)
        draw_rounded_box(ax, cx, 2.38, col_w, 2.04, fc=cbg, ec=cec, lw=1.3, radius=0.05)
        draw_rounded_box(ax, cx + 0.06, 3.94, col_w - 0.12, 0.40, fc=cec, ec=cec, lw=0.8, radius=0.03)
        ax.text(cx + col_w / 2, 4.20, ctitle, ha="center", va="center", fontsize=6.9, fontweight="bold", color="white")
        ax.text(cx + col_w / 2, 4.03, csub, ha="center", va="center", fontsize=6.1, color="#F1F5F9")
        ax.text(cx + 0.12, 3.52, ctech, ha="left", va="center", fontsize=6.6, fontweight="bold", color=NAVY, linespacing=1.32)
        ax.plot([cx + 0.12, cx + col_w - 0.12], [3.15, 3.15], color=SLATE_BORDER, lw=0.8, ls="--")
        ax.text(cx + 0.12, 2.75, cverif, ha="left", va="center", fontsize=6.3, color=SLATE_TEXT, linespacing=1.32)

        if i < 3:
            arrow = FancyArrowPatch((cx + col_w + 0.02, 3.40), (cx + col_w + col_gap - 0.02, 3.40),
                                    arrowstyle="-|>", mutation_scale=11, color=NAVY, lw=1.4)
            ax.add_patch(arrow)

    # Bloque Inferior: Máquina de Estados Determinista
    draw_rounded_box(ax, 0.15, 0.15, 10.7, 2.10, fc=SLATE_BG, ec=SLATE_BORDER, lw=1.1, radius=0.06)
    ax.text(5.5, 2.08, "MÁQUINA DE ESTADOS DETERMINISTA DEL PEDIDO (stateMachine.ts · State Transition Testing ISO 29119-4 Cl. 7.5)",
            ha="center", va="center", fontsize=8.1, fontweight="bold", color=NAVY)

    states = [
        (0.32, 1.18, 1.38, 0.54, "PENDIENTE\n(RECIBIDO)", BLUE_LIGHT, BLUE, NAVY),
        (2.14, 1.18, 1.38, 0.54, "PAGADO\n(Webhook Culqi)", BLUE_LIGHT, BLUE, NAVY),
        (3.96, 1.18, 1.42, 0.54, "PREPARACION\n(Picking Textil)", BLUE_LIGHT, BLUE, NAVY),
        (5.82, 1.18, 1.38, 0.54, "EN_CAMINO\n(Despacho)", BLUE_LIGHT, BLUE, NAVY),
        (7.64, 1.18, 1.35, 0.54, "ENTREGADO\n(Cerrado OK)", GREEN_LIGHT, GREEN, GREEN),
        (9.45, 1.18, 1.22, 0.54, "REEMBOLSADO\n(Nota Créd.)", RUST_LIGHT, RUST, RUST),
    ]
    for sx, sy, sw, sh, stxt, sfc, sec, stc in states:
        draw_rounded_box(ax, sx, sy, sw, sh, fc=sfc, ec=sec, lw=1.4, radius=0.04)
        ax.text(sx + sw / 2, sy + sh / 2, stxt, ha="center", va="center", fontsize=6.6, fontweight="bold", color=stc)

    seq_arrows = [
        (1.70, 1.45, 2.14, 1.45, "Pago OK"),
        (3.52, 1.45, 3.96, 1.45, "PATCH"),
        (5.38, 1.45, 5.82, 1.45, "PATCH"),
        (7.20, 1.45, 7.64, 1.45, "PATCH"),
        (8.99, 1.45, 9.45, 1.45, "Refund"),
    ]
    for x1, y1, x2, y2, lbl in seq_arrows:
        a = FancyArrowPatch((x1, y1), (x2, y2), arrowstyle="-|>", mutation_scale=10, color=BLUE, lw=1.3)
        ax.add_patch(a)
        ax.text((x1 + x2) / 2, y1 + 0.15, lbl, ha="center", va="center", fontsize=5.8, fontweight="bold", color=BLUE)

    # Estado CANCELADO
    draw_rounded_box(ax, 3.45, 0.28, 2.65, 0.48, fc=RED_LIGHT, ec=RED, lw=1.3, radius=0.04)
    ax.text(4.77, 0.52, "CANCELADO (POST /api/orders/:id/cancel)\nRestituye Stock Atómicamente",
            ha="center", va="center", fontsize=6.4, fontweight="bold", color=RED)

    for cx_from in [1.01, 2.83, 4.67, 6.51]:
        a_canc = FancyArrowPatch((cx_from, 1.18), (4.77, 0.76), arrowstyle="-|>", mutation_scale=9,
                                 color=RED, lw=1.0, linestyle="--")
        ax.add_patch(a_canc)

    # Nota de Transición Inválida bloqueada
    draw_rounded_box(ax, 6.45, 0.28, 4.22, 0.48, fc="#FEF2F2", ec=RED, lw=1.1, radius=0.04)
    ax.text(8.56, 0.52, "REGLA STT (CP-05): Transición Ilegal (ej. ENTREGADO -> PENDIENTE)\nBloqueada con HTTP 409 Conflict (code: INVALID_TRANSITION)",
            ha="center", va="center", fontsize=6.2, fontweight="bold", color=RED)

    ax.text(1.75, 0.52, "Concurrencia ACID:\nSELECT ... FOR UPDATE\nEvita Race Conditions",
            ha="center", va="center", fontsize=6.4, fontweight="bold", color=NAVY_MID,
            bbox=dict(boxstyle="round,pad=0.28", fc="white", ec=SLATE_BORDER, lw=0.8))

    out_path = os.path.join(ASSETS_DIR, "infog_qa_02_arquitectura_estados.png")
    fig.savefig(out_path, dpi=300, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    return out_path


# ==============================================================================
# FIGURA 3: MATRIZ DE RIESGOS, COBERTURA DE CÓDIGO Y RENDIMIENTO SLA
# ==============================================================================
def generate_fig3_riesgos_cobertura_sla():
    fig = plt.figure(figsize=(11.0, 4.3), dpi=300, facecolor="white")
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, 11.0)
    ax.set_ylim(0, 4.3)
    ax.axis("off")

    draw_rounded_box(ax, 0.15, 3.74, 10.7, 0.42, fc=NAVY, ec=BLUE, lw=1.5, radius=0.05)
    ax.text(5.5, 3.95, "FIGURA 3 — COBERTURA ESTRUCTURAL POR MÓDULO, MATRIZ DE RIESGOS TÉCNICOS Y CUMPLIMIENTO SLA",
            ha="center", va="center", fontsize=9.4, fontweight="bold", color="white")

    # Panel 1: Cobertura Backend
    draw_rounded_box(ax, 0.15, 0.15, 3.55, 3.46, fc=SLATE_BG, ec=SLATE_BORDER, lw=1.0, radius=0.05)
    ax.text(1.92, 3.42, "COBERTURA BACKEND (LÓGICA CORE)", ha="center", va="center",
            fontsize=7.6, fontweight="bold", color=NAVY)

    cov_items = [
        ("password.utils", 100.0, GREEN),
        ("jwt.utils", 100.0, GREEN),
        ("validators (Zod)", 100.0, GREEN),
        ("routes (Express)", 100.0, GREEN),
        ("controllers (Branch)", 82.4, BLUE),
        ("middlewares (Auth)", 80.9, BLUE),
        ("memory.repos", 74.9, TEAL),
    ]
    for i, (mname, pct, col) in enumerate(reversed(cov_items)):
        ry = 0.32 + i * 0.41
        ax.text(1.48, ry + 0.12, mname, ha="right", va="center", fontsize=6.5, fontweight="bold", color=NAVY_MID)
        bw = (pct / 100.0) * 1.62
        draw_rounded_box(ax, 1.55, ry + 0.03, bw, 0.19, fc=col, ec=col, lw=0.5, radius=0.02)
        ax.text(1.55 + bw + 0.06, ry + 0.12, f"{pct:.1f}%", ha="left", va="center",
                fontsize=6.4, fontweight="bold", color=col)

    # Panel 2: Matriz de Riesgos
    draw_rounded_box(ax, 3.85, 0.15, 3.70, 3.46, fc=SLATE_BG, ec=SLATE_BORDER, lw=1.0, radius=0.05)
    ax.text(5.70, 3.42, "MATRIZ DE RIESGOS Y CONTROLES (ISO 29119)", ha="center", va="center",
            fontsize=7.6, fontweight="bold", color=NAVY)

    risks = [
        ("RSK-01: Timeout OSE Nubefact", "MEDIA / ALTO",
         "Cola asíncrona emitInvoiceWorker y reintentos sin bloquear checkout.", RUST_LIGHT, RUST),
        ("RSK-02: Race Condition Stock", "MEDIA / ALTO",
         "Transacción ACID con bloqueo pesimista SELECT ... FOR UPDATE.", RED_LIGHT, RED),
        ("RSK-03: Webhook Culqi Falsificado", "BAJA / CRÍTICO",
         "Firma HMAC-SHA256 con crypto.timingSafeEqual sobre rawBody.", RED_LIGHT, RED),
        ("RSK-04: Descuadre IGV 18%", "BAJA / MEDIO",
         "Aritmética exacta Decimal.js en splitIgv (tolerancia 0.00).", BLUE_LIGHT, BLUE),
    ]
    for idx, (rtitle, rlevel, rmit, rbg, rec) in enumerate(reversed(risks)):
        ry = 0.26 + idx * 0.75
        draw_rounded_box(ax, 3.98, ry, 3.44, 0.65, fc=rbg, ec=rec, lw=1.1, radius=0.04)
        ax.text(4.08, ry + 0.45, rtitle, ha="left", va="center", fontsize=6.5, fontweight="bold", color=NAVY)
        ax.text(7.32, ry + 0.45, rlevel, ha="right", va="center", fontsize=5.9, fontweight="bold", color=rec)
        ax.text(4.08, ry + 0.19, rmit, ha="left", va="center", fontsize=6.0, color=SLATE_TEXT)

    # Panel 3: SLAs y Criterios de Salida
    draw_rounded_box(ax, 7.70, 0.15, 3.15, 3.46, fc=SLATE_BG, ec=SLATE_BORDER, lw=1.0, radius=0.05)
    ax.text(9.27, 3.42, "MÉTRICAS VS. CRITERIOS DE SALIDA", ha="center", va="center",
            fontsize=7.6, fontweight="bold", color=NAVY)

    slas = [
        ("Tasa Aprobación (Pass Rate)", "Meta: 100%", "Actual: 100% (194/194)", "CONFORME", GREEN),
        ("Latencia API Transaccional p95", "Meta: <= 800 ms", "Actual: 342 ms", "CONFORME", GREEN),
        ("Recuperación Desastres (RTO)", "Meta: <= 15 min", "Actual: 3.2 seg (Neon)", "EXCELENTE", BLUE),
        ("Coexistencia ISO/IEC 25010", "Meta: Degrad. < 10%", "Actual: 1.7% Degrad.", "CONFORME", GREEN),
        ("Defectos Críticos / Bloqueantes", "Meta: 0 Abiertos", "Actual: 0 Defectos", "CONFORME", GREEN),
    ]
    for idx, (sname, smeta, sact, sstat, scol) in enumerate(reversed(slas)):
        ry = 0.25 + idx * 0.60
        draw_rounded_box(ax, 7.82, ry, 2.91, 0.52, fc="white", ec=scol, lw=1.0, radius=0.03)
        ax.text(7.92, ry + 0.35, sname, ha="left", va="center", fontsize=6.3, fontweight="bold", color=NAVY)
        ax.text(10.65, ry + 0.35, sstat, ha="right", va="center", fontsize=5.7, fontweight="bold", color=scol)
        ax.text(7.92, ry + 0.14, f"{smeta}  |  {sact}", ha="left", va="center", fontsize=5.9, color=SLATE_TEXT)

    out_path = os.path.join(ASSETS_DIR, "infog_qa_03_riesgos_cobertura_sla.png")
    fig.savefig(out_path, dpi=300, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    return out_path


# ==============================================================================
# COMPILADOR DE WORD (.DOCX) FORMATO INFOGRAFÍA EJECUTIVA FORMAL (4 HOJAS)
# ==============================================================================
def set_cell_bg(cell, hex_color):
    tcPr = cell._tc.get_or_add_tcPr()
    tcPr.append(parse_xml(f'<w:shd {nsdecls("w")} w:fill="{hex_color}"/>'))


def set_cell_margins(table, top=70, bottom=70, left=110, right=110):
    tblPr = table._tbl.tblPr
    tblPr.append(parse_xml(f'''
        <w:tblCellMar {nsdecls("w")}>
            <w:top w:w="{top}" w:type="dxa"/>
            <w:bottom w:w="{bottom}" w:type="dxa"/>
            <w:left w:w="{left}" w:type="dxa"/>
            <w:right w:w="{right}" w:type="dxa"/>
        </w:tblCellMar>
    '''))


def style_compact_table(table, header_bg="0F172A", header_fg=RGBColor(255, 255, 255), font_pt=8.0):
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    tblPr = table._tbl.tblPr
    tblPr.append(parse_xml(f'''
        <w:tblBorders {nsdecls("w")}>
            <w:top w:val="single" w:sz="10" w:space="0" w:color="0F172A"/>
            <w:bottom w:val="single" w:sz="10" w:space="0" w:color="0F172A"/>
            <w:insideH w:val="single" w:sz="4" w:space="0" w:color="CBD5E1"/>
            <w:left w:val="none"/>
            <w:right w:val="none"/>
            <w:insideV w:val="none"/>
        </w:tblBorders>
    '''))
    set_cell_margins(table, top=65, bottom=65, left=100, right=100)

    # Header row
    hdr_tr = table.rows[0]._tr.get_or_add_trPr()
    hdr_tr.append(parse_xml(f'<w:tblHeader {nsdecls("w")}/>'))
    hdr_tr.append(parse_xml(f'<w:cantSplit {nsdecls("w")}/>'))
    for cell in table.rows[0].cells:
        set_cell_bg(cell, header_bg)
        for p in cell.paragraphs:
            p.paragraph_format.space_before = Pt(1)
            p.paragraph_format.space_after = Pt(1)
            for r in p.runs:
                r.font.name = "Calibri"
                r.font.bold = True
                r.font.size = Pt(font_pt)
                r.font.color.rgb = header_fg

    # Data rows
    for r_idx in range(1, len(table.rows)):
        row = table.rows[r_idx]
        trPr = row._tr.get_or_add_trPr()
        trPr.append(parse_xml(f'<w:cantSplit {nsdecls("w")}/>'))
        bg = "F8FAFC" if (r_idx % 2 == 0) else "FFFFFF"
        for cell in row.cells:
            if bg != "FFFFFF":
                set_cell_bg(cell, bg)
            for p in cell.paragraphs:
                p.paragraph_format.space_before = Pt(1)
                p.paragraph_format.space_after = Pt(1)
                p.paragraph_format.line_spacing = 1.08
                for r in p.runs:
                    r.font.name = "Calibri"
                    r.font.size = Pt(font_pt)
                    if not r.font.color.rgb:
                        r.font.color.rgb = RGBColor(30, 41, 59)


def add_section_banner(doc, title_text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(7)
    p.paragraph_format.space_after = Pt(3)
    p.paragraph_format.keep_with_next = True
    pPr = p._p.get_or_add_pPr()
    pPr.append(parse_xml(f'<w:shd {nsdecls("w")} w:val="clear" w:color="auto" w:fill="EFF6FF"/>'))
    pPr.append(parse_xml(f'''
        <w:pBdr {nsdecls("w")}>
            <w:left w:val="single" w:sz="24" w:space="6" w:color="1665D8"/>
            <w:bottom w:val="single" w:sz="6" w:space="2" w:color="BFDBFE"/>
        </w:pBdr>
    '''))
    r = p.add_run("  " + title_text)
    r.font.name = "Calibri"
    r.font.bold = True
    r.font.size = Pt(9.8)
    r.font.color.rgb = RGBColor(15, 23, 42)
    return p


def add_populated_table(doc, headers, rows_data, font_pt=7.8):
    table = doc.add_table(rows=1 + len(rows_data), cols=len(headers))
    for c_idx, h_text in enumerate(headers):
        table.rows[0].cells[c_idx].text = h_text
    for r_idx, r_data in enumerate(rows_data):
        for c_idx, val in enumerate(r_data):
            cell = table.rows[r_idx + 1].cells[c_idx]
            cell.text = ""
            p = cell.paragraphs[0]
            # Si contiene "::" separamos parte en negrita
            if "::" in val:
                bold_part, rest_part = val.split("::", 1)
                rb = p.add_run(bold_part)
                rb.bold = True
                rb.font.color.rgb = RGBColor(15, 23, 42)
                rr = p.add_run(rest_part)
            else:
                rr = p.add_run(val)
    style_compact_table(table, font_pt=font_pt)
    return table


def build_executive_docx(fig1_path, fig2_path, fig3_path):
    doc = docx.Document()

    # Configurar página A4 con márgenes ejecutivos compactos (0.52 in = 1.32 cm)
    for section in doc.sections:
        section.page_width = Inches(8.27)
        section.page_height = Inches(11.69)
        section.top_margin = Inches(0.48)
        section.bottom_margin = Inches(0.48)
        section.left_margin = Inches(0.52)
        section.right_margin = Inches(0.52)

        # Header discreto
        hdr = section.header.paragraphs[0]
        hdr.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        rh = hdr.add_run("LEOFIT SOLUTIONS S.A.C. | PLAN DE PRUEBAS DE SOFTWARE (ISO/IEC/IEEE 29119-3 & 29119-4) · DOC-QA-29119-01")
        rh.font.name = "Calibri"
        rh.font.size = Pt(7.5)
        rh.font.color.rgb = RGBColor(100, 116, 139)

    # ==========================================================================
    # PÁGINA 1: PORTADA EJECUTIVA INTEGRADA + PROPÓSITO + FIGURA 1 + MÓDULOS SUT
    # ==========================================================================
    # Banner Hero Institucional (Tabla 1x1 con fondo Navy #0F172A)
    hero_tbl = doc.add_table(rows=1, cols=1)
    hero_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_cell_margins(hero_tbl, top=110, bottom=110, left=160, right=160)
    hc = hero_tbl.rows[0].cells[0]
    set_cell_bg(hc, "0F172A")
    hp = hc.paragraphs[0]
    hp.paragraph_format.space_before = Pt(0)
    hp.paragraph_format.space_after = Pt(2)
    r_inst = hp.add_run("UNIVERSIDAD TECNOLÓGICA DEL PERÚ (UTP) · CURSO INTEGRADOR II: SOFTWARE (SECCIÓN 35374 · CICLO 2026-I)\n")
    r_inst.font.name = "Calibri"
    r_inst.font.size = Pt(8.0)
    r_inst.font.bold = True
    r_inst.font.color.rgb = RGBColor(147, 197, 253)

    r_title = hp.add_run("PLAN DE PRUEBAS DE SOFTWARE — SÍNTESIS EJECUTIVA E INFOGRÁFICA\n")
    r_title.font.name = "Calibri"
    r_title.font.size = Pt(14.5)
    r_title.font.bold = True
    r_title.font.color.rgb = RGBColor(255, 255, 255)

    r_sub = hp.add_run("Sistema Web PWA de Gestión de Pedidos, Facturación Electrónica SUNAT (UBL 2.1) y Control de Inventario Multicanal — LeoFit Solutions")
    r_sub.font.name = "Calibri"
    r_sub.font.size = Pt(9.0)
    r_sub.font.color.rgb = RGBColor(203, 213, 225)

    # Ficha de Metadatos y Control de Versiones (Secciones 1, 2 y 3 consolidadas)
    meta_rows = [
        ["Código / Versión:: DOC-QA-29119-01 (v2.4.0 — 06/11/2026)",
         "Estándares:: ISO/IEC/IEEE 29119-3 (Estructura) · 29119-4 (Técnicas) · ISO 25010",
         "Docente Evaluador:: Ing. Enrique Lee Huamani Uriarte"],
        ["QA Lead Senior:: Jim A. Dávila Morales (U18206081)",
         "Scrum Master / DevSecOps:: Lady L. Loayza Rodríguez (U22221489)",
         "Equipo G01:: V. Cárdenas (PO/DBA) · H. Roman (FE) · D. Rojas (BA/Cloud)"],
        ["Historial Versiones:: v1.0 (14/09 APF1 Auth/Mocks) -> v2.0 (18/10 APF2 Culqi/Catálogo) -> v2.4 (06/11 Final: 194 Tests, CPE Nubefact & DRP)",
         "Repositorio Auditado:: github.com/Leofit-Solutions-Grupo01/leofit-pedidos-sistema",
         "Estado Global QA:: 194 / 194 Pruebas Aprobadas (100% Pass · 0 Defectos Críticos)"]
    ]
    meta_tbl = doc.add_table(rows=3, cols=3)
    for r_i, r_d in enumerate(meta_rows):
        for c_i, val in enumerate(r_d):
            cell = meta_tbl.rows[r_i].cells[c_i]
            set_cell_bg(cell, "F1F5F9" if r_i % 2 == 0 else "FFFFFF")
            p = cell.paragraphs[0]
            p.paragraph_format.space_before = Pt(1)
            p.paragraph_format.space_after = Pt(1)
            b_part, rest = val.split("::", 1)
            rb = p.add_run(b_part + ":")
            rb.font.name = "Calibri"
            rb.font.bold = True
            rb.font.size = Pt(7.5)
            rb.font.color.rgb = RGBColor(22, 101, 216)
            rr = p.add_run(rest)
            rr.font.name = "Calibri"
            rr.font.size = Pt(7.5)
            rr.font.color.rgb = RGBColor(15, 23, 42)
    set_cell_margins(meta_tbl, top=45, bottom=45, left=80, right=80)

    # Sección 4, 5, 6, 7, 8: Propósito, Alcance, Objetivos y Referencias
    add_section_banner(doc, "1. PROPÓSITO, ALCANCE ARQUITECTÓNICO, OBJETIVOS DE CALIDAD Y MARCO NORMATIVO (SECC. 4 A 8)")
    p_intro = doc.add_paragraph()
    p_intro.paragraph_format.space_before = Pt(2)
    p_intro.paragraph_format.space_after = Pt(3)
    p_intro.paragraph_format.line_spacing = 1.08
    r1 = p_intro.add_run(
        "Propósito y Alcance: Verificar y validar integralmente la plataforma LeoFit Solutions en sus 3 capas reales: "
        "Frontend PWA (React 19, Vite 6, TailwindCSS 4), Backend API REST (Node.js 20, Express 4.19, TypeScript 5.4, Zod) "
        "y Persistencia Relacional (PostgreSQL 16 en Neon Serverless bajo 3FN/BCNF), junto con pasarelas Sandbox (Culqi API v2 y Nubefact OSE). "
        "Objetivos Cuantitativos: (1) 100% conformidad funcional en módulos core; (2) 0.00 discrepancia aritmética en IGV 18% vía Decimal.js; "
        "(3) Mitigación total OWASP Top 10 (JWT HS256, RBAC ADMIN/OPERATOR, HMAC-SHA256 con timingSafeEqual); "
        "(4) Latencia transaccional p95 <= 800 ms (medido: 342 ms); (5) Continuidad DRP con RTO <= 15 min (medido: 3.2 s) y RPO = 0 s."
    )
    r1.font.name = "Calibri"
    r1.font.size = Pt(8.0)
    r1.font.color.rgb = RGBColor(30, 41, 59)

    # Insertar FIGURA 1
    p_fig1 = doc.add_paragraph()
    p_fig1.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_fig1.paragraph_format.space_before = Pt(2)
    p_fig1.paragraph_format.space_after = Pt(2)
    p_fig1.add_run().add_picture(fig1_path, width=Inches(7.15))

    # Sección 9 y 10: Elementos de Prueba (Módulos Reales) y Alcance Funcional
    add_section_banner(doc, "2. ELEMENTOS DE PRUEBA (MÓDULOS REALES DEL REPOSITORIO) Y EXCLUSIONES (SECC. 9 Y 10)")
    mod_headers = ["ID", "Módulo / Controlador Real", "Endpoints Reales y Tablas PostgreSQL 16", "Alcance In-Scope vs. Exclusiones Out-of-Scope"]
    mod_rows = [
        ["MOD-01", "Autenticación y RBAC::\nauth.controller.ts",
         "POST /api/auth/login, /refresh, /logout, /register\nGET /api/auth/me, /profile | Tabla: users",
         "In-Scope:: JWT HS256, HttpOnly cookies, bloqueo por rol (ADMIN vs OPERATOR) y rate-limiting."],
        ["MOD-02", "Catálogo e Inventario::\nproduct.controller.ts",
         "GET/POST /api/products, PUT/DELETE /:id\nPATCH /variant/:variantId/stock | product_variants",
         "In-Scope:: Variantes por talla (sizes) y color (colors), SKU único y vista vw_low_stock_alert."],
        ["MOD-03", "Pedidos y Máquina Estados::\norder.controller.ts",
         "POST /api/orders, PATCH /:id/status, POST /:id/cancel\nGET /track/:orderNumber | orders, order_items",
         "In-Scope:: Idempotency-Key (JCS), cálculo flete Lima/Provincia, trigger trg_decrement_stock."],
        ["MOD-04", "Pasarela Pagos y Webhooks::\npaymentWebhook.controller.ts",
         "POST /api/webhooks/:provider (culqi)\nPOST /api/orders/:id/payment-link | Tabla: payments",
         "In-Scope:: Firma HMAC-SHA256 sobre rawBody, idempotencia de cargos y reembolsos (/refund)."],
        ["MOD-05", "Facturación SUNAT CPE::\ninvoice.controller.ts",
         "GET /api/invoices/order/:orderId, /:id/pdf, /:id/xml\nPOST /order/:id/credit-note, GET /api/sunat/ruc/:numero",
         "In-Scope:: Boleta (BBB1), Factura (FFF1), Nota Crédito (FC01/BC01) vía Nubefact y CDR."],
        ["MOD-06", "Clientes, Salud y DRP::\nclient / dashboard / health",
         "GET/POST /api/clients, GET /api/dashboard/stats\nGET /health/live, /ready | backup_strategy.sh",
         "Out-of-Scope (Excluido):: Cobro bancario real en producción, Guía Remisión GRE y GPS en vivo."]
    ]
    add_populated_table(doc, mod_headers, mod_rows, font_pt=7.5)

    doc.add_page_break()

    # ==========================================================================
    # PÁGINA 2: ENFOQUE, NIVELES, TÉCNICAS ISO 29119-4 + FIGURA 2 + ENTORNOS/HERRAMIENTAS
    # ==========================================================================
    add_section_banner(doc, "3. ENFOQUE SHIFT-LEFT, NIVELES DE PRUEBA Y TÉCNICAS ISO/IEC/IEEE 29119-4 (SECC. 11, 12 Y 13)")

    # Insertar FIGURA 2
    p_fig2 = doc.add_paragraph()
    p_fig2.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_fig2.paragraph_format.space_before = Pt(2)
    p_fig2.paragraph_format.space_after = Pt(3)
    p_fig2.add_run().add_picture(fig2_path, width=Inches(7.15))

    tech_headers = ["Técnica ISO/IEC/IEEE 29119-4", "Módulo / Endpoint Real", "Justificación por Riesgo Técnico o de Negocio", "Clases / Condiciones Evaluadas"]
    tech_rows = [
        ["Partición de Equivalencia (EP)::\nCláusula 7.2 (Caja Negra)",
         "MOD-05 & MOD-06::\nGET /api/sunat/ruc/:numero\nPOST /api/clients",
         "Evita rechazos fiscales en el OSE Nubefact por documentos tributarios malformados antes de emitir el XML UBL 2.1.",
         "Válidas: DNI (8 dígitos), RUC (11 dígitos prefijo 10/20).\nInválidas: longitud != 8/11, letras, RUC sin estado ACTIVO."],
        ["Análisis Valores Límite (BVA)::\nCláusula 7.3 (Caja Negra)",
         "MOD-02 & MOD-03::\nPATCH /variant/:id/stock\nPOST /api/orders",
         "Los errores críticos de sobre-venta textil (over-selling) ocurren exactamente en las fronteras numéricas de inventario.",
         "Fronteras evaluadas: stock = -1 (400 Bad Request), stock = 0 (Agotado), stock = 1 (Alerta), stock = disp, disp + 1 (Rechazo)."],
        ["Tablas de Decisión (DTT)::\nCláusula 7.4 (Caja Negra)",
         "MOD-03 & MOD-05::\norders.controller.ts\nnubefact.service.ts",
         "Gobierna la lógica combinatoria de facturación y logística según tipo de cliente, destino geográfico y confirmación de pago.",
         "Reglas: [Envío: Lima / Provincia] x [Doc: DNI->Boleta BBB1 / RUC->Factura FFF1] x [Pago Culqi: OK / Fallido]."],
        ["Transición de Estados (STT)::\nCláusula 7.5 (Caja Negra)",
         "MOD-03::\nstateMachine.ts\nPATCH /api/orders/:id/status",
         "Impide saltos operacionales ilegales o retrocesos de pedidos ya entregados o cancelados mediante bloqueo FOR UPDATE.",
         "Secuencia: PENDIENTE -> PAGADO -> PREPARACION -> EN_CAMINO -> ENTREGADO. Salto ilegal -> HTTP 409 INVALID_TRANSITION."],
        ["Pruebas de Escenario / E2E::\nCláusula 7.7 (Caja Negra)",
         "Full-Stack::\nCatálogo PWA -> Carrito ->\nCulqi -> CPE PDF",
         "Valida la integración real entre componentes React 19, contratos API Express y persistencia de comprobantes.",
         "Viaje completo del usuario comprador y del operador logístico descargando comprobante y rótulo térmico."],
        ["Branch Testing & Error Guessing::\nCláusulas 8.2 y 9.1",
         "MOD-01 & MOD-04::\nauth.middleware.ts\npaymentWebhook.controller",
         "Garantiza cobertura >80% en ramas de seguridad y resistencia contra webhooks falsificados o ataques de replay.",
         "Ramas: Token ausente (401), expirado (401), rol OPERATOR en ruta ADMIN (403), firma HMAC alterada (401)."]
    ]
    add_populated_table(doc, tech_headers, tech_rows, font_pt=7.4)

    # Sección 14, 15, 16, 17, 18: Entornos, Datos, Herramientas, Roles y Cronograma
    add_section_banner(doc, "4. ENTORNOS, DATOS DE PRUEBA, HERRAMIENTAS, ROLES Y CRONOGRAMA (SECC. 14 A 18)")
    ops_headers = ["Dimensión del Plan", "Especificación Técnica Verificada en el Proyecto LeoFit Solutions"]
    ops_rows = [
        ["14. Entornos de Prueba::",
         "1) Local/DEV: Node.js 20 + PostgreSQL 16 Docker (puerto 5432).  2) CI Pipeline: GitHub Actions (ubuntu-latest) con contenedor efímero PostgreSQL.  3) Staging/QA: Render Web Service + Neon Serverless PostgreSQL (branch qa_staging) conectado a Culqi Sandbox y Nubefact Demo."],
        ["15. Datos de Prueba (Seeds)::",
         "Roles Reales: admin@leofit.pe (ADMIN), operador@leofit.pe (OPERATOR). Tarjetas Sandbox Culqi: 4111...1111 (Aprobada), 4000...0002 (Fondos insuf.). RUC Prueba SUNAT: 20100070970 (Activo/Habido). SKUs: POLO-DRY-BLK-M (stock 15), LEG-FIT-NAVY-S (stock 0)."],
        ["16. Herramientas QA::",
         "Backend: Jest v29.7 + Supertest v6.3 (125 tests). Frontend: Vitest v4.1 + React Testing Library v16.3 + jsdom (69 tests). Rendimiento/Coexistencia: k6 + Python ISO 25010 scripts. CI/CD: GitHub Actions. Gestión Defectos: GitHub Issues con etiquetas de severidad."],
        ["17. Roles y Responsables::",
         "QA Lead Senior: Jim Dávila (Diseño 29119, suites Supertest, liberación). DevSecOps/SM: Lady Loayza (Pipeline CI, seguridad HMAC/JWT). PO/DBA: Víctor Cárdenas (Datos BCNF, simulacro DRP). Frontend Lead: Harley Roman (Suites Vitest/WCAG). BA/Cloud: Daniel Rojas (SUNAT/k6)."],
        ["18. Cronograma Ejecutado::",
         "Fase 1 (Sem 06-08): Pruebas Unitarias Dominio [100%]. Fase 2 (Sem 09-12): Integración API y BD [100%]. Fase 3 (Sem 13-15): Pasarelas Culqi y Nubefact OSE [100%]. Fase 4 (Sem 16-17): Carga k6, Coexistencia ISO 25010 y Simulacro DRP [100%]. Fase 5 (Sem 18): Cierre y Sustentación."]
    ]
    add_populated_table(doc, ops_headers, ops_rows, font_pt=7.5)

    doc.add_page_break()

    # ==========================================================================
    # PÁGINA 3: RIESGOS, MÉTRICAS, CRITERIOS (FIGURA 3) + TRAZABILIDAD Y CASOS + FIRMAS
    # ==========================================================================
    add_section_banner(doc, "5. RIESGOS, CRITERIOS DE ENTRADA/SALIDA, INCIDENTES Y MÉTRICAS DE CALIDAD (SECC. 19 A 23)")

    # Insertar FIGURA 3
    p_fig3 = doc.add_paragraph()
    p_fig3.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_fig3.paragraph_format.space_before = Pt(2)
    p_fig3.paragraph_format.space_after = Pt(3)
    p_fig3.add_run().add_picture(fig3_path, width=Inches(7.15))

    gov_headers = ["Componente de Gobernanza", "Criterios, Umbrales y Protocolos Oficiales Aplicados"]
    gov_rows = [
        ["20. Criterios Entrada / Salida::",
         "Entrada: Compilación limpia tsc --noEmit, esquema BCNF migrado, credenciales Sandbox activas.  Salida: 100% pass rate (194/194 tests), 0 defectos críticos/bloqueantes, cobertura de ramas >80% en lógica core, p95 <= 800 ms y RTO DRP <= 15 min."],
        ["21. Entregables de Prueba::",
         "(1) Plan de Pruebas ISO/IEC/IEEE 29119-3; (2) 27 suites automatizadas en repositorio (125 BE + 69 FE); (3) Logs de auditoría CI/CD en GitHub Actions; (4) Informe Experimental de Coexistencia ISO/IEC 25010; (5) Acta de Simulacro DRP (BACKUP_RESTORE_DRILL.md)."],
        ["22. Gestión de Defectos (SLA)::",
         "Taxonomía en GitHub Issues: Bloqueante (Caída total / fallo cobro -> Hotfix < 4h, detiene release); Crítica (Fallo CPE SUNAT / corrupción stock -> < 12h); Mayor (Filtros / UI secundaria -> < 48h); Menor (Ajustes cosméticos CSS -> siguiente sprint)."]
    ]
    add_populated_table(doc, gov_headers, gov_rows, font_pt=7.4)

    # Sección 24 y 25: Matriz Unificada de Trazabilidad y Casos de Prueba Representativos de Alto Nivel
    add_section_banner(doc, "6. MATRIZ DE TRAZABILIDAD Y CASOS DE PRUEBA REPRESENTATIVOS DE ALTO NIVEL (SECC. 24 Y 25)")
    tc_headers = ["ID / Prioridad", "Requisito y Riesgo Mitigado", "Técnica ISO 29119-4", "Precondición, Entrada y Pasos de Ejecución", "Resultado Esperado y Oráculo de Verificación"]
    tc_rows = [
        ["CP-01::\nPrioridad: ALTA",
         "RF-01: Control Acceso RBAC\nMitiga: Escalada privilegios",
         "Branch Testing (Cl. 8.2)\n+ Error Guessing",
         "Pre: Usuario autenticado con rol OPERATOR.\nPaso: Enviar POST /api/products con Bearer JWT de operador intentando crear prenda.",
         "HTTP 403 Forbidden:: Middleware requireRole('ADMIN') bloquea mutación y registra intento en log de auditoría."],
        ["CP-02::\nPrioridad: ALTA",
         "RF-02: Integridad de Stock\nMitiga: RSK-02 (Over-selling)",
         "Boundary Value Analysis\n(BVA — Cl. 7.3)",
         "Pre: Variante id=1 con stock disponible = 5.\nPaso: 1) PATCH /api/products/variant/1/stock con -1. 2) Crear orden por 6 unidades.",
         "HTTP 400 Bad Request:: Validador Zod y trigger trg_decrement_stock impiden saldo negativo; stock permanece íntegro."],
        ["CP-03::\nPrioridad: ALTA",
         "RF-03: Orden Idempotente\nMitiga: Doble cargo por red",
         "Partición Equivalencia\n+ Idempotencia JCS",
         "Pre: Cliente y variante activos.\nPaso: Enviar 2 peticiones POST /api/orders idénticas con misma cabecera Idempotency-Key.",
         "HTTP 201 / 200 OK:: Primera petición crea pedido; segunda retorna respuesta cacheada sin duplicar fila en tabla orders."],
        ["CP-04::\nPrioridad: CRÍTICA",
         "RF-04: Webhook Seguro Culqi\nMitiga: RSK-03 (Spoofing)",
         "Error Guessing (Cl. 9.1)\nFirma Criptográfica",
         "Pre: Orden en estado PENDIENTE.\nPaso: Enviar POST /api/webhooks/culqi con payload válido pero cabecera HMAC-SHA256 alterada.",
         "HTTP 401 Unauthorized:: crypto.timingSafeEqual rechaza la firma; la orden no cambia a PAGADO ni emite factura."],
        ["CP-05::\nPrioridad: ALTA",
         "RF-05: Ciclo de Vida Pedido\nMitiga: Corrupción logística",
         "State Transition Testing\n(STT — Cl. 7.5)",
         "Pre: Pedido en estado final ENTREGADO.\nPaso: Operador envía PATCH /api/orders/:id/status con body {\"status\": \"PENDIENTE\"}.",
         "HTTP 409 Conflict:: stateMachine.ts rechaza transición ilegal devolviendo código INVALID_TRANSITION."],
        ["CP-06::\nPrioridad: ALTA",
         "RF-06: Emisión CPE SUNAT\nMitiga: RSK-01 & RSK-04",
         "Decision Table (Cl. 7.4)\n+ EP (RUC 11 dígitos)",
         "Pre: Pedido PAGADO con RUC 20100070970.\nPaso: Invocar emisión CPE y consultar GET /api/invoices/order/:orderId y /:id/xml.",
         "HTTP 200 OK:: Serie FFF1 correlativa generada sin brechas, IGV 18% exacto (Decimal.js) y estado ACEPTADO en OSE."]
    ]
    add_populated_table(doc, tc_headers, tc_rows, font_pt=7.2)

    # Sección 26: Aprobaciones y Firmas Oficiales
    add_section_banner(doc, "7. APROBACIONES Y CONFORMIDAD DEL PLAN DE PRUEBAS (SECC. 26)")
    sig_tbl = doc.add_table(rows=2, cols=3)
    sig_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    sigs = [
        ("Jim Alessandro Dávila Morales", "QA Engineer Lead Senior / Backend (U18206081)\nEstado: APROBADO Y EJECUTADO"),
        ("Lady Luz Loayza Rodríguez", "Scrum Master / DevSecOps Lead (U22221489)\nEstado: APROBADO EN PIPELINE CI/CD"),
        ("Ing. Enrique Lee Huamani Uriarte", "Docente Asesor Evaluador — UTP\nCurso Integrador II: Software (2026-I)")
    ]
    for c_i, (name, role) in enumerate(sigs):
        c_top = sig_tbl.rows[0].cells[c_i]
        c_bot = sig_tbl.rows[1].cells[c_i]
        set_cell_bg(c_top, "F8FAFC")
        set_cell_bg(c_bot, "F1F5F9")
        p_t = c_top.paragraphs[0]
        p_t.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_t.paragraph_format.space_before = Pt(8)
        p_t.paragraph_format.space_after = Pt(2)
        rt = p_t.add_run("________________________________________\n" + name)
        rt.font.name = "Calibri"
        rt.font.bold = True
        rt.font.size = Pt(8.0)
        rt.font.color.rgb = RGBColor(15, 23, 42)

        p_b = c_bot.paragraphs[0]
        p_b.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_b.paragraph_format.space_before = Pt(1)
        p_b.paragraph_format.space_after = Pt(3)
        rb = p_b.add_run(role)
        rb.font.name = "Calibri"
        rb.font.size = Pt(7.2)
        rb.font.color.rgb = RGBColor(71, 85, 105)
    set_cell_margins(sig_tbl, top=40, bottom=40, left=80, right=80)

    # Guardar en ubicaciones oficiales
    out_docx_main = os.path.join(DOCS_PLAN_DIR, "PLAN_DE_PRUEBAS_SOFTWARE_ISO29119.docx")
    doc.save(out_docx_main)

    if os.path.exists(DOCX_LOCAL_DIR):
        shutil.copy2(out_docx_main, os.path.join(DOCX_LOCAL_DIR, "PLAN_DE_PRUEBAS_SOFTWARE_ISO29119.docx"))

    print(" -> Word (.docx) Ejecutivo generado en:", out_docx_main)
    return out_docx_main


# ==============================================================================
# COMPILADOR DE HTML Y PDF A4 VERTICAL CON GRÁFICOS EMBEBIDOS (3-4 PÁGINAS)
# ==============================================================================
def build_executive_html_and_pdf():
    common_css = """
    <style>
      * { box-sizing: border-box; margin: 0; padding: 0; }
      body {
        font-family: 'Segoe UI', Calibri, Arial, sans-serif;
        font-size: 7.8pt;
        line-height: 1.26;
        color: #1E293B;
        background-color: #FFFFFF;
      }
      .hero-box {
        background-color: #0F172A;
        color: #FFFFFF;
        padding: 8px 12px;
        border-bottom: 2.5px solid #1665D8;
        margin-bottom: 5px;
      }
      .hero-sup {
        font-size: 6.8pt;
        font-weight: bold;
        color: #93C5FD;
        text-transform: uppercase;
      }
      .hero-title {
        font-size: 12.5pt;
        font-weight: bold;
        color: #FFFFFF;
        margin: 1px 0;
      }
      .hero-sub {
        font-size: 7.6pt;
        color: #CBD5E1;
      }
      .sec-banner {
        background-color: #EFF6FF;
        border-left: 3.5px solid #1665D8;
        border-bottom: 1px solid #BFDBFE;
        color: #0F172A;
        font-weight: bold;
        font-size: 8.2pt;
        padding: 2.5px 7px;
        margin-top: 5px;
        margin-bottom: 3px;
        text-transform: uppercase;
      }
      p.compact-p {
        font-size: 7.4pt;
        margin-bottom: 4px;
        text-align: justify;
        color: #334155;
      }
      table.infog-table {
        width: 100%;
        border-collapse: collapse;
        margin-bottom: 4px;
        font-size: 7.0pt;
      }
      table.infog-table th {
        background-color: #0F172A;
        color: #FFFFFF;
        font-weight: bold;
        text-align: left;
        padding: 3px 5px;
        border-top: 1px solid #0F172A;
        border-bottom: 1px solid #0F172A;
      }
      table.infog-table td {
        padding: 2.8px 5px;
        border-bottom: 0.5px solid #CBD5E1;
        vertical-align: top;
      }
      table.infog-table tr.alt td {
        background-color: #F8FAFC;
      }
      table.meta-table {
        width: 100%;
        border-collapse: collapse;
        margin-bottom: 4px;
        font-size: 6.9pt;
      }
      table.meta-table td {
        padding: 2.5px 5px;
        border: 0.5px solid #CBD5E1;
        background-color: #F8FAFC;
      }
      .fig-box {
        text-align: center;
        margin: 3px 0;
      }
      .page-hdr {
        font-size: 6.8pt;
        color: #64748B;
        text-align: right;
        border-bottom: 0.5px solid #CBD5E1;
        padding-bottom: 2px;
        margin-bottom: 4px;
      }
      .lbl-blue { color: #1665D8; font-weight: bold; }
      .lbl-navy { color: #0F172A; font-weight: bold; }
      .lbl-red { color: #B91C1C; font-weight: bold; }
      .lbl-green { color: #15803D; font-weight: bold; }
    </style>
    """

    page1_body = """
      <div class="hero-box">
        <div class="hero-sup">Universidad Tecnológica del Perú (UTP) &bull; Curso Integrador II: Software (Sección 35374 &bull; Ciclo 2026-I)</div>
        <div class="hero-title">PLAN DE PRUEBAS DE SOFTWARE — SÍNTESIS EJECUTIVA E INFOGRÁFICA</div>
        <div class="hero-sub">Sistema Web PWA de Gestión de Pedidos, Facturación Electrónica SUNAT (UBL 2.1) y Control de Inventario Multicanal — LeoFit Solutions</div>
      </div>

      <table class="meta-table">
        <tr>
          <td style="width:34%;"><span class="lbl-blue">Código / Versión:</span> DOC-QA-29119-01 (v2.4.0 — 06/11/2026)</td>
          <td style="width:36%;"><span class="lbl-blue">Marco Rector:</span> ISO/IEC/IEEE 29119-3 &amp; 29119-4 · ISO 25010</td>
          <td style="width:30%;"><span class="lbl-blue">Docente Asesor:</span> Ing. Enrique Lee Huamani Uriarte</td>
        </tr>
        <tr>
          <td><span class="lbl-blue">QA Lead Senior:</span> Jim A. Dávila Morales (U18206081)</td>
          <td><span class="lbl-blue">Scrum Master / DevSecOps:</span> Lady L. Loayza R. (U22221489)</td>
          <td><span class="lbl-blue">Equipo G01:</span> V. Cárdenas · H. Roman · D. Rojas</td>
        </tr>
        <tr>
          <td colspan="2"><span class="lbl-blue">Control de Versiones:</span> v1.0 (14/09 APF1 Auth/Mocks) &rarr; v2.0 (18/10 APF2 Culqi/Catálogo) &rarr; v2.4 (06/11 Final: 194 Tests, CPE Nubefact &amp; DRP)</td>
          <td><span class="lbl-green">Dictamen QA:</span> 194 / 194 Tests Aprobados (100%)</td>
        </tr>
      </table>

      <div class="sec-banner">1. Propósito, Alcance Arquitectónico, Objetivos Cuantitativos y Referencias (Secciones 4 a 8)</div>
      <p class="compact-p">
        <span class="lbl-navy">Propósito y Alcance:</span> Establecer la verificación y validación formal del sistema real <b>LeoFit Solutions</b> en sus 3 capas:
        <b>Frontend PWA</b> (React 19, Vite 6, TailwindCSS 4), <b>Backend API REST</b> (Node.js 20, Express 4.19, TypeScript 5.4, Zod) y <b>Base de Datos Relacional</b> (PostgreSQL 16 en Neon Serverless bajo 3FN/BCNF), integrando Culqi Sandbox y Nubefact OSE.
        <span class="lbl-navy">Objetivos y Normativa:</span> (1) 100% conformidad funcional; (2) 0.00 discrepancia en IGV 18% vía <code>Decimal.js</code> (Res. 097-2012/SUNAT);
        (3) Mitigación OWASP ASVS v4.0.3 (JWT HS256, RBAC, HMAC-SHA256 con <code>timingSafeEqual</code>); (4) Latencia p95 &le; 800 ms (medido: 342 ms); (5) Continuidad DRP con RTO &le; 15 min (medido: 3.2 s) y RPO = 0 s.
      </p>

      <div class="fig-box">
        <img src="infog_qa_01_dashboard_piramide.png" width="525">
      </div>

      <div class="sec-banner">2. Elementos Bajo Prueba (Módulos Reales del Repositorio) y Alcance Funcional (Secciones 9 y 10)</div>
      <table class="infog-table">
        <thead>
          <tr>
            <th style="width:8%;">ID</th>
            <th style="width:22%;">Módulo / Controlador Real</th>
            <th style="width:35%;">Endpoints Reales y Tablas PostgreSQL 16</th>
            <th style="width:35%;">Alcance In-Scope vs. Exclusiones Out-of-Scope</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td><b>MOD-01</b></td>
            <td><b>Autenticación y RBAC</b><br><code>auth.controller.ts</code></td>
            <td><code>POST /api/auth/login</code>, <code>/refresh</code>, <code>/logout</code>, <code>/register</code><br><code>GET /api/auth/me</code>, <code>/profile</code> | Tabla: <code>users</code></td>
            <td><b>In-Scope:</b> JWT HS256, HttpOnly cookies, control RBAC (<code>ADMIN</code> vs <code>OPERATOR</code>) y rate-limiting.</td>
          </tr>
          <tr class="alt">
            <td><b>MOD-02</b></td>
            <td><b>Catálogo e Inventario</b><br><code>product.controller.ts</code></td>
            <td><code>GET/POST /api/products</code>, <code>PUT/DELETE /:id</code><br><code>PATCH /variant/:variantId/stock</code> | <code>product_variants</code></td>
            <td><b>In-Scope:</b> Variantes por talla (<code>sizes</code>) y color (<code>colors</code>), SKU único y vista <code>vw_low_stock_alert</code>.</td>
          </tr>
          <tr>
            <td><b>MOD-03</b></td>
            <td><b>Pedidos y Estados</b><br><code>order.controller.ts</code></td>
            <td><code>POST /api/orders</code>, <code>PATCH /:id/status</code>, <code>POST /:id/cancel</code><br><code>GET /track/:orderNumber</code> | <code>orders</code>, <code>order_items</code></td>
            <td><b>In-Scope:</b> <code>Idempotency-Key</code> (JCS), flete Lima/Provincia, trigger <code>trg_decrement_stock</code>.</td>
          </tr>
          <tr class="alt">
            <td><b>MOD-04</b></td>
            <td><b>Pagos y Webhooks Culqi</b><br><code>paymentWebhook.controller.ts</code></td>
            <td><code>POST /api/webhooks/:provider</code> (culqi)<br><code>POST /api/orders/:id/payment-link</code> | Tabla: <code>payments</code></td>
            <td><b>In-Scope:</b> Firma HMAC-SHA256 sobre <code>rawBody</code>, idempotencia de cargos y reembolsos (<code>/refund</code>).</td>
          </tr>
          <tr>
            <td><b>MOD-05</b></td>
            <td><b>Facturación SUNAT CPE</b><br><code>invoice.controller.ts</code></td>
            <td><code>GET /api/invoices/order/:orderId</code>, <code>/:id/pdf</code>, <code>/:id/xml</code><br><code>POST /order/:id/credit-note</code>, <code>GET /api/sunat/ruc/:numero</code></td>
            <td><b>In-Scope:</b> Boleta (<code>BBB1</code>), Factura (<code>FFF1</code>), Nota Crédito (<code>FC01/BC01</code>) vía Nubefact y CDR.</td>
          </tr>
          <tr class="alt">
            <td><b>MOD-06</b></td>
            <td><b>Clientes, Salud y DRP</b><br><code>client / dashboard / health</code></td>
            <td><code>GET/POST /api/clients</code>, <code>GET /api/dashboard/stats</code><br><code>GET /health/live</code>, <code>/ready</code> | <code>backup_strategy.sh</code></td>
            <td><span class="lbl-red">Out-of-Scope (Excluido):</span> Cobro con tarjetas reales en producción, Guía Remisión GRE y GPS en vivo.</td>
          </tr>
        </tbody>
      </table>
    """

    page2_body = """
      <div class="page-hdr">LEOFIT SOLUTIONS S.A.C. | PLAN DE PRUEBAS DE SOFTWARE (ISO/IEC/IEEE 29119-3 &amp; 29119-4) &bull; PÁGINA 2 DE 3</div>
      <div class="sec-banner">3. Enfoque Shift-Left, Niveles de Prueba y Técnicas ISO/IEC/IEEE 29119-4 (Secciones 11, 12 y 13)</div>

      <div class="fig-box">
        <img src="infog_qa_02_arquitectura_estados.png" width="485">
      </div>

      <table class="infog-table">
        <thead>
          <tr>
            <th style="width:22%;">Técnica ISO/IEC/IEEE 29119-4</th>
            <th style="width:20%;">Módulo / Endpoint Real</th>
            <th style="width:30%;">Justificación por Riesgo Técnico o de Negocio</th>
            <th style="width:28%;">Clases / Condiciones Evaluadas</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td><b>Partición de Equivalencia (EP)</b><br>Cláusula 7.2 (Caja Negra)</td>
            <td><b>MOD-05 &amp; MOD-06</b><br><code>GET /api/sunat/ruc/:numero</code><br><code>POST /api/clients</code></td>
            <td>Evita rechazos fiscales en el OSE Nubefact por documentos tributarios inválidos antes de emitir el XML UBL 2.1.</td>
            <td><b>Válidas:</b> DNI (8 dígitos), RUC (11 dígitos prefijo 10/20).<br><b>Inválidas:</b> longitud &ne; 8/11, letras, RUC en BAJA.</td>
          </tr>
          <tr class="alt">
            <td><b>Análisis Valores Límite (BVA)</b><br>Cláusula 7.3 (Caja Negra)</td>
            <td><b>MOD-02 &amp; MOD-03</b><br><code>PATCH /variant/:id/stock</code><br><code>POST /api/orders</code></td>
            <td>Los errores críticos de sobre-venta textil (over-selling) ocurren exactamente en las fronteras numéricas de inventario.</td>
            <td><b>Fronteras:</b> <code>stock = -1</code> (400 Bad Request), <code>0</code> (Agotado), <code>1</code> (Alerta), <code>disp</code> (OK), <code>disp + 1</code> (Rechazo).</td>
          </tr>
          <tr>
            <td><b>Tablas de Decisión (DTT)</b><br>Cláusula 7.4 (Caja Negra)</td>
            <td><b>MOD-03 &amp; MOD-05</b><br><code>orders.controller.ts</code><br><code>nubefact.service.ts</code></td>
            <td>Gobierna la lógica combinatoria de facturación y logística según tipo de documento, destino y confirmación de pago.</td>
            <td><b>Reglas:</b> [Envío: Lima / Provincia] &times; [Doc: DNI&rarr;Boleta BBB1 / RUC&rarr;Factura FFF1] &times; [Pago: OK / Fallido].</td>
          </tr>
          <tr class="alt">
            <td><b>Transición de Estados (STT)</b><br>Cláusula 7.5 (Caja Negra)</td>
            <td><b>MOD-03</b><br><code>stateMachine.ts</code><br><code>PATCH /api/orders/:id/status</code></td>
            <td>Impide saltos operacionales ilegales o retrocesos de pedidos entregados o cancelados mediante bloqueo <code>FOR UPDATE</code>.</td>
            <td><b>Secuencia:</b> PENDIENTE &rarr; PAGADO &rarr; PREPARACION &rarr; EN_CAMINO &rarr; ENTREGADO. Ilegal &rarr; <code>HTTP 409</code>.</td>
          </tr>
          <tr>
            <td><b>Pruebas de Escenario / E2E</b><br>Cláusula 7.7 (Caja Negra)</td>
            <td><b>Full-Stack</b><br>Catálogo PWA &rarr; Carrito &rarr; Culqi &rarr; CPE PDF</td>
            <td>Valida la integración real entre componentes React 19, contratos API Express y descarga de comprobantes PDF/XML.</td>
            <td>Recorrido completo del comprador y del operador logístico generando rótulo térmico y factura.</td>
          </tr>
          <tr class="alt">
            <td><b>Branch Testing &amp; Error Guessing</b><br>Cláusulas 8.2 y 9.1</td>
            <td><b>MOD-01 &amp; MOD-04</b><br><code>auth.middleware.ts</code><br><code>paymentWebhook.controller</code></td>
            <td>Garantiza cobertura &gt;80% en ramas de seguridad y resistencia contra webhooks falsificados o ataques de replay.</td>
            <td>Token ausente (401), expirado (401), rol OPERATOR en ruta ADMIN (403), firma HMAC alterada (401).</td>
          </tr>
        </tbody>
      </table>

      <div class="sec-banner">4. Entornos, Datos de Prueba, Herramientas, Roles y Cronograma Ejecutado (Secciones 14 a 18)</div>
      <table class="infog-table">
        <thead>
          <tr>
            <th style="width:20%;">Dimensión Operativa</th>
            <th style="width:80%;">Especificación Técnica Verificada en el Proyecto LeoFit Solutions</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td><b>14. Entornos de Prueba</b></td>
            <td><b>1) Local/DEV:</b> Node.js 20 + PostgreSQL 16 Docker (puerto 5432). <b>2) CI Pipeline:</b> GitHub Actions (<code>ubuntu-latest</code>) con servicio efímero PostgreSQL 16. <b>3) Staging/QA:</b> Render Web Service + Neon Serverless PostgreSQL (branch <code>qa_staging</code>) integrado con Culqi Sandbox y Nubefact Demo.</td>
          </tr>
          <tr class="alt">
            <td><b>15. Datos de Prueba</b></td>
            <td><b>Usuarios (Seeds):</b> <code>admin@leofit.pe</code> (ADMIN), <code>operador@leofit.pe</code> (OPERATOR). <b>Tarjetas Culqi Sandbox:</b> <code>4111...1111</code> (Aprobada), <code>4000...0002</code> (Fondos insuf.). <b>RUC SUNAT:</b> <code>20100070970</code> (Activo/Habido). <b>SKUs:</b> <code>POLO-DRY-BLK-M</code> (stock 15), <code>LEG-FIT-NAVY-S</code> (stock 0).</td>
          </tr>
          <tr>
            <td><b>16. Herramientas QA</b></td>
            <td><b>Backend:</b> Jest v29.7 + Supertest v6.3 (125 tests). <b>Frontend:</b> Vitest v4.1 + React Testing Library v16.3 + jsdom (69 tests). <b>Rendimiento/Coexistencia:</b> k6 + scripts Python ISO 25010. <b>CI/CD:</b> GitHub Actions. <b>Gestión Defectos:</b> GitHub Issues.</td>
          </tr>
          <tr class="alt">
            <td><b>17. Roles del Equipo</b></td>
            <td><b>QA Lead Senior:</b> Jim Dávila (Diseño 29119, suites Supertest, liberación). <b>DevSecOps/SM:</b> Lady Loayza (Pipeline CI, seguridad HMAC/JWT). <b>PO/DBA:</b> Víctor Cárdenas (Datos BCNF, DRP). <b>Frontend Lead:</b> Harley Roman (Suites Vitest/WCAG). <b>BA/Cloud:</b> Daniel Rojas (SUNAT/k6).</td>
          </tr>
          <tr>
            <td><b>18. Cronograma QA</b></td>
            <td><b>Fase 1 (Sem 06-08):</b> Unitarias Dominio [100%]. <b>Fase 2 (Sem 09-12):</b> Integración API/BD [100%]. <b>Fase 3 (Sem 13-15):</b> Pasarelas Culqi/Nubefact [100%]. <b>Fase 4 (Sem 16-17):</b> Carga k6, Coexistencia ISO 25010 y Simulacro DRP [100%]. <b>Fase 5 (Sem 18):</b> Cierre y Sustentación.</td>
          </tr>
        </tbody>
      </table>
    """

    page3_body = """
      <div class="page-hdr">LEOFIT SOLUTIONS S.A.C. | PLAN DE PRUEBAS DE SOFTWARE (ISO/IEC/IEEE 29119-3 &amp; 29119-4) &bull; PÁGINA 3 DE 3</div>
      <div class="sec-banner">5. Riesgos, Criterios de Entrada/Salida, Gestión de Defectos y Métricas (Secciones 19 a 23)</div>

      <div class="fig-box">
        <img src="infog_qa_03_riesgos_cobertura_sla.png" width="525">
      </div>

      <table class="infog-table">
        <thead>
          <tr>
            <th style="width:22%;">Gobernanza de Calidad</th>
            <th style="width:78%;">Criterios, Umbrales y Protocolos Oficiales Aplicados</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td><b>20. Criterios Entrada / Salida</b></td>
            <td><b>Entrada:</b> Compilación limpia <code>tsc --noEmit</code>, esquema BCNF migrado, credenciales Sandbox activas. <b>Salida:</b> 100% pass rate (194/194 tests), 0 defectos críticos/bloqueantes, cobertura de ramas &ge; 80% en lógica core, p95 &le; 800 ms y RTO DRP &le; 15 min.</td>
          </tr>
          <tr class="alt">
            <td><b>21. Entregables de Prueba</b></td>
            <td>(1) Plan de Pruebas ISO/IEC/IEEE 29119-3; (2) 27 suites automatizadas en repositorio (125 BE + 69 FE); (3) Logs de auditoría CI/CD en GitHub Actions; (4) Informe Experimental de Coexistencia ISO/IEC 25010; (5) Acta de Simulacro DRP (<code>BACKUP_RESTORE_DRILL.md</code>).</td>
          </tr>
          <tr>
            <td><b>22. Gestión Defectos (SLA)</b></td>
            <td><b>Bloqueante</b> (Caída / fallo cobro &rarr; Hotfix &lt; 4h, detiene release); <b>Crítica</b> (Fallo CPE SUNAT / corrupción stock &rarr; &lt; 12h); <b>Mayor</b> (Filtros / UI secundaria &rarr; &lt; 48h); <b>Menor</b> (Ajustes cosméticos CSS &rarr; siguiente sprint).</td>
          </tr>
        </tbody>
      </table>

      <div class="sec-banner">6. Matriz de Trazabilidad y Casos de Prueba Representativos de Alto Nivel (Secciones 24 y 25)</div>
      <table class="infog-table">
        <thead>
          <tr>
            <th style="width:11%;">ID / Prioridad</th>
            <th style="width:19%;">Requisito y Riesgo</th>
            <th style="width:17%;">Técnica ISO 29119-4</th>
            <th style="width:27%;">Precondición, Entrada y Pasos</th>
            <th style="width:26%;">Resultado Esperado (Oráculo)</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td><b>CP-01</b><br><span class="lbl-red">ALTA</span></td>
            <td><b>RF-01:</b> Acceso RBAC<br>Mitiga: Escalada privilegios</td>
            <td>Branch Testing (Cl. 8.2)<br>+ Error Guessing</td>
            <td><b>Pre:</b> Usuario con rol <code>OPERATOR</code>.<br><b>Paso:</b> Enviar <code>POST /api/products</code> con Bearer JWT de operador.</td>
            <td><b>HTTP 403 Forbidden:</b> Middleware <code>requireRole('ADMIN')</code> bloquea mutación y audita evento.</td>
          </tr>
          <tr class="alt">
            <td><b>CP-02</b><br><span class="lbl-red">ALTA</span></td>
            <td><b>RF-02:</b> Stock Variante<br>Mitiga: RSK-02 (Over-selling)</td>
            <td>Boundary Value Analysis<br>(BVA — Cl. 7.3)</td>
            <td><b>Pre:</b> Variante <code>id=1</code> con <code>stock=5</code>.<br><b>Paso:</b> 1) <code>PATCH /variant/1/stock</code> con <code>-1</code>. 2) Orden por 6 uds.</td>
            <td><b>HTTP 400 Bad Request:</b> Validador Zod y trigger <code>trg_decrement_stock</code> impiden saldo negativo.</td>
          </tr>
          <tr>
            <td><b>CP-03</b><br><span class="lbl-red">ALTA</span></td>
            <td><b>RF-03:</b> Idempotencia<br>Mitiga: Doble orden por red</td>
            <td>Equivalence Part.<br>+ Idempotencia JCS</td>
            <td><b>Pre:</b> Cliente y variante activos.<br><b>Paso:</b> Enviar 2 veces <code>POST /api/orders</code> con igual <code>Idempotency-Key</code>.</td>
            <td><b>HTTP 201 / 200 OK:</b> Primera crea pedido; segunda retorna caché sin duplicar fila en <code>orders</code>.</td>
          </tr>
          <tr class="alt">
            <td><b>CP-04</b><br><span class="lbl-red">CRÍTICA</span></td>
            <td><b>RF-04:</b> Webhook Culqi<br>Mitiga: RSK-03 (Spoofing)</td>
            <td>Error Guessing (Cl. 9.1)<br>Firma HMAC-SHA256</td>
            <td><b>Pre:</b> Orden en <code>PENDIENTE</code>.<br><b>Paso:</b> Enviar <code>POST /api/webhooks/culqi</code> con firma HMAC alterada.</td>
            <td><b>HTTP 401 Unauthorized:</b> <code>crypto.timingSafeEqual</code> rechaza firma; pedido no pasa a PAGADO.</td>
          </tr>
          <tr>
            <td><b>CP-05</b><br><span class="lbl-red">ALTA</span></td>
            <td><b>RF-05:</b> Ciclo Pedido<br>Mitiga: Corrupción logística</td>
            <td>State Transition Testing<br>(STT — Cl. 7.5)</td>
            <td><b>Pre:</b> Pedido en estado <code>ENTREGADO</code>.<br><b>Paso:</b> Enviar <code>PATCH /api/orders/:id/status</code> hacia <code>PENDIENTE</code>.</td>
            <td><b>HTTP 409 Conflict:</b> <code>stateMachine.ts</code> bloquea transición ilegal (<code>INVALID_TRANSITION</code>).</td>
          </tr>
          <tr class="alt">
            <td><b>CP-06</b><br><span class="lbl-red">ALTA</span></td>
            <td><b>RF-06:</b> Emisión CPE<br>Mitiga: RSK-01 &amp; RSK-04</td>
            <td>Decision Table (Cl. 7.4)<br>+ EP (RUC 11 dígitos)</td>
            <td><b>Pre:</b> Pedido <code>PAGADO</code> con RUC <code>20100070970</code>.<br><b>Paso:</b> Emitir CPE y consultar <code>/api/invoices/order/:orderId</code>.</td>
            <td><b>HTTP 200 OK:</b> Factura <code>FFF1</code> correlativa sin brechas, IGV 18% exacto y CDR <code>ACEPTADO</code>.</td>
          </tr>
        </tbody>
      </table>

      <div class="sec-banner">7. Aprobaciones y Conformidad Formal del Plan de Pruebas (Sección 26)</div>
      <table class="meta-table">
        <tr>
          <td style="width:33%; text-align:center; padding:6px;">
            <b>____________________________________</b><br>
            <span class="lbl-navy">Jim Alessandro Dávila Morales</span><br>
            QA Lead Senior / Backend (U18206081)<br>
            <span class="lbl-green">APROBADO Y EJECUTADO</span>
          </td>
          <td style="width:34%; text-align:center; padding:6px;">
            <b>____________________________________</b><br>
            <span class="lbl-navy">Lady Luz Loayza Rodríguez</span><br>
            Scrum Master / DevSecOps Lead (U22221489)<br>
            <span class="lbl-green">APROBADO EN PIPELINE CI/CD</span>
          </td>
          <td style="width:33%; text-align:center; padding:6px;">
            <b>____________________________________</b><br>
            <span class="lbl-navy">Ing. Enrique Lee Huamani Uriarte</span><br>
            Docente Asesor Evaluador — UTP<br>
            <span class="lbl-blue">CURSO INTEGRADOR II (2026-I)</span>
          </td>
        </tr>
      </table>
    """

    full_html = f"""<!DOCTYPE html>
<html lang="es">
<head><meta charset="UTF-8"><title>Plan de Pruebas ISO 29119 — LeoFit Solutions</title>{common_css}</head>
<body style="max-width:210mm; margin:0 auto; padding:10mm;">
{page1_body}
<hr style="margin:14px 0; border:none; border-top:2px dashed #CBD5E1;">
{page2_body}
<hr style="margin:14px 0; border:none; border-top:2px dashed #CBD5E1;">
{page3_body}
</body></html>"""

    # Guardamos HTML con rutas relativas a assets/ para visualización local
    html_browser = full_html.replace('src="infog_qa_', 'src="assets/infog_qa_')
    out_html_main = os.path.join(DOCS_PLAN_DIR, "PLAN_DE_PRUEBAS_SOFTWARE_ISO29119.html")
    with open(out_html_main, "w", encoding="utf-8") as f:
        f.write(html_browser)

    if os.path.exists(HTML_LOCAL_DIR):
        local_assets = os.path.join(HTML_LOCAL_DIR, "assets")
        os.makedirs(local_assets, exist_ok=True)
        for fn in os.listdir(ASSETS_DIR):
            shutil.copy2(os.path.join(ASSETS_DIR, fn), os.path.join(local_assets, fn))
        shutil.copy2(out_html_main, os.path.join(HTML_LOCAL_DIR, "PLAN_DE_PRUEBAS_SOFTWARE_ISO29119.html"))

    # Compilar PDF A4 Vertical exactamente en 3 páginas (1 Story por página)
    import tempfile
    raw_pdf_path = os.path.join(tempfile.gettempdir(), f"leofit_raw_pdf_{os.getpid()}.pdf")
    out_pdf_main = os.path.join(DOCS_PLAN_DIR, "PLAN_DE_PRUEBAS_SOFTWARE_ISO29119.pdf")

    rect = fitz.paper_rect("a4")  # 595 x 842 pt
    margin = 24.0  # ~8.5mm
    where = rect + (margin, margin, -margin, -margin)

    arch = fitz.Archive(ASSETS_DIR)
    writer = fitz.DocumentWriter(raw_pdf_path)

    pages_html = [
        f"<!DOCTYPE html><html><head>{common_css}</head><body>{page1_body}</body></html>",
        f"<!DOCTYPE html><html><head>{common_css}</head><body>{page2_body}</body></html>",
        f"<!DOCTYPE html><html><head>{common_css}</head><body>{page3_body}</body></html>",
    ]

    for idx, p_html in enumerate(pages_html):
        st = fitz.Story(html=p_html, archive=arch)
        device = writer.begin_page(rect)
        more, _ = st.place(where)
        st.draw(device)
        writer.end_page()
        if more:
            print(f" [!] Advertencia: Página {idx+1} tuvo ligero overflow (more={more})")

    writer.close()

    # Post-proceso de compresión con PyMuPDF (deflate streams, reduce de ~47MB a ~1MB)
    doc_raw = fitz.open(raw_pdf_path)
    doc_raw.save(out_pdf_main, garbage=4, deflate=True)
    doc_raw.close()
    del doc_raw
    import gc
    gc.collect()
    try:
        if os.path.exists(raw_pdf_path):
            os.remove(raw_pdf_path)
    except Exception:
        pass

    if os.path.exists(DOCX_LOCAL_DIR):
        shutil.copy2(out_pdf_main, os.path.join(DOCX_LOCAL_DIR, "PLAN_DE_PRUEBAS_SOFTWARE_ISO29119.pdf"))

    size_mb = os.path.getsize(out_pdf_main) / (1024 * 1024)
    print(f" -> PDF Oficial A4 Optimizado (3 páginas, {size_mb:.2f} MB) generado en: {out_pdf_main}")
    return out_pdf_main, 3


if __name__ == "__main__":
    f1 = generate_fig1_dashboard_piramide()
    f2 = generate_fig2_arquitectura_estados()
    f3 = generate_fig3_riesgos_cobertura_sla()
    build_executive_docx(f1, f2, f3)
    build_executive_html_and_pdf()
    print("\nCOMPILACIÓN INFOGRÁFICA EJECUTIVA COMPLETADA CON ÉXITO.")
