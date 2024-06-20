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

function sendChatMessage() {
    const messageValue = document.getElementById("message-text");
    messageValue.value = "";
}

openButton.addEventListener("click", openChat);
closeButton.addEventListener("click", closeChat);
