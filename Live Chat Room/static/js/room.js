let socketio = io();

document.addEventListener("readystatechange", (event) => {
  if (event.target.readyState === "complete") {
    initApp();
  }
});

const initApp = () => {
  disableReloadWhenSubmit();
  addMessageToMessageBox();
};

const disableReloadWhenSubmit = () => {
  const entry = document.getElementById("entry");
  entry.addEventListener("submit", (event) => {
    event.preventDefault();
  });
};

const addMessageToMessageBox = () => {
  socketio.on("message", (data) => {
    createMessage(data.name, data.message, data.timestamp);
  });
};

const sendMessage = () => {
  const message = document.getElementById("message");
  if (message.value === "") return;
  socketio.emit("message", message.value);
  message.value = "";
};

const createMessage = (name, message, timestamp) => {
  const messages = document.getElementById("messages");
  const div = document.createElement("div");
  div.className = "text";

  const strong = document.createElement("strong");
  strong.textContent = name;

  const time = document.createElement("span");
  time.className = "muted";
  time.textContent = timestamp;

  const msg = document.createElement("span");
  msg.appendChild(strong);
  msg.appendChild(document.createTextNode(`: ${message}`));

  div.appendChild(msg);
  div.appendChild(time);
  messages.appendChild(div);
};
