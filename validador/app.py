from flask import Flask
import pika
import time
from flask_mail import Mail
from flask_mail import Message
import sys

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

def callback(ch, method, properties, body):
    cmd = body.decode()

    with open('log.txt', 'w') as f:
        sys.stdout = f # Change the standard output to the file we created.
        print("respuesta microservicios contabilidad", cmd)
        sys.stdout = original_stdout

    with app.app_context():
        msg = Message('Alerta!', sender =   'gehdevtests@gmail.com ', recipients = ['r.orellana@uniandes.edu.co', 's.ocampor@uniandes.edu.co', 'cx.diaz@uniandes.edu.co'])
        msg.body = "se genera alerta en el validador - voting para el servidor =  " + cmd
        mail.send(msg)
    
    ch.basic_ack(delivery_tag=method.delivery_tag)
    
    
channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='canal_validador', on_message_callback=callback)
channel.start_consuming()


@app.route('/')
def index():
    return 'OK'