document.addEventListener("DOMContentLoaded", function() {
    const chatForm = document.getElementById('chat-form');
    const userInput = document.getElementById('user-input');
    const chatBox = document.getElementById('chat-box');
    
    // Add initial greeting message
    displayBotMessage("Hello! I am Dr. Chat, your mental wellness companion. How can I help you today?");
    
    chatForm.addEventListener('submit', function(e) {
        e.preventDefault();
        sendMessage();
    });

    // Function to display bot messages
    function displayBotMessage(message) {
        const botMessageDiv = document.createElement('div');
        botMessageDiv.className = 'bot-message';
        botMessageDiv.textContent = message;
        chatBox.appendChild(botMessageDiv);
        chatBox.scrollTop = chatBox.scrollHeight;
    }
    
    function sendMessage() {
        let input = document.getElementById("user-input").value;
        let chatBox = document.getElementById("chat-box");

        if (input.trim() === "") return;

        // Show user message
        const userMessageDiv = document.createElement('div');
        userMessageDiv.className = 'user-message';
        userMessageDiv.textContent = input;
        chatBox.appendChild(userMessageDiv);

        // Clear input and scroll to bottom
        document.getElementById("user-input").value = "";
        chatBox.scrollTop = chatBox.scrollHeight;

        // Send to Flask backend
        fetch("/api/chat", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ message: input })
        })
        .then(res => res.json())
        .then(data => {
            // Display bot message using the helper function
            displayBotMessage(data.response);
        })
        .catch(error => {
            console.error('Error:', error);
            displayBotMessage('Sorry, something went wrong. Please try again later.');
        });
    }
});
