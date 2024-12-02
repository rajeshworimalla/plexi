def test_login_missing_fields(client):
    """Test Case: Login with Missing Fields"""
    
    # Missing 'email' field
    response = client.post('/login', data={
        # 'email': 'johndoe@example.com',  # Email is missing
        'password': 'securepassword'
    })

    # Check response status for an error
    assert response.status_code == 400  # Expect 400 Bad Request
    assert b"Email and password are required." in response.data  # Adjust based on your app's error message

    # Missing 'password' field
    response = client.post('/login', data={
        'email': 'johndoe@example.com',
        # 'password': 'securepassword'  # Password is missing
    })

    # Check response status for an error
    assert response.status_code == 400  # Expect 400 Bad Request
    assert b"Email and password are required." in response.data
