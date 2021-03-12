getMessages();
setInterval(getMessages, 1000);

function sendMessage() {
    const chatBox = document.getElementById("chatInput");
    const message = chatBox.value;
    chatBox.value = "";
    if (message !== "") {
        const request = new XMLHttpRequest();
        request.onreadystatechange = function () {
            if (this.readyState === 4 && this.status === 200) {
                console.log(this.response);
            }
        };
        request.open("POST", "send-message");
        request.send(message)
    }
    chatBox.focus();
}

function getMessages() {

    const request = new XMLHttpRequest();
    request.onreadystatechange = function () {
        if (this.readyState === 4 && this.status === 200) {
            renderMessages(this.response);
        }
    };
    request.open("GET", "get-messages");
    request.send()
}

function renderMessages(rawMessage) {
    let chat = document.getElementById('chat');

    chat.innerHTML = "";
    const history = JSON.parse(rawMessage);
    for (const message of history) {
        chat.innerHTML += message + "<br/>";
    }

}
