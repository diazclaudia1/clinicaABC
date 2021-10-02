from registro.vistas.registro import *
from flask_restful import Api


def registrar_rutas(app):
    
    api = Api(app)
    api.add_resource(VistaRegistroHistoria, '/registro-historia')