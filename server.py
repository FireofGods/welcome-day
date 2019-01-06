import flask
import flask_socketio as socketiolib

app = flask.Flask(__name__)
socketio = socketiolib.SocketIO(app)

message_log = []

def store_message(message):
    """
    stores the message in a message backlog. currently is a list but in th future will switch to a database
    message is a json with the following keys: username, date, message. all of the values are strings
    """
    message_log.append(message)

@socketio.on("login")
def login(login_data):
    login_text = "{} has connected!".format(login_data['username'])
    print(login_text)
    for message_json in message_log:
        socketiolib.emit("show_message", message_json)
    socketiolib.emit("show_message", {"username": "system", "text": login_text, "date": "nope"}, broadcast=True)
    store_message({"username": "system", "text": login_text, "date": "nope"})

@socketio.on("message")
def message(message):
    store_message(message)
    socketio.emit("show_message", message, broadcast=True)


socketio.run(app)
