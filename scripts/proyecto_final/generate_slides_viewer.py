# -*- coding: utf-8 -*-
"""
@file generate_slides_viewer.py
@description Genera un visor HTML interactivo y un documento Markdown oficial 
             de la Presentación de Sustentación Final (25 Diapositivas).
"""

import os
import pptx
import html

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

# Carpeta oficial de Entrega Final Semana 18
OFFICIAL_FINAL_DIR = os.path.join(BASE_DIR, "docs", "01_ENTREGA_FINAL_PROYECTO_SEMANA_18")
os.makedirs(OFFICIAL_FINAL_DIR, exist_ok=True)
OUT_HTML_OFFICIAL = os.path.join(OFFICIAL_FINAL_DIR, "03_VISOR_WEB_PRESENTACION_SUSTENTACION.html")
PPTX_PATH = os.path.join(OFFICIAL_FINAL_DIR, "03_PRESENTACION_OFICIAL_SUSTENTACION_LEOFIT.pptx")

prs = pptx.Presentation(PPTX_PATH)

slides_data = []

for idx, slide in enumerate(prs.slides):
    slide_num = idx + 1
    notes = ""
    if slide.has_notes_slide and slide.notes_slide.notes_text_frame:
        notes = slide.notes_slide.notes_text_frame.text.strip()
    
    # Extract text boxes and tables
    texts = []
    tables = []
    
    for shape in slide.shapes:
        if shape.has_table:
            t = shape.table
            table_rows = []
            for r in t.rows:
                table_rows.append([c.text.strip().replace("\n", " ") for c in r.cells])
            tables.append(table_rows)
        elif shape.has_text_frame:
            txt = shape.text_frame.text.strip()
            if txt:
                texts.append(txt)
    
    slides_data.append({
        "num": slide_num,
        "texts": texts,
        "tables": tables,
        "notes": notes
    })

print(f"Extracted {len(slides_data)} slides from PPTX.")

# 1. Generar Markdown
md_lines = [
    "# LeoFit Solutions — Presentación Oficial de Sustentación Final de Ingeniería",
    "## Sistema de Gestión de Pedidos y Control de Inventario Multicanal (Ciclo 2026-I)",
    "**Asignatura:** Curso Integrador II: Software (100000S12F) · **Docente Asesor:** Ing. Enrique Lee Huamani Uriarte  ",
    "**Equipo de Ingeniería:** Grupo 01 (Lady Loayza, Victor Cardenas, Harley Roman, Jim Davila, Daniel Rojas)  ",
    "**Entregable Oficial:** Semana 18 · Sustentación Final de Grado · Formato Widescreen 16:9 (25 Diapositivas)  ",
    "",
    "---",
    ""
]

for s in slides_data:
    num = s["num"]
    md_lines.append(f"## Diapositiva {num:02d}")
    for t in s["texts"]:
        # format text block
        lines = t.split("\n")
        if len(lines) == 1 and len(lines[0]) < 80 and not lines[0].startswith("-"):
            md_lines.append(f"### {lines[0]}")
        else:
            for l in lines:
                if l.startswith("-"):
                    md_lines.append(l)
                else:
                    md_lines.append(f"{l}  ")
        md_lines.append("")
    
    for tbl in s["tables"]:
        if tbl:
            # Header
            header = tbl[0]
            md_lines.append("| " + " | ".join(header) + " |")
            md_lines.append("| " + " | ".join(["---"] * len(header)) + " |")
            for row in tbl[1:]:
                md_lines.append("| " + " | ".join(row) + " |")
            md_lines.append("")
            
    if s["notes"]:
        md_lines.append("> **Notas del Orador:**  ")
        for nl in s["notes"].split("\n"):
            md_lines.append(f"> {nl}  ")
        md_lines.append("")
        
    md_lines.append("---")
    md_lines.append("")

# Markdown informativo opcional en docs/
out_md = os.path.join(OFFICIAL_FINAL_DIR, "03_PRESENTACION_OFICIAL_SUSTENTACION_LEOFIT.md")
with open(out_md, "w", encoding="utf-8") as f:
    f.write("\n".join(md_lines))
print(f"Markdown Oficial escrito en {out_md}")

# 2. Generar HTML Interactivo
html_content = """<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>LeoFit Solutions — Sustentación Final de Ingeniería (Semana 18)</title>
  <style>
    :root {
      --navy: #0F172A;
      --blue: #1665D8;
      --accent: #C2410C;
      --green: #15803D;
      --dark: #1E293B;
      --gray: #64748B;
      --lgray: #F8FAFC;
      --lblue: #EFF6FF;
      --white: #FFFFFF;
    }
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      font-family: 'Segoe UI', system-ui, -apple-system, sans-serif;
      background: #0B1120;
      color: #E2E8F0;
      display: flex;
      flex-direction: column;
      height: 100vh;
      overflow: hidden;
    }
    header.top-bar {
      background: var(--navy);
      border-bottom: 2px solid var(--blue);
      padding: 10px 24px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-shrink: 0;
    }
    .brand {
      font-size: 16px;
      font-weight: 700;
      color: var(--white);
      letter-spacing: 0.5px;
    }
    .brand span { color: var(--accent); }
    .controls {
      display: flex;
      gap: 12px;
      align-items: center;
    }
    button.btn {
      background: var(--blue);
      color: white;
      border: none;
      padding: 6px 14px;
      border-radius: 6px;
      font-weight: 600;
      cursor: pointer;
      font-size: 13px;
      transition: background 0.2s;
    }
    button.btn:hover { background: #1E40AF; }
    button.btn-outline {
      background: transparent;
      border: 1px solid var(--gray);
      color: #CBD5E1;
    }
    button.btn-outline:hover { background: rgba(255,255,255,0.08); }
    .slide-counter {
      font-weight: 700;
      font-size: 14px;
      color: var(--white);
      min-width: 80px;
      text-align: center;
    }
    .main-stage {
      flex: 1;
      display: flex;
      overflow: hidden;
      position: relative;
    }
    .slide-viewport {
      flex: 1;
      display: flex;
      align-items: center;
      justify-content: center;
      padding: 20px;
      overflow-y: auto;
    }
    .slide-card {
      width: 100%;
      max-width: 1200px;
      aspect-ratio: 16 / 9;
      background: var(--white);
      color: var(--dark);
      border-radius: 12px;
      box-shadow: 0 20px 40px rgba(0,0,0,0.5);
      padding: 40px 48px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      position: relative;
      overflow: hidden;
    }
    .slide-card.dark-theme {
      background: var(--navy);
      color: var(--white);
      border: 2px solid var(--blue);
    }
    .slide-header {
      border-bottom: 2px solid #E2E8F0;
      padding-bottom: 12px;
      margin-bottom: 20px;
    }
    .slide-card.dark-theme .slide-header {
      border-bottom-color: rgba(255,255,255,0.15);
    }
    .slide-category {
      font-size: 12px;
      font-weight: 800;
      color: var(--accent);
      letter-spacing: 1px;
      text-transform: uppercase;
      margin-bottom: 4px;
    }
    .slide-title {
      font-size: 24px;
      font-weight: 800;
      color: var(--navy);
      line-height: 1.25;
    }
    .slide-card.dark-theme .slide-title {
      color: var(--white);
    }
    .slide-body {
      flex: 1;
      overflow-y: auto;
      font-size: 15px;
      line-height: 1.6;
    }
    .slide-body ul {
      margin-left: 20px;
      margin-bottom: 12px;
    }
    .slide-body li {
      margin-bottom: 6px;
    }
    .slide-body p {
      margin-bottom: 10px;
    }
    .table-container {
      margin: 14px 0;
      overflow-x: auto;
    }
    table {
      width: 100%;
      border-collapse: collapse;
      font-size: 13.5px;
    }
    th, td {
      border: 1px solid #CBD5E1;
      padding: 8px 12px;
      text-align: center;
    }
    th {
      background: var(--navy);
      color: white;
      font-weight: 700;
    }
    tr:nth-child(even) { background: #F1F5F9; }
    .slide-footer {
      border-top: 1px solid #E2E8F0;
      padding-top: 10px;
      margin-top: 15px;
      display: flex;
      justify-content: space-between;
      font-size: 11px;
      color: var(--gray);
    }
    .slide-card.dark-theme .slide-footer {
      border-top-color: rgba(255,255,255,0.15);
      color: #94A3B8;
    }
    .notes-panel {
      width: 360px;
      background: #0F172A;
      border-left: 2px solid #1E293B;
      padding: 20px;
      display: flex;
      flex-direction: column;
      overflow-y: auto;
      transition: transform 0.3s;
    }
    .notes-panel.collapsed {
      display: none;
    }
    .notes-header {
      font-size: 14px;
      font-weight: 700;
      color: var(--accent);
      text-transform: uppercase;
      margin-bottom: 12px;
      letter-spacing: 0.5px;
      display: flex;
      justify-content: space-between;
    }
    .notes-content {
      font-size: 13.5px;
      line-height: 1.65;
      color: #CBD5E1;
      white-space: pre-wrap;
    }
    .badge {
      display: inline-block;
      padding: 3px 8px;
      border-radius: 4px;
      font-size: 11px;
      font-weight: 700;
      background: var(--blue);
      color: white;
    }
  </style>
</head>
<body>
  <header class="top-bar">
    <div class="brand">LEOFIT <span>SOLUTIONS</span> · SUSTENTACIÓN FINAL SEMANA 18</div>
    <div class="controls">
      <button class="btn" onclick="prevSlide()">◀ Anterior</button>
      <span class="slide-counter" id="slideNum">1 / 25</span>
      <button class="btn" onclick="nextSlide()">Siguiente ▶</button>
      <a href="03_PRESENTACION_OFICIAL_SUSTENTACION_PROYECTO_FINAL.pptx" class="btn" style="text-decoration:none;" download>Descargar PPTX</a>
    </div>
  </header>

  <div class="main-stage">
    <div class="slide-viewport">
      <div class="slide-card" id="slideCard">
        <!-- Rendered dynamically -->
      </div>
    </div>
    <aside class="notes-panel collapsed" id="notesPanel">
      <div class="notes-header">
        <span>Detalle Técnico</span>
        <span class="badge" id="notesBadge">Slide 1</span>
      </div>
      <div class="notes-content" id="notesContent"></div>
    </aside>
  </div>

  <script>
    const slides = SLIDES_DATA_PLACEHOLDER;
    let curIndex = 0;

    function renderSlide(idx) {
      if (idx < 0) idx = 0;
      if (idx >= slides.length) idx = slides.length - 1;
      curIndex = idx;
      
      const s = slides[curIndex];
      document.getElementById('slideNum').textContent = `${curIndex + 1} / ${slides.length}`;
      document.getElementById('notesBadge').textContent = `Slide ${curIndex + 1}`;
      document.getElementById('notesContent').textContent = s.notes || "Sin notas adicionales registradas.";
      
      const card = document.getElementById('slideCard');
      const isDark = (curIndex === 0 || curIndex === slides.length - 1);
      
      if (isDark) {
        card.classList.add('dark-theme');
      } else {
        card.classList.remove('dark-theme');
      }
      
      let html = '';
      
      // Header
      if (curIndex > 0 && curIndex < slides.length - 1) {
        const cat = s.texts[0] || "PROYECTO FINAL - INGENIERIA DE SOFTWARE";
        const title = s.texts[1] || "";
        html += `
          <div class="slide-header">
            <div class="slide-category">${escapeHtml(cat)}</div>
            <div class="slide-title">${escapeHtml(title)}</div>
          </div>
        `;
      }
      
      html += `<div class="slide-body">`;
      
      if (isDark) {
        for (let i = 0; i < s.texts.length; i++) {
          const t = s.texts[i];
          if (i === 1) {
            html += `<h1 style="color:var(--white);font-size:28px;margin:15px 0;line-height:1.2;">${escapeHtml(t).replace(/\\n/g, '<br>')}</h1>`;
          } else if (i === 0) {
            html += `<div style="color:var(--accent);font-weight:700;font-size:14px;letter-spacing:1px;">${escapeHtml(t)}</div>`;
          } else {
            html += `<p style="white-space:pre-wrap;font-size:14px;line-height:1.5;">${escapeHtml(t)}</p>`;
          }
        }
      } else {
        // Body texts (skip category and title if present)
        const startIdx = (s.texts.length > 2 && s.texts[0].length < 50) ? 2 : 0;
        for (let i = startIdx; i < s.texts.length; i++) {
          const t = s.texts[i];
          if (t.includes("\\n- ") || t.startsWith("- ")) {
            html += `<ul>`;
            const items = t.split(/\\n?- /);
            for (const item of items) {
              if (item.trim()) {
                html += `<li>${escapeHtml(item.trim())}</li>`;
              }
            }
            html += `</ul>`;
          } else {
            html += `<p style="white-space:pre-wrap;">${escapeHtml(t)}</p>`;
          }
        }
      }
      
      // Tables
      for (const tbl of s.tables) {
        html += `<div class="table-container"><table>`;
        if (tbl.length > 0) {
          html += `<tr>`;
          for (const h of tbl[0]) html += `<th>${escapeHtml(h)}</th>`;
          html += `</tr>`;
          for (let r = 1; r < tbl.length; r++) {
            html += `<tr>`;
            for (const c of tbl[r]) html += `<td>${escapeHtml(c)}</td>`;
            html += `</tr>`;
          }
        }
        html += `</table></div>`;
      }
      
      html += `</div>`;
      
      // Footer
      html += `
        <div class="slide-footer">
          <span>LeoFit Solutions - Grupo 01 | UTP Curso Integrador II</span>
          <span>Sustentación Final (Semana 18)</span>
        </div>
      `;
      
      card.innerHTML = html;
    }

    function prevSlide() { if (curIndex > 0) renderSlide(curIndex - 1); }
    function nextSlide() { if (curIndex < slides.length - 1) renderSlide(curIndex + 1); }
    function toggleNotes() {
      document.getElementById('notesPanel').classList.toggle('collapsed');
    }

    function escapeHtml(str) {
      if (!str) return '';
      return String(str)
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;')
        .replace(/'/g, '&#039;');
    }

    window.addEventListener('keydown', (e) => {
      if (e.key === 'ArrowRight' || e.key === 'PageDown' || e.key === ' ') nextSlide();
      if (e.key === 'ArrowLeft' || e.key === 'PageUp') prevSlide();
      if (e.key === 'n' || e.key === 'N') toggleNotes();
    });

    renderSlide(0);
  </script>
</body>
</html>
"""

import json
html_with_data = html_content.replace("SLIDES_DATA_PLACEHOLDER", json.dumps(slides_data, ensure_ascii=False))

with open(OUT_HTML_OFFICIAL, "w", encoding="utf-8") as f:
    f.write(html_with_data)
print(f"HTML Oficial escrito en {OUT_HTML_OFFICIAL}")
print("Slides viewer generation completed successfully!")
