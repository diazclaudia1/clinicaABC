from flask import Flask

from flask import app, request
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
from flask_cors import CORS
from flask_jwt_extended.utils import get_jwt, get_jwt_header, get_jwt_identity

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import UniqueConstraint
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

app = Flask(__name__)  
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///autorizador.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY']='clave-jwt'
app.config['PROPAGATE_EXCEPTIONS'] = True

app_context = app.app_context()
app_context.push()
db = SQLAlchemy(app)

db.init_app(app)

cors = CORS(app)
jwt = JWTManager(app)

@app.before_first_request
def create_tables():
    db.create_all()

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50))
    contrasena = db.Column(db.String(50))
    rol = db.Column(db.String(50))


class UsuarioSchema(SQLAlchemyAutoSchema):
    class Meta:
         model = Usuario
         exclude = ('contrasena',)
         include_relationships = True
         load_instance = True

usuario_schema = UsuarioSchema()

@app.route('/')
def index():
    return 'OK'

@app.route('/tea')
def otrometodoGet():
    return 'TEA'

@app.route('/tea', methods = ['POST'])
def otrometodoPost():
    return 'TEA-POST'    

@app.route('/registro', methods = ['POST'])
def post():
    nuevo_usuario = Usuario(nombre=request.json["nombre"], contrasena=request.json["contrasena"],rol=request.json["rol"])
    db.session.add(nuevo_usuario)
    db.session.commit()
    # return usuario_schema.dump(nuevo_usuario)
    additional_claims = {"rol": nuevo_usuario.rol}
    token_de_acceso = create_access_token(identity = nuevo_usuario.id, additional_claims= additional_claims)
    return {"msg":"usuario creado exitosamente", "token":token_de_acceso}

@app.route('/auth', methods = ['POST'])
def postAuth():
        usuario = Usuario.query.filter(Usuario.nombre == request.json["nombre"]).first()
        # return usuario_schema.dump(usuario)
        db.session.commit()
        if usuario is None:
            return "El usuario no existe", 404
        else:
            additional_claims = {"rol": usuario.rol}
            token_de_acceso = create_access_token(identity = usuario.id,additional_claims=additional_claims)
            return {"msg":"Inicio de sesión exitoso", "token": token_de_acceso,"usuario":usuario_schema.dump(usuario)}


@app.route('/auth', methods = ['GET'])
@jwt_required()
def get():
    jwtHeader = get_jwt()
    if(jwtHeader["rol"] != "medico"):
            return "El usuario no esta autorizado para acceder al recurso", 403
    
    return jwtHeader

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')





