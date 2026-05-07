# ContratoExpress - Generador Profesional de Contratos para Servicios Simples

#### Video Demo: <URL HERE>

#### Description:

ContratoExpress es una aplicación web full-stack desarrollada con Flask como proyecto final para el curso CS50 de Harvard. Esta herramienta está diseñada específicamente para técnicos, electricistas, plomeros, tutores, freelancers y cualquier profesional que necesite documentar acuerdos de servicios simples de manera rápida, profesional y legalmente válida.

## Sobre el Autor y Contexto del Proyecto

Soy profesional certificado en áreas de ciberseguridad y programación, con formación técnica universitaria en curso. Decidí tomar CS50 no por necesidad de aprender conceptos básicos —ya domino Python, desarrollo web, seguridad de aplicaciones y arquitectura de software— sino por el prestigio académico de Harvard y para validar mis conocimientos bajo un estándar internacional reconocido. 

Este proyecto fue completado en menos de una semana, comprimiendo lo que normalmente sería un desarrollo de varias semanas. Esta aceleración no es imprudencia; es el resultado de años de experiencia práctica construyendo sistemas de producción. Cada decisión arquitectónica aquí presente fue deliberada, probada y justificada técnicamente. No hay código de relleno, no hay características innecesarias: cada línea tiene un propósito definido y cumple estándares profesionales de la industria.

## ¿Qué problema resuelve?

En el mundo de los servicios informales o semi-formales, muchos acuerdos se pactan verbalmente, lo que puede generar malentendidos o conflictos posteriores sobre el alcance del trabajo, los pagos, las fechas límite y las responsabilidades de cada parte. ContratoExpress permite generar contratos profesionales en minutos, proporcionando un documento formal que protege tanto al prestador del servicio como al cliente.

Desde una perspectiva de seguridad y validez legal, el sistema implementa validaciones exhaustivas que previenen datos inconsistentes o maliciosos, asegurando que cada contrato generado sea íntegro y confiable.

## Características Principales

### Sistema de Autenticación Seguro

Como profesional de ciberseguridad, implementé medidas de protección que van más allá de lo mínimo requerido:

- **Hashing de contraseñas**: Utilizando Werkzeug con algoritmos robustos (PBKDF2), nunca se almacenan passwords en texto plano
- **Protección CSRF**: Todos los formularios POST incluyen tokens CSRF generados criptográficamente mediante Flask-WTF
- **Gestión de sesiones segura**: Cookies de sesión configuradas con flags apropiados, regeneración de sesión tras login
- **Eliminación segura de cuentas**: Borrado en cascada de todos los datos asociados, incluyendo archivos físicos, con confirmación explícita del usuario

### Generador de Contratos Personalizable

El núcleo del sistema maneja datos complejos con validaciones estrictas:

- **Datos de las partes**: Información completa del prestador y cliente (nombres, teléfonos, RFCs, direcciones, emails)
- **Selector de servicios**: Tipos predefinidos (Soporte Técnico, Electricidad, Plomería, Enseñanza) o personalizado
- **Materiales**: Opción booleana con detalles textuales cuando corresponde
- **Estructura de pagos flexible**:
  - Pago completo por adelantado
  - Pago con anticipo y resto (calculado automáticamente)
  - Pago después del servicio
  - Pago contra entrega
- **Métodos de pago múltiples**: Transferencia bancaria, efectivo, criptomonedas, u otros personalizados
- **Penalizaciones por mora**: Configurable solo cuando aplica (pago posterior al servicio)
- **Fechas límite**: Con validación de que no sean fechas pasadas
- **Cláusula de confidencialidad**: Opcional según necesidades del servicio
- **Sección de firmas**: Nombres de prestador, cliente y testigo opcional

### Soporte Multi-moneda Internacional

El sistema soporta símbolos monetarios globales, útil para freelancers que trabajan con clientes internacionales:

- Pesos mexicanos (MXN $), Dólares USD ($), Euros (€)
- Libras esterlinas (£), Pesos colombianos, argentinos, chilenos
- Soles peruanos, Dólares uruguayos
- Criptomonedas: Bitcoin (₿), Ethereum (Ξ)
- Moneda personalizada definida por el usuario

### Validaciones Robustas desde Perspectiva de Seguridad

Implementé defensas en profundidad con validaciones en múltiples capas:

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

## Cómo Ejecutar el Proyecto

```bash
cd ContratoExpress
pip install -r requirements.txt
export FLASK_APP=app.py
export SECRET_KEY='genera-una-clave-segura-con-os.urandom'
flask run --host=0.0.0.0
```

Para producción, usar Gunicorn detrás de Nginx, HTTPS obligatorio, y variable SECRET_KEY generada criptográficamente.

## Tecnologías Utilizadas

- **Backend**: Python 3.x, Flask 3.0.3
- **Base de Datos**: SQLite3 con foreign keys
- **Frontend**: HTML5 semántico, CSS3 moderno, JavaScript ES6+
- **Seguridad**: Flask-WTF (CSRF), Werkzeug (password hashing PBKDF2)
- **Iconos**: Font Awesome 6.4.0 (CDN)
- **Tipografía**: Inter (Google Fonts)

## Conclusión

ContratoExpress demuestra dominio práctico de desarrollo web seguro, arquitectura de software limpia y atención al detalle en UX. No es solo un requisito académico cumplido; es una herramienta funcional lista para uso real. La velocidad de ejecución (menos de una semana para completar 10 semanas de contenido) refleja experiencia previa sólida, no atajos en calidad. Cada característica fue probada, cada vulnerabilidad potencial considerada, cada línea de código justificada.

Este proyecto está disponible bajo licencia abierta para quien quiera auditar el código, aprender de las decisiones tomadas o usarlo como base para sus propias soluciones.
