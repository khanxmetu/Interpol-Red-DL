import time

from flask import Flask
import pika
from flask_socketio import SocketIO

from notice_consumer import NoticeConsumer

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

if __name__ == "__main__":
    notice_consumer = NoticeConsumer(socketio)
    socketio.start_background_task(target=notice_consumer.run)
    socketio.run(app, host="0.0.0.0", debug=False, allow_unsafe_werkzeug=True)