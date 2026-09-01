# Guía de Contribución - Leofit Solutions

¡Gracias por tu interés en contribuir al proyecto **Leofit Solutions - Sistema de Gestión de Pedidos & Inventario**! Este documento describe los lineamientos y directrices para proponer mejoras, reportar errores y enviar código.

---

## 🧭 Tabla de Contenidos
1. [Código de Conducta](#-código-de-conducta)
2. [¿Cómo puedo contribuir?](#-cómo-puedo-contribuir)
3. [Flujo de Trabajo con Git](#-flujo-de-trabajo-con-git)
4. [Configuración del Entorno de Desarrollo](#-configuración-del-entorno-de-desarrollo)
5. [Estándares de Código y Commits](#-estándares-de-código-y-commits)
6. [Ejecución de Pruebas](#-ejecución-de-pruebas)
7. [Proceso de Pull Request (PR)](#-proceso-de-pull-request-pr)

---

## 📜 Código de Conducta
Al participar en este proyecto, te comprometes a adherirte al [Código de Conducta](CODE_OF_CONDUCT.md). Por favor, léelo antes de interactuar con el equipo o la comunidad.

---

## 💡 ¿Cómo puedo contribuir?

* **Reportando Errores (Bugs):** Abre un *Issue* en GitHub describiendo el comportamiento esperado, el comportamiento observado, pasos exactos para reproducirlo y capturas de pantalla si aplica.
* **Proponiendo Mejoras o Nuevas Funcionalidades:** Abre un *Issue* de tipo *Feature Request* detallando la justificación del cambio y el valor que aporta al negocio de Leofit.
* **Enviando Código:** Corrige errores abiertos o implementa funcionalidades aprobadas mediante un Pull Request.

---

## 🌿 Flujo de Trabajo con Git

Trabajamos con el modelo de ramas basado en características:

1. **Haz un Fork** del repositorio a tu cuenta personal (o clona el repo oficial si eres miembro del equipo).
2. **Crea una rama descriptiva** a partir de `main`:
   ```bash
   git checkout -b feature/nombre-de-la-funcionalidad
   # o para correcciones:
   git checkout -b fix/descripcion-del-bug
   ```
3. Realiza tus cambios manteniendo commits atómicos y claros.
4. Sube tu rama a tu repositorio remoto:
   ```bash
   git push origin feature/nombre-de-la-funcionalidad
   ```
5. Abre un **Pull Request** hacia la rama `main`.

---

## 💻 Configuración del Entorno de Desarrollo

### Requisitos Previos
* **Node.js**: v20.x o v22.x LTS
* **npm**: v10.x o superior
* **Git**: v2.x

### Instalación y Ejecución

```bash
# 1. Clonar el repositorio
git clone https://github.com/Leofit-Solutions-Grupo01/leofit-pedidos-sistema.git
cd leofit-pedidos-sistema

# 2. Instalar dependencias del frontend
cd frontend
npm install

# 3. Iniciar el servidor de desarrollo
npm run dev

# 4. Compilar para producción (validación de build)
npm run build
```

La aplicación estará disponible en `http://localhost:5173`.

---

## 📝 Estándares de Código y Commits

### Convención de Commits (Conventional Commits)
Los mensajes de commit deben seguir el siguiente formato:

```text
<tipo>(<alcance opcional>): <descripción corta en imperativo>
```

**Tipos permitidos:**
* `feat`: Nueva funcionalidad (ej. `feat(pedidos): agregar filtro por estado de entrega`).
* `fix`: Corrección de bug (ej. `fix(auth): corregir redirección tras login`).
* `docs`: Cambios en la documentación (ej. `docs: actualizar guía de despliegue`).
* `style`: Formateo de código, estilos CSS o UI sin alterar lógica.
* `refactor`: Refactorización de código sin añadir funcionalidades ni corregir bugs.
* `test`: Adición o modificación de pruebas unitarias o de integración.
* `chore`: Tareas de mantenimiento, dependencias o configuración de build.

### Estilo de Código
* Utilizar TypeScript estricto. Evitar el uso de `any`.
* Componentes funcionales con Hooks en React.
* Clases utilitarias de TailwindCSS para consistencia visual.

---

## 🧪 Ejecución de Pruebas

Antes de enviar un Pull Request, asegúrate de que todas las pruebas pasen localmente:

```bash
cd frontend
npm test
```

---

## 🚀 Proceso de Pull Request (PR)

1. Asegúrate de que el código compila limpiamente (`npm run build`) y pasa las pruebas (`npm test`).
2. Actualiza la documentación en `/docs` o `README.md` si tu cambio altera el comportamiento o la arquitectura.
3. Asigna a al menos un revisor del equipo para su aprobación (*Code Review*).
4. Verifica que los flujos de GitHub Actions (CI/CD y Security Scan) finalicen en verde.
