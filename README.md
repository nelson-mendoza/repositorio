# ContratoExpress v3.3: Generador Inteligente de Contratos de Servicios Profesionales

#### Video Demo:  <INSERTA AQUÍ LA URL DE TU VIDEO DE YOUTUBE/LOOM>

#### Descripción:

**ContratoExpress v3.3** es una aplicación web completa desarrollada con el framework **Flask** de Python, diseñada para automatizar y simplificar la creación de contratos de servicios profesionales legalmente robustos. En un entorno donde los freelancers, consultores y pequeñas agencias a menudo pierden tiempo valioso redactando documentos legales desde cero o utilizando plantillas genéricas inseguras, esta herramienta ofrece una solución dinámica, segura y adaptable a múltiples jurisdicciones y monedas. El proyecto no solo genera texto, sino que construye un flujo de trabajo integral que incluye autenticación de usuarios, validación de datos en tiempo real, personalización de marca (logotipos), y generación de documentos finales en formatos listos para imprimir (HTML/PDF) con soporte para firmas digitales.

### Funcionalidades Principales

El núcleo de la aplicación reside en su capacidad para interactuar con el usuario mediante un formulario intuitivo que captura todos los detalles esenciales de un acuerdo comercial: identificación de las partes (contratista y cliente), alcance del trabajo, cronograma de pagos, cláusulas específicas y selección de moneda. A diferencia de un simple procesador de textos, ContratoExpress implementa un motor de validación backend riguroso (`rules.py`) que asegura la integridad de los datos antes de cualquier procesamiento. 

Una de las características más destacadas es su soporte **multi-moneda**, permitiendo a los usuarios generar contratos en USD, EUR, GBP, entre otras, con el símbolo correcto y formato numérico apropiado. Además, el sistema incluye un módulo de **gestión de activos** que permite a los usuarios subir sus propios logotipos corporativos, los cuales se incrustan dinámicamente en el encabezado del contrato generado, aportando un nivel de profesionalismo esencial para la imagen de marca.

La seguridad es una prioridad en la arquitectura de ContratoExpress. La aplicación cuenta con un sistema de **autenticación de usuarios** completo, que incluye registro, inicio de sesión seguro con hash de contraseñas (utilizando `werkzeug.security`), y gestión de sesiones. Esto garantiza que cada usuario tenga acceso exclusivo a su propio historial de contratos guardados. El historial permite revisar, visualizar o volver a descargar contratos generados anteriormente, facilitando la administración documental a lo largo del tiempo.

### Estructura del Proyecto y Archivos

El proyecto está organizado siguiendo las mejores prácticas de desarrollo web modular en Python:

*   **`app.py`**: Es el cerebro de la aplicación. Contiene todas las rutas (endpoints) necesarias para el funcionamiento del sitio. Gestiona la lógica de negocio, incluyendo el manejo de formularios, la interacción con la base de datos SQLite, la subida de archivos (logos) y la renderizado de plantillas. Aquí se encuentra la lógica para generar el HTML final del contrato inyectando las variables del usuario en la plantilla maestra.
*   **`rules.py`**: Este módulo separa la lógica de validación del controlador principal. Define funciones estrictas para verificar emails, formatos de moneda, longitudes de texto y reglas de negocio específicas (por ejemplo, asegurar que las fechas de fin sean posteriores a las de inicio). Esta separación de preocupaciones hace que el código sea más limpio, mantenible y fácil de testear.
*   **`templates/`**: Directorio que alberga los archivos HTML. Incluye `layout.html` (la plantilla base con la navegación y estilos globales), `login.html`, `register.html`, `index.html` (el dashboard), `new_contract.html` (el formulario de entrada) y `contract_template.html` (el diseño visual exacto del contrato generado). Se utilizó **Jinja2**, el motor de plantillas de Flask, para la herencia de plantillas y la inyección dinámica de datos.
*   **`static/`**: Contiene los archivos CSS personalizados para dar una apariencia moderna y responsiva, así como las carpetas de subida para los logotipos de los usuarios.
*   **`requirements.txt`**: Lista las dependencias externas necesarias, principalmente `Flask`, `Werkzeug` para seguridad, y librerías auxiliares para el manejo de imágenes y PDFs.
*   **`flask_humanizado.txt`**: Script maestro utilizado para generar la estructura inicial y el código base de este proyecto, demostrando la capacidad de automatización en la creación de software.

### Decisiones de Diseño y Desafíos Técnicos

Durante el desarrollo, se tomaron varias decisiones arquitectónicas clave. Se optó por **SQLite** como sistema de gestión de bases de datos debido a su ligereza y portabilidad; no requiere configuración de servidores externos, lo que hace que el proyecto sea fácil de desplegar y probar en entornos locales sin complicaciones de infraestructura. Para el almacenamiento de archivos (logos), se implementó un sistema de nombres únicos basado en timestamps para evitar colisiones de archivos, asegurando que cada usuario mantenga su identidad visual sin sobrescribir la de otros.

Un desafío significativo fue la generación del documento final. Inicialmente se consideró el uso de librerías pesadas de generación de PDF directas desde Python. Sin embargo, se decidió optar por una estrategia híbrida: generar primero un **HTML altamente estilizado** con CSS específico para impresión (`@media print`). Esto permite que el usuario utilice la función nativa "Guardar como PDF" del navegador, lo cual ofrece una fidelidad visual superior y mayor control sobre el resultado final sin depender de motores de renderizado externos complejos que a menudo rompen el diseño.

Otra decisión importante fue la implementación de validaciones tanto en el frontend (JavaScript) como en el backend (Python). Aunque la validación del lado del cliente mejora la experiencia de usuario al ofrecer retroalimentación inmediata, se reforzó toda la lógica en el servidor (`rules.py`) para prevenir cualquier intento de inyección de datos malformados o malintencionados, siguiendo el principio de "nunca confiar en la entrada del usuario".

### Conclusión

ContratoExpress v3.3 demuestra cómo la tecnología web moderna puede resolver problemas cotidianos del mundo profesional. Combina una interfaz amigable con una lógica de backend sólida, ofreciendo una herramienta que no solo ahorra tiempo, sino que eleva la calidad percibida de los servicios de quienes la utilizan. El proyecto sirve como un testimonio de la versatilidad de Python y Flask para construir aplicaciones full-stack funcionales, seguras y escalables.

---
*Proyecto desarrollado como parte del curso CS50x de Harvard.*