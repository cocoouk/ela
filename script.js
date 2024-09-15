
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
