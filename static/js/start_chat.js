document.getElementById('start-chat-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const recipientId = document.getElementById('recipient-id').value;

    const response = await fetch('/start_chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ recipient_id: recipientId })
    });

    const result = await response.json();
    if (response.ok) {
      alert(result.message);
      // Redirect to the chat window or update the chat list
      window.location.href = `/chat/${result.chat_id}`;
    } else {
      alert(result.error || 'Failed to start chat.');
    }
  });
  // async function updateChatList() {
  //   const response = await fetch('/chats');
  //   const chatList = await response.json();
  //   // Update the UI with the new chat list
  // }
  