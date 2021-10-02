from flask import request
from flask_jwt_extended import jwt_required
from flask_restful import Resource
from flask_jwt_extended.utils import get_jwt
import requests
import json



class VistaRegistroHistoria(Resource):
    @jwt_required()
    def post(self):
        
        
        response = requests.post("http://127.0.0.1:5002/historia", json = request.json, headers = request.headers)
        
        if response.status_code == 200:
            return json.loads(response.text)
        else:
            return {"mensaje: Error "+response.status_code}