from flask import Flask, render_template, request, redirect, session, flash, url_for, send_from_directory, abort
from flask_wtf.csrf import CSRFProtect
from rules import get_db, validate_contract, register_user, login_user
import os, time, functools, sqlite3

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'cs50-dev-secret-key-change-in-prod')
app.config['WTF_CSRF_SSL_STRICT'] = False
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
csrf = CSRFProtect(app)

def init_db():
    conn = sqlite3.connect('contracts.db')
    cursor = conn.cursor()
    cursor.execute('PRAGMA foreign_keys = ON')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS contracts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            city_location TEXT NOT NULL,
            provider_name TEXT NOT NULL,
            provider_phone TEXT NOT NULL,
            provider_logo TEXT,
            client_name TEXT NOT NULL,
            client_phone TEXT NOT NULL,
            service_type TEXT NOT NULL,
            service_title TEXT NOT NULL,
            service_desc TEXT NOT NULL,
            has_materials BOOLEAN,
            materials_details TEXT,
            is_quote_pending BOOLEAN,
            payment_structure TEXT NOT NULL,
            payment_timing TEXT NOT NULL,
            total_amount REAL NOT NULL,
            advance_amount REAL,
            remaining_amount REAL,
            payment_method TEXT NOT NULL,
            bank_details TEXT,
            crypto_wallet TEXT,
            other_method TEXT,
            deadline DATE NOT NULL,
            penalty_rate REAL,
            rfc_provider TEXT,
            rfc_client TEXT,
            address_provider TEXT,
            address_client TEXT,
            email_client TEXT,
            witness_name TEXT,
            include_confidentiality BOOLEAN,
            include_signatures BOOLEAN,
            sig_provider_name TEXT,
            sig_client_name TEXT,
            sig_witness_name TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
        )
    ''')
    conn.commit()
    conn.close()

init_db()

def login_required(f):
    @functools.wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.after_request
def add_security_headers(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'SAMEORIGIN'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    return response

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def validate_image_mime(file):
    file.seek(0)
    header = file.read(8)
    file.seek(0)
    return (header.startswith(b'\x89PNG\r\n\x1a\n') or 
            header.startswith(b'\xff\xd8\xff') or 
            header.startswith(b'GIF87a') or header.startswith(b'GIF89a'))

@app.route('/')
def index():
    if 'user_id' in session:
        return render_template('dashboard.html')
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        confirm = request.form.get('confirm', '')
        
        if not username or len(username) < 3:
            flash("Usuario muy corto (mínimo 3 caracteres).", "error")
            return redirect(url_for('register'))
        if not password or len(password) < 6:
            flash("Contraseña débil (mínimo 6 caracteres).", "error")
            return redirect(url_for('register'))
        if password != confirm:
            flash("Las contraseñas no coinciden.", "error")
            return redirect(url_for('register'))
        
        try:
            success, msg = register_user(username, password)
            if success:
                flash("Cuenta creada. Inicie sesión.", "success")
                return redirect(url_for('login'))
            else:
                flash(msg, "error")
        except Exception as e:
            flash("Error interno al registrar.", "error")
            app.logger.error(f"Register error: {e}")
        
        return redirect(url_for('register'))
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        
        try:
            user_id = login_user(username, password)
            if user_id:
                session.clear()
                session['user_id'] = user_id
                session['username'] = username
                return redirect(url_for('index'))
            else:
                flash("Credenciales inválidas.", "error")
        except Exception as e:
            flash("Error interno al iniciar sesión.", "error")
            app.logger.error(f"Login error: {e}")
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/delete_account', methods=['POST'])
@login_required
def delete_account():
    conn = get_db()
    cursor = conn.cursor()
    logos = [row[0] for row in cursor.execute("SELECT provider_logo FROM contracts WHERE user_id = ? AND provider_logo IS NOT NULL", (session['user_id'],)).fetchall()]
    cursor.execute("DELETE FROM contracts WHERE user_id = ?", (session['user_id'],))
    cursor.execute("DELETE FROM users WHERE id = ?", (session['user_id'],))
    conn.commit()
    conn.close()
    for logo in logos:
        filepath = os.path.join(UPLOAD_FOLDER, logo)
        if os.path.exists(filepath):
            try:
                os.remove(filepath)
            except OSError:
                pass
    session.clear()
    flash("Cuenta eliminada.", "warning")
    return redirect(url_for('register'))

@app.route('/new_contract', methods=['GET', 'POST'])
@login_required
def new_contract():
    if request.method == 'POST':
        errors = validate_contract(request.form.to_dict(flat=True))
        
        logo_filename = None
        if 'logo' in request.files:
            file = request.files['logo']
            if file and file.filename != '' and allowed_file(file.filename):
                if validate_image_mime(file):
                    ext = file.filename.rsplit('.', 1)[1].lower()
                    logo_filename = f"logo_{session['user_id']}_{int(time.time())}.{ext}"
                    file.save(os.path.join(app.config['UPLOAD_FOLDER'], logo_filename))
                else:
                    errors.append("El archivo no es una imagen válida.")
            elif file and file.filename != '':
                errors.append("Solo se permiten PNG/JPG.")

        if errors:
            for e in errors:
                flash(e, "error")
            return render_template('form.html', form_data=request.form.to_dict(flat=True))

        if request.form.get('service_type') == 'Otros':
            service_title = request.form.get('service_title_custom', '').strip()
        else:
            service_title = request.form.get('service_title_std', '').strip()
        
        if not service_title:
            flash("El título del servicio es obligatorio.", "error")
            return render_template('form.html', form_data=request.form.to_dict(flat=True))

        payment_structure = request.form.get('payment_structure')
        try:
            total = float(request.form.get('total_amount') or 0)
        except (ValueError, TypeError):
            total = 0.0
        
        advance = 0.0
        remaining = 0.0
        if payment_structure == 'advance':
            try:
                advance = float(request.form.get('advance_amount') or 0)
            except (ValueError, TypeError):
                advance = 0.0
            remaining = total - advance

        penalty = 0.0
        if request.form.get('apply_penalty') == '1' and request.form.get('payment_timing') == 'after':
            try:
                penalty = float(request.form.get('penalty_rate') or 0)
            except (ValueError, TypeError):
                penalty = 0.0

        conn = get_db()
        cursor = conn.cursor()
        try:
            # ✅ CORREGIDO: 35 columnas, 35 valores exactos
            cursor.execute('''
                INSERT INTO contracts (
                    user_id, city_location, provider_name, provider_phone, provider_logo,
                    client_name, client_phone, service_type, service_title, service_desc,
                    has_materials, materials_details, is_quote_pending,
                    payment_structure, payment_timing, total_amount, advance_amount, remaining_amount,
                    payment_method, bank_details, crypto_wallet, other_method, deadline, penalty_rate,
                    rfc_provider, rfc_client, address_provider, address_client, email_client,
                    witness_name, include_confidentiality, include_signatures,
                    sig_provider_name, sig_client_name, sig_witness_name
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                session['user_id'], request.form.get('city_location'),
                request.form.get('provider_name'), request.form.get('provider_phone'), logo_filename,
                request.form.get('client_name'), request.form.get('client_phone'),
                request.form.get('service_type'), service_title, request.form.get('service_desc'),
                1 if request.form.get('has_materials') else 0, request.form.get('materials_details'),
                1 if request.form.get('is_quote_pending') else 0,
                payment_structure, request.form.get('payment_timing'), total, advance, remaining,
                request.form.get('payment_method'), request.form.get('bank_details'),
                request.form.get('crypto_wallet'), request.form.get('other_method'),
                request.form.get('deadline'), penalty,
                request.form.get('rfc_provider'), request.form.get('rfc_client'),
                request.form.get('address_provider'), request.form.get('address_client'),
                request.form.get('email_client'), request.form.get('witness_name'),
                1 if request.form.get('include_confidentiality') else 0,
                1 if request.form.get('include_signatures') else 0,
                request.form.get('sig_provider_name'), request.form.get('sig_client_name'),
                request.form.get('sig_witness_name')
            ))
            conn.commit()
            contract_id = cursor.lastrowid
            conn.close()
            flash("Contrato generado con éxito.", "success")
            return redirect(url_for('view_contract', contract_id=contract_id))
        except Exception as e:
            conn.close()
            app.logger.error(f"Error al guardar contrato: {e}")
            flash("Error interno al guardar. Intente nuevamente.", "error")
            return render_template('form.html', form_data=request.form.to_dict(flat=True))
    
    return render_template('form.html', form_data=None)

@app.route('/history')
@login_required
def history():
    conn = get_db()
    contracts = conn.execute("SELECT * FROM contracts WHERE user_id = ? ORDER BY created_at DESC", (session['user_id'],)).fetchall()
    conn.close()
    return render_template('history.html', contracts=contracts)

@app.route('/view/<int:contract_id>')
@login_required
def view_contract(contract_id):
    conn = get_db()
    contract = conn.execute("SELECT * FROM contracts WHERE id = ? AND user_id = ?", (contract_id, session['user_id'])).fetchone()
    conn.close()
    if not contract:
        flash("Contrato no encontrado.", "error")
        return redirect(url_for('history'))
    return render_template('pdf_view.html', contract=contract)

@app.route('/delete/<int:contract_id>', methods=['POST'])
@login_required
def delete_contract(contract_id):
    conn = get_db()
    contract = conn.execute("SELECT provider_logo FROM contracts WHERE id = ? AND user_id = ?", (contract_id, session['user_id'])).fetchone()
    if contract:
        if contract['provider_logo']:
            filepath = os.path.join(UPLOAD_FOLDER, contract['provider_logo'])
            if os.path.exists(filepath):
                try:
                    os.remove(filepath)
                except OSError:
                    pass
        conn.execute("DELETE FROM contracts WHERE id = ?", (contract_id,))
        conn.commit()
        flash("Contrato eliminado.", "warning")
    conn.close()
    return redirect(url_for('history'))

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    if '..' in filename or filename.startswith('/'):
        abort(403)
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
