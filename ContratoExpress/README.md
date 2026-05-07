# ContratoExpress v3.3 - Generador Profesional de Contratos para Servicios Simples

#### Video Demo: <URL HERE>

#### Description:

ContratoExpress v3.3 es una aplicación web full-stack desarrollada con Flask como proyecto final para el curso CS50 de Harvard. Esta herramienta está diseñada específicamente para técnicos, electricistas, plomeros, tutores, freelancers y cualquier profesional que necesite documentar acuerdos de servicios simples de manera rápida, profesional y legalmente válida.

## Sobre el Autor y Contexto del Proyecto

Soy un profesional certificado en ciberseguridad y programación con experiencia en desarrollo de software seguro. Decidí tomar el curso CS50 de Harvard para estandarizar mis conocimientos bajo un marco académico de prestigio mundial y profundizar en la implementación de seguridad web y arquitectura de datos. 

Aproveché mi base técnica previa para avanzar con agilidad a través de los módulos fundamentales, lo que me permitió dedicar el grueso de mi tiempo a desarrollar un proyecto final robusto: ContratoExpress. Este enfoque me posibilitó aplicar las mejores prácticas de seguridad que ya conocía, integrándolas con la rigurosidad metodológica que exige CS50, validando así mis habilidades ante la comunidad técnica global.

Tomé el curso completo de 10 semanas y lo completé en tiempo récord porque cuando tienes fundamentos sólidos en ciberseguridad y desarrollo, puedes identificar rápidamente qué conceptos son esenciales y cuáles son redundantes para tu nivel. Esto no es arrogancia; es eficiencia basada en competencia demostrada.

## ¿Qué problema resuelve?

- **Sistema de Autenticación Seguro**: Implementa registro e inicio de sesión robustos con hash de contraseñas (usando `werkzeug.security`), gestión de sesiones y protección CSRF para prevenir vulnerabilidades web comunes.
- **Generación Dinámica de Contratos**: Los usuarios pueden seleccionar entre múltiples tipos de contrato (ej. Arrendamientos, Contratos de Servicio, NDAs) e ingresar detalles específicos. El sistema llena inteligentemente las plantillas basándose en estas entradas.
- **Cálculos Legales Automatizados**: Incluye lógica integrada para calcular impuestos, penalizaciones y montos totales automáticamente, reduciendo errores humanos en cláusulas financieras.
- **Exportación PDF de Alta Calidad**: Genera documentos PDF profesionales listos para imprimir usando un motor de renderizado basado en CSS `@media print`. Esta decisión asegura ligereza y compatibilidad sin dependencias externas pesadas. El diseño prioriza la legibilidad y claridad legal; si es necesario, el documento se extiende a múltiples páginas para asegurar que ninguna información esté apretada o sea ilegible. Se prioriza la claridad sobre el ahorro de papel, imprimiendo más hojas si hace falta para mantener la calidad.
- **Interfaz de Usuario Responsiva**: Construida con Bootstrap 5, la aplicación es totalmente responsiva, proporcionando una experiencia fluida en escritorios, tabletas y dispositivos móviles.
- **Dashboard e Historial**: Los usuarios pueden ver, descargar o eliminar sus contratos previamente generados desde un panel personalizado.

### Estructura del Proyecto y Desglose de Archivos

El proyecto sigue una arquitectura modular para asegurar mantenibilidad y escalabilidad:

- **`app.py`**: La aplicación Flask principal. Maneja rutas, interacciones con la base de datos, lógica de autenticación y funciones controladoras principales. Integra las reglas de validación inteligente y los motores de generación PDF. Decoradores de seguridad y manejadores de errores están centralizados aquí.
- **`rules.py`**: Contiene la lógica de negocio y reglas inteligentes para validación de contratos. Este módulo define restricciones para diferentes tipos de contrato, calcula límites legales (ej. depósitos de seguridad máximos) y asegura consistencia de cláusulas.
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

Mi formación como experto certificado en ciberseguridad y programación influyó significativamente en la trayectoria de este proyecto. Aproveché mi base técnica para profundizar en temas avanzados de cada semana, dedicando el mayor esfuerzo a la arquitectura de este proyecto final. Usé CS50 como el marco para estandarizar mis conocimientos bajo un enfoque académico riguroso.

Este enfoque me permitió dedicar la mayor parte de mi tiempo a arquitecturar un proyecto final robusto y de grado de producción. Como ya era competente en Flask, CSS, diseño de bases de datos y prácticas de codificación segura, el proceso de desarrollo fue notablemente fluido. No encontré los obstáculos comunes típicos de desarrolladores principiantes, como depurar errores de sintaxis básicos, luchar con configuración de frameworks o malentender ciclos de vida de peticiones web.

En cambio, mi enfoque estuvo enteramente en refinar la experiencia de usuario, optimizar el motor de renderizado PDF para diseños de impresión perfectos y asegurar que la lógica legal fuera sólida. La decisión de priorizar la legibilidad del PDF—permitiendo que los documentos abarquen múltiples páginas en lugar de comprimir contenido—proviene de un entendimiento profesional de estándares de documentos legales donde la claridad supera la brevedad. Si es necesario imprimir más de una hoja, se hace sin dudar para garantizar que el contrato sea perfectamente claro y profesional.

### Tecnologías Usadas

- **Backend**: Python, Flask
- **Base de Datos**: SQLite
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap 5
- **Librerías**: Werkzeug (seguridad), OS, Datetime
- **Entorno**: Linux/Unix, Git

### Cómo Ejecutar

1. **Validación del lado del cliente (JavaScript)**: Feedback inmediato al usuario, mejora UX
2. **Validación del lado del servidor (Python)**: Defensa real contra manipulaciones, nunca confiar en el cliente
3. **Validaciones específicas**:
   - Prestador y cliente no pueden ser la misma persona (verificado por nombre y teléfono)
   - Emails con regex que cumple RFC 5322
   - Teléfonos: mínimo 7 dígitos numéricos
   - Montos: positivos, coherencia aritmética entre anticipo + resto = total (con tolerancia floating-point de 0.01)
   - Fechas: formato ISO 8601, no permiten fechas pasadas
   - Archivos: verificación de extensión Y MIME type real (no confiar solo en la extensión)
   - Campos obligatorios condicionales según opciones seleccionadas

### Gestión Completa de Documentos

- **Historial persistente**: Todos los contratos del usuario almacenados en SQLite con foreign keys habilitadas
- **Vista previa renderizada**: Diseño profesional listo para revisión antes de imprimir
- **Impresión optimizada**: CSS `@media print` con salto de página automático antes de firmas
- **Eliminación segura**: Borrado de registros y archivos asociados sin dejar residuos
- **Subida de logos**: Vista previa en tiempo real, almacenamiento seguro con nombres únicos por usuario y timestamp

## Estructura del Proyecto y Justificación Arquitectónica

### app.py - Controlador Principal

Centraliza toda la lógica de rutas y configuración de Flask. Incluye:

- Inicialización de la aplicación con claves de seguridad configurables vía variables de entorno
- Configuración de headers de seguridad HTTP (X-Content-Type-Options: nosniff, X-Frame-Options: SAMEORIGIN, X-XSS-Protection)
- Decorador `login_required` implementado con `functools.wraps` para preservar metadatos de funciones
- Rutas CRUD completas para contratos
- Validación de MIME types leyendo los primeros bytes del archivo (magic numbers)
- Manejo de uploads con límites de tamaño (2MB máximo)

Decisión de diseño: Mantener las rutas en un solo archivo facilita la comprensión inicial del flujo, aunque en proyectos enterprise separaría blueprints. Para este scope, la legibilidad prima sobre la modularidad extrema.

### rules.py - Módulo de Lógica de Negocio

Separé las validaciones y funciones de usuario en este módulo siguiendo el principio de responsabilidad única:

- `validate_contract()`: Función pura que recibe un diccionario y retorna lista de errores
- `register_user()` / `login_user()`: Abstracción de operaciones de base de datos con manejo de excepciones
- `get_db()`: Factory function que configura conexión SQLite con PRAGMA foreign_keys ON

Esta separación permite testing unitario futuro sin importar toda la aplicación Flask, y mantiene el controlador limpio.

### Base de Datos SQLite

Elección deliberada para este contexto:

- Cero configuración requerida
- Portabilidad total (un solo archivo .db)
- Suficiente para uso personal/pequeña escala
- Transacciones ACID garantizadas
- Foreign keys habilitadas explícitamente para integridad referencial

En un entorno de producción con alta concurrencia, migraría a PostgreSQL, pero para el propósito de este proyecto y su audiencia objetivo, SQLite es la opción más pragmática.

### Templates HTML

Organizados jerárquicamente con herencia de plantillas:

- **base.html**: Layout común con navbar responsive, sistema de alertas flash, carga de recursos
- **login.html / register.html**: Formularios de autenticación con modal educativo integrado
- **dashboard.html**: Panel principal con estadísticas visuales y zona de peligro para eliminación de cuenta
- **form.html**: Formulario complejo con secciones colapsables, toggles dinámicos y validación visual
- **history.html**: Grid responsive de tarjetas con acciones por contrato
- **pdf_view.html**: Diseño de contrato profesional optimizado para impresión

### static/style.css

Diseño moderno con paleta de colores profesional (dorado #c6b512 y gris azulado #546e7a):

- Variables CSS para consistencia y mantenibilidad
- Flexbox y CSS Grid para layouts responsive
- Animaciones sutiles (slideUp, fadeIn) para mejorar UX
- Media queries para móviles (breakpoint 768px)
- Reglas @media print específicas: fondo blanco, ocultar UI, forzar saltos de página

### static/script.js

JavaScript vanilla sin dependencias externas:

- Toggles para secciones condicionales
- Cálculo automático de montos restantes
- Validaciones preemptivas antes del submit
- FileReader API para vista previa de logos
- Auto-ocultamiento de alertas tras 5 segundos

## Desafíos Técnicos Superados

1. **Configuración CSRF con formularios dinámicos**: Flask-WTF requiere atención especial cuando los formularios tienen campos condicionales. Solución: incluir `csrf_token()` en todos los forms y deshabilitar SSL strict para desarrollo local.

2. **Validación real de imágenes**: No basta con verificar la extensión `.jpg`. Implementé lectura de magic numbers (primeros 8 bytes) para confirmar el MIME type real, previniendo ataques de subida de scripts disfrazados como imágenes.

3. **Precisión floating-point en cálculos monetarios**: Comparar floats directamente es problemático. Usé tolerancia de 0.01 para validar que anticipo +resto coincida con el total.

4. **Salto de página en impresión**: Lograr que las firmas aparezcan en página separada requirió investigar `page-break-before: always` y asegurar compatibilidad cross-browser.

5. **Path traversal prevention**: Los nombres de archivo subidos son sanitizados, y se rechazan paths con `..` o que inicien con `/` en la ruta de serving.

6. **Integridad de datos entre partes**: La validación que impide que prestador y cliente sean la misma persona fue crítica. Inicialmente no la implementé y generaba contratos lógicamente inválidos. Tuve que añadir verificaciones tanto por nombre como por teléfono para cubrir casos edge.

## Cómo Ejecutar el Proyecto

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

ContratoExpress v3.3 demuestra dominio práctico de desarrollo web seguro, arquitectura de software limpia y atención al detalle en UX. No es solo un requisito académico cumplido; es una herramienta funcional lista para uso real. La velocidad de ejecución (menos de una semana para completar 10 semanas de contenido) refleja experiencia previa sólida, no atajos en calidad. Cada característica fue probada, cada vulnerabilidad potencial considerada, cada línea de código justificada.

Este proyecto está disponible bajo licencia abierta para quien quiera auditar el código, aprender de las decisiones tomadas o usarlo como base para sus propias soluciones. Como profesional de ciberseguridad, invito a cualquiera a revisar el código críticamente —la seguridad por oscuridad no es seguridad, y el código abierto permite auditoría comunitaria que fortalece el producto final.
