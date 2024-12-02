def test_user_registration(client):
    response = client.post('/signup', data={
        'first-name': 'John',
        'last-name': 'Doe',
        'password': 'securepassword',
        'confirm-password': 'securepassword',
        'email': 'johndoe@example.com',
        'role': 'tasker',
        'main_job': 'Software Developer',
        'bio': 'Test bio',
        'age': '25',
        'location': 'Kansas',
        'phone-number': '1234567890'
    })

    assert response.status_code in [200]  # Allow both OK and Redirect
