from flask import Flask, send_from_directory, render_template
from flask_sockets import Sockets
import json

app = Flask(__name__)
sockets = Sockets(app)

all_sockets = []
all_chat = []

@sockets.route('/socket')
def dodo(sock):
    all_sockets.append(sock)
    while not sock.closed:
        message = sock.receive()
        message = json.loads(message)
        print(message)
        all_chat.append(message)
        for ws in all_sockets:
            ws.send(json.dumps(all_chat))


@app.route('/')
def cse116():
    return render_template('CSE312.html')


@app.route('/static_files/<path:filename>')
def send_style(filename):
    return send_from_directory('static_files', filename)


if __name__ == '__main__':
    from gevent import pywsgi
    from geventwebsocket.handler import WebSocketHandler
    server = pywsgi.WSGIServer(('', 8312), app, handler_class=WebSocketHandler)
    server.serve_forever()
