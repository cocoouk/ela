// Function to send a message to the chat
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

// Wait for the document to be fully loaded before running the link handler
document.addEventListener('DOMContentLoaded', () => {
    // Select all elements with the class 'gdrive-link'
    const gdriveLinks = document.querySelectorAll('.gdrive-link');
    
    gdriveLinks.forEach(link => {
        // Attach an event listener to each Google Drive link
        link.addEventListener('click', function(event) {
            event.preventDefault();  // Prevent the default action (opening the link)
            const linkUrl = this.href;  // Capture the link's URL
            var chatMessages = document.getElementById('chat-messages');
            chatMessages.innerHTML += '<p><strong>Link:</strong> <a href="' + linkUrl + '" target="_blank">' + linkUrl + '</a></p>';
        });
    });
});
