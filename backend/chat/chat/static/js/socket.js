import {getNewMessageHTML} from './messages.js';

const socket = new WebSocket(`ws://127.0.0.1:8000/ws/chat/`);
const messages = document.getElementById('messages');

socket.onmessage = function(event) {
    const message = JSON.parse(event.data);

    console.log(message);

    addMessage(message.id,
               message.username,
               message.date,
               message.text)
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
    const messageHTML = getNewMessageHTML(
        message_id=message_id,
        username=username,
        date=date,
        text=text,
    );
    messages.innerHTML += messageHTML;
}

window.sendMessage = sendMessage;
