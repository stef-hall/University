let g_url = "http://localhost:8085/api/messages";
let g_intervalID = setInterval(retrieveMessage, 1000);
let g_usernameDialog = null;
let g_username = null;

window.onload = function() {
	g_usernameDialog = document.getElementById('usernameDialog');
	g_usernameDialog.showModal();
}

function setUsername(event) {
	 event.preventDefault();
	 let usernameInput = document.getElementById('username');
	 g_username = usernameInput.value;
	 g_usernameDialog.close();
}

class Message {
	constructor(username, message, time) {
		this.username = username;
		this.message = message;
		this.time = time;
	}
}

function createMessage(message) {
    let div = document.createElement('div');

    let uname = document.createElement('p');
    uname.textContent= message.username
    uname.setAttribute("class", "username");
    div.append(uname);


    let p = document.createElement('p');
    div.append(p);
    p.textContent = message.message;
    if (message.username == g_username) {
        div.setAttribute("class", "message-self");
    } else {
        div.setAttribute("class", "message-other");
    }
    
    const ts = new Date(message.time);
    let times = document.createElement('p');
    times.textContent= ts.toTimeString().split(" ")[0]
    times.setAttribute("class", "timestamp");
    div.append(times);

    


    let mainChat = document.querySelector("#chat-log-container");
    mainChat.append(div); 

}

function clearChatLog() {
	 let chatLog = document.querySelector("#chat-log-container");
	 chatLog.replaceChildren();
}	

async function retrieveMessage() {
	try {
		let response = await axios.get(g_url);

		let messages = response.data;	

        clearChatLog()
        for(let message of messages) {
            createMessage(message);
        }

	} catch(error) {
        clearInterval(g_intervalID);
		console.log(error);
		alert("An error occured getting the messages.");
		clearInterval(g_intervalID);
	}

}

async function sendMessage(eventData) {
    eventData.preventDefault();
    let timestamp = new Date();
    const localISOString = timestamp.getFullYear() + '-' +
            String(timestamp.getMonth() + 1).padStart(2, '0') + '-' +
            String(timestamp.getDate()).padStart(2, '0') + 'T' +
            String(timestamp.getHours()).padStart(2, '0') + ':' +
            String(timestamp.getMinutes()).padStart(2, '0') + ':' +
            String(timestamp.getSeconds()).padStart(2, '0');
    let input = document.querySelector("#message-text");
    let messageObject = new Message(g_username, input.value, localISOString);
    input.value = "";

    try {
        await axios.post(g_url, messageObject);
    } catch(error) {
        console.error(error);
        alert("An error occured sending te message. " + error.message);
    }
}

