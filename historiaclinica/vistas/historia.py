from historiaclinica.modelos.modelos import *
from flask import request
from flask_jwt_extended import jwt_required
from flask_restful import Resource
from flask_jwt_extended.utils import get_jwt



historia_schema = HistoriaClinicaSchema

class VistaHistoria(Resource):
    @jwt_required()
    def post(self):
        
        jwtHeader = get_jwt()
        if(jwtHeader["rol"] == "medico"):         

            nueva_historia = Historia(registro=request.json["registro"])
            db.session.add(nueva_historia)
            db.session.commit()        
            return {"mensaje": "historia creada exitosamente"}

        return "El usuario no esta autorizado para acceder al recurso", 403
