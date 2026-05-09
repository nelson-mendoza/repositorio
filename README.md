ContratoExpress: Generador de Contratos para Servicios Simples

demo de video:

Descripción:

ContratoExpress es una aplicación web para pequeños emprendedores, freelancers y con el único objetivo de ofrecer servicios simples, pero que necesitan crear contratos básicos lo más rápida y profesionalmente posible. Este proyecto surgió porque vi una necesidad real en mi región: los trabajadores independientes, desde electricistas y plomeros hasta pintores y freelancers, sufren impagos o los clientes quieren más servicio del acordado por el mismo precio. Como solución, puedes acordar qué sucede ese día y tener un documento escrito en segundos con ContratoExpress. Con unos pocos clics, tienes un archivo listo para firmar, perfecto si haces esto varias veces cada día. También tienes todo el poder de eliminar tu cuenta cuando quieras.

Autenticación y registro seguros con generación de contratos en PDF: opciones básicas y cierto nivel de personalización para atraer a una audiencia constante orientada a la velocidad, junto con otra que valora la profesionalidad o el detalle. Además de los contratos de servicio, es perfecto para emitir recibos de pago; si no quieres dejar una sección de firmas, simplemente bastaba con indicar lo que se pagó y contar con un registro funcionalidad. El diseño en sí es bastante hermoso: con un tono oscuro y una designación, los colores contrastan bien, por lo que resulta agradable a la vista. Tiene, en particular, texto brillante sobre negro optimizado, sobre un fondo negro, para la máxima nitidez y comodidad al visualizarlo.

Este proyecto se basa en Flask para el backend y en HTML5, CSS3, Vanilla JS para el frontend. Esta es una buena oportunidad para explicar por qué esta elección, porque fue el stack que me permitió aprender con más profundidad estas habilidades en lugar de empezar desde cero con otro framework en CS50. Y para mí, la seguridad fue lo primero desde el primer día. Para ello, tuve que crear mi propio sistema de autenticación implementando hashing SHA-256 con sales aleatorias para las contraseñas, de modo que incluso si la base de datos se viera comprometida, las credenciales de los usuarios permanecieran seguras. También incorporé protección CSRF (Cross-Site Request Forgery) a todos los formularios, apliqué validación de entradas en el nivel del backend para evitar inyecciones SQL y XSS, y añadí cabeceras HTTP seguras para prevenir ataques de clickjacking. Así que las soluciones mágicas no cuentan; sé cómo funcionan estos protocolos a nivel básico y los implementé todos correctamente, para que estuviera completamente en control de la seguridad de mis usuarios.

De las primeras características de las que me siento más orgulloso está el motor de generación de PDF. Mi debate me estaba atormentando mucho al inicio, para las primeras bibliotecas que debía usar. También probé FPDF, que es más sencillo de configurar y puede funcionar hasta el nivel de milímetros con cada descarga, pero está basado en coordenadas y no tiene soporte para CSS, lo que me privaría de los beneficios estéticos de ver exactamente lo que había diseñado, así que decidí no usarlo. Por último, pero no menos importante, decidí ir con pdfkit (en realidad un envoltorio para wkhtmltopdf), ya que me permitió maquetar los contratos en diseño HTML y CSS, algo con lo que estaba lo bastante familiarizado porque conocía ambas tecnologías de memoria. Esta decisión no solo ayudó a acelerar el desarrollo, sino que también les dio a los usuarios una vista previa perfecta de cómo se vería su documento antes de descargarlo. Pero esta decisión introdujo un gran desafío técnico: depender de un binario externo que no siempre está disponible o que puede haber conflictos entre versiones instaladas de wkhtmltopdf en distintos entornos de Linux, especialmente en GitHub Codespaces. Además, esto nos ha enseñado a desplegar nuestro código y las necesidades de portabilidad del software, llegando hasta las dependencias del sistema más allá de Python.

Esto está diseñado para ser ligero y sin servidor (serverless), por lo que utiliza una base de datos SQLite que consta de dos tablas principales: la tabla users y la tabla contracts. Esto se creó para que fuera escalable. Cada contrato individual contiene tanto su texto como las preferencias de estilo (fuente, color, moneda) y la fecha de creación, para que los usuarios puedan generar sus documentos cuando quieran. La gestión segura de sesiones en el servidor significa que los usuarios solo tienen acceso a sus propios datos.

El frontend utilizó también HTML5 semántico para la estructura, CSS3 moderno y JavaScript vanilla para las interacciones dinámicas (evitando frameworks pesados como React o Vue para mantener el proyecto ligero y educativo). Quería dejar claro, con las firmes bases de CS50 bajo tus pies, que puedes construir interfaces hermosas y responsivas sin abstracciones complejas. La interfaz guía al usuario paso a paso mediante un formulario intuitivo que realiza validaciones de datos en el frontend (por ejemplo, asegurándose de que el formato del teléfono y del correo electrónico sea correcto) antes de siquiera enviarlo al servidor.

Para resumir, este es un proyecto centrado en mucho aprendizaje y desarrollo. En el camino surgieron algunas complicaciones técnicas debido a discrepancias en la codificación de caracteres de PDF, ajustes del margen de impresión y optimización de consultas SQL. En resumen, obtienes una aplicación funcional y segura que demuestra lo que puedo hacer: resolver problemas difíciles creando algo útil, desde cero.

Estructura del Proyecto y Archivos en Funcionalidad

Este proyecto está bien estructurado para separar responsabilidades y mejorar el mantenimiento.

app. py**: Aquí es donde se ejecuta la aplicación. Incluye todas las rutas de Flask, la lógica de autenticación, el manejo de sesiones, las validaciones de formularios y tu punto de entrada principal para generar PDFs. Aquí es donde interactúan la base de datos, las plantillas y el motor de renderizado.

rules. py**: mi módulo personalizado que escribí para centralizar todas las utilidades relacionadas con validaciones y la base de datos. Incluye expresiones regulares para validar números de teléfono internacionales, correos electrónicos y importes de dinero, manteniendo app. py limpio y legible.

requirements. txt**: Especifica todas las dependencias de Python necesarias (Flask, Werkzeug, Flask-WTF, pdfkit — Oubustits) para una replicación rápida y sencilla del entorno virtual.

templates/**: directorio con todos los archivos HTML renderizados por Jinja2.

layout. base.

login. html / register. html:

contract_form. html: La plantilla inicial para crear un contrato, con campos dinámicos

contract_template. html`: La plantilla HTML exacta que renderizas para generar un PDF, con estilos tanto para el navegador como para la página impresa.

static/**: Aloja recursos estáticos.

css/style. css: Una hoja de estilos personalizada (CSS) que aporta la identidad visual de tu aplicación, integrando un diseño responsive para móviles.

js/script. js: Para la lógica local (actualizaciones dinámicas del total; validación inmediata en los campos del formulario antes de enviar).

uploads/**: Directorio temporal para logotipos subidos por los usuarios durante una sesión, que debe limpiarse al finalizar.

wkhtmltopdf_0.12.6-2build2_amd64. deb`**: Un paquete binario agregado manualmente para asegurar la compatibilidad en el entorno de evaluación; esto ayuda a usar un repositorio actualizado que evita cualquier error.

Instalación y Configuración

Sigue estas instrucciones paso a paso para poner este proyecto en funcionamiento localmente, o en un entorno cercano a CS50. Aquí tienes algunas soluciones a problemas con los que a menudo me encontré durante el proceso de desarrollo.

Nota: Los repositorios oficiales a veces crean conflictos de versiones con el motor de renderizado de PDF en el entorno de CS50 y en varios contenedores de Linux. Para asegurar que el proyecto funcione desde la primera ejecución, adjunté directamente en el repositorio el paquete binario necesario.

Pasos de instalación

Navega a la carpeta del proyecto:

cd ContratoExpress/

Instala las dependencias de Python:

Lo único que necesitas hacer para eso es instalar primero las bibliotecas necesarias de Flask y manejo de formularios:

pip install -r requirements. txt

Instala el motor de renderizado de PDF:

wkhtmltopdf es necesario para que funcione la generación de contratos. Usa el paquete . debian/nodejs/deb incluido desde la raíz del proyecto para evitar conflictos con los repositorios del entorno:

sudo dpkg -i wkhtmltopdf_0.12.6-2build2_amd64. deb

Corrige dependencias rotas (paso crucial):

Este comando se ejecutará para resolver automáticamente otras dependencias que queden sin resolver después de la instalación manual del paquete.

sudo apt install -f

No te saltes este paso. Luego necesitas cumplir con las dependencias base para que pueda tomar e instalar el . deb que requiere.

Ejecuta la aplicación:

Después de eso, completa los primeros pasos y simplemente ejecuta:

flask run

Flask se enlazará a una dirección local y a un puerto. Luego, simplemente haz clic en el enlace que aparece en el editor de VSCode o ábrelo en el navegador.

Seguridad y Privacidad

La seguridad no era una opción adicional, era un requisito de diseño. Pero nunca contraseñas en texto plano; usas hashlib, que produce una cadena hash y, en cada ejecución, genera un salt único por usuario. Las sesiones tienen caducidad por inactividad y todos los formularios incluyen protección contra CSRF. La aplicación también verifica el tipo MIME de los archivos cargados (logotipos) como protección para evitar la ejecución de scripts (una vulnerabilidad común que investigué personalmente y contra la que me protegí de forma proactiva).

Este proyecto fue uno de arduo trabajo, perseverancia y pura curiosidad. Realmente espero que ContratoExpress sea tan valioso para quien lo use.
