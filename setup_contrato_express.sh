#!/bin/bash

# Script de instalación para ContratoExpress
# Crea una aplicación Flask completa para gestión de contratos

echo "Creando estructura de directorios..."
mkdir -p contrato_express/static
mkdir -p contrato_express/templates
mkdir -p contrato_express/static/uploads

cd contrato_express

# Crear requirements.txt
cat > requirements.txt << 'EOF'
Flask==3.0.0
Flask-SQLAlchemy==3.1.1
Flask-Login==0.6.3
Werkzeug==3.0.1
EOF

# Crear app.py
cat > app.py << 'EOF'
import os
import sqlite3
from flask import Flask, render_template, request, redirect, session, flash, url_for, send_file
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from datetime import datetime
import io

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['DATABASE'] = 'contratos.db'

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def get_db():
    conn = sqlite3.connect(app.config['DATABASE'])
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    c = conn.cursor()
    
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    c.execute('''
        CREATE TABLE IF NOT EXISTS contracts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            cliente_nombre TEXT NOT NULL,
            cliente_dni TEXT,
            servicio_desc TEXT NOT NULL,
            monto_total REAL NOT NULL,
            tipo_pago TEXT NOT NULL,
            anticipo REAL DEFAULT 0,
            resto REAL DEFAULT 0,
            fecha_entrega DATE,
            penalizacion TEXT,
            firma_cliente TEXT,
            firma_proveedor TEXT,
            logo_path TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if not username or not password:
            flash('Usuario y contraseña requeridos', 'error')
            return redirect(url_for('register'))
            
        conn = get_db()
        user = conn.execute('SELECT id FROM users WHERE username = ?', (username,)).fetchone()
        
        if user:
            flash('El usuario ya existe', 'error')
            conn.close()
            return redirect(url_for('register'))
            
        hashed_pw = generate_password_hash(password)
        conn.execute('INSERT INTO users (username, password_hash) VALUES (?, ?)', 
                     (username, hashed_pw))
        conn.commit()
        conn.close()
        
        flash('Registro exitoso. Inicia sesión.', 'success')
        return redirect(url_for('login'))
        
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        conn = get_db()
        user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
        conn.close()
        
        if user and check_password_hash(user['password_hash'], password):
            session['user_id'] = user['id']
            session['username'] = user['username']
            return redirect(url_for('dashboard'))
        else:
            flash('Credenciales inválidas', 'error')
            
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
        
    conn = get_db()
    stats = {
        'total': conn.execute('SELECT COUNT(*) FROM contracts WHERE user_id = ?', (session['user_id'],)).fetchone()[0],
        'monto': conn.execute('SELECT SUM(monto_total) FROM contracts WHERE user_id = ?', (session['user_id'],)).fetchone()[0] or 0
    }
    recent = conn.execute('''
        SELECT * FROM contracts 
        WHERE user_id = ? 
        ORDER BY created_at DESC LIMIT 5
    ''', (session['user_id'],)).fetchall()
    conn.close()
    
    return render_template('dashboard.html', stats=stats, recent=recent)

@app.route('/crear', methods=['GET', 'POST'])
def crear_contrato():
    if 'user_id' not in session:
        return redirect(url_for('login'))
        
    if request.method == 'POST':
        cliente = request.form.get('cliente')
        dni = request.form.get('dni')
        servicio = request.form.get('servicio')
        monto = float(request.form.get('monto'))
        tipo_pago = request.form.get('tipo_pago')
        anticipo = float(request.form.get('anticipo', 0))
        resto = float(request.form.get('resto', 0))
        fecha = request.form.get('fecha')
        penalizacion = request.form.get('penalizacion')
        firma_cli = request.form.get('firma_cliente')
        firma_prov = request.form.get('firma_proveedor')
        
        logo_path = None
        if 'logo' in request.files:
            file = request.files['logo']
            if file.filename != '':
                filename = secure_filename(f"{session['user_id']}_{file.filename}")
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                logo_path = filename

        conn = get_db()
        conn.execute('''
            INSERT INTO contracts (user_id, cliente_nombre, cliente_dni, servicio_desc, 
            monto_total, tipo_pago, anticipo, resto, fecha_entrega, penalizacion, 
            firma_cliente, firma_proveedor, logo_path)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (session['user_id'], cliente, dni, servicio, monto, tipo_pago, 
              anticipo, resto, fecha, penalizacion, firma_cli, firma_prov, logo_path))
        conn.commit()
        conn.close()
        
        flash('Contrato creado correctamente', 'success')
        return redirect(url_for('historial'))
        
    return render_template('crear_contrato.html')

@app.route('/historial')
def historial():
    if 'user_id' not in session:
        return redirect(url_for('login'))
        
    conn = get_db()
    contratos = conn.execute('''
        SELECT * FROM contracts WHERE user_id = ? ORDER BY created_at DESC
    ''', (session['user_id'],)).fetchall()
    conn.close()
    return render_template('historial.html', contratos=contratos)

@app.route('/ver/<int:id>')
def ver_contrato(id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
        
    conn = get_db()
    contrato = conn.execute('''
        SELECT * FROM contracts WHERE id = ? AND user_id = ?
    ''', (id, session['user_id'])).fetchone()
    conn.close()
    
    if not contrato:
        flash('Contrato no encontrado', 'error')
        return redirect(url_for('historial'))
        
    return render_template('ver_contrato.html', contrato=contrato)

@app.route('/eliminar/<int:id>', methods=['POST'])
def eliminar_contrato(id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
        
    conn = get_db()
    conn.execute('DELETE FROM contracts WHERE id = ? AND user_id = ?', (id, session['user_id']))
    conn.commit()
    conn.close()
    
    flash('Contrato eliminado', 'info')
    return redirect(url_for('historial'))

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
EOF

# Crear templates/base.html
cat > templates/base.html << 'EOF'
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}ContratoExpress{% endblock %}</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
</head>
<body>
    <nav class="navbar">
        <div class="container">
            <a href="{{ url_for('dashboard') }}" class="brand">ContratoExpress</a>
            <div class="menu">
                {% if session.user_id %}
                    <a href="{{ url_for('dashboard') }}">Panel</a>
                    <a href="{{ url_for('crear_contrato') }}">Nuevo Contrato</a>
                    <a href="{{ url_for('historial') }}">Historial</a>
                    <a href="{{ url_for('logout') }}" class="btn-logout">Salir</a>
                {% endif %}
            </div>
        </div>
    </nav>

    <main class="container">
        {% with messages = get_flashed_messages(with_categories=true) %}
            {% if messages %}
                {% for category, message in messages %}
                    <div class="alert alert-{{ category }}">{{ message }}</div>
                {% endfor %}
            {% endif %}
        {% endwith %}
        
        {% block content %}{% endblock %}
    </main>

    <script src="{{ url_for('static', filename='script.js') }}"></script>
</body>
</html>
EOF

# Crear templates/login.html
cat > templates/login.html << 'EOF'
{% extends "base.html" %}
{% block title %}Iniciar Sesión{% endblock %}

{% block content %}
<div class="auth-box">
    <h2>Iniciar Sesión</h2>
    <form method="POST">
        <div class="form-group">
            <label>Usuario</label>
            <input type="text" name="username" required autocomplete="off">
        </div>
        <div class="form-group">
            <label>Contraseña</label>
            <input type="password" name="password" required>
        </div>
        <button type="submit" class="btn-primary">Entrar</button>
    </form>
    <p class="mt-3">¿No tienes cuenta? <a href="{{ url_for('register') }}">Regístrate</a></p>
</div>
{% endblock %}
EOF

# Crear templates/register.html
cat > templates/register.html << 'EOF'
{% extends "base.html" %}
{% block title %}Registro{% endblock %}

{% block content %}
<div class="auth-box">
    <h2>Crear Cuenta</h2>
    <form method="POST">
        <div class="form-group">
            <label>Usuario</label>
            <input type="text" name="username" required autocomplete="off">
        </div>
        <div class="form-group">
            <label>Contraseña</label>
            <input type="password" name="password" required>
        </div>
        <button type="submit" class="btn-primary">Registrarse</button>
    </form>
    <p class="mt-3">¿Ya tienes cuenta? <a href="{{ url_for('login') }}">Inicia sesión</a></p>
</div>
{% endblock %}
EOF

# Crear templates/dashboard.html
cat > templates/dashboard.html << 'EOF'
{% extends "base.html" %}
{% block title %}Panel Principal{% endblock %}

{% block content %}
<div class="dashboard-header">
    <h1>Hola, {{ session.username }}</h1>
    <a href="{{ url_for('crear_contrato') }}" class="btn-primary">+ Nuevo Contrato</a>
</div>

<div class="stats-grid">
    <div class="card">
        <h3>Contratos Totales</h3>
        <p class="stat-number">{{ stats.total }}</p>
    </div>
    <div class="card">
        <h3>Monto Acumulado</h3>
        <p class="stat-number">${{ "%.2f"|format(stats.monto) }}</p>
    </div>
</div>

<h3>Recientes</h3>
<table class="data-table">
    <thead>
        <tr>
            <th>Cliente</th>
            <th>Servicio</th>
            <th>Monto</th>
            <th>Fecha</th>
            <th>Acción</th>
        </tr>
    </thead>
    <tbody>
        {% for c in recent %}
        <tr>
            <td>{{ c.cliente_nombre }}</td>
            <td>{{ c.servicio_desc[:30] }}...</td>
            <td>${{ "%.2f"|format(c.monto_total) }}</td>
            <td>{{ c.created_at[:10] }}</td>
            <td><a href="{{ url_for('ver_contrato', id=c.id) }}">Ver</a></td>
        </tr>
        {% else %}
        <tr><td colspan="5">No hay contratos recientes</td></tr>
        {% endfor %}
    </tbody>
</table>
{% endblock %}
EOF

# Crear templates/crear_contrato.html
cat > templates/crear_contrato.html << 'EOF'
{% extends "base.html" %}
{% block title %}Crear Contrato{% endblock %}

{% block content %}
<div class="form-container">
    <h2>Nuevo Contrato de Servicio</h2>
    <form method="POST" enctype="multipart/form-data" id="contractForm">
        
        <div class="section-title">Datos del Cliente</div>
        <div class="row">
            <div class="col">
                <label>Nombre Completo</label>
                <input type="text" name="cliente" required>
            </div>
            <div class="col">
                <label>DNI / ID</label>
                <input type="text" name="dni">
            </div>
        </div>

        <div class="section-title">Detalles del Servicio</div>
        <label>Descripción del Servicio</label>
        <textarea name="servicio" rows="4" required></textarea>

        <div class="row">
            <div class="col">
                <label>Monto Total ($)</label>
                <input type="number" step="0.01" name="monto" id="monto" required onchange="calcularPagos()">
            </div>
            <div class="col">
                <label>Fecha de Entrega</label>
                <input type="date" name="fecha">
            </div>
        </div>

        <div class="section-title">Condiciones de Pago</div>
        <select name="tipo_pago" id="tipoPago" onchange="togglePagos()">
            <option value="unico">Pago Único</option>
            <option value="anticipo">Anticipo + Resto</option>
            <option value="parcial">Pagos Parciales</option>
        </select>

        <div id="pagosExtra" style="display:none;" class="row">
            <div class="col">
                <label>Anticipo ($)</label>
                <input type="number" step="0.01" name="anticipo" id="anticipo" value="0">
            </div>
            <div class="col">
                <label>Resto ($)</label>
                <input type="number" step="0.01" name="resto" id="resto" readonly>
            </div>
        </div>

        <div class="section-title">Cláusulas y Firmas</div>
        <label>Penalización por retraso (opcional)</label>
        <input type="text" name="penalizacion" placeholder="Ej: 5% diario">

        <div class="row">
            <div class="col">
                <label>Firma Cliente (Nombre)</label>
                <input type="text" name="firma_cliente" required>
            </div>
            <div class="col">
                <label>Firma Proveedor (Tu Nombre)</label>
                <input type="text" name="firma_proveedor" required>
            </div>
        </div>

        <label>Logo de la empresa (Opcional)</label>
        <input type="file" name="logo" accept="image/*">

        <button type="submit" class="btn-primary btn-block">Generar Contrato</button>
    </form>
</div>
{% endblock %}
EOF

# Crear templates/ver_contrato.html
cat > templates/ver_contrato.html << 'EOF'
{% extends "base.html" %}
{% block title %}Ver Contrato #{{ contrato.id }}{% endblock %}

{% block content %}
<div class="contract-paper">
    <div class="contract-header">
        {% if contrato.logo_path %}
            <img src="{{ url_for('static', filename='uploads/' + contrato.logo_path) }}" class="logo">
        {% endif %}
        <h1>CONTRATO DE PRESTACIÓN DE SERVICIOS</h1>
        <p class="ref">Ref: #{{ contrato.id }} - {{ contrato.created_at[:10] }}</p>
    </div>

    <div class="contract-body">
        <p><strong>Entre:</strong> {{ session.username }} (Proveedor) y <strong>{{ contrato.cliente_nombre }}</strong> (Cliente, DNI: {{ contrato.cliente_dni }}).</p>
        
        <h3>1. Objeto del Contrato</h3>
        <p>{{ contrato.servicio_desc }}</p>

        <h3>2. Honorarios y Pago</h3>
        <p>Monto total: <strong>${{ "%.2f"|format(contrato.monto_total) }}</strong>.</p>
        <p>Modalidad: {{ contrato.tipo_pago }}. 
           {% if contrato.tipo_pago != 'unico' %}
           Anticipo: ${{ "%.2f"|format(contrato.anticipo) }}, Resto: ${{ "%.2f"|format(contrato.resto) }}.
           {% endif %}
        </p>

        <h3>3. Plazo de Entrega</h3>
        <p>Fecha límite: {{ contrato.fecha_entrega or 'A convenir' }}.</p>
        {% if contrato.penalizacion %}
        <p class="warning"><strong>Penalización:</strong> {{ contrato.penalizacion }}</p>
        {% endif %}

        <div class="signatures">
            <div class="sig-box">
                <p>{{ contrato.firma_cliente }}</p>
                <span>EL CLIENTE</span>
            </div>
            <div class="sig-box">
                <p>{{ contrato.firma_proveedor }}</p>
                <span>EL PROVEEDOR</span>
            </div>
        </div>
    </div>
</div>

<div class="actions">
    <button onclick="window.print()" class="btn-secondary">Imprimir / PDF</button>
    <a href="{{ url_for('historial') }}" class="btn-secondary">Volver</a>
</div>
{% endblock %}
EOF

# Crear templates/historial.html
cat > templates/historial.html << 'EOF'
{% extends "base.html" %}
{% block title %}Historial{% endblock %}

{% block content %}
<h2>Mis Contratos</h2>
<table class="data-table">
    <thead>
        <tr>
            <th>ID</th>
            <th>Cliente</th>
            <th>Monto</th>
            <th>Fecha Creación</th>
            <th>Acciones</th>
        </tr>
    </thead>
    <tbody>
        {% for c in contratos %}
        <tr>
            <td>#{{ c.id }}</td>
            <td>{{ c.cliente_nombre }}</td>
            <td>${{ "%.2f"|format(c.monto_total) }}</td>
            <td>{{ c.created_at[:10] }}</td>
            <td>
                <a href="{{ url_for('ver_contrato', id=c.id) }}" class="btn-sm">Ver</a>
                <form action="{{ url_for('eliminar_contrato', id=c.id) }}" method="POST" style="display:inline;" onsubmit="return confirm('¿Seguro?');">
                    <button type="submit" class="btn-sm btn-danger">Eliminar</button>
                </form>
            </td>
        </tr>
        {% else %}
        <tr><td colspan="5">Sin contratos registrados</td></tr>
        {% endfor %}
    </tbody>
</table>
{% endblock %}
EOF

# Crear static/style.css
cat > static/style.css << 'EOF'
:root {
    --primary: #2563eb;
    --secondary: #64748b;
    --success: #22c55e;
    --danger: #ef4444;
    --bg: #f8fafc;
    --text: #1e293b;
}

body {
    font-family: system-ui, -apple-system, sans-serif;
    background: var(--bg);
    color: var(--text);
    margin: 0;
    line-height: 1.6;
}

.container { max-width: 1000px; margin: 0 auto; padding: 20px; }
.navbar { background: white; padding: 1rem 0; box-shadow: 0 1px 3px rgba(0,0,0,0.1); margin-bottom: 2rem; }
.navbar .container { display: flex; justify-content: space-between; align-items: center; margin: 0 auto; }
.brand { font-weight: bold; font-size: 1.25rem; text-decoration: none; color: var(--primary); }
.menu a { margin-left: 15px; text-decoration: none; color: var(--text); }
.btn-logout { color: var(--danger) !important; }

.alert { padding: 1rem; border-radius: 6px; margin-bottom: 1rem; }
.alert-success { background: #dcfce7; color: #166534; }
.alert-error { background: #fee2e2; color: #991b1b; }
.alert-info { background: #e0f2fe; color: #075985; }

.auth-box, .form-container { background: white; padding: 2rem; border-radius: 8px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); max-width: 500px; margin: 0 auto; }
.form-container { max-width: 800px; }
.form-group { margin-bottom: 1rem; }
label { display: block; margin-bottom: 0.5rem; font-weight: 500; }
input, select, textarea { width: 100%; padding: 0.5rem; border: 1px solid #cbd5e1; border-radius: 4px; box-sizing: border-box; }
.row { display: flex; gap: 1rem; margin-bottom: 1rem; }
.col { flex: 1; }
.section-title { font-weight: bold; margin: 1.5rem 0 0.5rem; color: var(--primary); border-bottom: 1px solid #e2e8f0; }

.btn-primary { background: var(--primary); color: white; border: none; padding: 0.5rem 1rem; border-radius: 4px; cursor: pointer; text-decoration: none; display: inline-block; }
.btn-secondary { background: var(--secondary); color: white; border: none; padding: 0.5rem 1rem; border-radius: 4px; cursor: pointer; text-decoration: none; display: inline-block; }
.btn-danger { background: var(--danger); color: white; border: none; padding: 0.25rem 0.5rem; border-radius: 4px; cursor: pointer; font-size: 0.875rem; }
.btn-block { width: 100%; margin-top: 1rem; }
.btn-sm { padding: 0.25rem 0.5rem; font-size: 0.875rem; }

.stats-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1rem; margin-bottom: 2rem; }
.card { background: white; padding: 1.5rem; border-radius: 8px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }
.stat-number { font-size: 2rem; font-weight: bold; color: var(--primary); margin: 0.5rem 0 0; }
.data-table { width: 100%; border-collapse: collapse; background: white; border-radius: 8px; overflow: hidden; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }
.data-table th, .data-table td { padding: 0.75rem; text-align: left; border-bottom: 1px solid #e2e8f0; }
.data-table th { background: #f1f5f9; font-weight: 600; }

.contract-paper { background: white; padding: 3rem; border: 1px solid #e2e8f0; box-shadow: 0 4px 6px rgba(0,0,0,0.1); margin-bottom: 2rem; }
.contract-header { text-align: center; border-bottom: 2px solid var(--text); padding-bottom: 1rem; margin-bottom: 2rem; }
.logo { max-height: 60px; margin-bottom: 1rem; }
.signatures { display: flex; justify-content: space-around; margin-top: 4rem; }
.sig-box { text-align: center; border-top: 1px solid var(--text); width: 40%; padding-top: 0.5rem; }
.actions { text-align: center; gap: 1rem; display: flex; justify-content: center; }

@media print {
    .navbar, .actions, .btn-danger { display: none; }
    .contract-paper { box-shadow: none; border: none; }
}
EOF

# Crear static/script.js
cat > static/script.js << 'EOF'
function calcularPagos() {
    const monto = parseFloat(document.getElementById('monto').value) || 0;
    const tipo = document.getElementById('tipoPago').value;
    const anticipoInput = document.getElementById('anticipo');
    const restoInput = document.getElementById('resto');

    if (tipo === 'unico') {
        document.getElementById('pagosExtra').style.display = 'none';
    } else {
        document.getElementById('pagosExtra').style.display = 'flex';
        if (anticipoInput.value) {
            const anticipo = parseFloat(anticipoInput.value) || 0;
            restoInput.value = (monto - anticipo).toFixed(2);
        }
    }
}

function togglePagos() {
    const tipo = document.getElementById('tipoPago').value;
    const extra = document.getElementById('pagosExtra');
    
    if (tipo === 'unico') {
        extra.style.display = 'none';
    } else {
        extra.style.display = 'flex';
        calcularPagos();
    }
}

document.addEventListener('DOMContentLoaded', () => {
    const anticipo = document.getElementById('anticipo');
    if (anticipo) {
        anticipo.addEventListener('input', () => {
            const monto = parseFloat(document.getElementById('monto').value) || 0;
            const val = parseFloat(anticipo.value) || 0;
            document.getElementById('resto').value = (monto - val).toFixed(2);
        });
    }
});
EOF

# Crear .gitignore
cat > .gitignore << 'EOF'
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
ENV/
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Flask
instance/
.webassets-cache

# Database
*.db
*.sqlite
*.sqlite3

# Uploads
static/uploads/*
!static/uploads/.gitkeep

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db

# Environment variables
.env
.flaskenv

# Logs
*.log
EOF

# Crear archivo .gitkeep para uploads
touch static/uploads/.gitkeep

echo ""
echo "=========================================="
echo "✅ Proyecto creado exitosamente"
echo "=========================================="
echo ""
echo "Siguientes pasos:"
echo "1. cd contrato_express"
echo "2. pip install -r requirements.txt"
echo "3. python app.py"
echo ""
echo "La aplicación estará disponible en http://localhost:5000"
echo ""
