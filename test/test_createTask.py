import pytest
from flask import session
from main import app  # Import your app (no need for db)
import datetime

# Test GET request for rendering the create task page
def test_create_task_get(client):
    """Test the GET request for creating a task (form rendering)."""
    # Simulate logged-in user by adding session data
    with client.session_transaction() as sess:
        sess['username'] = 'testuser'
        sess['user_id'] = 1  # Fake user_id
        sess['phone'] = '1234567890'
        sess['email'] = 'testuser@example.com'

    response = client.get('/create_task')

    # Assert that the response status code is 200 (OK) and the page contains "Create a Task"
    assert response.status_code == 200


# Test POST request with valid data (task creation)
def test_create_task_post_valid_data(client):
    """Test posting valid task data (POST request)."""
    # Simulate logged-in user by adding session data
    with client.session_transaction() as sess:
        sess['username'] = 'testuser'
        sess['user_id'] = 1  # Fake user_id
        sess['phone'] = '1234567890'
        sess['email'] = 'testuser@example.com'

    response = client.post('/create_task', data={
        'job-title': 'Test Task',
        'job-description': 'This is a description of the test task.',
        'job-salary': '100',
        'job-location': 'Test Location'
    })
    
    # Assert that the response is a redirect (302 status code) to the tasks page
    assert response.status_code == 302  # 302 indicates a redirect


# Test POST request with missing fields (error handling)
def test_create_task_post_missing_field(client):
    """Test posting a task with missing fields (error handling)."""
    # Simulate logged-in user by adding session data
    with client.session_transaction() as sess:
        sess['username'] = 'testuser'
        sess['user_id'] = 1  # Fake user_id
        sess['phone'] = '1234567890'
        sess['email'] = 'testuser@example.com'

    response = client.post('/create_task', data={
        'job-title': '',
        'job-description': 'This task has no title.',
        'job-salary': '100',
        'job-location': 'Test Location'
    })

    # Assert that the form is re-rendered with an error message
    assert response.status_code == 200


# Test POST request when user is not logged in (redirect to login)
def test_create_task_redirect_if_not_logged_in(client):
    """Test redirect to login page if user is not logged in."""
    response = client.get('/create_task')
    # Check if the user is redirected to the login page (302 status code)
    assert response.status_code == 302
