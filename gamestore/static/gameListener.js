(function () {
    window.addEventListener("message", receiveMessage, false);

    function responseHandler(data, responseText, jqXHR) {
        console.log("Got: " + jqXHR.status);
        if(jqXHR.status === 204){
            return;
        }else{
            var messageType = data.messageType;
            if (messageType) {
                if (messageType === "ERROR") {
                    $("#gameFrame")[0].contentWindow.postMessage(data, "*");
                } else if (messageType === "LOAD") {
                    $("#gameFrame")[0].contentWindow.postMessage(data, "*");
                } else {
                    console.log("Received unknown messageType");
                }
            } else {
                console.log(data);
            }
        }
    }

    function sendMessage(message) {
        $.ajax({
            type: "POST",
            url: "./message/",
            data: JSON.stringify(message),
            headers: {
                "X-CSRFToken": csrf_token
            },
            success: responseHandler
        });
    }

    var gameMessageHandlers = {
        SETTING: function (message) {
            // Adjust iframe according to settings
            var maxWidth = $("#gamePanel").width()-30;
            $("#gameFrame").height(Math.min(message.options.height, maxWidth));
            $("#gameFrame").width(Math.min(message.options.width, maxWidth));
        },
        SAVE: sendMessage,
        LOAD_REQUEST: sendMessage,
        SCORE: sendMessage
    }

    function receiveMessage(event) {
        console.log(event);
        var message = event.data;
        var handler = gameMessageHandlers[message.messageType];
        if (handler) {
            handler(message);
        } else {
            console.log()
        }
    }
})();