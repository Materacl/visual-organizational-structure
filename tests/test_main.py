def test_home_page(client):
    """Test home page."""
    response = client.get('/')
    print(response.data.decode('utf-8'))  # Print the actual response data for debugging
    assert response.status_code == 200
    assert "Главная страница" in response.data.decode('utf-8')
    assert "Register" in response.data.decode('utf-8')
    assert "Login" in response.data.decode('utf-8')
    assert "Настройки" in response.data.decode('utf-8')
    assert "Поддержка" in response.data.decode('utf-8')


def test_home_page_authenticated(client, db):
    """Test home page for authenticated users."""
    # Create a mock user and login
    from visual_organizational_structure.models import User
    user = User(email="test@example.com", password="password")
    db.session.add(user)
    db.session.commit()

    # Log in the user
    with client.session_transaction() as sess:
        sess['user_id'] = user.id

    response = client.get('/')
    print(response.data.decode('utf-8'))  # Print the actual response data for debugging
    assert response.status_code == 200
    assert "Создать доску" in response.data.decode('utf-8')
