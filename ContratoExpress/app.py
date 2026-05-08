from flask import Flask, render_template, request, redirect, session, flash, url_for, send_from_directory, abort, send_file
from flask_wtf.csrf import CSRFProtect
from rules import get_db, validate_contract, register_user, login_user
from fpdf import FPDF
import os, time, functools, sqlite3, io

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'cs50-dev-secret-key-change-in-prod')
# Dev fallback key
app.config['WTF_CSRF_SSL_STRICT'] = False
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# Store uploads here
app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024
# Prevent huge uploads
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
# El error de CSRF me hizo querer tirar la toalla, pero ya quedó
csrf = CSRFProtect(app)

# Clase PDF optimizada para una sola hoja - version corregida
class PDFContrato(FPDF):
    def __init__(self, contract_data, upload_folder):
        super().__init__(orientation='P', unit='mm', format='A4')
        self.contract = contract_data
        self.upload_folder = upload_folder
        self.set_auto_page_break(auto=False)
        
    def header(self):
        pass
    
    def footer(self):
        pass
    
    def generate(self):
        self.add_page()
        self.set_margins(left=15, top=12, right=15)
        
        # Logo esquina superior derecha
        if self.contract.get('provider_logo'):
            logo_path = os.path.join(self.upload_folder, self.contract['provider_logo'])
            if os.path.exists(logo_path):
                try:
                    self.image(logo_path, x=165, y=8, w=35, h=0)
                except:
                    pass
        
        # Titulo
        self.set_font('Arial', 'B', 10)
        self.cell(0, 6, 'CONTRATO DE PRESTACION DE SERVICIOS PROFESIONALES', ln=True, align='C')
        
        self.set_font('Arial', '', 8)
        self.cell(0, 4, f"Contrato #{self.contract['id']}", ln=True, align='C')
        deadline_str = str(self.contract.get('deadline', ''))[:10] if self.contract.get('deadline') else ''
        city = self.contract.get('city_location', '')
        self.cell(0, 4, f"En {city}, a {deadline_str}.", ln=True, align='C')
        
        self.ln(2)
        
        # Datos en lineas separadas para evitar overflow
        self.set_font('Arial', '', 7)
        
        # Prestador
        p_name = self.contract.get('provider_name', '')
        p_phone = self.contract.get('provider_phone', '')
        p_rfc = self.contract.get('rfc_provider', '')
        p_addr = self.contract.get('address_provider', '')
        
        self.multi_cell(0, 3.5, f"PRESTADOR: {p_name}", border=0, ln=1)
        extras = []
        if p_phone: extras.append(f"Tel: {p_phone}")
        if p_rfc: extras.append(f"RFC: {p_rfc}")
        if p_addr: extras.append(f"Dom: {p_addr}")
        if extras:
            self.multi_cell(0, 3.5, " | ".join(extras), border=0, ln=1)
        
        # Cliente
        c_name = self.contract.get('client_name', '')
        c_phone = self.contract.get('client_phone', '')
        c_rfc = self.contract.get('rfc_client', '')
        c_addr = self.contract.get('address_client', '')
        
        self.multi_cell(0, 3.5, f"CLIENTE: {c_name}", border=0, ln=1)
        extras = []
        if c_phone: extras.append(f"Tel: {c_phone}")
        if c_rfc: extras.append(f"RFC: {c_rfc}")
        if c_addr: extras.append(f"Dom: {c_addr}")
        if extras:
            self.multi_cell(0, 3.5, " | ".join(extras), border=0, ln=1)
        
        self.ln(1.5)
        
        # Clausulas
        self._add_clause("PRIMERA. OBJETO DEL CONTRATO", 
            f"EL PRESTADOR se obliga a realizar el servicio de: {self.contract.get('service_title', '')}\nDescripcion: {self.contract.get('service_desc', '')}")
        
        has_mat = self.contract.get('has_materials')
        if has_mat:
            mat = self.contract.get('materials_details', '')
            self._add_clause("SEGUNDA. MATERIALES", f"EL PRESTADOR incluye: {mat}. Los no especificados por cuenta de EL CLIENTE.")
        else:
            self._add_clause("SEGUNDA. MATERIALES", "Todos los materiales seran proporcionados por EL CLIENTE.")
        
        # Honorarios
        curr = self.contract.get('currency_symbol', '$') or '$'
        total = float(self.contract.get('total_amount', 0))
        tot_int = int(total)
        tot_cent = int((total % 1) * 100)
        curr_name = "pesos" if curr in ['$','MXN $','COP $','ARS $','CLP $','UYU $U'] else "unidades"
        
        pay_txt = f"Costo total: {curr}{total:.2f} ({tot_int} {curr_name} {tot_cent}/100 M.N.).\n"
        pay_struct = self.contract.get('payment_structure', '')
        adv = float(self.contract.get('advance_amount', 0) or 0)
        rem = float(self.contract.get('remaining_amount', 0) or 0)
        
        if pay_struct == 'advance':
            pay_txt += f"Anticipo: {curr}{adv:.2f} al firmar. Resto ({curr}{rem:.2f}) al finalizar."
        elif pay_struct == 'partial':
            pay_txt += "Pagos parciales segun avance."
        else:
            timing = "iniciar" if self.contract.get('payment_timing') == 'before' else "finalizar"
            pay_txt += f"Pago unico al {timing} el servicio."
        
        pm = self.contract.get('payment_method', '')
        if pm == 'transfer':
            pay_txt += f"\nTransferencia a: {self.contract.get('bank_details', '')}"
        elif pm == 'crypto':
            pay_txt += f"\nCrypto: {self.contract.get('crypto_wallet', '')}"
        elif pm == 'other':
            pay_txt += f"\n{self.contract.get('other_method', '')}"
        
        self._add_clause("TERCERA. HONORARIOS Y FORMA DE PAGO", pay_txt)
        
        deadline = str(self.contract.get('deadline', ''))[:10] if self.contract.get('deadline') else ''
        self._add_clause("CUARTA. PLAZO DE EJECUCION", f"Entrega maxima: {deadline}.")
        
        self._add_clause("QUINTA. GARANTIA", "30 dias naturales por defectos de ejecucion. No cubre mal uso.")
        
        clause_num = 6
        if self.contract.get('include_confidentiality'):
            self._add_clause("SEXTA. CONFIDENCIALIDAD", "Confidencialidad por 2 anos despues de terminacion.")
            clause_num = 7
        
        if self.contract.get('payment_timing') == 'after' and self.contract.get('penalty_rate'):
            pen = float(self.contract.get('penalty_rate', 0))
            num = "SEPTIMA" if clause_num == 7 else "SEXTA"
            self._add_clause(f"{num}. INCUMPLIMIENTO", f"Penalizacion del {pen:.1f}% diario. Terminacion despues de 15 dias.")
            if clause_num == 7: clause_num = 8
        
        term_num = "OCTAVA" if clause_num == 8 else ("SEPTIMA" if clause_num == 7 else "SEXTA")
        self._add_clause(f"{term_num}. TERMINACION", "Por mutuo acuerdo o incumplimiento.")
        
        if self.contract.get('include_signatures'):
            self.ln(3)
            self._add_signatures()
        
        self.set_y(285)
        self.set_font('Arial', 'I', 7)
        created = str(self.contract.get('created_at', ''))[:10] if self.contract.get('created_at') else ''
        self.cell(0, 5, f"Generado por ContratoExpress - {created}", ln=True, align='C')
    
    def _add_clause(self, title, content):
        self.set_font('Arial', 'B', 9)
        self.cell(0, 4.5, title, ln=True)
        self.set_font('Arial', '', 8)
        enc = content.encode('latin-1', errors='replace').decode('latin-1')
        self.multi_cell(0, 3.5, enc)
        self.ln(1.5)
    
    def _add_signatures(self):
        sig_p = self.contract.get('sig_provider_name') or self.contract.get('provider_name', '')
        sig_c = self.contract.get('sig_client_name') or self.contract.get('client_name', '')
        witness = self.contract.get('witness_name')
        sig_w = self.contract.get('sig_witness_name') or witness if witness else None
        
        margin = 15
        avail = 210 - 2*margin
        
        if sig_w:
            cw = (avail - 20) / 3
            positions = [margin, margin + cw + 10, margin + 2*(cw + 10)]
            names = [sig_p, sig_c, sig_w]
            labels = ["EL PRESTADOR", "EL CLIENTE", "TESTIGO"]
        else:
            cw = (avail - 10) / 2
            positions = [margin, margin + cw + 10]
            names = [sig_p, sig_c]
            labels = ["EL PRESTADOR", "EL CLIENTE"]
        
        y_start = self.get_y()
        for pos, name, label in zip(positions, names, labels):
            self.set_xy(pos, y_start)
            self.set_font('Arial', '', 8)
            self.cell(cw, 0.5, '', border='B')
            self.set_xy(pos, y_start + 6)
            enc_name = name.encode('latin-1', errors='replace').decode('latin-1')
            self.multi_cell(cw, 3, enc_name, align='C')
            self.set_xy(pos, y_start + 12)
            self.cell(cw, 4, label, align='C')

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
    # Main contracts table
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
            currency_symbol TEXT DEFAULT '$',
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
# Redirect if user not logged in
# Quick auth check
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.after_request
def add_security_headers(response):
# Basic security headers
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'SAMEORIGIN'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    return response

def allowed_file(filename):
# I only wanted image uploads here
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Por fin arreglé lo del MIME, casi me rindo
def validate_image_mime(file):
    file.seek(0)
    header = file.read(8)
    file.seek(0)
    return (header.startswith(b'\x89PNG\r\n\x1a\n') or 
            header.startswith(b'\xff\xd8\xff') or 
            header.startswith(b'GIF87a') or header.startswith(b'GIF89a'))

@app.route('/')
def index():
# Logged users go to dashboard
    if 'user_id' in session:
        return render_template('dashboard.html')
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
# Signup route
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
# Login route
def login():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        
        try:
# Simple password check (use hashing in production!)
            user_id = login_user(username, password)
            if user_id:
# Reset old session data
                session.clear()
# Set session variable
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
# Delete user data + uploaded logos
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
# Keep form checks here
# This route gathers form data, validates it, and writes the final contract to SQLite.
        # Validaciones de integridad: Prestador no puede ser Cliente
        # Uff, por fin logré que esto funcione. Me costó horrores evitar que el prestador y el cliente sean la misma persona.
        # Al principio no lo validaba y generaba contratos raros. Espero que esto sea suficiente.
# Avoid contracts where provider and client are literally the same person
        nombre_prestador = request.form.get('provider_name', '').strip().lower()
        nombre_cliente = request.form.get('client_name', '').strip().lower()
        telefono_prestador = request.form.get('provider_phone', '').strip()
        telefono_cliente = request.form.get('client_phone', '').strip()
        
        if nombre_prestador and nombre_cliente and nombre_prestador == nombre_cliente:
            flash('Error: El nombre del prestador del servicio no puede ser igual al del cliente.', 'error')
            return render_template('form.html', form_data=request.form.to_dict(flat=True))
        
        if telefono_prestador and telefono_cliente and telefono_prestador == telefono_cliente:
            flash('Error: El número de teléfono del prestador no puede ser igual al del cliente.', 'error')
            return render_template('form.html', form_data=request.form.to_dict(flat=True))
        
        # Determinar símbolo de moneda
        tipo_moneda = request.form.get('tipo_moneda', 'pesos')
# Currency symbol for PDF
        simbolo_moneda = '$'
        
        if tipo_moneda == 'usd':
            simbolo_moneda = 'USD $'
        elif tipo_moneda == 'eur':
            simbolo_moneda = 'EUR €'
        elif tipo_moneda == 'gbp':
            simbolo_moneda = 'GBP £'
        elif tipo_moneda == 'mxn':
            simbolo_moneda = 'MXN $'
        elif tipo_moneda == 'cop':
            simbolo_moneda = 'COP $'
        elif tipo_moneda == 'ars':
            simbolo_moneda = 'ARS $'
        elif tipo_moneda == 'clp':
            simbolo_moneda = 'CLP $'
        elif tipo_moneda == 'pen':
            simbolo_moneda = 'PEN S/'
        elif tipo_moneda == 'uyu':
            simbolo_moneda = 'UYU $U'
        elif tipo_moneda == 'btc':
            simbolo_moneda = '₿'
        elif tipo_moneda == 'eth':
            simbolo_moneda = 'Ξ'
        elif tipo_moneda == 'otra':
            simbolo_moneda = request.form.get('moneda_personalizada', '$') or '$'
        
        errors = validate_contract(request.form.to_dict(flat=True))
        
        logo_filename = None
        if 'logo' in request.files:
# Optional logo upload
            file = request.files['logo']
# File extension alone is not enough
# Check extension first
            if file and file.filename != '' and allowed_file(file.filename):
# Check image header bytes
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

# Custom service name
        if request.form.get('service_type') == 'Otros':
            service_title = request.form.get('service_title_custom', '').strip()
        else:
            service_title = request.form.get('service_title_std', '').strip()
        
        if not service_title:
            flash("El título del servicio es obligatorio.", "error")
            return render_template('form.html', form_data=request.form.to_dict(flat=True))

        payment_structure = request.form.get('payment_structure')
        try:
# HTML forms send strings
            total = float(request.form.get('total_amount') or 0)
        except (ValueError, TypeError):
            total = 0.0
        
        advance = 0.0
        remaining = 0.0
        if payment_structure == 'advance':
            try:
# Forms send numbers as text
                advance = float(request.form.get('advance_amount') or 0)
            except (ValueError, TypeError):
                advance = 0.0
# Calculate remaining payment automatically
            remaining = total - advance

        penalty = 0.0
# Only apply discount if provided
        if request.form.get('apply_penalty') == '1' and request.form.get('payment_timing') == 'after':
            try:
                penalty = float(request.form.get('penalty_rate') or 0)
            except (ValueError, TypeError):
                penalty = 0.0

        conn = get_db()
        cursor = conn.cursor()
        try:
            # Save to DB
            cursor.execute('''
                INSERT INTO contracts (
                    user_id, city_location, provider_name, provider_phone, provider_logo,
                    client_name, client_phone, service_type, service_title, service_desc,
                    has_materials, materials_details, is_quote_pending,
                    payment_structure, payment_timing, total_amount, advance_amount, remaining_amount,
                    payment_method, bank_details, crypto_wallet, other_method, deadline, penalty_rate,
                    rfc_provider, rfc_client, address_provider, address_client, email_client,
                    witness_name, include_confidentiality, include_signatures,
                    sig_provider_name, sig_client_name, sig_witness_name, currency_symbol
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
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
                request.form.get('sig_witness_name'), simbolo_moneda
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

@app.route('/descargar_pdf/<int:contract_id>')
@login_required
def descargar_pdf(contract_id):
    conn = get_db()
    contract = conn.execute("SELECT * FROM contracts WHERE id = ? AND user_id = ?", 
                           (contract_id, session['user_id'])).fetchone()
    conn.close()
    
    if not contract:
        flash("Contrato no encontrado.", "error")
        return redirect(url_for('history'))
    
    # Convertir row a diccionario
    contract_data = dict(contract)
    
    try:
        pdf = PDFContrato(contract_data, UPLOAD_FOLDER)
        pdf.generate()
        
        # Generar PDF en memoria
        pdf_buffer = io.BytesIO()
        pdf_output = pdf.output(dest='S').encode('latin-1', errors='replace')
        pdf_buffer.write(pdf_output)
        pdf_buffer.seek(0)
        
        filename = f"contrato_{contract_id}.pdf"
        return send_file(
            pdf_buffer,
            mimetype='application/pdf',
            as_attachment=True,
            download_name=filename
        )
    except Exception as e:
        app.logger.error(f"Error al generar PDF: {e}")
        flash("Error al generar el PDF. Intente nuevamente.", "error")
        return redirect(url_for('view_contract', contract_id=contract_id))
