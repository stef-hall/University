function myEventHandler(eventData) {
    let input = document.querySelector("#message-text");
    let message = input.value;
    let div = document.createElement('div');
    let p = document.createElement('p');
    
    div.append(p);
    p.textContent = message;
    div.setAttribute("class", "message-self");
    
    const ts = new Date();
    let times = document.createElement('p');
    times.textContent= ts.toTimeString().split(" ")[0]
    times.setAttribute("class", "timestamp");
    div.append(times);


    let mainChat = document.querySelector("#chat-log-container");
    mainChat.append(div);

    messageReciever()
}

function messageReciever() {
    let messages = [];
    messages[0] = "Hello World";
    messages[1] = "How's life?";
    messages[2] = "Caught any good fish lately?";

    let idx = Math.floor(messages.length * Math.random());
    let message = messages[idx];
    let div = document.createElement('div');
    let p = document.createElement('p');
    
    div.append(p);
    p.textContent = message;
    div.setAttribute("class", "message-other");
    
    const ts = new Date();
    let times = document.createElement('p');
    times.textContent= ts.toTimeString().split(" ")[0]
    times.setAttribute("class", "timestamp");
    div.append(times);


    let mainChat = document.querySelector("#chat-log-container");
    mainChat.append(div); 
}

let btnRef = document.querySelector("#message-button");
btnRef.addEventListener('click', myEventHandler);

