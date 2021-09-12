from flask import Flask
import pika
import time
from flask_mail import Mail
from flask_mail import Message
import sys
from datetime import datetime
import json

canal_con_error=""
uuid_peticion=""

arrayValidar = {}

def notificacion(canal_con_error, uuid_peticion):
    with app.app_context():
        msg = Message('Alerta!', sender ='gehdevtests@gmail.com ', recipients = ['r.orellana@uniandes.edu.co'])
        msg.body = "Errores encontrados: "  + canal_con_error + "\nPetición UUID: "+ uuid_peticion
        mail.send(msg)   


def callback(ch, method, properties, body):
    cmd = body.decode()

    ##Acumulación de mensajes en array indexado por uuiid
    mensaje = json.loads(cmd)
    
    peticionValidar = []

    if mensaje['uuid'] in arrayValidar:
        peticionValidar = arrayValidar[mensaje['uuid']]
    
    peticionValidar.append(mensaje)

    arrayValidar[mensaje['uuid']] = peticionValidar
    largoArray = len(arrayValidar[mensaje['uuid']])
    ###########################################################

    # using with statement
    with open('log.txt', 'a') as f:
        f.write("{0} -- {1}\n".format(datetime.now().strftime("%Y-%m-%d %H:%M"), cmd))
        print(cmd)

    notificacion(canal_con_error, uuid_peticion)
    
    ch.basic_ack(delivery_tag=method.delivery_tag)


app = Flask(__name__)

sleepTime = 20
print(' [*] Inicia en  ', sleepTime, ' segundos.')

time.sleep(sleepTime)

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = 'gehdevtests@gmail.com '
app.config['MAIL_PASSWORD'] = 'zkadjaefpsxbbldd'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
mail = Mail(app)
mail.init_app(app)
original_stdout = sys.stdout

connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
channel = connection.channel()
channel.queue_declare(queue='canal_validador', durable=True)       
channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='canal_validador', on_message_callback=callback)
channel.start_consuming()


@app.route('/')
def index():
    return 'OK'

