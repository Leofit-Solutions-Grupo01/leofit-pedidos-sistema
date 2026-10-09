---
marp: true
theme: default
class: lead
paginate: true
---

# Leofit Solutions
## Sistema PWA de Gestión de Pedidos e Inventario
### Presentación APF1: Propuesta y Requisitos

**Curso:** Arquitectura de Software
**Integrantes:** Grupo 01
**Fecha:** [Fecha APF1]

---

## 1. Problema y Objetivo

- **Problema:** Procesos de venta manuales, falta de control de inventario y seguimiento de pedidos ineficiente en Leofit.
- **Objetivo:** Desarrollar un sistema de gestión integral (PWA) que optimice la toma de pedidos, controle el inventario y mejore la experiencia de los clientes y administradores.

---

## 2. Alcance y Requisitos

### Requisitos Funcionales
- Gestión de Catálogo y Productos.
- Carrito de compras y checkout.
- Panel de administración para gestión de pedidos.
- Seguimiento de estado de pedidos.

### Requisitos No Funcionales
- Interfaz PWA, responsiva y móvil (Mobile-First).
- Tiempos de respuesta < 2s.
- Alta disponibilidad y escalabilidad.

---

## 3. Arquitectura Inicial

- **Patrón Arquitectónico:** Cliente-Servidor (Monolito modular inicial).
- **Frontend:** React + Vite + TailwindCSS.
- **Backend:** Node.js + Express + TypeScript.
- **Base de Datos:** PostgreSQL (Relacional) con Prisma/Supabase.

---

## 4. Conclusiones y Próximos Pasos

- Validación de viabilidad técnica y operativa.
- Definición clara de requerimientos funcionales y reglas de negocio.
- **Próximos Pasos:** Desarrollo del MVP (Producto Mínimo Viable), configuración del entorno CI/CD y diseño de la base de datos para la entrega APF2.

