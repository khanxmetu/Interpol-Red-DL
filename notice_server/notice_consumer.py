import time

class NoticeConsumer:
    def __init__(self, socketio):
        self._socketio = socketio
        pass
    def run(self):
        while True:
            self._socketio.emit('notification', {
                "data":"asdasd"
            })
            time.sleep(1)