from flask import Flask, send_from_directory, render_template, request, make_response
from flask_socketio import SocketIO, emit
import json
import html

# from pymongo import MongoClient

app = Flask(__name__)
socket_server = SocketIO(app)

# mongo_client = MongoClient()
# db = mongo_client["cse312x"]
#
# chat_collection = db["chat"]

chat_history = []

@app.route('/send-message', methods=["POST"])
def message():
    clean_message = html.escape(request.data.decode())
    print(clean_message)
    if clean_message != "":
        chat_history.append(clean_message)
        # chat_collection.insert_one({'message': clean_message})
    return "message received"


@app.route('/get-messages')
def messages():
    # all_chat = chat_collection.find({}, {'_id': 0})
    return json.dumps(chat_history)


@socket_server.on('connect')
def connect():
    print(request.sid + " connected")
    # all_chat = chat_collection.find({}, {'_id': 0})
    # emit('message', json.dumps(list(all_chat)))


@socket_server.on('disconnect')
def disconnect():
    print(request.sid + " disconnected")


@socket_server.on('message')
def message(the_message):
    parsed_message = json.loads(the_message)
    # chat_collection.insert_one(
    #     {'username': html.escape(parsed_message['username']), 'message': html.escape(parsed_message['message'])})
    # all_chat = chat_collection.find({}, {'_id': 0})
    # socket_server.emit('message', json.dumps(list(all_chat)), broadcast=True)


@app.route('/')
def cse312():
    print("serving request")
    resp = make_response(render_template('CSE312.html'))
    resp.headers["X-Content-Type-Options"] = "nosniff"
    return resp

@app.route('/chat')
def chat():
    print("serving request")
    resp = make_response(render_template('chat.html'))
    resp.headers["X-Content-Type-Options"] = "nosniff"
    return resp


@app.route('/static_files/<path:filename>')
def serve_static(filename):
    resp = make_response(send_from_directory('static_files', filename))
    resp.headers["X-Content-Type-Options"] = "nosniff"
    return resp


# @app.after_request
# def after(resp):
#     resp.headers['Access-Control-Allow-Origin'] = "*"
#     return resp

if __name__ == '__main__':
    socket_server.run(app, host="0.0.0.0", port=5000)
    # from gevent import pywsgi
    # from geventwebsocket.handler import WebSocketHandler
    # server = pywsgi.WSGIServer(('', 8312), app, handler_class=WebSocketHandler)
    # server.serve_forever()
