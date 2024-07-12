from flask import Flask
import pika

app = Flask(__name__)

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
    app.run(host="0.0.0.0")