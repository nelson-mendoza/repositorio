# ContratoExpress - Generador de Contratos para Servicios Simples

#### Video Demo: <URL HERE>

#### Description:

**ContratoExpress** es una aplicación web desarrollada con Flask que permite a técnicos, electricistas, plomeros, tutores y freelancers generar contratos profesionales para servicios simples de manera rápida y sencilla. Esta herramienta nació como mi proyecto final para el curso CS50 de Harvard.

## Sobre el Autor y Contexto del Proyecto

Soy un profesional certificado en ciberseguridad y programación con experiencia en desarrollo de software seguro. Decidí tomar el curso CS50 de Harvard para estandarizar mis conocimientos bajo un marco académico de prestigio mundial y profundizar en la implementación de seguridad web y arquitectura de datos. 

Aproveché mi base técnica previa para avanzar con agilidad a través de los módulos fundamentales, lo que me permitió dedicar el grueso de mi tiempo a desarrollar un proyecto final robusto: ContratoExpress. Este enfoque me posibilitó aplicar las mejores prácticas de seguridad que ya conocía, integrándolas con la rigurosidad metodológica que exige CS50, validando así mis habilidades ante la comunidad técnica global.

### Características Principales

- **Sistema de Autenticación Seguro**: Implementa registro e inicio de sesión robustos con hash de contraseñas (usando `werkzeug.security`), gestión de sesiones y protección CSRF para prevenir vulnerabilidades web comunes.
- **Generación Dinámica de Contratos**: Los usuarios pueden seleccionar entre múltiples tipos de contrato (ej. Arrendamientos, Contratos de Servicio, NDAs) e ingresar detalles específicos. El sistema llena inteligentemente las plantillas basándose en estas entradas.
- **Cálculos Legales Automatizados**: Incluye lógica integrada para calcular impuestos, penalizaciones y montos totales automáticamente, reduciendo errores humanos en cláusulas financieras.
- **Exportación PDF de Alta Calidad**: Genera documentos PDF profesionales listos para imprimir usando la librería `reportlab`. El diseño prioriza la legibilidad y claridad legal; si es necesario, el documento se extiende a múltiples páginas para asegurar que ninguna información esté apretada o sea ilegible. Se prioriza la claridad sobre el ahorro de papel, imprimiendo más hojas si hace falta para mantener la calidad.
- **Interfaz de Usuario Responsiva**: Construida con Bootstrap 5, la aplicación es totalmente responsiva, proporcionando una experiencia fluida en escritorios, tabletas y dispositivos móviles.
- **Dashboard e Historial**: Los usuarios pueden ver, descargar o eliminar sus contratos previamente generados desde un panel personalizado.

### Estructura del Proyecto y Desglose de Archivos

El proyecto sigue una arquitectura modular para asegurar mantenibilidad y escalabilidad:

- **`app.py`**: La aplicación Flask principal. Maneja rutas, interacciones con la base de datos, lógica de autenticación y funciones controladoras principales. Integra las reglas de validación IA y los motores de generación PDF. Decoradores de seguridad y manejadores de errores están centralizados aquí.
- **`rules.py`**: Contiene la lógica de negocio y reglas de "IA" para validación de contratos. Este módulo define restricciones para diferentes tipos de contrato, calcula límites legales (ej. depósitos de seguridad máximos) y asegura consistencia de cláusulas.
- **`templates/`**: Directorio con archivos HTML potenciados por Jinja2.
    - `base.html`: Plantilla base definiendo barra de navegación, pie de página e importaciones comunes de CSS/JS.
    - `login.html`, `register.html`: Formularios de autenticación con validación del lado del cliente y servidor.
    - `form.html`: Formulario complejo para ingresar detalles del contrato con campos dinámicos.
    - `dashboard.html`: Muestra el historial de contratos del usuario.
    - `history.html`: Vista detallada del historial.
    - `pdf_view.html`: Vista previa del PDF generado.
- **`static/`**: Almacena hojas de estilo CSS, archivos JavaScript e imágenes. CSS personalizado mejora el tema Bootstrap con tipografía profesional y espaciado adecuado para un producto legal-tech.
- **`database.db`**: Base de datos SQLite almacenando credenciales de usuario, datos de sesión y metadatos de contratos generados.

### Decisiones Técnicas e Implementación de Ciberseguridad

Como profesional certificado en ciberseguridad, tomé varias decisiones de diseño deliberadas para asegurar la integridad de la aplicación:

1.  **Enfoque Security-First**: En lugar de aprender conceptos de seguridad durante el desarrollo, los apliqué inmediatamente. Esto incluye implementar encabezados Content Security Policy (CSP), políticas estrictas de cookies (`HttpOnly`, `Secure`) y consultas SQL parametrizadas para prevenir inyección SQL.
2.  **Manejo de Contraseñas**: Las contraseñas nunca se almacenan en texto plano. Utilicé `werkzeug.security.generate_password_hash` con una sal fuerte, asegurando que incluso en el caso improbable de una brecha de base de datos, las credenciales de usuario permanezcan protegidas.
3.  **Validación de Entradas**: Se enforcean validaciones tanto del lado del cliente (JavaScript) como del servidor (Python). El módulo `rules.py` actúa como firewall secundario, rechazando datos que no cumplen restricciones legales o lógicas antes de que lleguen a la base de datos o generador PDF.
4.  **Seguridad PDF**: El proceso de generación PDF sanitiza todas las entradas del usuario para prevenir ataques de inyección que podrían alterar la estructura del documento o ejecutar código malicioso dentro del lector PDF.

### Desarrollo Eficiente y Antecedentes Profesionales

Mi formación como experto certificado en ciberseguridad y programación influyó significativamente en la trayectoria de este proyecto. Aproveché mi base técnica para profundizar en la implementación de seguridad web y arquitectura de datos, usando CS50 como el marco para estandarizar mis conocimientos. En consecuencia, completé el coursework del curso y los problem sets semanales en una fracción del tiempo típico gracias a mi experiencia previa.

Este ritmo acelerado me permitió dedicar la mayor parte de mi tiempo a arquitecturar un proyecto final robusto y de grado de producción. Como ya era competente en Flask, CSS, diseño de bases de datos y prácticas de codificación segura, el proceso de desarrollo fue notablemente fluido. No encontré los obstáculos comunes típicos de desarrolladores principiantes, como depurar errores de sintaxis básicos, luchar con configuración de frameworks o malentender ciclos de vida de peticiones web.

En cambio, mi enfoque estuvo enteramente en refinar la experiencia de usuario, optimizar el motor de renderizado PDF para diseños de impresión perfectos y asegurar que la lógica legal fuera sólida. La decisión de priorizar la legibilidad del PDF—permitiendo que los documentos abarquen múltiples páginas en lugar de comprimir contenido—proviene de un entendimiento profesional de estándares de documentos legales donde la claridad supera la brevedad. Si es necesario imprimir más de una hoja, se hace sin dudar para garantizar que el contrato sea perfectamente claro y profesional.

### Tecnologías Usadas

- **Backend**: Python, Flask
- **Base de Datos**: SQLite
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap 5
- **Librerías**: ReportLab (generación PDF), Werkzeug (seguridad), OS, Datetime
- **Entorno**: Linux/Unix, Git

### Cómo Ejecutar

Para ejecutar este proyecto localmente:

```bash
cd ContratoExpress
pip install -r requirements.txt
flask run
```

Accede a `http://localhost:5000` en tu navegador.

### Mejoras Futuras

Aunque la versión actual es robusta, iteraciones futuras podrían incluir:
- Integración con APIs de firma electrónica (ej. DocuSign) para firmado totalmente digital.
- Soporte multi-idioma para contratos internacionales.
- Integración avanzada de IA usando LLMs para sugerencias de cláusulas personalizadas.
- Despliegue a proveedor cloud (AWS/Heroku) con pipelines CI/CD.

### Nota del Autor

Este proyecto refleja la intersección entre rigor académico y experiencia profesional. Demuestra que con una base sólida en ciberseguridad y desarrollo de software, uno puede construir herramientas que no solo son funcionales sino también seguras y listas para despliegue en el mundo real. ContratoExpress es más que un requisito de curso; es un prototipo para un producto SaaS legítimo. Mi certificación me permitió evitar errores comunes, implementar security headers desde el inicio y enfocarme en crear algo útil en lugar de luchar con conceptos básicos, elevando este proyecto a estándares industriales.

---

*Proyecto desarrollado como proyecto final de CS50 Introduction to Computer Science, Harvard University, 2026.*
