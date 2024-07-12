from config import Config

from mongoengine import connect, Document, StringField


class Notice(Document):
    notice_id = StringField(primary_key=True, max_length=20)
    name = StringField(max_length=20)


class NoticeDBManager:
    def __init__(self, config: Config):
        self._config = config
        connect(db=self._config.DB_NAME, host=self._config.DB_HOST, port=self._config.DB_PORT)

if __name__ == "__main__":
    config = Config(db_host='db')
    NoticeDBManager(config)
    notice = Notice(notice_id='2024-20', name='ABC')
    notice.save()