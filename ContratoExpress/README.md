# ContratoExpress v3.3

#### Video Demo: <TU_URL_AQUI>

#### Description:

Mi nombre es **Nelson Abner Mendoza Pérez**, soy de Cacahoatán, Chiapas, México, y actualmente curso la carrera de Ingeniería en Tecnologías de la Información e Innovación Digital. Elegí desarrollar **ContratoExpress v3.3** como mi proyecto final para CS50x porque vivo en una zona donde el trabajo independiente y el comercio local son los motores de la economía. Sin embargo, lamentablemente, la gran mayoría de los acuerdos se realizan "de palabra".

He sido testigo de cómo amigos técnicos, electricistas, albañiles o programadores enfrentan problemas legales o falta de pagos simplemente porque no existía un documento firmado que pusiera orden a la transacción. Mi objetivo fue utilizar todo lo aprendido en el curso —desde la lógica de programación hasta el manejo de bases de datos y seguridad— para crear una herramienta con utilidad real: una aplicación web que transforme un formulario rápido en un contrato legal serio, profesional y bien estructurado.

## Estructura del Proyecto (Archivos y Funcionalidad)

Para garantizar que el sistema sea escalable y fácil de mantener, decidí seguir una arquitectura de software organizada de la siguiente manera:

*   **app.py (El Controlador Central):** Es el corazón de la aplicación donde configuré todas las rutas de Flask. No me limité a la gestión de rutas básica; implementé medidas de seguridad para el manejo de sesiones y me aseguré de que el ciclo de vida de los datos sea limpio. Un ejemplo de esto es la lógica de eliminación de cuentas: cuando un usuario decide darse de baja, el servidor no solo borra su registro en la base de datos, sino que ejecuta una función de limpieza que elimina físicamente del sistema de archivos todas las imágenes (como logos o firmas) asociadas a ese usuario para evitar la acumulación de "basura digital".

*   **rules.py (Capa de Lógica de Negocio):** Este es, desde un punto de vista de ingeniería, el archivo más importante. Decidí extraer toda la lógica pesada fuera de las rutas de Flask para mantener el código limpio. Aquí se encuentran las reglas de validación y todas las funciones que interactúan con SQLite. Al tenerlo separado, pude realizar pruebas de seguridad de forma aislada. Además, aquí es donde fuerzo a la base de datos a respetar la integridad referencial mediante el comando `PRAGMA foreign_keys = ON`.

*   **contracts.db (El Corazón de la Información):** La base de datos no es una tabla simple. Está diseñada con 35 columnas para capturar la complejidad de un contrato real, incluyendo campos para RFC/Tax ID, direcciones detalladas, cláusulas de penalización por retraso, porcentajes de anticipo y opciones de pago modernas como criptomonedas.

*   **templates/ (La Interfaz de Usuario):** Utilicé el motor Jinja2 para evitar la redundancia de código. El archivo `base.html` define una estética oscura, elegante y profesional. El archivo más complejo aquí es `pdf_view.html`, que actúa como el lienzo donde los datos capturados se transforman en el documento legal final.

*   **static/ (Diseño y Comportamiento):** El archivo `style.css` contiene cientos de líneas de código personalizadas para ofrecer una experiencia de usuario sobria. Por otro lado, `script.js` añade "inteligencia" al frontend; por ejemplo, el formulario es dinámico: si el usuario selecciona ciertos tipos de pago, aparecen campos adicionales mediante la manipulación del DOM, mejorando la usabilidad.

## Decisiones de Diseño y Desafíos Técnicos

Durante el desarrollo, me enfrenté a varias decisiones críticas que definieron la robustez del proyecto:

1.  **SQL Puro vs. ORM:** Aunque existen herramientas que automatizan las consultas (ORMs), decidí escribir cada `INSERT` y `SELECT` de forma manual. Manejar 35 variables en una sola consulta fue un reto de precisión, pero lo hice para tener un control total sobre la seguridad y el rendimiento, asegurándome de que no existan vulnerabilidades de inyección SQL.

2.  **Seguridad de Archivos (Magic Numbers):** Como me apasiona la ciberseguridad, implementé una validación de archivos basada en sus primeros bytes. El programa no confía en la extensión del nombre del archivo (como .jpg), sino que "abre" el archivo binario para confirmar que es una imagen real. Esto evita que un usuario malintencionado suba scripts ejecutables disfrazados de imágenes.

3.  **Arquitectura de Impresión:** Un desafío mayor fue la vista de impresión. Lo que se ve bien en una pantalla no siempre se traduce bien al papel. Tomé la decisión deliberada de priorizar la legibilidad sobre el ahorro de espacio. Implementé reglas de CSS específicas para impresión que generan automáticamente una segunda hoja si el contrato es muy largo, evitando que las firmas queden "huérfanas" o amontonadas al final de la página.

4.  **Validación de Datos Cruzados:** En `rules.py` creé filtros para prevenir errores humanos. El sistema valida, por ejemplo, que el prestador y el cliente no tengan los mismos datos de contacto y realiza cálculos aritméticos en el backend para confirmar que la suma del anticipo y el resto coincida exactamente con el total del contrato, manejando los problemas de precisión decimal que a veces tiene la programación.

## Reflexión Final

ContratoExpress v3.3 representa la culminación de mi aprendizaje en CS50x. Me obligó a integrar el diseño de interfaces (UX/UI), la seguridad informática, la gestión de bases de datos y la lógica de negocios. Estoy orgulloso de haber creado algo que no solo cumple con los rigurosos estándares de Harvard, sino que tiene el potencial de ayudar a los trabajadores independientes de mi comunidad a proteger su esfuerzo y profesionalizar su oficio.
