from flask import Flask
from threading import Thread

app = Flask('gork')


@app.route('/')
def home():
    return "Gork lives. 🙃"


def run():
    app.run(host='0.0.0.0', port=8080)


def keep_alive():
    thread = Thread(target=run)
    thread.start()
