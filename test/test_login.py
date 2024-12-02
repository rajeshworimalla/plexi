def test_user_login_success(client):
    """Test Case: Successful user login."""
    response = client.post('/login', data={
        'email': 'requester123@gmail.com',
        'password': 'password123'
    })
    assert response.status_code == 302  # Redirect to dashboard
