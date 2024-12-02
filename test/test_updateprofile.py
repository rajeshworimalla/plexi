def test_user_profile_update(client):
    """Test Case: Create a new user, update profile, and password."""

    # Step 1: Sign up as a new user
    signup_response = client.post('/signup', data={
        'first-name': 'Test',
        'last-name': 'User',
        'password': 'testpassword123',
        'confirm-password': 'testpassword123',
        'email': 'testuser@example.com',
        'role': 'requester',
        'main_job': 'Tester',
        'bio': 'Testing user profile update',
        'age': '25',
        'location': 'Test City',
        'phone-number': '1234567890'
    })
    assert signup_response.status_code in (200, 302)  # Ensure signup is successful

    # Step 2: Log in with the newly created user
    login_response = client.post('/login', data={
        'email': 'testuser@example.com',
        'password': 'testpassword123'
    })
    assert login_response.status_code == 302  # Ensure successful login and redirect

    # Step 3: Update username and bio
    update_response = client.post('/settings-profile', data={
        'username': 'updated_username',
        'bio': 'Updated bio for test.',
        'job-title': 'Updated Main Job'
    })
    assert update_response.status_code == 200  # Stay on the same page after the update

    # Step 4: Update password
    password_update_response = client.post('/settings_password', data={
        'current-pass': 'testpassword123',
        'new-pass': 'updatedpassword456',
        'confirm-pass': 'updatedpassword456'
    })

    # Step 5: Verify the password update
    # Check for successful redirect after password update (302 redirect)
    assert password_update_response.status_code == 302  # Expecting a redirect after password update
    assert '/settings_password' in password_update_response.location  # Check if redirected to settings_password

    # Step 6: Verify the password update by logging in again
    relogin_response = client.post('/login', data={
        'email': 'testuser@example.com',
        'password': 'updatedpassword456'
    })
    assert relogin_response.status_code == 302  # Check for successful login with the new password
    assert 'dashboard' in relogin_response.location  # Check if redirected to the dashboard

    # Step 7: Delete the test user (cleanup step)
    delete_user_response = client.post('/delete_user', data={
        'email': 'testuser@example.com'
    })
