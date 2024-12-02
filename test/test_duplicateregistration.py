def test_user_registration_existing_email(client):
    """Test Case: Attempt to register with an existing email."""
    response = client.post('/signup', data={
        'first-name': 'John',
        'last-name': 'Doe',
        'password': 'securepassword',
        'confirm-password': 'securepassword',
        'email': 'jahndoe@example.com',  # Existing email
        'role': 'requester',
        'main_job': 'janitor',
        'bio': 'Existing user',
        'age': 30,
        'location': 'NY',
        'phone-number': '9876543210'
    })
    assert b"User already exists" in response.data