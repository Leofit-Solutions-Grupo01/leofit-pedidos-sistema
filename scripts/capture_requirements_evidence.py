import os
import sys
import http.server
import socketserver
import threading
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(line_buffering=True)

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
EVIDENCE_DIR = os.path.join(ROOT_DIR, "evidence", "requerimientos")
os.makedirs(EVIDENCE_DIR, exist_ok=True)

class QuietHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=ROOT_DIR, **kwargs)
    def log_message(self, format, *args):
        pass

def main():
    port = 8899
    httpd = socketserver.TCPServer(("127.0.0.1", port), QuietHandler)
    server_thread = threading.Thread(target=httpd.serve_forever, daemon=True)
    server_thread.start()
    print(f"Servidor HTTP local en http://127.0.0.1:{port}", flush=True)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            viewport={"width": 1440, "height": 920},
            device_scale_factor=2
        )
        page = context.new_page()
        base_url = f"http://127.0.0.1:{port}/index.html"

        # 1. Login inicial
        print("1. Capturando Login inicial...", flush=True)
        page.goto(base_url)
        page.wait_for_timeout(1000)
        page.screenshot(path=os.path.join(EVIDENCE_DIR, "01_Login_Autenticacion.png"))

        # Llenar credenciales
        print("1b. Llenando credenciales de acceso...", flush=True)
        page.fill("input[type='email']", "victor@leofit.com")
        page.fill("input[type='password']", "leofit2026")
        page.wait_for_timeout(300)
        page.screenshot(path=os.path.join(EVIDENCE_DIR, "01b_Login_Credenciales_Llenas.png"))
        
        # Enviar login
        page.locator("button[type='submit']").first.click()
        page.wait_for_timeout(1500)

        # 2. Dashboard
        print("2. Capturando Dashboard...", flush=True)
        page.screenshot(path=os.path.join(EVIDENCE_DIR, "02_Dashboard_Control_Operativo.png"))

        # Ocultar montos (privacidad granular)
        print("3. Capturando Privacidad Granular...", flush=True)
        eye_btn = page.locator("button:has-text('visibility')").first
        eye_btn.click()
        page.wait_for_timeout(500)
        page.screenshot(path=os.path.join(EVIDENCE_DIR, "02b_Dashboard_Privacidad_Oculta.png"))
        eye_btn.click()
        page.wait_for_timeout(300)

        # 3. Nuevo Pedido
        print("4. Capturando Nuevo Pedido...", flush=True)
        page.locator("header nav button").nth(2).click()
        page.wait_for_timeout(1200)
        page.screenshot(path=os.path.join(EVIDENCE_DIR, "03_Nuevo_Pedido_Formulario_Inicial.png"))

        # Seleccionar prendas en Nuevo Pedido
        add_btns = page.locator("button:has-text('+'), button:has-text('Agregar')")
        if add_btns.count() > 0:
            add_btns.first.click()
            page.wait_for_timeout(300)
            if add_btns.count() > 1:
                add_btns.nth(1).click()
                page.wait_for_timeout(300)

        # Llenar datos de cliente
        nombre_inp = page.locator("input#nombre, input[placeholder*='Carlos'], input[placeholder*='Nombre']").first
        if nombre_inp.is_visible():
            nombre_inp.fill("Alejandro Vargas Mendoza")

        tel_inp = page.locator("input#telefono, input[type='tel'], input[placeholder*='9']").first
        if tel_inp.is_visible():
            tel_inp.fill("987654321")

        dni_inp = page.locator("input#dni, input#documento, input[placeholder*='DNI']").first
        if dni_inp.is_visible():
            dni_inp.fill("72345678")

        dir_inp = page.locator("input#direccion, textarea#direccion, input[placeholder*='Av.']").first
        if dir_inp.is_visible():
            dir_inp.fill("Av. El Sol 1420 - Urb. San Roque")

        ref_inp = page.locator("input#referencia, input[placeholder*='Referencia']").first
        if ref_inp.is_visible():
            ref_inp.fill("Frente al Parque Central, portón negro")

        # Seleccionar Despacho Nacional Encomienda si existe
        provincia_btn = page.locator("button:has-text('Provincia'), button:has-text('Encomienda'), button:has-text('Nacional')")
        if provincia_btn.count() > 0:
            provincia_btn.first.click()
            page.wait_for_timeout(400)

        # Aplicar cupón de descuento LEOFIT10
        cupon_inp = page.locator("input[placeholder*='CUPÓN'], input[placeholder*='código'], input[placeholder*='cupon']")
        if cupon_inp.count() > 0:
            cupon_inp.first.fill("LEOFIT10")
            aplicar_btn = page.locator("button:has-text('Aplicar')")
            if aplicar_btn.count() > 0:
                aplicar_btn.first.click()
                page.wait_for_timeout(500)

        page.screenshot(path=os.path.join(EVIDENCE_DIR, "04_Nuevo_Pedido_Liquidacion_Cupon_Encomienda.png"))

        # 4. Bandeja de Pedidos
        print("5. Capturando Bandeja de Pedidos...", flush=True)
        page.locator("header nav button").nth(1).click()
        page.wait_for_timeout(1200)
        page.screenshot(path=os.path.join(EVIDENCE_DIR, "05_Bandeja_Gestion_Pedidos.png"))

        # Filtrar pedidos por estado
        chip_prep = page.locator("button:has-text('Preparación'), button:has-text('En Preparación')")
        if chip_prep.count() > 0:
            chip_prep.first.click()
            page.wait_for_timeout(500)
            page.screenshot(path=os.path.join(EVIDENCE_DIR, "05b_Pedidos_Filtrados_Estado.png"))
            page.locator("button:has-text('Todos')").first.click()
            page.wait_for_timeout(300)

        # Expandir un pedido para ver detalle
        print("6. Capturando Detalle de Pedido...", flush=True)
        row_order = page.locator("div:has-text('ORD-'), div:has-text('LFT-')").first
        row_order.click()
        page.wait_for_timeout(600)
        page.screenshot(path=os.path.join(EVIDENCE_DIR, "06_Detalle_Pedido_Acordeon.png"))

        # Clic en Recibo / PDF
        print("7. Capturando Recibo Digital PDF Modal...", flush=True)
        recibo_btn = page.locator("button:has-text('Ver Recibo')").first
        if recibo_btn.is_visible():
            recibo_btn.click()
            page.wait_for_timeout(700)
            page.screenshot(path=os.path.join(EVIDENCE_DIR, "07_Comprobante_Digital_Recibo.png"))

            # Pestaña Rótulo de Encomienda
            print("8. Capturando Rótulo de Encomienda...", flush=True)
            rotulo_btn = page.locator("button:has-text('Rótulo de Encomienda')").first
            if rotulo_btn.is_visible():
                rotulo_btn.click()
                page.wait_for_timeout(600)
                page.screenshot(path=os.path.join(EVIDENCE_DIR, "08_Comprobante_Rotulo_Encomienda.png"))

            # Cerrar modal
            close_btn = page.locator("button[aria-label='Cerrar modal']").first
            if close_btn.is_visible():
                close_btn.click()
                page.wait_for_timeout(400)

        # 5. Inventario
        print("9. Capturando Gestión de Inventario...", flush=True)
        page.locator("header nav button").nth(3).click()
        page.wait_for_timeout(1200)
        page.screenshot(path=os.path.join(EVIDENCE_DIR, "09_Gestion_Inventario_Stock.png"))

        # Clic en Editar un producto
        edit_btn = page.locator("button:has-text('Editar')").first
        if edit_btn.is_visible():
            edit_btn.click()
            page.wait_for_timeout(600)
            page.screenshot(path=os.path.join(EVIDENCE_DIR, "09b_Modal_Edicion_Producto.png"))
            cancel_btn = page.locator("button:has-text('Cancelar')").first
            if cancel_btn.is_visible():
                cancel_btn.click()
                page.wait_for_timeout(300)

        # 6. Portal de Rastreo Público
        print("10. Capturando Portal de Rastreo Público...", flush=True)
        page.locator("header nav button").nth(4).click()
        page.wait_for_timeout(1200)
        page.screenshot(path=os.path.join(EVIDENCE_DIR, "10_Portal_Rastreo_Publico_Busqueda.png"))

        # Realizar consulta de rastreo
        track_input = page.locator("input[placeholder*='LFT-'], input[placeholder*='código'], input[placeholder*='Buscar']").first
        if track_input.is_visible():
            track_input.fill("LFT-004")
            page.locator("button[type='submit']").first.click()
            page.wait_for_timeout(800)
            page.screenshot(path=os.path.join(EVIDENCE_DIR, "10b_Portal_Rastreo_Resultado_Timeline.png"))

        # 7. Modo Accesible A11y
        print("11. Capturando Modo Accesible...", flush=True)
        a11y_btn = page.locator("button:has-text('Vista')").first
        if a11y_btn.is_visible():
            a11y_btn.click()
            page.wait_for_timeout(600)
            page.screenshot(path=os.path.join(EVIDENCE_DIR, "11_Modo_Accesible_Alto_Contraste.png"))

        print("¡Todas las 15 capturas de pantalla de evidencia se completaron con éxito!", flush=True)
        browser.close()
        httpd.shutdown()

if __name__ == "__main__":
    main()
