from flask import Flask
import pika
import uuid

app = Flask(__name__)


@app.route('/')
def index():
    return 'OK'

@app.route('/tea')
def otrometodo():
    return 'teadossssss'

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
