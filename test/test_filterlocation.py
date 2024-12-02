def test_search_tasks_by_location(client):
    """Test Case: Search Tasks by Location"""

    # Step 1: Create a new user
    signup_response = client.post('/signup', data={
        'first-name': 'Test',
        'last-name': 'User',
        'email': 'testuser@example.com',
        'password': 'securepassword',
        'confirm-password': 'securepassword',
        'role': 'tasker',
        'main_job': 'Test Messaging',
        'bio': 'Test bio',
        'age': '30',
        'location': 'Test City',
        'phone-number': '1234567890'
    })
    assert signup_response.status_code in (200, 302)  # Ensure signup was successful

    # Step 2: Log in as the newly created user
    login_response = client.post('/login', data={
        'email': 'testuser@example.com',
        'password': 'securepassword'
    })
    assert login_response.status_code == 302  # Ensure successful login and redirect

    # Step 3: Define the location to search
    location = 'Test City'

    # Step 4: Perform the search by location
    search_response = client.post('/filter_jobs', data={
        'location': location,  # Send location as a form parameter
        'budget': ''  # Empty budget since we're only filtering by location
    })

    # Assert the response status code
    assert search_response.status_code == 200  # Ensure the search was successful

    # Step 5: Delete the test user after the test
    delete_user_response = client.post('/delete_user', data={
        'email': 'testuser@example.com'
    })
    assert delete_user_response.status_code == 200  # Ensure user deletion was successful
