def test_search_tasks_by_budget(client):
    """Test Case 3.2: Search Tasks by Max Budget"""

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

    # Step 3: Define the max budget
    max_budget = 100

    # Step 4: Perform the search by max budget
    search_response = client.post('/filter_jobs', data={  # Update the URL to match your defined route
        'budget': max_budget,  # Send budget as a form parameter
        'location': 'Test Location'  # Optional: Add location if needed
    })

    # Assert the response status code
    assert search_response.status_code == 200  # Ensure the search was successful

    # Step 5: Delete the test user after the test
    delete_user_response = client.post('/delete_user', data={
        'email': 'testuser@example.com'
    })
    assert delete_user_response.status_code == 200  # Ensure user deletion was successful
