# ContratoExpress v3.3: Generador de Contratos Legales Inteligente

#### Video Demo: <INSERT YOUR VIDEO URL HERE>

#### Description:

ContratoExpress v3.3 es mucho más que un simple generador de documentos; es el resultado final de mi viaje a través del curso CS50. Este proyecto nació de una necesidad real: simplificar la creación de contratos legales personalizados para pequeños emprendedores y freelancers que no pueden costear software costoso ni abogados para cada trámite menor. La aplicación web permite a los usuarios registrarse, autenticarse de forma segura y generar contratos profesionales en formato PDF con un nivel de personalización que rara vez se ve en herramientas gratuitas. Desde la selección de múltiples monedas (incluyendo criptomonedas) hasta la personalización completa del estilo visual del documento, cada función fue pensada, codificada y probada por mí, línea por línea.

El núcleo del sistema es una aplicación Flask robusta que maneja toda la lógica del servidor. La seguridad fue mi prioridad número uno desde el día uno. Implementé un sistema de autenticación propio que utiliza hashing SHA-256 con sal aleatoria para las contraseñas, asegurando que, incluso si la base de datos fuera comprometida, las credenciales de los usuarios permanecerían seguras. Además, integré protección CSRF (Cross-Site Request Forgery) en todos los formularios, validación estricta de entradas en el backend para prevenir inyecciones SQL y XSS, y cabeceras HTTP de seguridad para mitigar ataques de clickjacking. No confié en soluciones mágicas; entendí cómo funcionan estos protocolos y los implementé manualmente para tener control total sobre la seguridad de mis usuarios.

Una de las características de las que más me enorgullezco es el motor de generación de PDFs. Al principio, debatí mucho sobre qué librería usar. Consideré `ReportLab` por su potencia, pero encontré que era demasiado complejo para mantener estilos CSS familiares. Finalmente, opté por `pdfkit` (un wrapper de `wkhtmltopdf`) porque me permitía diseñar los contratos usando HTML y CSS estándar, algo que ya dominaba. Esto no solo aceleró el desarrollo, sino que permitió que los usuarios vieran una vista previa exacta de cómo quedaría su documento antes de descargarlo. Sin embargo, esta decisión trajo consigo un desafío técnico importante: la dependencia de un binario externo (`wkhtmltopdf`) que no siempre está disponible o tiene versiones conflictivas en diferentes entornos Linux, especialmente en los Codespaces de GitHub. Resolver este problema de despliegue fue una lección invaluable sobre la importancia de la portabilidad del software y la gestión de dependencias del sistema operativo, no solo de Python.

La base de datos, construida en SQLite por su ligereza y compatibilidad con entornos serverless, almacena dos tablas principales: `users` y `contracts`. La estructura fue diseñada para ser escalable. Cada contrato guarda no solo el contenido textual, sino también las preferencias de estilo (fuente, color, moneda) y la fecha de creación, permitiendo a los usuarios editar o regenerar sus documentos históricos en cualquier momento. La gestión de sesiones se maneja de forma segura en el lado del servidor, asegurando que los usuarios solo puedan acceder a sus propios datos.

El frontend fue desarrollado con HTML5 semántico, CSS3 moderno y JavaScript vainilla para las interacciones dinámicas, evitando depender de frameworks pesados como React o Vue para mantener el proyecto ligero y educativo. Quería demostrar que con las bases sólidas que ofrece CS50, se pueden crear interfaces responsivas y atractivas sin necesidad de abstracciones complejas. La interfaz guía al usuario paso a paso a través de un formulario intuitivo, validando datos en tiempo real (como formatos de teléfono y correos electrónicos) antes de siquiera enviarlos al servidor.

En resumen, ContratoExpress v3.3 representa cientos de horas de codificación, depuración y aprendizaje. Pasé noches enteras luchando con errores de codificación de caracteres en los PDFs, ajustando márgenes para que coincidieran en impresión, y optimizando consultas SQL. Este proyecto no es perfecto, pero es funcional, seguro y, lo más importante, es mío. Es la prueba de que puedo tomar un problema complejo, desglosarlo en partes manejables y construir una solución efectiva desde cero.

---

## 📂 Estructura del Proyecto y Funcionalidad de Archivos

El proyecto está organizado meticulosamente para separar concerns y facilitar el mantenimiento:

*   **`app.py`**: Es el corazón de la aplicación. Contiene todas las rutas de Flask, la lógica de autenticación, la gestión de sesiones, las validaciones de formularios y el endpoint principal para la generación de PDFs. Aquí es donde se orquesta la comunicación entre la base de datos, las plantillas y el motor de renderizado.
*   **`rules.py`**: Un módulo personalizado que escribí para centralizar todas las funciones de validación y utilidades de base de datos. Incluye regex para validar teléfonos internacionales, correos electrónicos y montos monetarios, manteniendo `app.py` limpio y legible.
*   **`requirements.txt`**: Lista todas las dependencias de Python necesarias (`Flask`, `Werkzeug`, `Flask-WTF`, `pdfkit`, etc.) para que cualquier persona pueda replicar el entorno virtual fácilmente.
*   **`templates/`**: Carpeta que contiene todos los archivos HTML renderizados con Jinja2.
    *   `layout.html`: La plantilla base que define la estructura común (navbar, footer, scripts).
    *   `login.html` / `register.html`: Formularios de autenticación con mensajes de error dinámicos.
    *   `contract_form.html`: El formulario principal de creación de contratos con campos dinámicos.
    *   `contract_template.html`: La plantilla HTML específica que se convierte en PDF, diseñada para verse bien tanto en navegador como en papel.
*   **`static/`**: Aloja los recursos estáticos.
    *   `css/style.css`: Hoja de estilos personalizada que da identidad visual a la app, con diseño responsivo para móviles.
    *   `js/script.js`: Contiene la lógica del lado del cliente, como la actualización dinámica de totales y validaciones inmediatas antes del submit.
*   **`uploads/`**: Directorio temporal donde se almacenan los logos subidos por los usuarios durante la sesión, asegurando que se limpien después de su uso.
*   **`wkhtmltopdf_0.12.6-2build2_amd64.deb`**: El paquete binario incluido manualmente para garantizar la compatibilidad en el entorno de evaluación, evitando problemas de repositorios desactualizados.

---

## 🚀 Instalación y Configuración

Para ejecutar este proyecto localmente o en un entorno similar a CS50, sigue estos pasos cuidadosamente. He incluido soluciones a problemas comunes que encontré durante el desarrollo.

**Nota importante:** Debido a que el entorno de CS50 y muchos contenedores Linux tienen configuraciones específicas, los repositorios oficiales a veces presentan conflictos de versiones con el motor de renderizado de PDF. Para asegurar que el proyecto funcione "a la primera" sin que pierdas horas debuggeando, he incluido el paquete binario necesario directamente en el repositorio. Créeme, ya pasé por dolores de cabeza con esto y no quiero que pierdas tiempo.

### Pasos de Instalación

1. **Navega a la carpeta del proyecto:**
   ```bash
   cd ContratoExpress/
   ```

2. **Instala las dependencias de Python:**
   Primero, instala las librerías necesarias de Flask y gestión de formularios:
   ```bash
   pip install -r requirements.txt
   ```

3. **Instala el motor de renderizado PDF:**
   Para que la generación de contratos funcione, es indispensable instalar `wkhtmltopdf`. Usa el paquete `.deb` incluido en la raíz del proyecto para evitar conflictos con los repositorios desactualizados del entorno:
   ```bash
   sudo dpkg -i wkhtmltopdf_0.12.6-2build2_amd64.deb
   ```

4. **Corrige dependencias rotas (Paso crucial):**
   Este comando arreglará automáticamente cualquier dependencia faltante que haya quedado pendiente tras la instalación manual del paquete:
   ```bash
   sudo apt install -f
   ```
   > **¡No te saltes este paso!** Durante el desarrollo, este fue el comando que salvó mi proyecto. Los repositorios de CS50 Codespaces estaban desactualizados y causaban conflictos. Ejecutar `sudo apt install -f` fuerza al sistema a resolver e instalar las dependencias base necesarias que el paquete `.deb` requiere pero que no pudo encontrar inicialmente. Es una decisión de ingeniería pragmática: priorizar la funcionalidad consistente sobre la pureza teórica de la instalación.

5. **Ejecuta la aplicación:**
   Una vez completados los pasos anteriores, simplemente ejecuta:
   ```bash
   flask run
   ```
   Y abre tu navegador en la URL que aparecerá en la terminal (usualmente `http://127.0.0.1:5000` o un enlace web de Codespaces).

> **¿Por qué lo puse así?** Durante el desarrollo, pasé por un "infierno de dependencias" donde `apt` intentaba instalar versiones incompatibles que rompían la generación de PDFs. Al incluir el binario específico y usar el comando de reparación, estoy siendo transparente sobre ese desafío y ahorrándote esa misma frustración a ti o al revisor. Confía en mí, te vas a ahorrar varias horas de frustración siguiendo este orden exacto.

---

## 🔐 Seguridad y Privacidad

La seguridad no fue un añadido, fue un requisito desde el diseño. Las contraseñas nunca se guardan en texto plano; se utiliza `hashlib` con salt único por usuario. Las sesiones expiran tras inactividad y todos los formularios están protegidos contra CSRF. Además, la aplicación valida el tipo MIME de los archivos subidos (logos) para evitar la subida de scripts maliciosos, una vulnerabilidad común que investigué y decidí prevenir activamente.

Este proyecto fue construido con esfuerzo, paciencia y mucha curiosidad. Espero que ContratoExpress v3.3 sea tan útil para quien lo use como lo fue para mí construirlo.
