import time

from flask import Flask, render_template
import pika
from flask_socketio import SocketIO

from config import Config
from notice_consumer import NoticeConsumer
from notice_db_manager import NoticeDBManager
from notice_update_notifier import NoticeUpdateNotifier


app = Flask(__name__)
socketio = SocketIO(app)


from datetime import datetime
NOTICES = [
    {
        "notice_id": "asdsd",
        "forename": "asd",
        "name": "Bob",
        "last_fetched": datetime.now()
    }
]

config = Config.load_from_env()
notice_db_manager = NoticeDBManager(config)
notice_update_notifier = NoticeUpdateNotifier(config, socketio)
notice_consumer = NoticeConsumer(
    config, notice_db_manager, notice_update_notifier
)

@app.route('/')
def notice_list_view():
    return render_template("notice_list.html", notices=NOTICES)

@app.route('/notice/<notice_id>')
def notice_view(notice_id: str):
    pass

if __name__ == "__main__":
    socketio.start_background_task(target=notice_consumer.run)
    socketio.run(app, host="0.0.0.0", debug=False, allow_unsafe_werkzeug=True)