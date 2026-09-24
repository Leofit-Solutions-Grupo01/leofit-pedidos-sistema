-- =============================================================================
-- SISTEMA DE GESTIÓN DE PEDIDOS Y CONTROL DE INVENTARIO - LEOFIT SOLUTIONS
-- SCRIPT DML: DATOS INICIALES (SEEDS)
-- Catálogo deportivo completo: tallas, colores, distritos, métodos de pago,
-- productos, variantes de inventario y clientes.
-- =============================================================================
-- VERSION : 2.0.0
-- MOTOR   : PostgreSQL 16+
-- =============================================================================

-- Deshabilitar triggers de FK durante la carga masiva
SET session_replication_role = replica;

-- =============================================================================
-- 1. TALLAS (tabla sizes)
-- =============================================================================
INSERT INTO sizes (id, code, label) VALUES
(1, 'S',     'Small'),
(2, 'M',     'Medium'),
(3, 'L',     'Large'),
(4, 'XL',    'Extra Large'),
(5, 'XXL',   'Double Extra Large'),
(6, 'UNICA', 'Talla Única')
ON CONFLICT (code) DO UPDATE SET label = EXCLUDED.label;

SELECT setval('sizes_id_seq', (SELECT MAX(id) FROM sizes));

-- =============================================================================
-- 2. COLORES (tabla colors)
-- =============================================================================
INSERT INTO colors (id, name, hex) VALUES
(1,  'Negro Lavado',    '#1A1A1A'),
(2,  'Blanco Crudo',    '#F5F0E8'),
(3,  'Gris Jaspe',      '#8A8A8A'),
(4,  'Negro Mate',      '#0D0D0D'),
(5,  'Azul Marino',     '#002368'),
(6,  'Rojo Fuego',      '#CC2200'),
(7,  'Verde Militar',   '#3B4A2F'),
(8,  'Negro / Rojo',    '#440000'),
(9,  'Gris / Blanco',   '#C0C0C0'),
(10, 'Azul / Negro',    '#001338')
ON CONFLICT (name) DO UPDATE SET hex = EXCLUDED.hex;

SELECT setval('colors_id_seq', (SELECT MAX(id) FROM colors));

-- =============================================================================
-- 3. DISTRITOS DE REPARTO (tabla districts)
-- =============================================================================
INSERT INTO districts (id, name) VALUES
(1,  'Jesús María'),
(2,  'San Isidro'),
(3,  'San Miguel'),
(4,  'Barranco'),
(5,  'Miraflores'),
(6,  'Surco'),
(7,  'La Molina'),
(8,  'Lince'),
(9,  'San Borja'),
(10, 'Magdalena del Mar')
ON CONFLICT (name) DO NOTHING;

SELECT setval('districts_id_seq', (SELECT MAX(id) FROM districts));

-- =============================================================================
-- 4. MÉTODOS DE PAGO (tabla payment_methods)
-- =============================================================================
INSERT INTO payment_methods (id, code, name) VALUES
(1, 'YAPE',           'Yape'),
(2, 'PLIN',           'Plin'),
(3, 'TRANSFERENCIA',  'Transferencia Bancaria'),
(4, 'CONTRAENTREGA',  'Contraentrega en Efectivo'),
(5, 'EFECTIVO',       'Efectivo Directo')
ON CONFLICT (code) DO UPDATE SET name = EXCLUDED.name;

SELECT setval('payment_methods_id_seq', (SELECT MAX(id) FROM payment_methods));

-- =============================================================================
-- 5. USUARIOS DEL SISTEMA (tabla users)
-- Contraseña de prueba: "password" — hash bcrypt $2b$ rounds=10
-- =============================================================================
INSERT INTO users (id, name, email, password_hash, role, is_active) VALUES
(1, 'Víctor Leandro Cárdenas Fernández', 'admin@leofit.pe',    '$2b$10$92IXUNpkjO0rOQ5byMi.Ye4oKoEa3Ro9llC/.og/at2.uheWG/igi', 'ADMIN',    TRUE),
(2, 'Lady Luz Loayza Rodriguez',          'operador@leofit.pe', '$2b$10$92IXUNpkjO0rOQ5byMi.Ye4oKoEa3Ro9llC/.og/at2.uheWG/igi', 'OPERATOR', TRUE)
ON CONFLICT (id) DO NOTHING;

SELECT setval('users_id_seq', (SELECT MAX(id) FROM users));

-- =============================================================================
-- 6. CATEGORÍAS (tabla categories)
-- =============================================================================
INSERT INTO categories (id, name, description) VALUES
(1, 'Camisetas',         'Línea de camisetas oversize y fit en algodón peinado 20/1 y 24/1'),
(2, 'Shorts',            'Shorts deportivos con forro de compresión y bolsillos con cierre'),
(3, 'Joggers',           'Pantalones de entrenamiento corte slim con rib ajustado'),
(4, 'Tirantes / Bividis','Prendas sin mangas corte halter y espalda nadadora para entrenamiento'),
(5, 'Accesorios',        'Correas de levantamiento, muñequeras, shakers y gorras deportivas')
ON CONFLICT (id) DO NOTHING;

SELECT setval('categories_id_seq', (SELECT MAX(id) FROM categories));

-- =============================================================================
-- 7. PRODUCTOS (tabla products)
-- =============================================================================
INSERT INTO products (id, category_id, name, description, base_price, image_url, is_active) VALUES
(1, 1, 'Camiseta Oversize Heavy Acid Wash',
   'Confeccionada en algodón 100% 20/1 con proceso acid wash industrial y estampado serigráfico de alta densidad.',
   65.00, 'https://images.unsplash.com/photo-1521572267360-ee0c2909d518?w=500', TRUE),

(2, 2, 'Short 2-en-1 Pro Performance',
   'Short exterior de secado rápido con calza interior de compresión y bolsillo elástico para smartphone.',
   55.00, 'https://images.unsplash.com/photo-1591195853828-11db59a44f6b?w=500', TRUE),

(3, 3, 'Jogger Slim Tech Fleece',
   'Jogger térmico con tecnología stretch de 4 vías, bolsillos termosellados y pretina reforzada.',
   79.00, 'https://images.unsplash.com/photo-1552902865-b72c031ac5ea?w=500', TRUE),

(4, 4, 'Bividi Drop Cut Raw Edge',
   'Musculosa deportiva con corte drop armhole para máxima ventilación y rango de movimiento.',
   45.00, 'https://images.unsplash.com/photo-1581655353564-df123a1eb820?w=500', TRUE),

(5, 5, 'Straps de Levantamiento Reforzados',
   'Par de correas de algodón con soporte acolchado de neopreno para muñecas.',
   28.00, 'https://images.unsplash.com/photo-1517838277536-f5f99be501cd?w=500', TRUE),

(6, 1, 'Camiseta Slim Fit Essential',
   'Camiseta entallada de algodón 24/1 peinado, corte recto con cuello acanalado reforzado.',
   55.00, 'https://images.unsplash.com/photo-1562157873-818bc0726f68?w=500', TRUE),

(7, 2, 'Short Board 5" Training',
   'Short running liviano con bolsillos traseros con velcro y banda reflectante para seguridad.',
   49.00, 'https://images.unsplash.com/photo-1562886877-f88e38ac9b55?w=500', TRUE),

(8, 5, 'Gorra Snapback Dry-Fit',
   'Gorra deportiva con tejido dry-fit, visera pre-curvada y cierre snapback regulable.',
   38.00, 'https://images.unsplash.com/photo-1523450001312-faa4e2e37f0f?w=500', TRUE)
ON CONFLICT (id) DO NOTHING;

SELECT setval('products_id_seq', (SELECT MAX(id) FROM products));

-- =============================================================================
-- 8. VARIANTES DE PRODUCTO E INVENTARIO (tabla product_variants)
-- Deshabilitamos el trigger de descuento de stock para los seeds
-- =============================================================================
ALTER TABLE order_items DISABLE TRIGGER trg_decrement_stock_on_order;

INSERT INTO product_variants (id, product_id, size_id, color_id, sku, stock, alert_threshold) VALUES
-- Camiseta Oversize Heavy Acid Wash (product 1) — color: Negro Lavado (1)
(1,  1, 1, 1, 'LF-TSH-OVR-BLK-S',   12, 3),
(2,  1, 2, 1, 'LF-TSH-OVR-BLK-M',   18, 3),
(3,  1, 3, 1, 'LF-TSH-OVR-BLK-L',    8, 3),
(4,  1, 4, 1, 'LF-TSH-OVR-BLK-XL',   2, 3),  -- ⚠ stock bajo
(5,  1, 5, 1, 'LF-TSH-OVR-BLK-XXL',  4, 3),

-- Short 2-en-1 Pro Performance (product 2) — color: Gris Jaspe (3)
(6,  2, 2, 3, 'LF-SHT-2N1-GRY-M',   15, 4),
(7,  2, 3, 3, 'LF-SHT-2N1-GRY-L',   10, 4),
(8,  2, 4, 3, 'LF-SHT-2N1-GRY-XL',   3, 4),  -- ⚠ stock bajo

-- Jogger Slim Tech Fleece (product 3) — color: Negro Mate (4)
(9,  3, 2, 4, 'LF-JOG-SLM-BLK-M',    7, 3),
(10, 3, 3, 4, 'LF-JOG-SLM-BLK-L',    5, 3),
(11, 3, 4, 4, 'LF-JOG-SLM-BLK-XL',   9, 3),

-- Bividi Drop Cut Raw Edge (product 4) — color: Blanco Crudo (2)
(12, 4, 2, 2, 'LF-BIV-DRP-WHT-M',   14, 3),
(13, 4, 3, 2, 'LF-BIV-DRP-WHT-L',    6, 3),
-- también en Negro Lavado (1)
(14, 4, 2, 1, 'LF-BIV-DRP-BLK-M',   11, 3),

-- Straps de Levantamiento (product 5) — color: Negro/Rojo (8), talla única (6)
(15, 5, 6, 8, 'LF-ACC-STP-RED-U',    25, 5),

-- Camiseta Slim Fit Essential (product 6) — colores: Azul Marino (5) y Rojo Fuego (6)
(16, 6, 1, 5, 'LF-TSH-SLM-NVY-S',    9, 3),
(17, 6, 2, 5, 'LF-TSH-SLM-NVY-M',   14, 3),
(18, 6, 3, 5, 'LF-TSH-SLM-NVY-L',    7, 3),
(19, 6, 2, 6, 'LF-TSH-SLM-RED-M',    5, 3),
(20, 6, 3, 6, 'LF-TSH-SLM-RED-L',    2, 3),  -- ⚠ stock bajo

-- Short Board 5" Training (product 7) — color: Verde Militar (7)
(21, 7, 2, 7, 'LF-SHT-BRD-GRN-M',   12, 3),
(22, 7, 3, 7, 'LF-SHT-BRD-GRN-L',    8, 3),

-- Gorra Snapback Dry-Fit (product 8) — color: Negro Mate (4), talla única (6)
(23, 8, 6, 4, 'LF-ACC-CAP-BLK-U',   30, 5)
ON CONFLICT (id) DO NOTHING;

SELECT setval('product_variants_id_seq', (SELECT MAX(id) FROM product_variants));

-- =============================================================================
-- 9. CLIENTES (tabla clients)
-- =============================================================================
INSERT INTO clients (id, full_name, phone, address, district_id, reference) VALUES
(1, 'Carlos Eduardo Mendoza Flores',
   '987654321', 'Av. Brasil 1420 Dpto 802', 1,
   'A dos cuadras del Hospital del Niño'),

(2, 'Valeria Sofía Alarcón Benavides',
   '912345678', 'Calle Las Begonias 340', 2,
   'Frente a la torre financiera'),

(3, 'Rodrigo Alonso Quispe Huamán',
   '998877665', 'Av. Universitaria 2100 Cond. Los Robles Torre B 401', 3,
   'Espalda de Plaza San Miguel'),

(4, 'Maricielo Andrea Peña Ruiz',
   '934567890', 'Jr. Batalla de Junín 215', 4,
   'Cerca a la estación Bulevar del Metropolitano'),

(5, 'Diego Sebastián Torres Vílchez',
   '945678123', 'Av. Larco 880 Piso 3', 5,
   'Frente al Parque Kennedy'),

(6, 'Luciana Paola Ramos Callupe',
   '976543210', 'Calle Monte Bello 230', 6,
   'A media cuadra del Ovalo Higuereta'),

(7, 'Andrés Felipe Huanca Mamani',
   '923456789', 'Av. La Molina 1234 Urb. El Remanso', 7,
   'Portón azul, referencia estación La Molina')
ON CONFLICT (id) DO NOTHING;

SELECT setval('clients_id_seq', (SELECT MAX(id) FROM clients));

-- =============================================================================
-- 10. PEDIDOS (tabla orders)
-- =============================================================================
INSERT INTO orders (id, order_number, client_id, user_id, payment_method_id, status,
                    subtotal, shipping_cost, total_amount, notes) VALUES
(1, 'ORD-2026-001', 1, 1, 1, 'RECIBIDO',
   130.00, 10.00, 140.00, 'Cliente solicita entrega entre 2:00 pm y 5:00 pm'),

(2, 'ORD-2026-002', 2, 1, 2, 'PREPARACION',
   134.00, 12.00, 146.00, 'Empaque para regalo con dedicatoria'),

(3, 'ORD-2026-003', 3, 2, 3, 'EN_CAMINO',
   79.00,  8.00,  87.00, 'Repartidor motorizado en ruta. Código de seguimiento enviado.'),

(4, 'ORD-2026-004', 4, 1, 4, 'ENTREGADO',
   65.00, 10.00,  75.00, 'Pedido recibido conforme y cobrado en efectivo.'),

(5, 'ORD-2026-005', 5, 2, 1, 'RECIBIDO',
   183.00, 12.00, 195.00, 'Cliente VIP — empacar con bolsa premium y tarjeta de agradecimiento.'),

(6, 'ORD-2026-006', 6, 1, 5, 'CANCELADO',
   55.00,  8.00,  63.00, 'Cliente canceló por error en la talla seleccionada.')
ON CONFLICT (id) DO NOTHING;

SELECT setval('orders_id_seq', (SELECT MAX(id) FROM orders));

-- =============================================================================
-- 11. ÍTEMS DE PEDIDO (tabla order_items)
-- ⚡ Trigger de descuento deshabilitado — el stock fue cargado directamente
-- =============================================================================
INSERT INTO order_items (id, order_id, variant_id, quantity, unit_price, subtotal) VALUES
-- ORD-2026-001: 2× Camiseta Oversize Talla M
(1, 1, 2,  2, 65.00, 130.00),

-- ORD-2026-002: Short M + Camiseta L + Straps
(2, 2, 6,  1, 55.00,  55.00),
(3, 2, 3,  1, 65.00,  65.00),
(4, 2, 15, 1, 14.00,  14.00),

-- ORD-2026-003: 1× Jogger Slim M
(5, 3, 9,  1, 79.00,  79.00),

-- ORD-2026-004: 1× Camiseta Oversize S
(6, 4, 1,  1, 65.00,  65.00),

-- ORD-2026-005: Camiseta Slim Navy M + Jogger XL + Gorra
(7, 5, 17, 1, 55.00,  55.00),
(8, 5, 11, 1, 79.00,  79.00),
(9, 5, 23, 1, 38.00,  38.00),  -- cambio precio especial: 38 en lugar de 49+11

-- ORD-2026-006 (cancelado): Short 2-en-1 M
(10, 6, 6, 1, 55.00, 55.00)
ON CONFLICT (id) DO NOTHING;

SELECT setval('order_items_id_seq', (SELECT MAX(id) FROM order_items));

-- Reactivar trigger
ALTER TABLE order_items ENABLE TRIGGER trg_decrement_stock_on_order;

-- =============================================================================
-- 12. HISTORIAL DE ESTADOS (tabla order_status_history)
-- =============================================================================
INSERT INTO order_status_history (id, order_id, user_id, previous_status, new_status, comments) VALUES
(1, 1, 1, NULL,           'RECIBIDO',    'Pedido creado exitosamente desde WhatsApp'),
(2, 2, 1, 'RECIBIDO',     'PREPARACION', 'Prendas separadas en taller y empaquetadas'),
(3, 3, 2, 'PREPARACION',  'EN_CAMINO',   'Entregado a servicio de courier local'),
(4, 4, 1, 'EN_CAMINO',    'ENTREGADO',   'Entrega confirmada y recibida por el cliente'),
(5, 5, 2, NULL,           'RECIBIDO',    'Pedido VIP creado y priorizado'),
(6, 6, 1, NULL,           'RECIBIDO',    'Pedido creado'),
(7, 6, 1, 'RECIBIDO',     'CANCELADO',   'Cliente solicitó cancelación por talla incorrecta')
ON CONFLICT (id) DO NOTHING;

SELECT setval('order_status_history_id_seq', (SELECT MAX(id) FROM order_status_history));

-- Restaurar rol de replicación
SET session_replication_role = DEFAULT;

-- =============================================================================
-- VERIFICACIÓN RÁPIDA POST-SEED
-- =============================================================================
DO $$
DECLARE
    v_sizes     INT; v_colors INT; v_districts INT; v_products INT;
    v_variants  INT; v_clients INT; v_orders    INT;
BEGIN
    SELECT COUNT(*) INTO v_sizes     FROM sizes;
    SELECT COUNT(*) INTO v_colors    FROM colors;
    SELECT COUNT(*) INTO v_districts FROM districts;
    SELECT COUNT(*) INTO v_products  FROM products;
    SELECT COUNT(*) INTO v_variants  FROM product_variants;
    SELECT COUNT(*) INTO v_clients   FROM clients;
    SELECT COUNT(*) INTO v_orders    FROM orders;

    RAISE NOTICE '✅ Seeds cargados — sizes: %, colors: %, districts: %, products: %, variants: %, clients: %, orders: %',
        v_sizes, v_colors, v_districts, v_products, v_variants, v_clients, v_orders;
END;
$$;