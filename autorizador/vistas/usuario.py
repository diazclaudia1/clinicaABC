from flask_jwt_extended.utils import get_jwt, get_jwt_header, get_jwt_identity
from autorizador.modelos.modelos import Usuario,  db, UsuarioSchema
from flask import app, request
from flask_jwt_extended import create_access_token, jwt_required
from flask_restful import Resource


usuario_schema = UsuarioSchema()

class VistaRegistro(Resource):

    def post(self):

        nuevo_usuario = Usuario(nombre=request.json["nombre"], contrasena=request.json["contrasena"],rol=request.json["rol"])
        db.session.add(nuevo_usuario)
        db.session.commit()
        additional_claims = {"rol": nuevo_usuario.rol}
        token_de_acceso = create_access_token(identity = nuevo_usuario.id, additional_claims= additional_claims)
        return {"msg":"usuario creado exitosamente", "token":token_de_acceso}


class VistaAuth(Resource):

    def post(self):
        usuario = Usuario.query.filter(Usuario.nombre == request.json["nombre"]).first()
        # return usuario_schema.dump(usuario)
        db.session.commit()
        if usuario is None:
            return "El usuario no existe", 404
        else:
            additional_claims = {"rol": usuario.rol}
            token_de_acceso = create_access_token(identity = usuario.id,additional_claims=additional_claims)
            return {"msg":"Inicio de sesión exitoso", "token": token_de_acceso,"usuario":usuario_schema.dump(usuario)}


class VistaHU(Resource):
    
    @jwt_required()
    def get(self):
        jwtHeader = get_jwt()
        if(jwtHeader["rol"] != "medico"):
             return "El usuario no esta autorizado para acceder al recurso", 403
        
        return jwtHeader