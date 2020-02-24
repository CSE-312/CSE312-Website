from flask import Flask, send_from_directory, render_template, request
from flask_socketio import SocketIO, emit
import json
import html

from pymongo import MongoClient

app = Flask(__name__)
socket_server = SocketIO(app)

# mongo_client = MongoClient()
# db = mongo_client["cse312"]
#
# chat_collection = db["chat"]


@socket_server.on('connect')
def connect():
    print(request.sid + " connected")
    # all_chat = chat_collection.find({}, {'_id': 0})
    # emit('message', json.dumps(list(all_chat)))


@socket_server.on('disconnect')
def disconnect():
    print(request.sid + " disconnected")
import html

@socket_server.on('message')
def message(the_message):
    parsed_message = json.loads(the_message)
    # chat_collection.insert_one(
    #     {'username': parsed_message['username'], 'message': html.escape(parsed_message['message'])})
    # all_chat = chat_collection.find({}, {'_id': 0})
    # socket_server.emit('message', json.dumps(list(all_chat)), broadcast=True)


@app.route('/')
def cse312():
    print("serving request")
    return render_template('CSE312.html')


@app.route('/static_files/<path:filename>')
def serve_static(filename):
    return send_from_directory('static_files', filename)


if __name__ == '__main__':
    socket_server.run(app, port=8312)
    # from gevent import pywsgi
    # from geventwebsocket.handler import WebSocketHandler
    # server = pywsgi.WSGIServer(('', 8312), app, handler_class=WebSocketHandler)
    # server.serve_forever()
