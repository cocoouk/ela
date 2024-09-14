function sendMessage() {
    var userInput = document.getElementById('user-input');
    var message = userInput.value;
    userInput.value = '';

    fetch('/chat', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: 'message=' + encodeURIComponent(message)
    })
    .then(response => response.json())
    .then(data => {
        var chatMessages = document.getElementById('chat-messages');
        chatMessages.innerHTML += '<p><strong>You:</strong> ' + message + '</p>';
        chatMessages.innerHTML += '<p><strong>AI:</strong> ' + data.response + '</p>';
    });
}
