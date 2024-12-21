from flask import Flask, render_template
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('index.html')

users = {}

@socketio.on('connect')
def handle_connect():
    print('A user connected.')

@socketio.on('set username')
def set_username(username):
    users[request.sid] = username
    print(f"User {username} connected.")

@socketio.on('chat message')
def handle_message(message):
    username = users.get(request.sid, "Anonymous")
    emit('chat message', {'user': username, 'text': message}, broadcast=True)

@socketio.on('disconnect')
def handle_disconnect():
    username = users.pop(request.sid, "Anonymous")
    print(f"User {username} disconnected.")

if __name__ == '__main__':
    socketio.run(app, debug=True)
