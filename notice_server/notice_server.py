import time

from flask import Flask
import pika
from flask_socketio import SocketIO

app = Flask(__name__)
socketio = SocketIO(app)

NOTICES = [
    {
        "notice_1": {
            "adas": "asdasd"
        }
    }
]

@app.route('/')
def notice_list_view():
    return NOTICES

@app.route('/notice/<notice_id>')
def notice_view(notice_id: str):
    pass

class Consumer:
    def __init__(self):
        pass
    def run(self):
        while True:
            socketio.emit("dummy data")
            time.sleep(1)

if __name__ == "__main__":
    consumer = Consumer()
    socketio.start_background_task(target=consumer.run)
    socketio.run(app, host="0.0.0.0", debug=False, allow_unsafe_werkzeug=True)