import re

from flask import Blueprint, jsonify, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from .db import get_db
from .models import User

main_bp = Blueprint('main', __name__)
COMPANY_NAME = 'Placeholder Industries'
EMAIL_PREVIEW_MAX_LENGTH = 200
EMAIL_VARIABLE_PATTERN = re.compile(
    r"{{\s*(firstname|lastname|email|role|company)\s*}}"
)
EMAIL_TEMPLATE_MARKERS = ("{{", "}}", "{%", "%}", "{#", "#}")


def _contains_unsupported_email_syntax(template):
    remaining_text = EMAIL_VARIABLE_PATTERN.sub("", template)
    return any(marker in remaining_text for marker in EMAIL_TEMPLATE_MARKERS)


def _render_email_preview(template, user):
    if _contains_unsupported_email_syntax(template):
        raise ValueError("Unsupported email signature syntax")

    values = {
        "firstname": user.first_name or "",
        "lastname": user.last_name or "",
        "email": user.email or "",
        "role": user.role or "",
        "company": COMPANY_NAME,
    }
    return EMAIL_VARIABLE_PATTERN.sub(lambda match: values[match.group(1)], template)


@main_bp.route('/')
def index():
    if current_user.is_authenticated:
        return render_template('home.html')
    return render_template('index.html')


@main_bp.route('/profile')
@login_required
def profile():
    return redirect(url_for('main.view_profile', id=current_user.id))


@main_bp.route('/profiles/<int:id>')
@login_required
def view_profile(id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = ? AND enabled = 1", (id,))
    row = cursor.fetchone()
    conn.close()
    if not row:
        return "User not found", 404
    internal_notes = row['internal_notes'] if str(current_user.id) == str(id) else None
    user = User(
        str(row['id']),
        row['username'],
        row['password_hash'],
        row['first_name'],
        row['last_name'],
        row['email'],
        row['about'],
        row['role'],
        internal_notes,
        row['email_signature'],
    )
    return render_template('view_profile.html', user=user)


@main_bp.route('/profiles/<int:id>/email-preview', methods=['POST'])
@login_required
def email_preview(id):
    if str(current_user.id) != str(id):
        return "Forbidden", 403

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = ?", (id,))
    row = cursor.fetchone()
    conn.close()
    if not row:
        return "User not found", 404

    user = User(
        str(row['id']), row['username'], row['password_hash'], row['first_name'],
        row['last_name'], row['email'], row['about'], row['role'], row['internal_notes']
    )
    email_template = request.form.get('email_template', '')
    if len(email_template) > EMAIL_PREVIEW_MAX_LENGTH:
        return "Email template is too long", 400
    if _contains_unsupported_email_syntax(email_template):
        return jsonify(error='The signature template contains unsupported syntax.'), 400

    return jsonify(preview=_render_email_preview(email_template, user))


@main_bp.route('/profiles/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_profile(id):
    if str(current_user.id) != str(id):
        return "Forbidden", 403

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = ?", (id,))
    row = cursor.fetchone()
    conn.close()
    if not row:
        return "User not found", 404

    user = User(
        str(row['id']),
        row['username'],
        row['password_hash'],
        row['first_name'],
        row['last_name'],
        row['email'],
        row['about'],
        row['role'],
        row['internal_notes'],
        row['email_signature'],
    )

    if request.method == 'POST':
        first_name = request.form.get('first_name', '')
        last_name = request.form.get('last_name', '')
        email = request.form.get('email', '')
        about = request.form.get('about', '')
        email_signature = request.form.get('email_signature', user.email_signature)

        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE users
            SET first_name = ?, last_name = ?, email = ?, about = ?, email_signature = ?
            WHERE id = ? AND enabled = 1
        ''', (first_name, last_name, email, about, email_signature, id))
        conn.commit()
        conn.close()

        flash('Profile updated!', 'success')
        return redirect(url_for('main.view_profile', id=id))

    return render_template('edit_profile.html', user=user)


@main_bp.route('/employees')
@login_required
def employees():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, username, first_name, last_name, role FROM users WHERE enabled = 1"
    )
    rows = cursor.fetchall()
    conn.close()
    employees_list = []
    for row in rows:
        employees_list.append({
            'id': row['id'],
            'username': row['username'],
            'name': f"{row['first_name'] or ''} {row['last_name'] or ''}".strip(),
            'role': row['role']
        })
    return render_template('employees.html', employees=employees_list)


@main_bp.route('/healthz')
def health():
    status = {"status": "healthy"}
    code = 200
    try:
        db = get_db()
        db.execute("SELECT 1")
        status["db"] = "connected"
    except Exception:
        status["status"] = "unhealthy"
        status["db"] = "disconnected"
        code = 503
    return jsonify(status), code
