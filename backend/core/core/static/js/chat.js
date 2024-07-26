const openButton = document.getElementById('open-chat-btn');
const closeButton = document.getElementById('close-chat-btn');
const adminChatWindow = document.getElementById('admin-chat');

function openChat() {
    adminChatWindow.style.display = "flex";
    openButton.style.display = "none";
}

function closeChat() {
    adminChatWindow.style.display = "none";
    openButton.style.display = "flex";
}

async function renderMessages() {
    const messageValue = document.getElementById("message-text");

    const headers = new Headers();

    const response = await sendRequest(`http://${location.hostname}/chat/api/v1/messages/`, {method: "GET"});

    if (!response.ok) {return}

    const messages = await response.json();

    messages.forEach((message) => {
        const extra = message.from_admin ? "" : "self";

        document.getElementById('chat-messages').innerHTML += `
            <article class="chat-message ${extra}">
                <span class="chat-msg-body">${message.text}</span>
            </article>
        `;
    })
}

async function sendChatMessage() {
    const messageValue = document.getElementById("message-text");

    const headers = new Headers();

    headers.append("Content-Type", "application/json");

    const response = await sendRequest(`http://${location.hostname}/chat/api/v1/messages/create/`, {
        method: "POST",
        headers: headers,
        body: JSON.stringify({
            "text": messageValue.value
        })
    });

    if (!response.ok) {
        document.getElementById('controls').style.borderTop = '2px solid indianred';
        messageValue.style.color = "2px solid indianred";

        setTimeout(() => {messageValue.style = ''}, 2000);
    } else {
        document.getElementById('chat-messages').innerHTML += `
            <article class="chat-message self">
                <span class="chat-msg-body">${messageValue.value}</span>
            </article>
        `;

        messageValue.value = "";
    }
}


renderMessages();

openButton.addEventListener("click", openChat);
closeButton.addEventListener("click", closeChat);
