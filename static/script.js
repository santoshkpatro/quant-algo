console.log('Hello')
const chatSocket = new WebSocket(
    'ws://'
    + window.location.host
    + '/ws/feed'
);

chatSocket.onmessage = function(e) {
    console.log(e.data)
    // const data = JSON.parse(e.data);
    // document.querySelector('#chat-log').value += (data.message + '\n');
};

chatSocket.onclose = function(e) {
    console.error('Chat socket closed unexpectedly');
};