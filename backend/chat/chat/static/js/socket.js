import {getNewMessageHTML} from './messages.js';

const socket = new WebSocket(`ws://${window.location.hostname}/chat/ws/`);
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
