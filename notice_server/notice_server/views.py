from flask import render_template, jsonify, g, url_for, redirect
from notice_server.notice_db_manager import NoticeDBManager


def index():
    return redirect(url_for("notice_list_page"))


def notice_list():
    notice_db_manager: NoticeDBManager = g.notice_db_manager
    notices = notice_db_manager.get_all_notices()
    notices_list_of_dict = [notice.to_dict() for notice in notices]
    return jsonify(notices_list_of_dict)


def notice_detail(notice_id: str):
    notice_db_manager: NoticeDBManager = g.notice_db_manager
    notice_dict = notice_db_manager.get_notice_by_id(
        notice_id).to_dict()
    return jsonify(notice_dict)

def notice_list_page():
    return render_template("notice_list.html")


def notice_detail_page(notice_id: str):
    return render_template("notice_detail.html", notice_id=notice_id)
