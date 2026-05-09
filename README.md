# ContratoExpress: Generador de Contratos para Servicios Simples

#### Video Demo: <INSERT YOUR VIDEO URL HERE>

---

# Introducción y Propósito del Proyecto

ContratoExpress es una solución tecnológica integral diseñada para abordar un vacío legal y administrativo crítico en la región de **Cacahoatán, Chiapas**.

En esta zona, una parte significativa de la economía depende de trabajadores independientes —como técnicos de soporte, electricistas, plomeros y freelancers creativos— quienes tradicionalmente operan bajo acuerdos verbales. Esta falta de formalización documental suele resultar en una vulnerabilidad extrema para el prestador del servicio, enfrentándose frecuentemente a impagos, malentendidos sobre el alcance del trabajo o la exigencia de tareas adicionales no presupuestadas inicialmente.

Este proyecto surge no solo como un ejercicio académico para el curso CS50x de Harvard, sino como una herramienta de impacto social real. Su objetivo primordial es proporcionar una infraestructura digital intuitiva que permita a los trabajadores documentar términos, condiciones y montos en cuestión de segundos.

Al transformar acuerdos informales en contratos PDF profesionales, ContratoExpress dignifica el trabajo técnico y ofrece una capa de seguridad jurídica necesaria para el desarrollo económico local.

---

# Análisis de Decisiones de Ingeniería (Design Choices)

## El Motor de Renderizado: Evolución hacia `pdfkit`

Una de las fases más intensas de investigación durante el desarrollo fue la selección del motor para la generación de documentos PDF.

Inicialmente, exploré la librería `FPDF` por su reputación de ligereza; sin embargo, pronto identifiqué limitaciones críticas. Su sistema de diseño basado en coordenadas cartesianas resultaba excesivamente rígido e ineficiente para implementar una interfaz de usuario moderna y responsiva.

Tras realizar diversas pruebas de concepto, opté por `pdfkit`, que funciona como un wrapper para `wkhtmltopdf`. Esta decisión técnica fue estratégica: me permitió utilizar la potencia combinada de HTML5 y CSS3 para el renderizado del documento.

Esto garantiza el principio de "lo que ves es lo que obtienes" (WYSIWYG), asegurando que la previsualización interactiva en el navegador sea una réplica exacta del archivo descargable.

Para garantizar la portabilidad absoluta del sistema, incluí el paquete binario `.deb` directamente en el repositorio, eliminando la dependencia de repositorios externos que podrían fallar durante la evaluación o despliegue.

---

## Seguridad: Arquitectura de Autenticación desde Cero

Siguiendo los principios fundamentales de la ciberseguridad aprendidos en CS50, rechacé el uso de sistemas de autenticación prefabricados o librerías de alto nivel como Flask-Login que ocultan la lógica interna.

Construí manualmente un sistema de gestión de usuarios y sesiones para tener un control granular sobre el flujo de datos.

Implementé un protocolo de cifrado robusto utilizando la librería `hashlib` para aplicar un hashing **SHA-256** reforzado con una *sal* (`salt`) aleatoria única por cada usuario.

Este enfoque de "defensa en profundidad" asegura que, incluso en el hipotético caso de una brecha en la base de datos SQLite, las credenciales originales permanezcan criptográficamente inaccesibles.

Adicionalmente, programé validaciones manuales estrictas contra ataques de:

- Cross-Site Scripting (XSS)
- Cross-Site Request Forgery (CSRF)

Garantizando así un entorno seguro para el manejo de información sensible.

---

# Estructura Detallada del Sistema

Para cumplir con los estándares de complejidad exigidos por Harvard, el proyecto se ha estructurado de forma modular, separando estrictamente la lógica de negocio de la interfaz de usuario.

## `app.py`

Es el cerebro orquestador de la aplicación.

Gestiona:

- El enrutamiento de Flask
- El control de sesiones de usuario
- La comunicación bidireccional entre la persistencia de datos y el motor PDF

---

## `rules.py`

Módulo de validación de lógica de negocio altamente especializado.

Utiliza expresiones regulares (`Regex`) avanzadas para auditar la integridad de cada campo ingresado:

- Estructura de correos electrónicos
- Teléfonos internacionales
- Consistencia de montos monetarios

Esta separación permite que el código sea escalable y fácil de depurar.

---

## `requirements.txt`

Documento de configuración técnica que lista las versiones exactas de las dependencias:

- Flask
- pdfkit
- Werkzeug
- Flask-WTF

Esto asegura que el entorno de ejecución sea replicable en cualquier servidor Linux.

---

## `templates/layout.html`

Archivo maestro de `Jinja2` que define:

- Arquitectura visual global
- Navegación responsiva
- Sistema de mensajería interactiva

---

## `templates/contract_form.html`

Formulario interactivo encargado de recopilar los datos del servicio.

Incluye validaciones en el frontend para optimizar la experiencia del usuario antes de la validación final en el servidor.

---

## `templates/contract_template.html`

Piedra angular del diseño del documento.

Es una plantilla HTML optimizada específicamente para el motor de renderizado, asegurando:

- Márgenes correctos
- Logotipos profesionales
- Tipografía consistente

En el PDF final.

---

## `static/css/style.css`

Contiene la definición de la identidad visual **"Clean Industrial"**.

Utiliza variables CSS y `media queries` para asegurar compatibilidad tanto en dispositivos móviles como en monitores de alta resolución.

---

## `static/js/script.js`

Proporciona interactividad dinámica, permitiendo:

- Cálculos automáticos
- Gestión de subtotales
- Actualización de vistas previas en tiempo real

---

## `uploads/`

Directorio de almacenamiento temporal gestionado con protocolos de limpieza automática para manejar logotipos personalizados de forma eficiente y segura.

---

## `wkhtmltopdf_0.12.6-2build2_amd64.deb`

Binario esencial incluido para garantizar que el motor de PDF funcione en cualquier entorno basado en Debian, eliminando la necesidad de instalaciones externas durante la evaluación.

---

# Guía Técnica de Instalación (Entorno Linux)

Para asegurar un despliegue exitoso, es imperativo seguir este protocolo técnico.

## 1. Acceder al Directorio

```bash
cd ContratoExpress/
```

---

## 2. Instalar Dependencias de Python

```bash
pip install -r requirements.txt
```

---

## 3. Instalar el Motor de PDF

```bash
sudo dpkg -i wkhtmltopdf_0.12.6-2build2_amd64.deb
```

---

## 4. Resolver Dependencias Base (Paso Crítico)

Este paso permite que el sistema operativo instale automáticamente las librerías requeridas por el paquete `.deb`.

```bash
sudo apt install -f
```

---

## 5. Lanzar la Aplicación

```bash
flask run
```

---

# Filosofía de Diseño y Privacidad

ContratoExpress ha sido diseñado bajo el concepto estético **"Clean Industrial"**.

La paleta de zinc y tonos oscuros no responde únicamente a una preferencia visual; también busca reducir la fatiga ocular de trabajadores que utilizan la aplicación en condiciones de iluminación variables.

Además, el sistema respeta la soberanía de datos del usuario, permitiendo la eliminación definitiva de la cuenta y todos sus registros asociados.

Este proyecto refleja un compromiso total con la creación de software robusto, ético y funcional orientado a resolver problemas reales dentro de la comunidad técnica de Chiapas.
