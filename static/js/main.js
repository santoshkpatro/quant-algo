const chatSocket = new WebSocket("ws://" + window.location.host + "/ws/feed/");

chatSocket.onmessage = function(e) {
    const data = JSON.parse(e.data);

    console.log(data)
    document.querySelector('#feed').value = data.val;
};

chatSocket.onclose = function(e) {
    console.error('Chat socket closed unexpectedly');
};