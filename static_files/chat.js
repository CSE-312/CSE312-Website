let socket = undefined;
const username = generateRandomId();


function setupSocket() {
    socket = new WebSocket('wss://' + window.location.host + '/socket');
    socket.addEventListener('message', renderMessages);
}

function sendMessage() {
    const chatBox = document.getElementById("chatInput");
    console.log(chatBox.value);
    const message = chatBox.value;
    if(socket.readyState !== 1){
        setupSocket();
    }
    socket.send(JSON.stringify({'username': username, 'message': message}))
}


function renderMessages(message) {
    console.log(message.data);
    document.getElementById('chat').innerHTML = "<p>" + message.data + "</p>"
}

function generateRandomId() {
    return "anon" + Math.random().toString()
}