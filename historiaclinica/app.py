from flask import Flask,app, request
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from flask_jwt_extended.utils import get_jwt, get_jwt_header, get_jwt_identity
from flask_jwt_extended import JWTManager, create_access_token, jwt_required


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///historia.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY']='clave-jwt'
app.config['PROPAGATE_EXCEPTIONS'] = True
app_context = app.app_context()
app_context.push()

db = SQLAlchemy()
    
class Historia(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    registro = db.Column(db.String(100))


class HistoriaClinicaSchema(SQLAlchemyAutoSchema):
    class Meta:
         model = Historia         
         include_relationships = True
         load_instance = True

historia_clinica = HistoriaClinicaSchema()         

db.init_app(app)
db.create_all()
cors = CORS(app)
jwt = JWTManager(app)
	
@app.route('/historia', methods = ['POST'])
@jwt_required()
def post():
    
    jwtHeader = get_jwt()
    if(jwtHeader["rol"] == "medico"):         

        nueva_historia = Historia(registro=request.json["registro"])
        db.session.add(nueva_historia)
        db.session.commit()        
        return {"mensaje": "historia creada exitosamente"}

    return "El usuario no esta autorizado para acceder al recurso", 403
		
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')