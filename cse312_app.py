from flask import Flask, send_from_directory, render_template, request
from flask_socketio import SocketIO
import json
import html

app = Flask(__name__)
socket_server = SocketIO(app)

# all_sockets = []
all_chat = []


@socket_server.on('connect')
def connect():
    # all_sockets.append(request.sid)
    print(request.sid + " connected")


@socket_server.on('disconnect')
def disconnect():
    # if request.sid in all_sockets:
    #     all_sockets.remove(request.sid)
    print(request.sid + " disconnected")


@socket_server.on('message')
def message(the_message):
    parsed_message = json.loads(the_message)
    all_chat.append({'username':parsed_message['username'], 'message':html.escape(parsed_message['message'])})

    socket_server.emit('message', json.dumps(all_chat), broadcast=True)


@app.route('/')
def cse116():
    return render_template('CSE312.html')


@app.route('/static_files/<path:filename>')
def send_style(filename):
    return send_from_directory('static_files', filename)


if __name__ == '__main__':
    socket_server.run(app, port=8312)
    # from gevent import pywsgi
    # from geventwebsocket.handler import WebSocketHandler
    # server = pywsgi.WSGIServer(('', 8312), app, handler_class=WebSocketHandler)
    # server.serve_forever()
