const openButton = document.getElementById('open-chat-btn');
const closeButton = document.getElementById('close-chat-btn');
const adminChatWindow = document.getElementById('admin-chat');

function openChat(button) {
    adminChatWindow.style.display = "flex";
    openButton.style.display = "none";
}

function closeChat(button) {
    adminChatWindow.style.display = "none";
    openButton.style.display = "flex";
}

openButton.addEventListener("click", openChat);
closeButton.addEventListener("click", closeChat);
