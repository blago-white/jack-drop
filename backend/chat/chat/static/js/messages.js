const messages = document.getElementById('messages');

async function fetchMessages() {
    const response = await fetch("http://127.0.0.1:8000/api/v1/messages/")
    const result = await response.json();

    result.forEach((message) => {
        messages.innerHTML += getNewMessageHTML(message.id, message.username, message.date, message.text);
    })
}

fetchMessages();

function getNewMessageHTML(message_id, username, date, text) {
    return `
        <li id="${message_id}">
            ${username} | ${date}
            <p class='message-text'>${text}</p>
            <button onclick="console.log('Delete:', ${message_id});"
                    class="btn btn-danger">
                Delete message
            </button>
        </li>
    `
}

export {getNewMessageHTML};
