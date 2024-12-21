from flask import Flask, render_template, request  # Import 'request'
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
socketio = SocketIO(app)

# Store usernames for connected clients
users = {}

@app.route('/')
def index():
    return render_template('index.html')

# Handle a new connection
@socketio.on('connect')
def handle_connect():
    print('A user connected.')

# Handle setting username
@socketio.on('set username')
def set_username(username):
    users[request.sid] = username  # Use 'request.sid' here
    print(f"User {username} connected.")

# Handle chat messages
@socketio.on('chat message')
def handle_message(message):
    username = users.get(request.sid, "Anonymous")  # Retrieve username by 'request.sid'
    emit('chat message', {'user': username, 'text': message}, broadcast=True)

# Handle disconnection
@socketio.on('disconnect')
def handle_disconnect():
    username = users.pop(request.sid, "Anonymous")  # Remove user from 'users'
    print(f"User {username} disconnected.")

if __name__ == '__main__':
    socketio.run(app, debug=True)
