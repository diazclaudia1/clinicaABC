from historiaclinica.modelos.modelos import *
from flask import request
from flask_jwt_extended import create_access_token, jwt_required,get_jwt_identity
from flask_restful import Resource
from flask_jwt_extended.config import config
from flask_jwt_extended.internal_utils import get_jwt_manager
import re
import jwt


historia_schema = HistoriaClinicaSchema

class VistaHistoria(Resource):
    @jwt_required()
    def post(self):
        
        nueva_historia = Historia(registro=request.json["registro"])
        db.session.add(nueva_historia)
        db.session.commit()
        
        key_2 = request.headers.get('Authorization')

        key_2 = re.sub("Bearer ","",key_2)
        #print(key_2)

        #usuario actual
        current_user_id = get_jwt_identity()    
        print(current_user_id)

        #buscar por usuario y por rol medico


        return {"mensaje": "historia creada exitosamente"}


