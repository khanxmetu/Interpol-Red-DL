import mongoengine
from mongoengine import DoesNotExist

from notice_server.models.notice import Notice
from notice_update_notifier import NoticeUpdateType


class NoticeDBManager:
    def __init__(self, db_name, db_user, db_pass, db_host, db_port) -> None:
        mongoengine.connect(
            db=db_name,
            username=db_user,
            password=db_pass,
            host=db_host,
            port=db_port
        )

    def get_notice_by_id(self, notice_id: str, default=None) -> Notice:
        try:
            return Notice.objects.get(notice_id=notice_id)
        except DoesNotExist as e:
            return default

    def update_notice_from_doc(self, new_notice: Notice) -> NoticeUpdateType:
        old_notice = self.get_notice_by_id(new_notice.notice_id)

        # Notice exists with exact details
        if old_notice and old_notice == new_notice:
            old_notice.last_fetched_date = new_notice.last_fetched_date
            old_notice.save()
            new_notice.reload()
            return NoticeUpdateType.REFETCHED

        # Notice modified
        elif old_notice:
            new_notice.first_fetched_date = old_notice.first_fetched_date
            new_notice.save()
            return NoticeUpdateType.MODIFIED

        # New notice
        else:
            new_notice.save()
            return NoticeUpdateType.CREATED

    def close(self):
        mongoengine.disconnect()
