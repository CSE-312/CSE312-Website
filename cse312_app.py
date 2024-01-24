import json

from flask import Flask, send_from_directory, render_template, request, make_response
from flask_socketio import SocketIO, emit

app = Flask(__name__)
socket_server = SocketIO(app)
content_directory = "content/"
content_root = content_directory + "cse312.json"


def load_content(content_filename):
    all_content = []
    with open(content_filename) as content_file:
        content = json.load(content_file)
        for week in content:
            with open(content_directory + week) as week_file:
                all_content.append(json.load(week_file))
    return all_content


@app.get('/')
def cse312():
    content = load_content(content_root)
    resp = make_response(render_template('cse312/cse312.html', weeks=content))
    resp.headers["X-Content-Type-Options"] = "nosniff"
    return resp


@app.get('/hw/<hw_url>')
def hw(hw_url):
    resp = make_response(render_template('hw/' + str(hw_url)))
    resp.headers["X-Content-Type-Options"] = "nosniff"
    return resp


@app.route('/static_files/<path:filename>')
def serve_static(filename):
    resp = make_response(send_from_directory('static_files', filename))
    resp.headers["X-Content-Type-Options"] = "nosniff"
    return resp


if __name__ == '__main__':
    socket_server.run(app, host="0.0.0.0", port=5000)
