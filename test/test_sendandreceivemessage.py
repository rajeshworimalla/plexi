from config import get_user_by_email

def test_send_message(client):
    """Test Case: Send a Message"""

    # Step 1: Create a sender user (if not already present)
    sender_signup_response = client.post('/signup', data={
        'first-name': 'Sender',
        'last-name': 'User',
        'email': 'sender@example.com',
        'password': 'securepassword',
        'confirm-password': 'securepassword',
        'role': 'tasker',
        'main_job': 'Test Messaging',
        'bio': 'Test bio',
        'age': '30',
        'location': 'Test City',
        'phone-number': '1234567890'
    })
    assert sender_signup_response.status_code in (200, 302)  # Ensure signup was successful

    # Create a recipient user (if not already present)
    recipient_signup_response = client.post('/signup', data={
        'first-name': 'Recipient',
        'last-name': 'User',
        'email': 'recipient@example.com',
        'password': 'securepassword',
        'confirm-password': 'securepassword',
        'role': 'tasker',
        'main_job': 'Test Messaging',
        'bio': 'Test bio',
        'age': '30',
        'location': 'Test City',
        'phone-number': '1234567890'
    })
    assert recipient_signup_response.status_code in (200, 302)  # Ensure signup was successful

    # Step 2: Check if the recipient exists in the database
    recipient_user = get_user_by_email('recipient@example.com')
    assert recipient_user is not None  # Ensure recipient exists in DB

    # Step 3: Log in as the sender user
    login_response = client.post('/login', data={
        'email': 'sender@example.com',
        'password': 'securepassword'
    })
    assert login_response.status_code == 302  # Ensure successful login and redirect

    # Step 4: Simulate sending a message (starting a chat)
    chat_response = client.post('/start_chat', data={
        'tosearch': 'recipient@example.com'  # Replace with a valid recipient email
    })

