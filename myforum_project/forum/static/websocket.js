
const chatSocket = new WebSocket('ws://' + window.location.host + '/ws/chat/');

chatSocket.onmessage = function (e) {
    const data = JSON.parse(e.data);
    console.log(data.message);
    // Обработка полученного сообщения
};

chatSocket.onclose = function (e) {
    console.error('WebSocket closed unexpectedly');
};