from autorizador import create_app
from autorizador.rutas import registrar_rutas
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from autorizador.modelos.modelos import Usuario, db


app = create_app('default')
app_context = app.app_context()
app_context.push()

db.init_app(app)
db.create_all()
cors = CORS(app)
registrar_rutas(app)
jwt = JWTManager(app)

@jwt.user_lookup_loader
def get_logged_user(jwt_header, jwt_data):
    identity = jwt_data['sub']
    return Usuario.query.filter_by(id=identity).one_or_none()