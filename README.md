# ContratoExpress: Generador de Contratos para Servicios Simples

**Video Demo:**  

---

## Descripción del Proyecto

ContratoExpress es una plataforma web desarrollada para formalizar acuerdos de servicios técnicos y profesionales en la región de Cacahoatán, Chiapas.

En el contexto local, trabajadores independientes como plomeros, técnicos de soporte y pintores suelen operar bajo acuerdos verbales, lo que deriva en problemas de impagos o exigencias de servicios adicionales no pactados. Esta herramienta permite documentar estos términos en segundos, generando un contrato legal en formato PDF listo para firmar.

La aplicación implementa un flujo completo de gestión de usuarios y documentos, permitiendo no solo la creación de contratos de servicio, sino también la emisión de constancias de pago.

El diseño visual utiliza un enfoque de alto contraste denominado **"Clean Industrial"**, con un fondo oscuro y tipografía optimizada para reducir la fatiga visual durante su uso en entornos de trabajo.

---

# Decisiones de Diseño y Arquitectura

## Selección del Motor de PDF: `pdfkit` vs `FPDF`

Una de las decisiones más analizadas durante el desarrollo fue la elección de la librería para generar documentos.

Se evaluó `FPDF` por su precisión milimétrica; sin embargo, su sistema basado en coordenadas impedía el uso de estilos CSS modernos.

Finalmente, se optó por `pdfkit` (wrapper de `wkhtmltopdf`) debido a que permite el renderizado directo de HTML5 y CSS3. Esto garantiza que la vista previa mostrada en el navegador sea idéntica al archivo PDF final.

Esta decisión implicó también el reto técnico de gestionar dependencias binarias externas dentro del sistema operativo.

---

## Seguridad y Autenticación Manual

Siguiendo el rigor técnico de CS50, se evitó el uso de frameworks de autenticación prefabricados.

Se implementó un sistema manual utilizando hashing `SHA-256` con una sal aleatoria única por usuario. Esta arquitectura garantiza que las credenciales permanezcan protegidas incluso ante una posible brecha de la base de datos.

Además, se integraron protecciones contra:

- CSRF
- XSS
- Inyecciones SQL

Todo mediante validaciones estrictas del lado del servidor.

---

# Estructura de Archivos y Funcionalidad

## `app.py`

Funciona como el núcleo del sistema.

Orquesta las rutas de Flask, gestiona la lógica de sesiones de usuario y coordina la comunicación entre la base de datos SQLite y el motor de renderizado PDF.

Contiene los endpoints críticos relacionados con:

- Manejo de contratos
- Gestión de usuarios
- Seguridad de cuentas

---

## `rules.py`

Módulo personalizado diseñado para centralizar la lógica de validación.

Utiliza expresiones regulares (`Regex`) para validar de forma estricta:

- Teléfonos internacionales
- Correos electrónicos
- Formatos monetarios

Esto permite mantener `app.py` enfocado exclusivamente en el flujo principal de la aplicación.

---

## `requirements.txt`

Define el entorno virtual necesario, incluyendo librerías como:

- Flask
- Werkzeug
- Flask-WTF
- pdfkit

---

## `templates/layout.html`

Define la estructura base de `Jinja2`, incluyendo:

- Navegación principal
- Manejo de mensajes `flash`
- Componentes reutilizables del sistema

---

## `templates/contract_form.html`

Formulario dinámico encargado de capturar los datos del contrato.

Integra validaciones en tiempo real para mejorar la experiencia del usuario y reducir errores de captura.

---

## `templates/contract_template.html`

Plantilla optimizada para el renderizado PDF.

Diseñada para mantener proporciones, márgenes y distribución correcta tanto en formato digital como impreso.

---

## `static/css/style.css`

Hoja de estilos personalizada que implementa el diseño oscuro del sistema y asegura compatibilidad responsiva para dispositivos móviles.

---

## `static/js/script.js`

Gestiona las interacciones dinámicas del frontend, incluyendo:

- Cálculo automático de totales
- Previsualización de datos
- Validaciones visuales antes del envío

---

## `uploads/`

Directorio destinado a la gestión temporal de logos personalizados.

Incluye protocolos de limpieza automática tras finalizar cada sesión.

---

## `wkhtmltopdf_..._amd64.deb`

Binario incluido manualmente para asegurar la portabilidad del motor de renderizado en entornos Linux y Codespaces, evitando conflictos de repositorios.

---

# Instalación y Configuración

Para asegurar el funcionamiento correcto del proyecto, es importante seguir estos pasos en orden.

## 1. Navegar al directorio del proyecto

```bash
cd ContratoExpress/
```

---

## 2. Instalar dependencias de Python

```bash
pip install -r requirements.txt
```

---

## 3. Instalar el motor PDF

```bash
sudo dpkg -i wkhtmltopdf_0.12.6-2build2_amd64.deb
```

---

## 4. Corregir dependencias del sistema

> Paso crucial para evitar errores de instalación.

```bash
sudo apt install -f
```

---

## 5. Ejecutar la aplicación

```bash
flask run
```

---

# Seguridad y Privacidad

La arquitectura del sistema se basa en la protección de datos desde el diseño.

Las contraseñas se gestionan mediante `hashlib`, las sesiones expiran automáticamente tras periodos de inactividad y se valida el tipo MIME de cada archivo subido para mitigar la ejecución de scripts maliciosos.

Este enfoque garantiza que la herramienta sea confiable para el uso profesional diario.
