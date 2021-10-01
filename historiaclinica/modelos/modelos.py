from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import UniqueConstraint
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields, Schema

import datetime


db = SQLAlchemy()

    
class Historia(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    registro = db.Column(db.String(100))


class HistoriaClinicaSchema(SQLAlchemyAutoSchema):
    class Meta:
         model = Historia         
         include_relationships = True
         load_instance = True
