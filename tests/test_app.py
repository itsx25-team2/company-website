import sqlite3

import pytest
from company_website import create_app
from company_website import auth
from company_website.models import User
from company_website.routes import _contains_unsupported_email_syntax, _render_email_preview


@pytest.fixture
def app():
    app = create_app()
    app.config['TESTING'] = True
    return app


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
        (1, 'dev', 'known-password'),
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
