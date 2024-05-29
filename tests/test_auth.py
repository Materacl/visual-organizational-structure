from visual_organizational_structure.models import User
from flask import url_for
from unittest.mock import patch


def test_register(client, db, session):
    """Test user registration."""
    response = client.post(url_for('auth.register'), data={
        'email': 'newuser@example.com',
        'password': 'password',
        'confirm': 'password'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b'Login' in response.data
    user = User.query.filter_by(email='newuser@example.com').first()
    assert user is not None


def test_login(client, db, session):
    """Test user login."""
    user = User(email='test@example.com', password='password')
    db.session.add(user)
    db.session.commit()

    response = client.post(url_for('auth.login'), data={
        'email': 'test@example.com',
        'password': 'password'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert 'Настройки' in response.data.decode('utf-8')
    assert 'Поддержка' in response.data.decode('utf-8')


def test_logout(client, db, session):
    """Test user logout."""
    user = User(email='test@example.com', password='password')
    db.session.add(user)
    db.session.commit()

    # Log in the user
    with client.session_transaction() as sess:
        sess['user_id'] = user.id

    response = client.get(url_for('auth.logout'), follow_redirects=True)
    assert response.status_code == 200
    assert 'Register' in response.data.decode('utf-8')
    assert 'Login' in response.data.decode('utf-8')


@patch('flask_mail.Mail.send')
def test_request_reset_password(mock_send, client, db, session):
    """Test requesting a password reset."""
    user = User(email='test@example.com', password='password')
    db.session.add(user)
    db.session.commit()

    response = client.post(url_for('auth.request_reset_password'), data={
        'email': 'test@example.com'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert 'На вашу почту было отправлено письмо с инструкциями' in response.data.decode('utf-8')
    mock_send.assert_called_once()


@patch('flask_mail.Mail.send')
def test_reset_password(mock_send, client, db, session):
    """Test resetting the password."""
    user = User(email='test@example.com', password='password')
    db.session.add(user)
    db.session.commit()

    token = user.get_reset_token()

    response = client.post(url_for('auth.reset_token', token=token), data={
        'password': 'newpassword',
        'confirm': 'newpassword'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert 'Ваш пароль был успешно изменен!' in response.data.decode('utf-8')

    user = User.query.filter_by(email='test@example.com').first()
    assert user is not None
    assert user.password != 'password'
    assert user.password == 'newpassword'
