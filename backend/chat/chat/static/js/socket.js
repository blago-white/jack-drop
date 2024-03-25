const socket = new WebSocket(`ws://127.0.0.1:8000/ws/chat/`);
const messages = document.getElementById('messages');

socket.onmessage = function(event) {
    message = JSON.parse(event.data);

    console.log(message);

    addMessage(message_id=message.message_id,
               username=message.username,
               text=message.text,
               date=message.date)
};

function sendMessage(event, username) {
    socket.send(JSON.stringify({
        username: username,
        text: getMessageText()
    }));
    return false;
}

function getMessageText() {
    return document.getElementById('inputMessage').value;
}

function deleteMessage(message_id) {
    socket.send(JSON.stringify({
        type: 'delete',
        payload: {
            message_id: message_id,
        }
    }));
}

function addMessage(message_id, username, date, text) {
    messageHTML = getNewMessageHTML(
        message_id=message_id,
        username=username,
        date=date,
        text=message,
    );
    messages.innerHTML += messageHTML;
}

function getNewMessageHTML(message_id, username, date, text) {
    return `
        <li id="${message_id}">
            ${username} | ${date}
            <p class='message-text'>${message.text}</p>
        </li>
    `
}
