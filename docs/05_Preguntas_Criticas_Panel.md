PREGUNTAS CRÍTICAS PARA EL PANEL PRINCIPAL
1. PREGUNTAS SOBRE LOS KPI'S (Métricas del Dashboard)
Sobre "Pedidos Hoy: 4"

¿"Pedidos Hoy" significa pedidos creados hoy o pedidos entregados hoy?

¿Se contabilizan solo los pedidos confirmados o también los cancelados?

¿A qué hora se reinicia el contador? ¿Medianoche o a las 6:00 am (hora de apertura del negocio)?

¿Qué pasa si Víctor recibe un pedido a las 11:59 pm y otro a las 12:01 am? ¿Cómo se separan por días?

¿Los pedidos de WhatsApp y llamadas telefónicas se registran con la misma prioridad?

¿Qué sucede si Víctor registra un pedido de un día anterior (porque se le olvidó) y luego el sistema lo cuenta como "pedido de hoy"?

Sobre "Pendientes: 5"

¿Un pedido "Pendiente" es lo mismo que "Recibido" (primer estado) o tiene otro significado?

¿Qué criterio define que un pedido pase de "Pendiente" a "En Camino"? ¿Es solo la decisión de Víctor?

¿Un pedido "Pendiente" puede volver a ese estado si el delivery falla?

¿Cómo se manejan los pedidos que llevan más de 24 horas en "Pendiente"? ¿Se debe alertar a Víctor?

¿Cuánto tiempo máximo debe estar un pedido en estado "Pendiente" antes de que el sistema lo marque como "Vencido" o "En Riesgo"?

Sobre "En Camino: 1"

¿"En Camino" significa que el delivery ya recogió el producto o que el repartidor está en ruta?

¿El sistema debe integrarse con la ubicación del delivery en tiempo real?

¿Qué pasa si un pedido "En Camino" no se entrega en el día? ¿Pasa a "Retrasado"?

¿El único pedido "En Camino" tiene tracking? ¿Cómo se actualiza su estado?

¿El delivery usa el sistema o solo comunica a Víctor por WhatsApp para actualizar manualmente?

Sobre "Entregados: 4"

¿"Entregados" significa que el cliente ya recibió el producto o que el delivery lo dejó en la dirección?

¿Quién confirma la entrega? ¿Víctor, el delivery o el cliente?

¿Qué pasa si un cliente dice que no recibió el producto (reclamo) después de que Víctor lo marcó como "Entregado"?

¿Cómo se manejan las devoluciones? ¿Un pedido "Entregado" puede volver a "En Camino" por devolución?

¿El sistema guarda la fecha y hora exacta de la entrega para calcular métricas de cumplimiento?

2. PREGUNTAS SOBRE LOS ICONOS Y DISEÑO
Iconos

El icono de calendario (event) en "Pedidos Hoy": ¿debe cambiar según el día de la semana?

El icono de reloj (schedule) en "Pendientes": ¿debe cambiar a reloj de arena cuando un pedido está atrasado?

El icono de camión (local_shipping) en "En Camino": ¿debe tener una variante con carga o vacío?

El icono de check (check_circle) en "Entregados": ¿debe ser verde siempre o cambiar a gris si el pedido fue devuelto?

¿Todos los iconos deben tener el mismo tamaño y alineación en todos los dispositivos (celular, tablet, desktop)?

Números

¿Los números (4, 5, 1, 4) deben mostrarse en color rojo (si son negativos) o en el color de la marca?

¿Si un número es 0, se debe mostrar "0" o "Sin pedidos"? ¿O un mensaje amigable?

¿Los números deben tener animación al cargar el dashboard (contar desde 0 hasta el valor final)?

¿Los números deben tener separadores de miles (ej: 1,234) o simplemente el número en crudo?

¿Qué pasa si el número supera los 999? ¿El diseño se rompe o se adapta?

3. PREGUNTAS SOBRE LA TABLA "ÚLTIMOS PEDIDOS"
Datos de la tabla (N° | Cliente | Fecha | Total | Estado)

¿El "N° Pedido" es autoincremental o tiene un formato específico (ej: LFT-001, LFT-20260827-001)?

Si un pedido fue creado por WhatsApp, ¿el campo "Cliente" guarda el número de teléfono o el nombre?

¿La fecha que se muestra es la de creación o la de última actualización?

¿El "Total" incluye el costo de delivery o solo el costo de los productos?

Si hay promociones o descuentos, ¿cómo se reflejan en el "Total"?

¿El estado de la tabla se actualiza automáticamente o requiere que Víctor actualice manualmente?

¿Cuántos pedidos se muestran en la tabla? ¿Los 5 más recientes o los 5 más urgentes?

¿La tabla debe ordenarse por fecha, estado o número de pedido? ¿Puede Víctor cambiar el orden?

Interacción con la tabla

¿Al hacer clic en una fila, se abre el detalle del pedido o solo al hacer clic en "Ver Detalle"?

¿Víctor puede cambiar el estado del pedido directamente desde la tabla (sin abrir el detalle)?

¿La tabla se actualiza automáticamente cuando un pedido cambia de estado o debe recargar la página?

¿Qué pasa si Víctor quiere ver más de 5 pedidos? ¿Debe haber un botón "Ver Todos" o "Cargar Más"?

¿Los pedidos "Entregados" deben ocultarse de la tabla para mostrar solo los activos?

¿La tabla muestra pedidos de hoy o de los últimos N días?

4. PREGUNTAS SOBRE EL BOTÓN "NUEVO PEDIDO"
Ubicación y comportamiento

¿El botón "Nuevo Pedido" es flotante (FAB) o está fijo en la interfaz?

¿El botón debe estar visible en todas las pantallas o solo en el Dashboard?

¿Al hacer clic en "Nuevo Pedido", se abre un modal o se navega a una nueva página?

¿Víctor puede crear un pedido desde el Dashboard sin navegar a la página de "Registro de Pedido"?

¿El botón debe tener un color diferente cuando no hay pedidos (ej: gris) para indicar que no hay acción?

¿Si Víctor está en el celular, el botón "Nuevo Pedido" debe estar en la parte inferior (como en apps nativas)?

5. PREGUNTAS SOBRE EL DISEÑO RESPONSIVE
Mobile-First

En celular, ¿las 4 tarjetas se muestran en 2 columnas de 2 o en 4 filas verticales?

En celular, ¿la tabla "Últimos Pedidos" debe hacer scroll horizontal o mostrar menos columnas?

En celular, ¿los textos y botones son lo suficientemente grandes para dedos (mínimo 44px de alto)?

¿Qué pasa en una pantalla muy pequeña (ej: 320px de ancho)? ¿El diseño se rompe?

¿El botón "Nuevo Pedido" en celular debe ser más grande o más pequeño que en desktop?

¿El nombre "Víctor" en la barra superior se recorta si la pantalla es muy angosta? ¿Qué hacer?

Breakpoints de Tailwind

¿Cómo se comportan las tarjetas en sm (640px), md (768px), lg (1024px), xl (1280px)?

¿Los iconos deben ser más grandes en desktop y más pequeños en mobile?

¿El padding y margen de los elementos cambian en cada breakpoint?

¿El texto de las tarjetas (ej: "Pedidos Hoy") se debe acortar en mobile para no ocupar espacio?

¿Qué sucede con el fondo blanco de las tarjetas en modo oscuro del celular?

6. PREGUNTAS SOBRE EL FLUJO Y USABILIDAD
Actualización en tiempo real

¿El dashboard se actualiza automáticamente cuando un nuevo pedido llega o Víctor debe recargar la página?

¿Víctor recibe una notificación push o un sonido cuando llega un nuevo pedido?

¿El número de "Pedidos Hoy" y "Pendientes" se actualiza sin recargar toda la página?

¿Si hay un error en la actualización, se muestra un mensaje de error al usuario?

Acciones rápidas

¿Víctor puede "Marcar como Listo" un pedido directamente desde el Dashboard?

¿Desde el Dashboard, Víctor puede llamar al cliente por teléfono con solo un clic?

¿El Dashboard debe mostrar un botón "Ver todos los Pendientes" para llevar a Víctor directamente a esa lista?

¿Víctor puede cambiar el estado de un pedido desde la tabla con un dropdown en lugar de abrir el detalle?

Feedback y validaciones

¿Qué mensaje ve Víctor cuando hace clic en "Nuevo Pedido" y no hay stock?

¿Qué mensaje ve Víctor cuando un pedido "En Camino" lleva más de 2 horas?

¿El dashboard muestra un banner de advertencia si hay pedidos "Pendientes" de hace más de 24 horas?

¿Qué pasa si Víctor intenta registrar un pedido con un cliente que ya existe? ¿El sistema lo detecta?

¿El sistema permite a Víctor escribir comentarios en el pedido (ej: "Cliente pidió talla M en rojo")?

7. PREGUNTAS SOBRE DATOS DE EJEMPLO (Mock Data)
Coherencia de datos

Si hay 4 "Pedidos Hoy", ¿la suma de "Pendientes" (5), "En Camino" (1) y "Entregados" (4) debe dar 10? ¿O no?

¿Los 4 pedidos entregados son de hoy o de ayer? Si son de hoy, ¿por qué no se contaron en "Pedidos Hoy"?

¿Los 5 "Pendientes" son de hoy o de varios días?

¿El total de pedidos en el sistema es la suma de todos los estados? ¿O hay pedidos "Cancelados" que no se muestran?

¿Los datos de ejemplo deben reflejar el comportamiento real de Leofit o son solo para la demostración?

Consistencia de datos

¿Víctor puede tener 5 "Pendientes" si solo tiene 1 "En Camino" y 4 "Entregados"? ¿Es lógico desde el punto de vista operativo?

¿Los pedidos "Entregados" deberían desaparecer del tablero después de 24 horas para no generar confusión?

¿Los números de las tarjetas se calculan al abrir el Dashboard o se guardan en la base de datos?

¿Qué pasa si Víctor abre el Dashboard en dos dispositivos al mismo tiempo? ¿Los números son consistentes?

8. PREGUNTAS DE SEGURIDAD Y PRIVACIDAD
Acceso y autenticación

¿Solo Víctor tiene acceso al Dashboard o pueden existir otros usuarios (ej: otro vendedor)?

¿El sistema guarda la sesión de Víctor o debe iniciar sesión cada vez?

¿Si Víctor cierra el navegador, vuelve a aparecer la pantalla de Login o se mantiene el Dashboard?

¿El sistema debe tener un temporizador de cierre de sesión por inactividad?

¿Las credenciales de Víctor (usuario, contraseña) se guardan en texto plano o están encriptadas?

Visibilidad de datos

¿El Dashboard muestra el nombre completo de los clientes? ¿O solo iniciales por privacidad?

¿Los datos de los clientes (dirección, teléfono) son visibles en el Dashboard o solo en la página de detalle?

¿Si alguien más ve el celular de Víctor, puede ver todos los datos de los clientes sin restricciones?

¿El sistema debe tener un modo de "Pantalla bloqueada" para que Víctor entregue el celular sin preocupación?

9. PREGUNTAS TÉCNICAS Y DE INFRAESTRUCTURA
Conexión a Internet

¿Qué pasa si Víctor abre el Dashboard sin internet? ¿El sistema muestra datos cacheados o muestra un error?

¿El Service Worker de la PWA guarda los datos del Dashboard para funcionamiento offline?

¿Cómo se sincronizan los datos cuando Víctor vuelve a tener conexión?

¿El Dashboard requiere conexión a la base de datos en tiempo real o solo cuando se abre?

¿Qué tan rápido debe cargar el Dashboard para que Víctor no se frustre? ¿Menos de 2 segundos?

Escalabilidad

¿El sistema está preparado para manejar 10 pedidos al día o 1000 pedidos al día?

¿La base de datos (MongoDB/MySQL) soporta el crecimiento de Leofit a largo plazo?

¿El Dashboard muestra un número máximo de pedidos o se adapta dinámicamente?

¿Qué pasa si Víctor tiene 500 pedidos "Pendientes"? ¿Las tarjetas se rompen o se adaptan?

¿El sistema debe mostrar una alerta cuando el inventario se acerque a cero?

Mantenimiento y actualizaciones

¿Cómo se actualiza el Dashboard cuando se agrega una nueva funcionalidad?

¿Víctor recibe notificación de actualizaciones o son automáticas (PWA)?

¿El sistema guarda logs de actividad para saber qué hizo Víctor en el Dashboard?

¿Qué pasa si hay un error en el sistema? ¿Víctor ve una pantalla de error o un mensaje amigable?

¿El sistema tiene un "Modo de Pruebas" donde Víctor puede simular pedidos sin afectar los datos reales?

10. PREGUNTAS DE NEGOCIO (Valor para Leofit)
ROI y mejora de procesos

¿Cómo se mide la mejora en el tiempo de atención después de implementar el sistema?

¿El Dashboard ayuda a Víctor a identificar qué productos se venden más y cuándo?

¿El sistema permite a Víctor ver el histórico de pedidos por cliente (para atención personalizada)?

¿El Dashboard muestra métricas de ingresos (ej: "Ventas del día: S/ 500")? ¿Por qué sí o por qué no?

¿El sistema permite generar reportes (ej: "Pedidos del mes", "Top 5 clientes")?

Crecimiento y futuro

¿Víctor podrá agregar más vendedores en el futuro y que cada uno tenga su propio Dashboard?

¿El sistema puede integrarse con pasarelas de pago (Culqi, PayPal) en el futuro?

¿El sistema puede enviar notificaciones automáticas a los clientes cuando su pedido cambie de estado?

¿El sistema puede generar un enlace de seguimiento para que el cliente vea el estado de su pedido?

¿El Dashboard podría mostrar un mapa con la ubicación de los deliveries "En Camino"?

11. PREGUNTAS DE DOCUMENTACIÓN Y PRESENTACIÓN
Para el curso

¿El Dashboard presentado es la versión final o es un MVP (Producto Mínimo Viable)?

¿Los datos del Dashboard son reales de Leofit o son simulados para la demostración?

¿Cómo se justifica que el Dashboard tenga exactamente esos KPI's y no otros?

¿Qué métricas se usarán para validar que el sistema realmente mejora el proceso (antes vs después)?

¿El Dashboard fue validado con Víctor (co-creación)? ¿Qué feedback dio?

Para el repositorio

¿El Dashboard está documentado en el README.md del repositorio?

¿El código del Dashboard tiene pruebas unitarias?

¿El Dashboard tiene enlaces a las otras pantallas (Login, Listado, Formulario, Productos)?

¿El código del Dashboard está optimizado para rendimiento (useMemo, React.memo)?

¿El Dashboard muestra un loading o skeleton mientras se cargan los datos?

PREGUNTAS MÁS CRÍTICAS (TOP 10)
Si tienes que priorizar, estas son las que debes responder primero:

#	Pregunta	Impacto
1	¿"Pedidos Hoy" significa pedidos creados hoy o entregados hoy?	Definición de la métrica clave
2	¿Cómo se sincronizan los datos cuando Víctor está offline y luego vuelve a internet?	Viabilidad técnica de la PWA
3	¿El total de pedidos en los KPI's (4+5+1+4=14) tiene sentido operativo o hay pedidos "Cancelados"?	Consistencia de los datos
4	¿Los pedidos "Pendientes" de hace más de 24 horas se marcan como "En Riesgo" o "Vencidos"?	Alertas y urgencia
5	¿Víctor puede actualizar el estado de un pedido directamente desde la tabla del Dashboard?	Usabilidad y eficiencia
6	¿Qué sucede si un cliente reclama que no recibió el pedido después de marcarlo como "Entregado"?	Gestión de incidencias
7	¿El Dashboard se actualiza automáticamente cuando llega un nuevo pedido o hay que recargar?	Experiencia de usuario
8	¿En celular, las tarjetas y tabla se ven bien o necesitan adaptaciones específicas?	Responsive y mobile-first
9	¿Quién valida que los datos del Dashboard sean correctos? ¿Víctor o el sistema?	Gobernanza de datos
10	¿El Dashboard muestra métricas de ingresos (ej: "Ventas del día: S/ 500")?	Valor de negocio