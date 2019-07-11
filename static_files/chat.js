console.log("starting page JS");

let socket = undefined;
const username = generateRandomId();


function setupSocket() {
    socket = new WebSocket('wss://' + window.location.host + '/socket');
    socket.addEventListener('message', renderMessages);
}

function sendMessage() {
    const chatBox = document.getElementById("chatInput");
    const message = chatBox.value;
    chatBox.value = "";
    // if (socket.readyState !== 1) {
    //     setupSocket();
    // }

    socket.send(JSON.stringify({'username': username, 'message': message}))
}


function renderMessages(rawMessage) {
    let chat = document.getElementById('chat');
    chat.innerHTML = "";
    const history = JSON.parse(rawMessage.data);
    for (const message of history) {
        chat.innerHTML += message['username'] + ": " + message["message"] + "<br/>";
    }
}

function generateRandomId() {
    return "anon_" + Math.random().toString()
}

console.log("ending page JS");