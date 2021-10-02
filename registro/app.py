from flask import Flask
import uuid
from registro import create_app
from registro.rutas import registrar_rutas
from flask_jwt_extended import JWTManager
from flask_cors import CORS

app = Flask(__name__)
app = create_app('default')
app_context = app.app_context()
app_context.push()

cors = CORS(app)
registrar_rutas(app)
jwt = JWTManager(app)


@app.route('/')
def index():
    return 'OK'

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
