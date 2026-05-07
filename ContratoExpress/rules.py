import sqlite3, re
from datetime import datetime, date
from werkzeug.security import generate_password_hash, check_password_hash

DATABASE = 'contracts.db'

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.execute("PRAGMA foreign_keys = ON")
    conn.row_factory = sqlite3.Row
    return conn

def validate_contract(data):
    errors = []
    # validaciones basicas
    if len(data.get('provider_name', '')) < 3:
        errors.append("Nombre del prestador muy corto.")
    if len(data.get('client_name', '')) < 3:
        errors.append("Nombre del cliente muy corto.")
    if len(data.get('city_location', '')) < 3:
        errors.append("Falta la ciudad de expedición.")
    phone_p = data.get('provider_phone', '').replace(" ", "").replace("-", "")
    phone_c = data.get('client_phone', '').replace(" ", "").replace("-", "")
    if not phone_p.isdigit() or len(phone_p) < 7:
        errors.append("Teléfono del prestador inválido (mínimo 7 dígitos).")
    if not phone_c.isdigit() or len(phone_c) < 7:
        errors.append("Teléfono del cliente inválido (mínimo 7 dígitos).")
    if len(data.get('service_desc', '')) < 5:
        errors.append("Descripción muy corta.")
    email = data.get('email_client', '')
    if email and not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
        errors.append("Email del cliente inválido.")
    try:
        total = float(data.get('total_amount', 0))
        if total <= 0:
            errors.append("El monto debe ser mayor a 0.")
        if data.get('payment_structure') == 'advance':
            advance = float(data.get('advance_amount', 0))
            remaining = float(data.get('remaining_amount', 0))
            if abs((advance + remaining) - total) > 0.01:
                errors.append("La suma del anticipo y resto no coincide con el total.")
    except (ValueError, TypeError):
        errors.append("Error en los montos: asegúrate de usar números válidos.")
    try:
        deadline_str = data.get('deadline')
        if not deadline_str:
            errors.append("Falta la fecha límite.")
        else:
            deadline = datetime.strptime(deadline_str, '%Y-%m-%d').date()
            if deadline < date.today():
                errors.append("La fecha límite no puede ser en el pasado.")
    except ValueError:
        errors.append("Formato de fecha inválido.")
    if data.get('has_materials') == 'on' and not data.get('materials_details'):
        errors.append("Debe detallar los materiales si los incluye.")
    if data.get('payment_method') == 'transfer' and not data.get('bank_details'):
        errors.append("Faltan datos bancarios.")
    if data.get('include_signatures') == 'on':
        if not data.get('sig_provider_name', '').strip():
            errors.append("Falta el nombre para la firma del prestador.")
        if not data.get('sig_client_name', '').strip():
            errors.append("Falta el nombre para la firma del cliente.")
    return errors

def register_user(username, password):
    conn = get_db()
    cursor = conn.cursor()
    existing = cursor.execute("SELECT id FROM users WHERE username = ?", (username,)).fetchone()
    if existing:
        conn.close()
        return False, "El usuario ya existe."
    password_hash = generate_password_hash(password)
    try:
        cursor.execute("INSERT INTO users (username, password_hash) VALUES (?, ?)", (username, password_hash))
        conn.commit()
        conn.close()
        return True, "Usuario creado."
    except Exception as e:
        conn.close()
        return False, str(e)

def login_user(username, password):
    conn = get_db()
    cursor = conn.cursor()
    user = cursor.execute("SELECT id, password_hash FROM users WHERE username = ?", (username,)).fetchone()
    conn.close()
    if user and check_password_hash(user['password_hash'], password):
        return user['id']
    return None
