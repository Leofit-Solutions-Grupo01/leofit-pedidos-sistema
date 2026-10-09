---
marp: true
theme: default
class: lead
paginate: true
---

# Leofit Solutions
## Sistema PWA de Gestión de Pedidos e Inventario
### Presentación APF2: Arquitectura y MVP

**Curso:** Arquitectura de Software
**Integrantes:** Grupo 01
**Fecha:** [Fecha APF2]

---

## 1. Avances desde APF1

- Diseño detallado de la arquitectura.
- Modelado de Base de Datos.
- Desarrollo del MVP (Catálogo y Pedidos básicos).
- Implementación de Pipelines CI/CD iniciales.

---

## 2. Arquitectura y Diagramas Clave

- **Modelo C4 (Contexto y Contenedores):** Separación clara entre PWA Frontend, API Backend y Base de Datos.
- **Patrones aplicados:** MVC en Backend, Componentes en Frontend.
- *Ver documento de arquitectura para diagramas detallados.*

---

## 3. Demo y Capturas

- Vista del Catálogo de Productos.
- Flujo de creación de pedido simulado.
- Panel de Administración básico.

---

## 4. Pruebas y Resultados Iniciales

- Pruebas unitarias en backend (Jest).
- Pruebas de integración para Endpoints clave (`/api/products`, `/api/orders`).
- Cobertura de código aceptable para MVP.

---

## 5. Conclusiones y Próximos Pasos

- MVP funcional logrado con éxito.
- Pipeline automatizado ahorra tiempo en despliegues.
- **Próximos Pasos:** Integración con servicios externos (WhatsApp, Pagos, SUNAT), optimización de rendimiento y auditoría de seguridad para el APF3.

