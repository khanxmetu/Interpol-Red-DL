import time

from flask import Flask, render_template, jsonify
import pika
from flask_socketio import SocketIO

from config import Config
from notice_consumer import NoticeConsumer
from notice_db_manager import NoticeDBManager
from notice_update_notifier import NoticeUpdateNotifier
from models.notice import Notice

app = Flask(__name__)
socketio = SocketIO(app)

config = Config.load_from_env()
notice_db_manager = NoticeDBManager(config)
notice_update_notifier = NoticeUpdateNotifier(config, socketio)
notice_consumer = NoticeConsumer(
    config, notice_db_manager, notice_update_notifier
)

@app.route('/api/notice_list')
def notice_list():
    notices_son_objects = [notice.to_mongo(use_db_field=False) for notice in Notice.objects()]
    return jsonify(notices_son_objects)

@app.route('/api/notice/<notice_id>')
def notice_detail(notice_id: str):
    notice_son_object = notice_db_manager.get_notice_by_id(notice_id).to_mongo(use_db_field=False)
    return jsonify(notice_son_object)

@app.route('/')
def notice_list_view():
    return render_template("notice_list.html")

@app.route('/notice/<notice_id>')
def notice_view(notice_id: str):
    return render_template("notice_detail.html", notice_id=notice_id)

if __name__ == "__main__":
    socketio.start_background_task(target=notice_consumer.run)
    socketio.run(app, host="0.0.0.0", debug=False, allow_unsafe_werkzeug=True)