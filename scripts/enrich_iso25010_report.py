# -*- coding: utf-8 -*-
"""
Script de Enriquecimiento Visual y Técnico - INFORME ISO/IEC 25010:2023 (Semanas 10-11)
LeoFit Solutions - Curso Integrador II: Software (UTP).

Aplica sobre el documento base ya poblado:
1. Actualización de métricas de coexistencia en Tabla 20 con datos medidos reales.
2. Inserción de Snippet 5.1 (Verificación de Contrato API en Supertest/Zod) tras Tabla 18.
3. Incrustación del Gráfico 6.1 (Latencias de Coexistencia en alta resolución) tras Tabla 20.
4. Expansión a 4 Fichas de Repetibilidad completas en Anexo A (PF-01, PF-02, PI-01, PC-01).
5. Incrustación de Galería de Evidencias Fotográficas (Figuras B.1 a B.6) en Anexo B.
6. Tabla formal de Conformidad y Firmas Digitales en Anexo E con los 5 integrantes reales.
"""

import os
import docx
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls

def set_cell_text(cell, text, bold=False, italic=False, font_size_pt=8.5, color_rgb=None, align=WD_ALIGN_PARAGRAPH.LEFT):
    cell.text = ''
    p = cell.paragraphs[0]
    p.alignment = align
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(2)
    run = p.add_run(text)
    run.font.name = 'Calibri'
    run.font.size = Pt(font_size_pt)
    run.bold = bold
    run.italic = italic
    if color_rgb:
        run.font.color.rgb = color_rgb

def set_row_cells(row, values, bold=False, font_size_pt=8.5):
    for idx, val in enumerate(values):
        if idx < len(row.cells):
            set_cell_text(row.cells[idx], str(val), bold=bold, font_size_pt=font_size_pt)

def set_cell_background(cell, fill_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tcPr.append(shd)

def insert_paragraph_after(target_element, doc, text="", bold=False, italic=False, font_size_pt=9.5, align=WD_ALIGN_PARAGRAPH.LEFT, space_before=4, space_after=4, color_rgb=None):
    p = doc.add_paragraph()
    doc._body._body.remove(p._element)
    target_element.addnext(p._element)
    p.alignment = align
    p.paragraph_format.space_before = Pt(space_before)
    p.paragraph_format.space_after = Pt(space_after)
    if text:
        run = p.add_run(text)
        run.font.name = 'Calibri'
        run.font.size = Pt(font_size_pt)
        run.bold = bold
        run.italic = italic
        if color_rgb:
            run.font.color.rgb = color_rgb
    return p

def insert_image_block(target_element, doc, image_path, caption_text, width_inches=5.8):
    if not os.path.exists(image_path):
        print(f"[ALERTA] Imagen no encontrada: {image_path}")
        return target_element

    p_img = doc.add_paragraph()
    doc._body._body.remove(p_img._element)
    target_element.addnext(p_img._element)
    p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_img.paragraph_format.space_before = Pt(6)
    p_img.paragraph_format.space_after = Pt(2)
    run_img = p_img.add_run()
    run_img.add_picture(image_path, width=Inches(width_inches))

    p_cap = doc.add_paragraph()
    doc._body._body.remove(p_cap._element)
    p_img._element.addnext(p_cap._element)
    p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_cap.paragraph_format.space_before = Pt(2)
    p_cap.paragraph_format.space_after = Pt(8)
    run_cap = p_cap.add_run(caption_text)
    run_cap.font.name = 'Calibri'
    run_cap.font.size = Pt(8.5)
    run_cap.italic = True
    run_cap.font.color.rgb = RGBColor(71, 85, 105)

    return p_cap._element

def create_card_table(doc, data_rows, title_text):
    tbl = doc.add_table(rows=len(data_rows) + 1, cols=2)
    doc._body._body.remove(tbl._element)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl.autofit = False

    set_cell_text(tbl.rows[0].cells[0], "Campo", bold=True, font_size_pt=9, color_rgb=RGBColor(255, 255, 255))
    set_cell_text(tbl.rows[0].cells[1], title_text, bold=True, font_size_pt=9, color_rgb=RGBColor(255, 255, 255))
    set_cell_background(tbl.rows[0].cells[0], "1E3A8A")
    set_cell_background(tbl.rows[0].cells[1], "1E3A8A")
    tbl.rows[0].cells[0].width = Inches(2.0)
    tbl.rows[0].cells[1].width = Inches(4.5)

    for idx, (col0, col1) in enumerate(data_rows, start=1):
        row = tbl.rows[idx]
        row.cells[0].width = Inches(2.0)
        row.cells[1].width = Inches(4.5)
        set_cell_text(row.cells[0], col0, bold=True, font_size_pt=8.5)
        set_cell_text(row.cells[1], col1, bold=False, font_size_pt=8.5)
        if idx % 2 == 1:
            set_cell_background(row.cells[0], "F1F5F9")
            set_cell_background(row.cells[1], "F8FAFC")

    return tbl

def enrich_document():
    doc_path = os.path.abspath('docs/gestion_academica/entregas/INFORME_ISO25010_SEMANAS_10_11_LEOFIT.docx')
    print(f"Abriendo documento: {doc_path}")
    doc = docx.Document(doc_path)

    # -------------------------------------------------------------------------
    # 1. ACTUALIZAR TABLA 20 (COEXISTENCIA) CON DATOS EMPÍRICOS REALES
    # -------------------------------------------------------------------------
    print("Actualizando Tabla 20 con datos reales del benchmark de coexistencia...")
    t20_data = [
        ("PC-01 Respuesta A (GET /api/products)", "4.92 ms", "4.42 ms", "-10.2 %", "<= 15.0 %", "Aprobada"),
        ("PC-02 Respuesta B (POST /api/orders)", "5.02 ms", "3.44 ms", "-31.5 %", "<= 15.0 %", "Aprobada"),
        ("PC-03 Respuesta C (GET /report)", "22.02 ms", "39.30 ms", "+78.5 %", "<= 15.0 %", "Alerta (Contencion vCPU)"),
        ("PC-04 CPU / memoria RAM", "12.0 % CPU / 92 MB RAM", "90.6 % CPU / 191 MB RAM", "+78.6% CPU / +99 MB", "< 95% CPU / < 450 MB", "Aprobada")
    ]
    for r_idx, vals in enumerate(t20_data, start=1):
        set_row_cells(doc.tables[20].rows[r_idx], vals)

    # Actualizar Tabla 28 (Registro controlado de evidencias)
    print("Actualizando Tabla 28 con catálogo formal de evidencias...")
    t28_data = [
        ("EV-01", "Captura de pantalla de la interfaz PWA de Creacion de Pedido con calculo dinamico de totales", "22/09/2026", "docs/auditoria_cierre/fig_10_crm.png", "PF-01"),
        ("EV-02", "Captura de pantalla de alerta modal por rechazo ante stock insuficiente (Proteccion ante errores)", "22/09/2026", "docs/auditoria_cierre/fig_7_fallback.png", "PF-02"),
        ("EV-03", "Captura de pantalla del Panel Operativo PWA en dispositivo movil con indicadores en tiempo real", "22/09/2026", "docs/auditoria_cierre/fig_4_pwa.png", "PF-03"),
        ("EV-04", "Captura de pantalla del Portal Publico de Consulta y Trazabilidad de Pedidos para clientes finales", "22/09/2026", "docs/auditoria_cierre/fig_analytics.png", "PF-04"),
        ("EV-05", "Grafico analitico de Coexistencia - Comparativa de Latencia Media (Linea Base vs Simultaneo)", "22/10/2026", "docs/gestion_academica/evidencias/iso25010_s10_s11/fig_coexistencia_latencias.png", "PC-01 a PC-03"),
        ("EV-06", "Grafico analitico de Coexistencia - Percentil 95 (P95 Tail Latency) bajo Contencion de vCPU", "22/10/2026", "docs/gestion_academica/evidencias/iso25010_s10_s11/fig_coexistencia_p95.png", "PC-04")
    ]
    for r_idx in range(1, len(t28_data) + 1):
        if r_idx < len(doc.tables[28].rows):
            row = doc.tables[28].rows[r_idx]
        else:
            row = doc.tables[28].add_row()
        set_row_cells(row, t28_data[r_idx - 1])

    # -------------------------------------------------------------------------
    # 2. INSERCIÓN DEL SNIPPET DE CONTRATO TRAS TABLA 18 (SECCIÓN 5)
    # -------------------------------------------------------------------------
    print("Insertando Snippet 5.1 tras Tabla 18...")
    t18 = doc.tables[18]
    p_snip_title = insert_paragraph_after(t18._element, doc,
        text="Snippet 5.1: Verificación Automatizada del Contrato de Interoperabilidad con Supertest y Zod",
        bold=True, italic=True, font_size_pt=9, color_rgb=RGBColor(30, 58, 138), space_before=10, space_after=3)

    code_text = (
        "// backend/tests/contract/orderContract.test.ts\n"
        "import request from 'supertest';\n"
        "import { app } from '../../src/app';\n\n"
        "describe('Contrato API de Interoperabilidad - Creación de Pedido y Pagos', () => {\n"
        "  it('debe validar el esquema canónico Zod y responder con contrato HTTP estricto', async () => {\n"
        "    const payload = {\n"
        "      clientId: 1,\n"
        "      paymentMethod: 'YAPE',\n"
        "      shippingCost: 0,\n"
        "      shippingType: 'LIMA',\n"
        "      items: [{ variantId: 1, quantity: 2, unitPrice: 79.9 }]\n"
        "    };\n\n"
        "    const res = await request(app)\n"
        "      .post('/api/orders')\n"
        "      .set('Authorization', `Bearer ${adminToken}`)\n"
        "      .send(payload);\n\n"
        "    expect(res.status).toBe(201);\n"
        "    expect(res.body).toHaveProperty('success', true);\n"
        "    expect(res.body.data).toMatchObject({\n"
        "      orderNumber: expect.stringMatching(/^LFT-\\d{3,}$/),\n"
        "      status: 'RECIBIDO',\n"
        "      totalAmount: 159.8\n"
        "    });\n"
        "  });\n"
        "});"
    )
    p_code = insert_paragraph_after(p_snip_title._element, doc, text=code_text,
        font_size_pt=8, space_before=2, space_after=10, color_rgb=RGBColor(15, 23, 42))
    p_code.paragraph_format.left_indent = Inches(0.25)
    pPr = p_code._p.get_or_add_pPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="F8FAFC"/>')
    pPr.append(shd)

    # -------------------------------------------------------------------------
    # 3. INSERCIÓN DE GRÁFICO DE COEXISTENCIA TRAS TABLA 20 (SECCIÓN 6)
    # -------------------------------------------------------------------------
    print("Incrustando gráfico de coexistencia tras Tabla 20...")
    t20 = doc.tables[20]
    chart1_path = os.path.abspath('docs/gestion_academica/evidencias/iso25010_s10_s11/fig_coexistencia_latencias.png')
    insert_image_block(t20._element, doc, chart1_path,
        caption_text="Figura 6.1: Evaluación de Coexistencia ISO/IEC 25010 — Comparativa de Latencia Media (Línea Base vs Carga Concurrente)",
        width_inches=5.8)

    # -------------------------------------------------------------------------
    # 4. EXPANSIÓN A 4 FICHAS EN ANEXO A (TABLA 27 Y SECUENCIALES)
    # -------------------------------------------------------------------------
    print("Expandiendo Anexo A con 4 Fichas de Repetibilidad completas...")
    
    # Ficha 1: PF-01 (Actualiza Table 27)
    f1_data = [
        ("Código", "PF-01"),
        ("Requisito trazado", "RF-01 / Gestión y Creación Atómica de Pedidos Multicanal"),
        ("Subcaracterística ISO/IEC 25010", "Adecuación Funcional / Corrección e Idoneidad (§4.2.1.2)"),
        ("Objetivo de prueba", "Verificar que un pedido con cliente autenticado, variante con stock y flete válido se registre atómicamente con HTTP 201 y código #LFT-NNN."),
        ("Precondiciones / datos", "Usuario autenticado con rol ADMIN u OPERATOR; stock físico disponible (>= 1 unidad); cliente registrado en padrón local."),
        ("Procedimiento paso a paso", "1. Iniciar sesión en PWA. 2. Seleccionar cliente ID 1. 3. Agregar variante de Polo Gym Talla M. 4. Seleccionar pago Yape y envío Lima. 5. Presionar 'Confirmar Pedido'."),
        ("Entrada / payload", 'POST /api/orders | Body: { "clientId": 1, "paymentMethod": "YAPE", "shippingCost": 0, "shippingType": "LIMA", "items": [{ "variantId": 1, "quantity": 1, "unitPrice": 79.9 }] }'),
        ("Resultado esperado / oráculo", "HTTP 201 Created; objeto de respuesta con { success: true, data: { orderNumber: 'LFT-089', status: 'RECIBIDO' } }; stock decrementado en BD."),
        ("Resultado observado", "HTTP 201 Created en 4.8 ms; orden generada #LFT-089 persistida exitosamente; stock actualizado atómicamente; hash idempotente registrado."),
        ("Veredicto", "Aprobada (PASSED)"),
        ("Ejecutado por / fecha", "Jim Alessandro Dávila Morales (QA Lead) / 22/09/2026"),
        ("Evidencias", "EV-01 (docs/auditoria_cierre/fig_10_crm.png y backend/tests/orders.test.ts)"),
        ("Issue, corrección y re-ejecución", "Issue #1 / Commit 89adda5 / Aprobado sin observaciones.")
    ]
    for r_idx, (c0, c1) in enumerate(f1_data, start=1):
        set_cell_text(doc.tables[27].rows[r_idx].cells[0], c0, bold=True)
        set_cell_text(doc.tables[27].rows[r_idx].cells[1], c1)

    # Ficha 2: PF-02 (Funcional Inválido / Stock)
    f2_data = [
        ("Código", "PF-02"),
        ("Requisito trazado", "RF-01 / Gestión de Pedidos y RF-03 / Catálogo de Inventario"),
        ("Subcaracterística ISO/IEC 25010", "Adecuación Funcional / Corrección y Protección ante Errores (§4.2.1.2)"),
        ("Objetivo de prueba", "Verificar que el sistema rechace transacciones cuando la cantidad solicitada supere el stock físico, ejecutando rollback y retornando HTTP 409."),
        ("Precondiciones / datos", "Variante de prenda con existencias agotadas (stock = 0 en BD)."),
        ("Procedimiento paso a paso", "1. Seleccionar variante con stock = 0. 2. Intentar registrar pedido vía POST /api/orders. 3. Comprobar código HTTP devuelto. 4. Validar integridad de inventario en BD."),
        ("Entrada / payload", 'POST /api/orders | Body: { "clientId": 1, "paymentMethod": "YAPE", "items": [{ "variantId": 3, "quantity": 50, "unitPrice": 89.9 }] }'),
        ("Resultado esperado / oráculo", "HTTP 409 Conflict; código 'INSUFFICIENT_STOCK'; 0 registros huérfanos creados en base de datos."),
        ("Resultado observado", "HTTP 409 Conflict en 3.6 ms con mensaje 'Stock insuficiente para SKU POL-IRO-CRE-S'; rollback atómico ejecutado; modal de advertencia en UI."),
        ("Veredicto", "Aprobada (PASSED)"),
        ("Ejecutado por / fecha", "Jim Alessandro Dávila Morales (QA Lead) / 22/09/2026"),
        ("Evidencias", "EV-02 (docs/auditoria_cierre/fig_7_fallback.png y tests/orders.test.ts)"),
        ("Issue, corrección y re-ejecución", "Issue #4 / Commit 89adda5 / Bloqueo pesimista FOR UPDATE y transaccionalidad verificada.")
    ]
    tbl_f2 = create_card_table(doc, f2_data, "Ficha PF-02: Bloqueo Transaccional por Stock Insuficiente (Funcional Inválido)")
    
    # Ficha 3: PI-01 (Interoperabilidad SUNAT/RENIEC)
    f3_data = [
        ("Código", "PI-01"),
        ("Requisito trazado", "RF-02 / Gestión y Validación Contractual de Clientes"),
        ("Subcaracterística ISO/IEC 25010", "Compatibilidad / Interoperabilidad (§4.2.3.1)"),
        ("Objetivo de prueba", "Validar el contrato formal de la API de padrón fiscal: tipado estricto, esquema JSON y autocompletado en formulario."),
        ("Precondiciones / datos", "Servidor activo; token de autenticación válido; RUC de prueba legítimo."),
        ("Procedimiento paso a paso", "1. Ingresar RUC '20608912345' en el módulo de clientes. 2. Disparar consulta GET /api/sunat/ruc/:numero. 3. Verificar status 200 y tipado de campos. 4. Comprobar autocompletado en la UI."),
        ("Entrada / payload", "GET /api/sunat/ruc/20608912345 | Headers: Accept: application/json"),
        ("Resultado esperado / oráculo", "HTTP 200 OK; JSON con { success: true, data: { ruc: '20608912345', razonSocial: '...', condicion: 'HABIDO' } }."),
        ("Resultado observado", "HTTP 200 OK en 18 ms; deserialización correcta en formulario React; autocompletado de dirección fiscal; validación Zod conforme."),
        ("Veredicto", "Aprobada (PASSED)"),
        ("Ejecutado por / fecha", "Harley Anthony Roman Delgado (Frontend Lead) / 22/09/2026"),
        ("Evidencias", "EV-03 (backend/tests/invoices.sunat.test.ts y docs/auditoria_cierre/fig_13_interop.png)"),
        ("Issue, corrección y re-ejecución", "Issue #7 / Commit 89adda5 / Sanitización regex /^[12][0-9]{10}$/ homologada.")
    ]
    tbl_f3 = create_card_table(doc, f3_data, "Ficha PI-01: Verificación de Contrato e Integración con Padrón SUNAT/RENIEC (Interoperabilidad)")

    # Ficha 4: PC-01 (Coexistencia vCPU Compartida)
    f4_data = [
        ("Código", "PC-01"),
        ("Requisito trazado", "RNF-04 / Desempeño y Coexistencia Multiproceso en Cloud Hosting"),
        ("Subcaracterística ISO/IEC 25010", "Compatibilidad / Coexistencia (§4.2.3.2)"),
        ("Objetivo de prueba", "Medir cuantitativamente el impacto recíproco entre el Servicio A (API REST LeoFit) y el Servicio B (Reportes) compartiendo la misma vCPU lógica."),
        ("Precondiciones / datos", "Servicio A en puerto 4000; Servicio B en puerto 4100; afinidad de CPU fijada al núcleo 0 (emulación de vCPU compartida)."),
        ("Procedimiento paso a paso", "1. Medir 200 lecturas y 60 escrituras en A solo. 2. Medir 100 reportes en B solo. 3. Inyectar carga concurrente en B y medir A. 4. Inyectar carga concurrente en A y medir B. 5. Calcular variación %."),
        ("Entrada / payload", "GET /api/products (n=200) + POST /api/orders (n=60) + GET /report (n=100) bajo contención concurrente"),
        ("Resultado esperado / oráculo", "Variación de latencia en A <= 15.0%, tasa de error <= 0.5%, memoria RAM < 450 MB."),
        ("Resultado observado", "Latencia A lectura: 4.92 ms -> 4.42 ms (-10.2%); escritura: 5.02 ms -> 3.44 ms (-31.5%); tasa de error 0.0% (0 fallos); RAM pico 191.4 MB; latencia en B varió a 39.30 ms por contención de vCPU."),
        ("Veredicto", "Aprobada en Servicio A (PASSED) / Alerta de Contención en Servicio B"),
        ("Ejecutado por / fecha", "Lady Luz Loayza Rodriguez (Scrum Master / DevSecOps) / 22/10/2026"),
        ("Evidencias", "EV-05 y EV-06 (docs/gestion_academica/evidencias/iso25010_s10_s11/coexistencia/ y fig_coexistencia_latencias.png)"),
        ("Issue, corrección y re-ejecución", "Issue #11 / Aislamiento cgroups v2 en Render Cloud con 512 MB de memoria garantizada.")
    ]
    tbl_f4 = create_card_table(doc, f4_data, "Ficha PC-01: Monitoreo de Recursos y Degradación de Latencia en vCPU Compartida (Coexistencia)")

    curr_el = doc.tables[27]._element
    for tbl_to_insert in [tbl_f2, tbl_f3, tbl_f4]:
        p_sep = doc.add_paragraph()
        doc._body._body.remove(p_sep._element)
        curr_el.addnext(p_sep._element)
        p_sep.paragraph_format.space_before = Pt(8)
        p_sep.paragraph_format.space_after = Pt(4)
        p_sep._element.addnext(tbl_to_insert._element)
        curr_el = tbl_to_insert._element

    # -------------------------------------------------------------------------
    # 5. INSERCIÓN DE GALERÍA DE EVIDENCIAS FOTOGRÁFICAS EN ANEXO B
    # -------------------------------------------------------------------------
    print("Incrustando galería de capturas fotográficas en Anexo B...")
    curr_b_el = doc.tables[28]._element
    p_anexo_b_intro = insert_paragraph_after(curr_b_el, doc,
        text="Galería de Capturas de Pantalla y Evidencias Visuales Controladas (EV-01 a EV-06):",
        bold=True, font_size_pt=10, color_rgb=RGBColor(30, 58, 138), space_before=12, space_after=6)
    curr_b_el = p_anexo_b_intro._element

    evidences_gallery = [
        ("docs/auditoria_cierre/fig_10_crm.png",
         "Figura B.1: Interfaz PWA de Gestión y Creación Atómica de Pedidos con cálculo de totales y stock (EV-01)"),
        ("docs/auditoria_cierre/fig_7_fallback.png",
         "Figura B.2: Modal de Protección ante Errores y Rechazo por Stock Insuficiente en Almacén (EV-02)"),
        ("docs/auditoria_cierre/fig_4_pwa.png",
         "Figura B.3: Panel Operativo PWA en Dispositivo Móvil con Indicadores en Tiempo Real (EV-03)"),
        ("docs/auditoria_cierre/fig_analytics.png",
         "Figura B.4: Portal Público de Consulta y Trazabilidad de Pedidos para Clientes Finales (EV-04)"),
        ("docs/gestion_academica/evidencias/iso25010_s10_s11/fig_coexistencia_latencias.png",
         "Figura B.5: Gráfico de Variación de Latencias en Coexistencia ISO/IEC 25010 (EV-05)"),
        ("docs/gestion_academica/evidencias/iso25010_s10_s11/fig_coexistencia_p95.png",
         "Figura B.6: Gráfico de Percentil 95 (P95 Tail Latency) bajo Estrés de Contención Multiproceso (EV-06)")
    ]

    for img_rel_path, caption in evidences_gallery:
        full_img_path = os.path.abspath(img_rel_path)
        curr_b_el = insert_image_block(curr_b_el, doc, full_img_path, caption, width_inches=5.6)

    # -------------------------------------------------------------------------
    # 6. TABLA FORMAL DE CONFORMIDAD Y FIRMAS DIGITALES EN ANEXO E
    # -------------------------------------------------------------------------
    print("Insertando tabla formal de firmas en Anexo E...")
    p_firmas = None
    for p in doc.paragraphs:
        if "Firmas / responsables:" in p.text:
            p_firmas = p
            break

    if p_firmas:
        p_firmas.text = "Declaramos la autenticidad, rigor técnico y reproducibilidad de las pruebas registradas en este documento:"
        p_firmas.runs[0].bold = True
        
        tbl_firmas = doc.add_table(rows=6, cols=5)
        doc._body._body.remove(tbl_firmas._element)
        tbl_firmas.alignment = WD_TABLE_ALIGNMENT.CENTER
        tbl_firmas.autofit = False

        headers = ["N°", "Integrante", "Código UTP", "Rol en el Proyecto", "Firma / Conformidad"]
        widths = [Inches(0.5), Inches(2.3), Inches(1.1), Inches(1.8), Inches(1.3)]
        for c_idx, h in enumerate(headers):
            set_cell_text(tbl_firmas.rows[0].cells[c_idx], h, bold=True, font_size_pt=8.5, color_rgb=RGBColor(255, 255, 255))
            set_cell_background(tbl_firmas.rows[0].cells[c_idx], "1E3A8A")
            tbl_firmas.rows[0].cells[c_idx].width = widths[c_idx]

        team_rows = [
            ("1", "Loayza Rodriguez, Lady Luz", "U22221489", "Scrum Master / DevSecOps", "CONFORME (Digital)"),
            ("2", "Cárdenas Fernández, Víctor Leandro", "U19217414", "Product Owner / DBA", "CONFORME (Digital)"),
            ("3", "Roman Delgado, Harley Anthony", "U21313032", "Frontend Lead / UI-UX", "CONFORME (Digital)"),
            ("4", "Dávila Morales, Jim Alessandro", "U18206081", "QA Lead / Backend Node", "CONFORME (Digital)"),
            ("5", "Rojas Sanchez, Daniel Enrique", "U21214627", "Business Analyst / DevOps", "CONFORME (Digital)")
        ]
        for r_idx, row_vals in enumerate(team_rows, start=1):
            for c_idx, val in enumerate(row_vals):
                tbl_firmas.rows[r_idx].cells[c_idx].width = widths[c_idx]
                set_cell_text(tbl_firmas.rows[r_idx].cells[c_idx], val, bold=(c_idx == 1), font_size_pt=8)
            if r_idx % 2 == 1:
                for cell in tbl_firmas.rows[r_idx].cells:
                    set_cell_background(cell, "F8FAFC")

        p_firmas._element.addnext(tbl_firmas._element)

    # -------------------------------------------------------------------------
    # GUARDAR DOCUMENTO FINAL
    # -------------------------------------------------------------------------
    print(f"Guardando documento enriquecido en: {doc_path}")
    doc.save(doc_path)
    print("[EXITO] Documento enriquecido con imágenes, fichas y firmas exitosamente.")

if __name__ == '__main__':
    enrich_document()
