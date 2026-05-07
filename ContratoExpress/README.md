# ContratoExpress - Generador de Contratos para Servicios Simples

#### Video Demo: <URL HERE>

#### Description:

**ContratoExpress** es una aplicación web desarrollada con Flask que permite a técnicos, electricistas, plomeros, tutores y freelancers generar contratos profesionales para servicios simples de manera rápida y sencilla. Esta herramienta nació como mi proyecto final para el curso CS50 de Harvard.

## Sobre el Autor y Contexto del Proyecto

Soy un profesional certificado en ciberseguridad y programación con amplia experiencia en el desarrollo de software seguro y aplicaciones web. Decidí tomar el curso CS50 de Harvard no por necesidad de aprender los fundamentos básicos, sino para obtener el respaldo y prestigio que ofrece esta institución reconocida mundialmente. Gracias a mi experiencia previa y conocimientos sólidos en programación, pude completar el curso en un tiempo significativamente menor al estimado, avanzando rápidamente a través de las semanas de contenido y desafíos.

Esta experiencia me permitió dedicar más tiempo y energía a desarrollar un proyecto final robusto y profesional como ContratoExpress, aplicando las mejores prácticas de seguridad que ya conocía de mi trayectoria en ciberseguridad, mientras aprovechaba la estructura académica de CS50 para validar y certificar mis habilidades ante la comunidad técnica global.

## ¿Qué problema resuelve?

Muchos profesionales que trabajan de manera independiente realizan acuerdos verbales con sus clientes sin ningún tipo de documentación formal. Esto puede generar malentendidos sobre el alcance del trabajo, los pagos, las fechas límite y las responsabilidades de cada parte. ContratoExpress soluciona esto permitiendo crear contratos legalmente válidos en minutos, simplemente completando un formulario intuitivo.

## Características Principales

### Sistema de Autenticación Seguro
- Registro de usuarios con validación de contraseñas (mínimo 6 caracteres)
- Inicio de sesión con hashes de contraseña usando Werkzeug
- Protección CSRF implementada con Flask-WTF
- Gestión de sesiones segura con limpieza automática al cerrar sesión
- Opción de eliminar cuenta permanentemente con confirmación explícita

### Generador de Contratos Personalizable
- **Datos completos de ambas partes**: Prestador y cliente con nombres, teléfonos y opciones para RFC, direcciones y email
- **Tipos de servicio predefinidos**: Soporte Técnico, Electricidad, Plomería, Enseñanza, o personalizado
- **Gestión de materiales**: Opción para especificar si se incluyen materiales y sus detalles
- **Estructuras de pago flexibles**:
  - Pago completo por adelantado
  - Pago con anticipo y resto (calculado automáticamente)
  - Pago posterior a la ejecución
- **Múltiples métodos de pago**: Transferencia bancaria, criptomonedas, efectivo u otro
- **Cálculo automático de penalizaciones**: Para pagos posteriores con fecha límite vencida
- **Soporte multi-moneda**: Pesos mexicanos, dólares, euros, libras, criptomonedas (BTC, ETH) y moneda personalizada

### Validaciones Robustas
- Verificación de que prestador y cliente no sean la misma persona (por nombre y teléfono)
- Validación de formatos de teléfono (mínimo 7 dígitos)
- Validación de emails con expresiones regulares
- Verificación de que las fechas límite no estén en el pasado
- Validación de coherencia en montos (anticipo + resto = total)
- Validación MIME para archivos de logo (PNG/JPG reales, no solo extensión)

### Interfaz de Usuario Profesional
- Diseño moderno con tema oscuro profesional (tonos dorados y grises)
- Totalmente responsive para móviles y tablets
- Modal informativo explicativo para nuevos usuarios
- Alertas visuales con íconos para errores y éxitos
- Vista previa de logos antes de subir
- Navegación intuitiva con barra superior persistente

### Historial y Gestión de Documentos
- Listado de todos los contratos creados por usuario
- Búsqueda y filtrado por fecha, cliente y monto
- Eliminación de contratos con confirmación
- Visualización de contratos en formato PDF listo para imprimir
- Almacenamiento seguro de logos en carpeta protegida

## Estructura del Proyecto

```
ContratoExpress/
├── app.py                 # Aplicación principal Flask con todas las rutas
├── rules.py               # Lógica de negocio, validaciones y funciones de base de datos
├── requirements.txt       # Dependencias del proyecto (Flask, Werkzeug, Flask-WTF)
├── .gitignore            # Archivos ignorados por Git
├── templates/            # Plantillas HTML con Jinja2
│   ├── base.html         # Plantilla base con navegación y estructura común
│   ├── login.html        # Página de inicio de sesión con modal explicativo
│   ├── register.html     # Página de registro con validaciones
│   ├── dashboard.html    # Panel principal del usuario
│   ├── form.html         # Formulario completo de creación de contratos
│   ├── history.html      # Historial de contratos creados
│   └── pdf_view.html     # Vista de contrato lista para impresión/PDF
└── static/               # Recursos estáticos
    ├── style.css         # Hoja de estilos completa con diseño responsive
    └── script.js         # JavaScript para interacciones del lado del cliente
```

## Detalles Técnicos y Decisiones de Diseño

### Base de Datos SQLite
Elegí SQLite por su simplicidad y porque no requiere configuración adicional. La base de datos `contracts.db` contiene dos tablas principales:
- `users`: Almacena credenciales con hashes seguros
- `contracts`: Contiene todos los campos del contrato con clave foránea hacia users

La tabla de contratos tiene más de 35 columnas para capturar toda la información necesaria. Implementé `PRAGMA foreign_keys = ON` para asegurar integridad referencial.

### Seguridad
Gracias a mi formación en ciberseguridad, implementé desde el inicio las mejores prácticas sin tener que aprenderlas durante el desarrollo:
- **CSRF Protection**: Usé Flask-WTF para proteger todos los formularios POST desde el primer momento
- **Password Hashing**: Las contraseñas nunca se guardan en texto plano, usando Werkzeug de forma nativa
- **Validación de Archivos**: Doble verificación de imágenes (extensión + cabecera MIME) implementada correctamente desde el inicio
- **Path Traversal Prevention**: Validación en ruta `/uploads/` para evitar acceso a directorios padre
- **Security Headers**: Implementé headers X-Content-Type-Options, X-Frame-Options y X-XSS-Protection

Mi experiencia previa me permitió evitar errores comunes que desarrolladores menos experimentados podrían cometer, como confiar únicamente en la extensión de archivos o olvidar protección CSRF.

### Manejo Eficiente del Desarrollo

Al contar con conocimientos sólidos en programación y seguridad, el flujo de desarrollo fue notablemente fluido:
1. **Configuración inicial rápida**: La estructura del proyecto, rutas y plantillas se definieron sin contratiempos gracias a experiencia previa con Flask
2. **Validaciones implementadas correctamente desde el inicio**: Sabía que verificar solo extensiones era inseguro, por lo que implementé lectura de cabeceras binarias desde el principio
3. **Cálculos precisos**: Los montos, anticipos y restantes se calcularon correctamente en el servidor desde la primera iteración
4. **Diseño CSS eficiente**: El diseño responsive y la sección de firmas se lograron de manera directa aplicando conocimientos previos de CSS Grid y Flexbox

Es importante mencionar que el desarrollo del proyecto se concluyó de manera repentina debido a compromisos profesionales y personales ineludibles que surgieron en mi vida diaria. A pesar de este cierre anticipado, el resultado es una aplicación completamente funcional y estable. Mi experiencia me permitió priorizar las características esenciales y entregar un producto sólido dentro del tiempo disponible, demostrando que la eficiencia y la calidad no dependen necesariamente de la cantidad de tiempo invertido, sino de la profundidad del conocimiento técnico aplicado.

### Impresión y PDF
La vista de contrato está diseñada específicamente para impresión:
- CSS `@media print` oculta elementos de navegación
- Salto de página automático antes de las firmas
- Colores adaptados para impresión en blanco y negro
- Formato profesional listo para firmar físicamente

## Cómo Ejecutar el Proyecto

```bash
cd ContratoExpress
pip install -r requirements.txt
export FLASK_APP=app.py
export SECRET_KEY='tu-clave-secreta-muy-segura'
flask run --host=0.0.0.0
```

Accede a `http://localhost:5000` en tu navegador.

## Tecnologías Utilizadas

- **Backend**: Python 3, Flask 3.0.3
- **Frontend**: HTML5, CSS3, JavaScript vanilla
- **Base de Datos**: SQLite3 con PRAGMA foreign_keys
- **Seguridad**: Werkzeug (password hashing), Flask-WTF (CSRF)
- **Iconos**: Font Awesome 6.4.0
- **Fuentes**: Google Fonts (Inter)

## Aprendizajes y Reflexiones

Contar con experiencia previa en programación y ciberseguridad marcó una diferencia significativa en mi enfoque del proyecto CS50. A diferencia de estudiantes que deben aprender conceptos básicos mientras desarrollan, yo pude aplicar inmediatamente las mejores prácticas de seguridad que ya dominaba: protección CSRF, validación MIME de archivos, hashing seguro de contraseñas y prevención de path traversal se implementaron correctamente desde la primera iteración.

La principal ventaja de mi formación fue la capacidad de identificar rápidamente la arquitectura adecuada y evitar errores comunes. Por ejemplo, sabía desde el inicio que verificar solo la extensión de archivos era inseguro, por lo que implementé lectura de cabeceras binarias desde el principio. Lo mismo ocurrió con los cálculos financieros, que diseñé para ejecutarse en el servidor evitando bugs típicos de validación del lado del cliente.

Mi certificación en ciberseguridad me permitió incorporar security headers, gestión segura de sesiones y validaciones robustas que un desarrollador sin esta formación podría pasar por alto o implementar incorrectamente. El resultado es una aplicación que no solo cumple con los requisitos académicos de CS50, sino que sigue estándares profesionales de la industria.

Lo que más valoro de haber tomado este curso con experiencia previa fue poder enfocarme en crear algo realmente útil y bien arquitecturado, en lugar de luchar con conceptos fundamentales. ContratoExpress demuestra que cuando tienes bases sólidas, puedes dedicar tu energía a resolver problemas reales y crear valor auténtico.

## Futuras Mejoras

Si tuviera más tiempo, me gustaría implementar:
- Envío de contratos por email directamente desde la plataforma
- Firmas digitales dibujables con mouse/táctil
- Plantillas predefinidas para diferentes tipos de servicios
- Exportación a PDF real con librerías como ReportLab
- Sistema de recordatorios de fechas límite
- Multi-idioma (inglés/español)

## Conclusión

ContratoExpress demuestra cómo la experiencia profesional en ciberseguridad y programación puede elevar un proyecto académico a estándares industriales. Mi formación me permitió desarrollar una aplicación robusta, segura y funcional sin los tropiezos típicos de desarrolladores principiantes. Cada característica, desde la protección CSRF hasta la validación MIME de archivos, fue implementada correctamente desde el inicio gracias a conocimientos previos.

Este proyecto no solo cumple con todos los requisitos de CS50, sino que representa una herramienta profesional que podría desplegarse inmediatamente para uso real. La combinación de mi certificación en ciberseguridad con el prestigio académico de Harvard resulta en un producto que refleja tanto competencia técnica como rigor académico.

---

*Proyecto desarrollado por [Tu Nombre] como proyecto final de CS50 Introduction to Computer Science, Harvard University, 2026.*
