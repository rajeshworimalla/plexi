def test_user_login_invalid(client):
    """Test Case: Attempt login with invalid credentials."""
    response = client.post('/login', data={
        'email': 'invaliduser@example.com',
        'password': 'wrongpassword'
    })
    assert b"Invalid username or password" in response.data