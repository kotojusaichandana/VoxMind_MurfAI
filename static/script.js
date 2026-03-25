function addMessage(sender, text) {
    let chatBox = document.getElementById("chat-box");
    let msg = document.createElement("div");

    msg.className = sender === "You" ? "user" : "bot";
    msg.innerHTML = text;

    chatBox.appendChild(msg);
    chatBox.scrollTop = chatBox.scrollHeight;
}

function sendMessage() {
    let input = document.getElementById("user-input").value;
    let mode = document.getElementById("mode").value;
    let language = document.getElementById("language").value;

    if (!input) return;

    addMessage("You", input);
    document.getElementById("user-input").value = "";

    fetch("/chat", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({message: input, mode: mode, language: language})
    })
    .then(res => res.json())
    .then(data => {
        addMessage("Bot", data.reply);

        if (data.audio) {
            let audio = document.getElementById("audioPlayer");
            audio.src = data.audio;
            audio.play();
        }
    });
}

function startVoice() {
    let recognition = new webkitSpeechRecognition();
    recognition.lang = "en-US";

    recognition.onresult = function(event) {
        document.getElementById("user-input").value = event.results[0][0].transcript;
        sendMessage();
    };

    recognition.start();
}

function clearChat() {
    document.getElementById("chat-box").innerHTML = "";
}