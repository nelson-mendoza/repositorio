# ContratoExpress: Generador de Contratos para Servicios Simples

#### Video Demo: <INSERT YOUR VIDEO URL HERE>

#### Description:

ContratoExpress es una aplicación web diseñada para pequeños emprendedores, freelancers y cualquier persona que ofrezca servicios simples y necesite generar contratos básicos de manera rápida y profesional. Este proyecto nació de una necesidad real en mi región: muchos trabajadores independientes, desde técnicos y plomeros hasta pintores y freelancers, a menudo sufren impagos o clientes que esperan servicios extras no pactados inicialmente por el mismo precio. ContratoExpress resuelve ese problema permitiendo que lo que se pacta ese día quede escrito en segundos. Con unos pocos clicks, tienes un contrato listo para firmar, ideal si necesitas hacerlo varias veces al día. Incluso tienes el poder total de borrar tu cuenta cuando lo desees.

La aplicación permite registrarse y autenticarse de forma segura, y generar contratos en formato PDF con opciones básicas y algunas personalizadas, buscando llegar tanto a un público que busca rapidez como a uno más profesional o detallado. Además de contratos de servicio, la herramienta es ideal para emitir constancias de pago; si no deseas agregar un apartado de firmas, puedes usarla simplemente para dejar por escrito y tener palabra formal acerca de lo pagado. El diseño es muy atractivo: está hecho para no lastimar la vista, utilizando un tono oscuro con colores que contrastan adecuadamente. El fondo negro sobre letras blancas brillantes ha sido ajustado cuidadosamente para ofrecer máxima nitidez y comodidad visual.

El proyecto utiliza Flask como servidor backend, combinado con HTML5, CSS3 y JavaScript vainilla en el frontend. Esta elección se debe a que fue el stack tecnológico enseñado en el curso CS50, lo que me permitió profundizar en estos conocimientos en lugar de empezar desde cero con otro framework. La seguridad fue mi prioridad número uno desde el día uno. Implementé un sistema de autenticación propio que utiliza hashing SHA-256 con sal aleatoria para las contraseñas, asegurando que, incluso si la base de datos fuera comprometida, las credenciales de los usuarios permanecerían seguras. Además, integré protección CSRF (Cross-Site Request Forgery) en todos los formularios, validación estricta de entradas en el backend para prevenir inyecciones SQL y XSS, y cabeceras HTTP de seguridad para mitigar ataques de clickjacking. No confié en soluciones mágicas; entendí cómo funcionan estos protocolos y los implementé manualmente para tener control total sobre la seguridad de mis usuarios.

Una de las características de las que más me enorgullezco es el motor de generación de PDFs. Al principio, debatí mucho sobre qué librería usar. También evalué `FPDF`, la cual era más accesible de instalar y permite precisión milimétrica en cada descarga; sin embargo, opera bajo coordenadas y sin soporte para estilos CSS, lo cual me privaría de las ventajas visuales de ver exactamente lo que tengo diseñado, por lo que decidí no implementarla. Finalmente, opté por `pdfkit` (un wrapper de `wkhtmltopdf`) porque me permitía diseñar los contratos usando HTML y CSS estándar, algo que ya dominaba. Esto no solo aceleró el desarrollo, sino que permitió que los usuarios vieran una vista previa exacta de cómo quedaría su documento antes de descargarlo. Sin embargo, esta decisión trajo consigo un desafío técnico importante: la dependencia de un binario externo (`wkhtmltopdf`) que no siempre está disponible o tiene versiones conflictivas en diferentes entornos Linux, especialmente en los Codespaces de GitHub. Resolver este problema de despliegue fue una lección invaluable sobre la importancia de la portabilidad del software y la gestión de dependencias del sistema operativo, no solo de Python.

La base de datos, construida en SQLite por su ligereza y compatibilidad con entornos serverless, almacena dos tablas principales: `users` y `contracts`. La estructura fue diseñada para ser escalable. Cada contrato guarda no solo el contenido textual, sino también las preferencias de estilo (fuente, color, moneda) y la fecha de creación, permitiendo a los usuarios generar sus documentos en cualquier momento. La gestión de sesiones se maneja de forma segura en el lado del servidor, asegurando que los usuarios solo puedan acceder a sus propios datos.

El frontend fue desarrollado con HTML5 semántico, CSS3 moderno y JavaScript vainilla para las interacciones dinámicas, evitando depender de frameworks pesados como React o Vue para mantener el proyecto ligero y educativo. Quería demostrar que con las bases sólidas que ofrece CS50, se pueden crear interfaces responsivas y atractivas sin necesidad de abstracciones complejas. La interfaz guía al usuario paso a paso a través de un formulario intuitivo, validando datos en tiempo real (como formatos de teléfono y correos electrónicos) antes de siquiera enviarlos al servidor.

En resumen, este proyecto representa un esfuerzo significativo de aprendizaje y desarrollo. Durante el proceso, enfrenté desafíos técnicos como errores de codificación de caracteres en los PDFs, ajustes de márgenes para impresión y optimización de consultas SQL. El resultado es una aplicación funcional y segura que demuestra mi capacidad para resolver problemas complejos mediante la construcción de soluciones prácticas desde cero.

---

## Estructura del Proyecto y Funcionalidad de Archivos

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

## Instalación y Configuración

Para ejecutar este proyecto localmente o en un entorno similar a CS50, sigue estos pasos cuidadosamente. He incluido soluciones a problemas comunes que encontré durante el desarrollo.

**Nota importante:** Debido a que el entorno de CS50 y muchos contenedores Linux tienen configuraciones específicas, los repositorios oficiales a veces presentan conflictos de versiones con el motor de renderizado de PDF. Para asegurar que el proyecto funcione correctamente desde el inicio, he incluido el paquete binario necesario directamente en el repositorio.

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
   Para que la generación de contratos funcione, es indispensable instalar `wkhtmltopdf`. Usa el paquete `.deb` incluido en la raíz del proyecto para evitar conflictos con los repositorios del entorno:
   ```bash
   sudo dpkg -i wkhtmltopdf_0.12.6-2build2_amd64.deb
   ```

4. **Corrige dependencias rotas (Paso crucial):**
   Este comando arreglará automáticamente cualquier dependencia faltante que haya quedado pendiente tras la instalación manual del paquete:
   ```bash
   sudo apt install -f
   ```
   > No te saltes este paso. Es necesario para resolver e instalar las dependencias base que el paquete `.deb` requiere.

5. **Ejecuta la aplicación:**
   Una vez completados los pasos anteriores, simplemente ejecuta:
   ```bash
   flask run
   ```
   Flask te asignará una dirección local y un puerto. Solo haz click en el enlace que aparecerá en el editor VSCode o ábrelo en tu navegador.

---

## Seguridad y Privacidad

La seguridad no fue un añadido, fue un requisito desde el diseño. Las contraseñas nunca se guardan en texto plano; se utiliza `hashlib` con salt único por usuario. Las sesiones expiran tras inactividad y todos los formularios están protegidos contra CSRF. Además, la aplicación valida el tipo MIME de los archivos subidos (logos) para evitar la subida de scripts maliciosos, una vulnerabilidad común que investigué y decidí prevenir activamente.

Este proyecto fue construido con esfuerzo, paciencia y mucha curiosidad. Espero que ContratoExpress sea tan útil para quien lo use como lo fue para mí construirlo.
