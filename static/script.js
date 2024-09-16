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
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        var chatMessages = document.getElementById('chat-messages');
        chatMessages.innerHTML += '<p><strong>You:</strong> ' + message + '</p>';
        chatMessages.innerHTML += '<p><strong>AI:</strong> ' + data.response + '</p>';
    })
    .catch(error => {
        var chatMessages = document.getElementById('chat-messages');
        chatMessages.innerHTML += '<p><strong>Error:</strong> Could not send message. ' + error.message + '</p>';
    });
}

// Capture GDrive Links Click Event
document.addEventListener('DOMContentLoaded', () => {
    const gdriveLinks = document.querySelectorAll('.gdrive-link');
    gdriveLinks.forEach(link => {
        link.addEventListener('click', function(event) {
            event.preventDefault();
            const linkUrl = this.href;
            var chatMessages = document.getElementById('chat-messages');
            chatMessages.innerHTML += '<p><strong>Link:</strong> ' + linkUrl + '</p>';
        });
    });
});

