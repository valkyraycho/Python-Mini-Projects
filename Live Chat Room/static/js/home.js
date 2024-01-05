let socketio = io();

document.addEventListener("readystatechange", (event) => {
  if (event.target.readyState === "complete") {
    initApp();
  }
});

const initApp = () => {
  checkInput();
};

const checkInput = () => {
  const name = document.getElementById("name");
  const room = document.getElementById("room");
  const join = document.getElementById("join");
  const create = document.getElementById("create");

  create.addEventListener("click", (event) => {
    if (!name.value) {
      event.preventDefault();
      alert("Please enter a name.");
    } else form.submit();
  });

  join.addEventListener("click", (event) => {
    event.preventDefault();

    if (!name.value) alert("Please enter a name.");
    else if (room.value === "") alert("Please enter a room code.");
    else {
      socketio.emit("checkRoom", room.value, (roomExist) => {
        if (!roomExist) alert("Room does not exist");
        else form.submit();
      });
    }
  });
};
/* 
  const clearInput = () => {
    document.getElementById("name").value = "";
    document.getElementById("room").value = "";
  }; */
