
const chatSocket = new WebSocket('ws://' + window.location.host + '/ws/chat/');

chatSocket.onmessage = function (e) {
    const data = JSON.parse(e.data);
    console.log(data.message);
    // Обработка полученного сообщения, если необходимо
};

chatSocket.onclose = function (e) {
    console.error('WebSocket closed unexpectedly');
};

// Пример отправки личного сообщения
function sendPrivateMessage(recipientId, content) {
    const data = {
        type: 'private.message',
        recipient_id: recipientId,
        content: content,
    };
    chatSocket.send(JSON.stringify(data));
}

// Пример отправки обычного чат-сообщения
function sendChatMessage(content) {
    const data = {
        type: 'chat.message',
        content: content,
    };
    chatSocket.send(JSON.stringify(data));
}
