from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import UniqueConstraint
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields, Schema

import datetime


db = SQLAlchemy()

    
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
