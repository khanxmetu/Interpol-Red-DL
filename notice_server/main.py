import os

from flask import Flask, render_template, g
from flask_socketio import SocketIO

from notice_server import views
from notice_server.notice_db_manager import NoticeDBManager
from notice_server.notice_consumer import NoticeConsumer
from notice_server.rabbitmq_client import RabbitMQConsumer
from notice_server.notice_update_notifier import NoticeUpdateNotifier

app = Flask("notice_server")
socketio = SocketIO(app)


notice_db_manager = NoticeDBManager(
    db_name=os.environ["DB_NAME"],
    db_user=os.environ["MONGO_INITDB_ROOT_USERNAME"],
    db_pass=os.environ["MONGO_INITDB_ROOT_PASSWORD"],
    db_host=os.environ["DB_HOST"],
    db_port=int(os.environ["DB_PORT"])
)
notice_db_manager.connect()

rmq_consumer = RabbitMQConsumer(
    username=os.environ["RABBITMQ_DEFAULT_USER"],
    password=os.environ["RABBITMQ_DEFAULT_PASS"],
    host=os.environ["RABBITMQ_HOST"],
    port=int(os.environ["RABBITMQ_PORT"])
)

update_notifier = NoticeUpdateNotifier(socketio=socketio)

notice_consumer = NoticeConsumer(
    queue_name=os.environ["QUEUE_NAME"],
    rmq_consumer=rmq_consumer,
    db_manager=notice_db_manager,
    update_notifier=update_notifier
)


@app.before_request
def add_dependencies():
    g.notice_db_manager = notice_db_manager


app.add_url_rule("/", view_func=views.index)
app.add_url_rule("/notice_list", view_func=views.notice_list_page)
app.add_url_rule("/api/notice_list", view_func=views.notice_list)
app.add_url_rule("/notice/<notice_id>", view_func=views.notice_detail_page)
app.add_url_rule("/api/notice/<notice_id>", view_func=views.notice_detail)


if __name__ == "__main__":
    socketio.start_background_task(target=notice_consumer.run)
    socketio.run(app, host="0.0.0.0", debug=False, allow_unsafe_werkzeug=True)