-- =============================================================================
-- SISTEMA DE GESTIÓN DE PEDIDOS Y CONTROL DE INVENTARIO - LEOFIT SOLUTIONS
-- SCRIPT DML: DATOS INICIALES Y SEMILLAS DE PRUEBA (SEEDS)
-- =============================================================================

-- 1. Usuarios del Sistema
INSERT INTO users (id, name, email, password_hash, role) VALUES
(1, 'Víctor Leandro Cárdenas Fernández', 'admin@leofit.pe', '$2b$10$92IXUNpkjO0rOQ5byMi.Ye4oKoEa3Ro9llC/.og/at2.uheWG/igi', 'ADMIN'),
(2, 'Lady Luz Loayza Rodriguez', 'operador@leofit.pe', '$2b$10$92IXUNpkjO0rOQ5byMi.Ye4oKoEa3Ro9llC/.og/at2.uheWG/igi', 'OPERATOR')
ON CONFLICT (id) DO NOTHING;

-- 2. Categorías
INSERT INTO categories (id, name, description) VALUES
(1, 'Camisetas', 'Línea de camisetas oversize y fit en algodón peinado 20/1 y 24/1'),
(2, 'Shorts', 'Shorts deportivos con forro de compresión y bolsillos con cierre'),
(3, 'Joggers', 'Pantalones de entrenamiento y corte slim con rib ajustado'),
(4, 'Tirantes / Bividis', 'Prendas sin mangas corte halter y espalda nadadora para entrenamiento pesado'),
(5, 'Accesorios', 'Correas de levantamiento, muñequeras, shakers y gorras deportivas')
ON CONFLICT (id) DO NOTHING;

-- 3. Productos
INSERT INTO products (id, category_id, name, description, base_price, image_url, is_active) VALUES
(1, 1, 'Camiseta Oversize Heavy Acid Wash', 'Confeccionada en algodón 100% 20/1 con proceso acid wash industrial y estampado serigráfico de alta densidad.', 65.00, 'https://images.unsplash.com/photo-1521572267360-ee0c2909d518?w=500', TRUE),
(2, 2, 'Short 2-en-1 Pro Performance', 'Short exterior de secado rápido con calza interior de compresión y bolsillo elástico para smartphone.', 55.00, 'https://images.unsplash.com/photo-1591195853828-11db59a44f6b?w=500', TRUE),
(3, 3, 'Jogger Slim Tech Fleece', 'Jogger térmico con tecnología stretch de 4 vías, bolsillos termosellados y pretina reforzada.', 79.00, 'https://images.unsplash.com/photo-1552902865-b72c031ac5ea?w=500', TRUE),
(4, 4, 'Bividi Drop Cut Raw Edge', 'Musculosa deportiva con corte drop armhole para máxima ventilación y rango de movimiento.', 45.00, 'https://images.unsplash.com/photo-1581655353564-df123a1eb820?w=500', TRUE),
(5, 5, 'Straps de Levantamiento Reforzados', 'Par de correas de algodón con soporte acolchado de neopreno para muñecas.', 28.00, 'https://images.unsplash.com/photo-1517838277536-f5f99be501cd?w=500', TRUE)
ON CONFLICT (id) DO NOTHING;

-- 4. Variantes de Producto e Inventario
INSERT INTO product_variants (id, product_id, size, color, sku, stock, alert_threshold) VALUES
(1, 1, 'S', 'Negro Lavado', 'LF-TSH-OVR-BLK-S', 12, 3),
(2, 1, 'M', 'Negro Lavado', 'LF-TSH-OVR-BLK-M', 18, 3),
(3, 1, 'L', 'Negro Lavado', 'LF-TSH-OVR-BLK-L', 8, 3),
(4, 1, 'XL', 'Negro Lavado', 'LF-TSH-OVR-BLK-XL', 2, 3), -- Alerta de stock bajo
(5, 2, 'M', 'Gris Jaspe', 'LF-SHT-2N1-GRY-M', 15, 4),
(6, 2, 'L', 'Gris Jaspe', 'LF-SHT-2N1-GRY-L', 10, 4),
(7, 3, 'M', 'Negro Mate', 'LF-JOG-SLM-BLK-M', 7, 3),
(8, 3, 'L', 'Negro Mate', 'LF-JOG-SLM-BLK-L', 5, 3),
(9, 4, 'M', 'Blanco Crudo', 'LF-BIV-DRP-WHT-M', 14, 3),
(10, 5, 'UNICA', 'Negro / Rojo', 'LF-ACC-STP-RED-U', 25, 5)
ON CONFLICT (id) DO NOTHING;

-- 5. Clientes
INSERT INTO clients (id, full_name, phone, address, district, reference) VALUES
(1, 'Carlos Eduardo Mendoza Flores', '987654321', 'Av. Brasil 1420 Dpto 802', 'Jesús María', 'A dos cuadras del Hospital del Niño'),
(2, 'Valeria Sofía Alarcón Benavides', '912345678', 'Calle Las Begonias 340', 'San Isidro', 'Frente a la torre financiera'),
(3, 'Rodrigo Alonso Quispe Huamán', '998877665', 'Av. Universitaria 2100 Condominio Los Robles Torre B 401', 'San Miguel', 'Espalda de Plaza San Miguel'),
(4, 'Maricielo Andrea Peña Ruiz', '934567890', 'Jr. Batalla de Junín 215', 'Barranco', 'Cerca a la estación Bulevar del Metropolitano')
ON CONFLICT (id) DO NOTHING;

-- 6. Pedidos
INSERT INTO orders (id, order_number, client_id, user_id, status, subtotal, shipping_cost, total_amount, payment_method, notes) VALUES
(1, 'ORD-2026-001', 1, 1, 'RECIBIDO', 130.00, 10.00, 140.00, 'YAPE', 'Cliente solicita entrega entre 2:00 pm y 5:00 pm'),
(2, 'ORD-2026-002', 2, 1, 'PREPARACION', 134.00, 12.00, 146.00, 'PLIN', 'Empaque para regalo con dedicatoria'),
(3, 'ORD-2026-003', 3, 2, 'EN_CAMINO', 79.00, 8.00, 87.00, 'TRANSFERENCIA', 'Repartidor motorizado en ruta. Código de seguimiento enviado.'),
(4, 'ORD-2026-004', 4, 1, 'ENTREGADO', 65.00, 10.00, 75.00, 'CONTRAENTREGA', 'Pedido recibido conforme y cobrado en efectivo.')
ON CONFLICT (id) DO NOTHING;

-- 7. Detalle de Items de Pedido
INSERT INTO order_items (id, order_id, variant_id, quantity, unit_price, subtotal) VALUES
(1, 1, 2, 2, 65.00, 130.00), -- 2 x Camiseta Oversize Talla M
(2, 2, 5, 1, 55.00, 55.00),  -- 1 x Short 2-en-1 Talla M
(3, 2, 3, 1, 65.00, 65.00),  -- 1 x Camiseta Oversize Talla L
(4, 2, 10, 1, 14.00, 14.00), -- 1 x Par Straps (descuento promocional)
(5, 3, 7, 1, 79.00, 79.00),  -- 1 x Jogger Slim Talla M
(6, 4, 1, 1, 65.00, 65.00)   -- 1 x Camiseta Oversize Talla S
ON CONFLICT (id) DO NOTHING;

-- 8. Historial de Estados
INSERT INTO order_status_history (id, order_id, user_id, previous_status, new_status, comments) VALUES
(1, 1, 1, NULL, 'RECIBIDO', 'Pedido creado exitosamente desde WhatsApp'),
(2, 2, 1, 'RECIBIDO', 'PREPARACION', 'Prendas separadas en taller de confección y empaquetadas'),
(3, 3, 2, 'PREPARACION', 'EN_CAMINO', 'Entregado a servicio de courier local'),
(4, 4, 1, 'EN_CAMINO', 'ENTREGADO', 'Entrega confirmada y recibida por el cliente')
ON CONFLICT (id) DO NOTHING;
