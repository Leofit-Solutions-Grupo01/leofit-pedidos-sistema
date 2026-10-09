---
marp: true
theme: default
class: lead
paginate: true
---

# Leofit Solutions
## Sistema PWA de Gestión de Pedidos e Inventario
### Presentación Final APF3: Integración y Producción

**Curso:** Arquitectura de Software
**Integrantes:** Grupo 01
**Fecha:** [Fecha APF3]

---

## 1. Problema y Objetivo Final

- **Contexto:** Leofit requería un sistema moderno para escalar sus ventas y controlar su inventario de manera precisa y segura.
- **Logro:** Hemos implementado una PWA robusta, integrada con servicios externos y completamente desplegada en producción.

---

## 2. Alcance Logrado

- Aplicación PWA funcional e instalable en dispositivos.
- Gestión completa de productos y clientes.
- Flujo de pedidos con validación atómica e inventario.
- Panel de Administración y Dashboard con métricas clave.

---

## 3. Arquitectura y Diagramas

- Arquitectura Cliente-Servidor (React + Node.js/Express).
- **Integraciones Externas:**
  - WhatsApp Cloud API (Notificaciones)
  - Pasarelas de Pago (Webhooks)
  - RENIEC/SUNAT (Validación de identidad)
- **CI/CD:** Pipelines en GitHub Actions para pruebas automatizadas y despliegue continuo en Render y Netlify/GitHub Pages.

---

## 4. Demo y Capturas

- Login y acceso al sistema.
- Creación de un pedido complejo.
- Recepción de Webhook de pago.
- Verificación de notificación de WhatsApp.

---

## 5. Pruebas y Resultados

- Pruebas Unitarias y de Integración automatizadas.
- Pruebas de Contrato y Regresión de API.
- Validación exitosa de los sistemas externos.

---

## 6. Seguridad y Rendimiento

- Auditoría de Seguridad (OWASP Top 10 mitigado).
- Escaneo de Dependencias y Secretos sin vulnerabilidades.
- Rendimiento optimizado: Lighthouse > 90.

---

## 7. Conclusiones y Próximos Pasos

- **Conclusiones:** El sistema cumple con los requerimientos funcionales y no funcionales definidos, siendo estable para operar en producción.
- **Próximos Pasos:** Capacitación a usuarios finales, monitoreo en producción y futuras mejoras iterativas basadas en feedback.
