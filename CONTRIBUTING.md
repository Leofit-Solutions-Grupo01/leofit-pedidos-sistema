# Guía de Contribución - Leofit Solutions

Este documento describe los lineamientos y directrices para proponer mejoras, reportar observaciones y enviar contribuciones al proyecto **Leofit Solutions - Sistema de Gestión de Pedidos & Inventario**.

---

## 1. Tabla de Contenidos
1. [Código de Conducta](#2-código-de-conducta)
2. [Modalidades de Contribución](#3-modalidades-de-contribución)
3. [Flujo de Trabajo con Git](#4-flujo-de-trabajo-con-git)
4. [Configuración del Entorno de Desarrollo](#5-configuración-del-entorno-de-desarrollo)
5. [Estándares de Código y Mensajes de Confirmación](#6-estándares-de-código-y-mensajes-de-confirmación)
6. [Ejecución de Pruebas Automatizadas](#7-ejecución-de-pruebas-automatizadas)
7. [Proceso de Solicitud de Extracción (Pull Request)](#8-proceso-de-solicitud-de-extracción-pull-request)

---

## 2. Código de Conducta
Al participar en este proyecto, los colaboradores se comprometen a adherirse a las directrices establecidas en el [Código de Conducta](CODE_OF_CONDUCT.md).

---

## 3. Modalidades de Contribución

* **Reporte de Errores (Bugs):** Abrir un *Issue* en GitHub detallando el comportamiento esperado, el comportamiento observado, pasos de reproducción y capturas de pantalla de soporte.
* **Propuesta de Nuevas Funcionalidades:** Abrir un *Issue* de tipo *Feature Request* justificando el cambio y el valor aportado a la operativa del negocio.
* **Envío de Código:** Subsanar incidencias abiertas o implementar funcionalidades previamente aprobadas a través de una Solicitud de Extracción (*Pull Request*).

---

## 4. Flujo de Trabajo con Git

El desarrollo se organiza bajo el modelo de ramas por funcionalidad (*Feature Branches*):

1. Realizar una bifurcación (*Fork*) o clonar el repositorio principal si se cuenta con permisos de colaborador.
2. Crear una rama descriptiva a partir de `main`:
   ```bash
   git checkout -b feature/nombre-de-la-funcionalidad
   # o para correcciones de errores:
   git checkout -b fix/descripcion-del-bug
   ```
3. Realizar los cambios manteniendo confirmaciones atómicas, coherentes y ordenadas.
4. Publicar la rama en el repositorio remoto:
   ```bash
   git push origin feature/nombre-de-la-funcionalidad
   ```
5. Abrir una Solicitud de Extracción (*Pull Request*) dirigida a la rama `main`.

---

## 5. Configuración del Entorno de Desarrollo

### Requisitos Previos
* **Node.js**: v20.x o v22.x LTS
* **npm**: v10.x o superior
* **Git**: v2.x

### Procedimiento de Instalación y Ejecución

```bash
# 1. Clonar el repositorio
git clone https://github.com/Leofit-Solutions-Grupo01/leofit-pedidos-sistema.git
cd leofit-pedidos-sistema/frontend

# 2. Instalar dependencias
npm install

# 3. Iniciar el servidor de desarrollo local
npm run dev

# 4. Compilar para producción (validación de build)
npm run build
```

---

## 6. Estándares de Código y Mensajes de Confirmación

### Convención de Commits (Conventional Commits)
Los mensajes de confirmación deben apegarse a la siguiente estructura formal:

```text
<tipo>(<alcance opcional>): <descripción corta en imperativo>
```

**Tipos estandarizados:**
* `feat`: Incorporación de una nueva funcionalidad.
* `fix`: Corrección de un defecto o error de software.
* `docs`: Modificaciones exclusivas en documentación técnica o académica.
* `style`: Ajustes de formato o estilos visuales sin alteración de lógica.
* `refactor`: Refactorización de código sin adición de funciones ni arreglo de bugs.
* `test`: Adición o actualización de pruebas unitarias o de integración.
* `chore`: Labores de mantenimiento de dependencias, scripts o configuración de compilación.

### Estilo de Programación
* Empleo estricto de TypeScript; prohibido el uso indiscriminado del tipo `any`.
* Componentes funcionales modulares basados en React Hooks.
* Clases utilitarias de TailwindCSS para consistencia visual de la interfaz.

---

## 7. Ejecución de Pruebas Automatizadas

Antes de someter cualquier Pull Request, se debe verificar la ejecución satisfactoria de la suite de pruebas unitarias:

```bash
cd frontend
npm test
```

---

## 8. Proceso de Solicitud de Extracción (Pull Request)

1. Verificar que la aplicación compile sin advertencias (`npm run build`) y que todas las pruebas pasen (`npm test`).
2. Actualizar la documentación técnica en `/docs` o `README.md` si los cambios impactan la arquitectura o el flujo del sistema.
3. Asignar al menos un revisor del equipo para la revisión formal de código (*Code Review*).
4. Comprobar que los pipelines de integración continua en GitHub Actions finalicen en estado exitoso (*Passing*).
