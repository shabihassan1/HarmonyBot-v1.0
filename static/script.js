async function sendMessage() {
    const userInput = document.getElementById('user-input').value;
    if (!userInput) return;

    const chatBox = document.getElementById('chat-box');

    // Display user's message
    const userMessage = document.createElement('div');
    userMessage.classList.add('message', 'user');
    userMessage.textContent = userInput;
    chatBox.appendChild(userMessage);

    // Clear the input field
    document.getElementById('user-input').value = '';

    // Send the message to the server
    const response = await fetch('/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: userInput })
    });

    const data = await response.json();

    // Create a new div for the bot's response
    const botMessage = document.createElement('div');
    botMessage.classList.add('message', 'bot');
    botMessage.innerHTML = data.response; // Use innerHTML to render Markdown

    chatBox.appendChild(botMessage);

    // Scroll to the bottom of the chat box
    chatBox.scrollTop = chatBox.scrollHeight;
}

function handleKeyPress(event) {
    if (event.key === 'Enter') {
        sendMessage();
    }
}

async function exitChat() {
    await fetch('/shutdown', { method: 'POST' });
}

function newChat() {
    const chatBox = document.getElementById('chat-box');
    chatBox.innerHTML = '<div class="message bot">Hi, Welcome to the Medical Bot. What is your query?</div>';
}
