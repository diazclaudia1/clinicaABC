from flask import Flask
import pika
import uuid
from historiaclinica import create_app
from historiaclinica.rutas import registrar_rutas
from historiaclinica.modelos.modelos import *
from flask_jwt_extended import JWTManager
from flask_cors import CORS

app = Flask(__name__)

app = create_app('default')
app_context = app.app_context()
app_context.push()

db.init_app(app)
db.create_all()
cors = CORS(app)
registrar_rutas(app)
jwt = JWTManager(app)

@app.route('/')
def index():
    return 'OK'


@app.route('/reporte/<cmd>')
def add(cmd):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
    channel = connection.channel()
    
    channel.queue_declare(queue='canal_contabilidad_1', durable=True)
    channel.queue_declare(queue='canal_contabilidad_2', durable=True)
    channel.queue_declare(queue='canal_contabilidad_3', durable=True)
    # channel.queue_declare(queue='task_queue', durable=True)
    uuidOne = uuid.uuid1()
    mensaje = cmd+'---'+str(uuidOne)
    print(mensaje)
    
    channel.basic_publish(
        exchange='',
        routing_key='canal_contabilidad_1',
        body=mensaje,
        properties=pika.BasicProperties(
            delivery_mode=2,  # make message persistent
        ))
    channel.basic_publish(
        exchange='',
        routing_key='canal_contabilidad_2',
        body=mensaje,
        properties=pika.BasicProperties(
            delivery_mode=2,  # make message persistent
        ))
    channel.basic_publish(
        exchange='',
        routing_key='canal_contabilidad_3',
        body=mensaje,
        properties=pika.BasicProperties(
            delivery_mode=2,  # make message persistent
        ))
    connection.close()
    return " [x] Sent: " + mensaje


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')


