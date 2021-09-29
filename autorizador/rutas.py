from autorizador.vistas.usuario import VistaAuth, VistaRegistro
from flask_restful import Api


def registrar_rutas(app):
    
    api = Api(app)
    api.add_resource(VistaAuth, '/auth')
    api.add_resource(VistaRegistro, '/registro')