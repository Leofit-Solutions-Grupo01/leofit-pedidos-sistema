# Reglas de Seguridad y Privacidad (Pre-Commit)

**Contexto:** Este proyecto se publicará como código abierto o será evaluado por jurados externos. Todo lo escrito en código y documentación será público.

## Directrices para el Agente de IA

1. **Rutas Locales (Sanitización):** NUNCA escribas rutas absolutas locales que revelen nombres de usuario de Windows/Linux/Mac (por ejemplo, `C:\Users\Loayza\...` o `/home/usuario/...`) dentro de la documentación (`.md`), archivos `.yaml`, comentarios en el código, o configuraciones. Usa siempre rutas relativas (`./docs`, `src/components`).
2. **Secretos y Variables de Entorno:**
   - Nunca reveles, generes o intentes guardar claves JWT, strings de conexión a base de datos (PostgreSQL, MongoDB), claves de AWS u otros secretos en archivos de código fuente, ni en la documentación.
   - Utiliza referencias de entorno simbólicas como `<TU_JWT_SECRET>`, `user:password@localhost` o `AWS_ACCESS_KEY_ID`.
3. **No-PII (Información de Identificación Personal):** Asegúrate de que los mock datas (`mockData.ts`) y los logs no contengan números de teléfono, DNI o correos electrónicos reales que pertenezcan a los desarrolladores del equipo.
4. **Git Ignore:** Antes de interactuar con comandos git, valida estrictamente que la carpeta `.agents`, `node_modules` y `.env` tengan reglas correspondientes si aplica (o si la política exige subirlos, que estén completamente sanitizados).
