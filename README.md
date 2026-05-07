# 📋 ContratoExpress v3.3
## Generador Inteligente de Contratos de Servicios Profesionales

> ¿Cansado de perder horas redactando contratos? ContratoExpress automatiza todo el proceso para que te enfoques en lo que realmente importa.

#### 🎥 Demo en video:  
<INSERTA AQUÍ LA URL DE TU VIDEO DE YOUTUBE/LOOM>

---

## 🚀 ¿Qué es ContratoExpress?

**ContratoExpress v3.3** es una aplicación web creada con **Flask** y Python que te permite generar contratos profesionales de servicios en cuestión de minutos. Sin complicaciones, sin plantillas genéricas... solo datos reales que se convierten en documentos listos para usar.

Piensa en ella como tu asistente legal que entiende de negocios. Llenas un formulario amigable, presionas un botón, y listo: tienes un contrato personalizado en PDF.

---

## ✨ Lo que hace especial a ContratoExpress

### 💼 Formulario Inteligente
Captura todos los detalles que realmente importan: quiénes son las partes, qué se acuerda, cuánto se paga, y bajo qué condiciones. Nada más, nada menos.

### 💱 Multi-moneda (¿Trabajas internacionalmente?)
Genera contratos en USD, EUR, GBP y más. Cada moneda con su símbolo correcto y formato numérico apropiado. Porque los detalles importan cuando hablamos de dinero.

### 🔐 Seguridad desde el primer día
- Registro e inicio de sesión con contraseñas encriptadas
- Tus contratos no son visibles para otros usuarios
- Validaciones en frontend y backend (no confiamos en nadie)

### 📱 Interfaz moderna y responsiva
Se ve bien en desktop, tablet o celular. Porque los contratos no esperan a que llegues a una oficina.

---

## 🏗️ Cómo está construido

El proyecto sigue una estructura limpia y modular. Aquí está el desglose:

```
repositorio/
├── app.py                 # El corazón de todo
├── rules.py              # Validaciones estrictas
├── requirements.txt      # Dependencias necesarias
├── templates/            # Plantillas HTML
│   ├── layout.html       # Base + navegación
│   ├── login.html
│   ├── register.html
│   └── index.html        # El formulario principal
└── static/               # CSS y subidas de usuarios
    └── uploads/          # Logos de clientes
```

**`app.py`** → Es donde sucede la magia. Define todas las rutas de la aplicación, maneja formularios, gestiona usuarios y genera los contratos finales.

**`rules.py`** → Separa la lógica de validación. Verifica emails, monedas, longitudes de texto... todo lo que puede salir mal. Mejor prevenir que lamentar.

**`templates/`** → El frontend. Plantillas HTML que Flask renderiza dinámicamente. `layout.html` es la base común (navegación, estilos globales), y el resto son vistas específicas.

**`static/`** → CSS personalizado y la carpeta donde los usuarios suben sus logos. Todo para que cada contrato luzca profesional.

**`requirements.txt`** → Las dependencias. Principalmente Flask, Werkzeug para seguridad, y librerías para PDFs e imágenes.

---

## 🤔 Decisiones de Diseño y Aprendizajes

### Por qué SQLite y no una base de datos "seria"

Al principio pensé en PostgreSQL o MySQL. Pero aquí está la verdad: SQLite es *perfecto* para aplicaciones medianas. Es ligero, no requiere configuración de servidor, y es portátil. El archivo `.db` es tu base de datos completa. Para una app como esta, es suficiente y elegante.

### El desafío de los PDFs

La primera idea fue usar librerías pesadas de generación de PDF en Python. Funcionaría, pero sería lento y complicado.

La solución: **generar HTML limpio y dejar que el navegador lo convierta a PDF**. Más rápido, más simple, y el usuario controla el resultado. Fue una buena decisión.

### Validación en dos puntos

Validamos en el frontend (JavaScript) para una experiencia fluida, *pero también en el backend* (Python). Porque no confiar en el navegador es regla número 1 en seguridad web.

---

## 📈 Cómo usar ContratoExpress

1. **Crea una cuenta** → Registro simple con email y contraseña
2. **Llena el formulario** → Datos de las partes, servicios, moneda, términos
3. **Descarga tu contrato** → En PDF, listo para usar o ajustar

---

## 🎓 El Contexto

Este proyecto fue desarrollado como parte del curso **CS50x de Harvard**. Un excelente ejercicio de cómo la tecnología web moderna puede resolver problemas reales del mundo profesional.

---

## 💡 Lecciones Aprendidas

- **La simplicidad escala mejor que la complejidad** → Una app enfocada es más útil que una que intenta hacerlo todo
- **La validación en dos capas es no-negociable** → Nunca confíes en el cliente
- **Los usuarios agradecen las decisiones por ellos** → Un buen UI/UX elimina dudas

---

¿Preguntas? Sugerencias? Este proyecto está aquí para crecer. 🚀
