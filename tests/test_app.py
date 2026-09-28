import sqlite3

import pytest
from werkzeug.security import generate_password_hash
from company_website import create_app
from company_website import auth
from company_website.config import Config
from company_website.models import User
from company_website.routes import _contains_unsupported_email_syntax, _render_email_preview


@pytest.fixture
def app(monkeypatch, tmp_path):
    monkeypatch.setattr(Config, 'DATABASE', str(tmp_path / 'database.db'))
    monkeypatch.setattr(Config, 'LEGACY_AUTH_DATABASE', str(tmp_path / 'legacy_auth.db'))
    return create_app({
        'TESTING': True,
        'SECRET_KEY': 'test-secret-key',
        'WTF_CSRF_ENABLED': False,
    })


@pytest.fixture
def client(app):
    return app.test_client()


def test_index(client):
    response = client.get('/')
    assert response.status_code == 200


def test_login_page(client):
    response = client.get('/login')
    assert response.status_code == 200


def test_profile_redirects_when_not_logged_in(client):
    response = client.get('/profile', follow_redirects=False)
    assert response.status_code == 302


def test_employees_redirects_when_not_logged_in(client):
    response = client.get('/employees', follow_redirects=False)
    assert response.status_code == 302


def test_healthz_endpoint(client):
    response = client.get('/healthz')
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'healthy'
    assert data['db'] == 'connected'


def test_email_preview_supports_profile_variables(app):
    user = User(
        '1', 'sample', '', first_name='Ada', last_name='Lovelace',
        email='ada@example.com', role='Engineer'
    )

    with app.app_context():
        preview = _render_email_preview(
            'Hello {{ firstname }} {{ lastname }} ({{ email }}, {{ role }}) - {{ company }}',
            user,
        )

    assert preview == 'Hello Ada Lovelace (ada@example.com, Engineer) - Placeholder Industries'


@pytest.mark.parametrize(
    'template',
    [
        '{{ 7 * 7 }}',
        '{{ config }}',
        '{{ firstname.__class__ }}',
        '{% for item in values %}{{ item }}{% endfor %}',
        '{# hidden expression #}',
    ],
)
def test_email_preview_rejects_executable_template_syntax(template):
    assert _contains_unsupported_email_syntax(template)

    user = User('1', 'sample', '', first_name='Ada')
    with pytest.raises(ValueError):
        _render_email_preview(template, user)


def test_legacy_lookup_uses_literal_credentials(monkeypatch, tmp_path):
    database_path = tmp_path / 'legacy.db'
    conn = sqlite3.connect(database_path)
    conn.execute(
        'CREATE TABLE legacy_users '
        '(id INTEGER PRIMARY KEY, username TEXT, password_hash TEXT)'
    )
    conn.execute(
        'INSERT INTO legacy_users (id, username, password_hash) VALUES (?, ?, ?)',
        (1, 'dev', generate_password_hash('known-password')),
    )
    conn.commit()
    conn.close()

    def connect_test_database():
        test_conn = sqlite3.connect(database_path)
        test_conn.row_factory = sqlite3.Row
        return test_conn

    monkeypatch.setattr(auth, 'get_legacy_db', connect_test_database)

    assert auth._get_legacy_user('dev', 'known-password')['username'] == 'dev'
    assert auth._get_legacy_user("dev' OR 1=1 --", 'anything') is None
    assert auth._get_legacy_user('dev', "' OR 1=1 --") is None


def _login_as(client, user_id=1):
    with client.session_transaction() as session:
        session['_user_id'] = str(user_id)
        session['_fresh'] = True


def test_app_requires_secret_key(monkeypatch, tmp_path):
    monkeypatch.setattr(Config, 'DATABASE', str(tmp_path / 'database.db'))
    monkeypatch.setattr(Config, 'LEGACY_AUTH_DATABASE', str(tmp_path / 'legacy_auth.db'))

    with pytest.raises(RuntimeError, match='SECRET_KEY'):
        create_app({'SECRET_KEY': None})


def test_csrf_rejects_post_without_token(app):
    app.config['WTF_CSRF_ENABLED'] = True
    response = app.test_client().post('/login', data={
        'username': 'dev',
        'password': 'password',
    })

    assert response.status_code == 400


def test_user_cannot_edit_another_profile(client):
    _login_as(client, user_id=1)

    assert client.get('/profiles/3/edit').status_code == 403
    assert client.post('/profiles/3/edit', data={'first_name': 'Changed'}).status_code == 403


def test_other_users_internal_notes_are_hidden(client):
    _login_as(client, user_id=1)

    response = client.get('/profiles/3')

    assert response.status_code == 200
    assert b'Secret project codename' not in response.data


def test_logout_requires_post(client):
    _login_as(client, user_id=1)

    assert client.get('/logout').status_code == 405
    assert client.post('/logout').status_code == 302


def test_disabled_user_session_is_rejected(client):
    _login_as(client, user_id=3)

    response = client.get('/profile', follow_redirects=False)

    assert response.status_code == 302
    assert response.headers['Location'].endswith('/login?next=%2Fprofile')


def test_account_migration_enables_only_dev(app):
    conn = sqlite3.connect(Config.DATABASE)
    rows = dict(conn.execute('SELECT username, enabled FROM users').fetchall())
    conn.close()

    assert rows['dev'] == 1
    assert all(enabled == 0 for username, enabled in rows.items() if username != 'dev')
