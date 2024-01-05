from datetime import datetime
from flask import Flask, render_template, request, session, redirect, url_for
from flask_socketio import join_room, leave_room, send, SocketIO, emit
import random
from string import ascii_uppercase

ROOM_CODE_LENGTH = 4

app = Flask(__name__)
app.config['SECRET_KEY'] = 'fjiewojfewpwfjfjewoj'
socketio = SocketIO(app)

rooms = {}


def generate_room_code():
    while True:
        room = ''.join(random.choice(ascii_uppercase)
                       for _ in range(ROOM_CODE_LENGTH))
        if room not in rooms:
            return room


@app.route('/', methods=['POST', 'GET'])
def home():
    session.clear()
    if request.method == 'POST':
        name = request.form.get('name')
        room = request.form.get('room')
        create = request.form.get('create', False)

        if create != False:
            room = generate_room_code()
            rooms[room] = {'members': 0, 'messages': []}

        session['name'] = name
        session['room'] = room

        return redirect(url_for('room'))

    return render_template('home.html')


@app.route('/room')
def room():
    room = session.get('room')
    name = session.get('name')
    if not room or not name or room not in rooms:
        return redirect(url_for('home'))
    print(rooms[room]['messages'])

    return render_template('room.html', room=room, messages=rooms[room]['messages'], name=name)


@socketio.on('checkRoom')
def checkRoom(room):
    return room in rooms


# socketio.on: `on`  registers event handlers for Socket.IO events
@socketio.on('message')
def message(msg):
    room = session.get('room')
    if room not in rooms:
        return

    content = {
        'name': session.get('name'),
        'message': msg,
        'timestamp': datetime.now().strftime("%H:%M")
    }

    send(content, to=room)
    rooms[room]['messages'].append(content)


@socketio.on('connect')
def connect(auth):
    room = session.get('room')
    name = session.get('name')
    if not room or not name:
        return

    if room not in rooms:
        return

    join_room(room)
    content = {'name': name, 'message': 'has entered the room.',
               'timestamp': datetime.now().strftime("%H:%M")}
    send(content, to=room)
    rooms[room]['members'] += 1


@socketio.on('disconnect')
def disconnect():
    room = session.get('room')
    name = session.get('name')
    leave_room(room)

    if room in rooms:
        rooms[room]['members'] -= 1
        if rooms[room]['members'] <= 0:
            del rooms[room]

    content = {'name': name, 'message': 'has left the room.',
               'timestamp': datetime.now().strftime("%H:%M")}
    send(content, to=room)


if __name__ == '__main__':
    socketio.run(app, debug=True)
