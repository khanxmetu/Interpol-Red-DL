import os

from flask import Flask, render_template, g
from notice_server import views
from notice_server.notice_db_manager import NoticeDBManager

app = Flask("notice_server")

notice_db_manager = NoticeDBManager(
    db_name=os.environ["DB_NAME"],
    db_user=os.environ["MONGO_INITDB_ROOT_USERNAME"],
    db_pass=os.environ["MONGO_INITDB_ROOT_PASSWORD"],
    db_host=os.environ["DB_HOST"],
    db_port=int(os.environ["DB_PORT"])
)
notice_db_manager.connect()

@app.before_request
def add_dependencies():
    g.notice_db_manager = notice_db_manager

app.add_url_rule("/", view_func=views.index)
app.add_url_rule("/notice_list", view_func=views.notice_list_page)
app.add_url_rule("/api/notice_list", view_func=views.notice_list)
app.add_url_rule("/notice/<notice_id>", view_func=views.notice_detail_page)
app.add_url_rule("/api/notice/<notice_id>", view_func=views.notice_detail)


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=5000)
