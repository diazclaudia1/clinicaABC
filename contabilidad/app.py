from flask import Flask
import pika
import os
import time
import sys

app = Flask(__name__)
original_stdout = sys.stdout

sleepTime = 5
print(' [*] Inicia en  ', sleepTime, ' segundos.')
MICROSERVICIO = os.getenv('MICROSERVICIO')
CANAL = 'canal_contabilidad_' + MICROSERVICIO
if not os.path.exists('sqlite:///db_contabilidad/test_'+MICROSERVICIO+'.db'):
    with open('log'+CANAL+'.txt', 'w') as f:
        sys.stdout = f # Change the standard output to the file we created.
        print('si existe ')
        sys.stdout = original_stdout


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db_contabilidad/test_'+MICROSERVICIO+'.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

time.sleep(sleepTime)

connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
channel = connection.channel()
channel.queue_declare(queue=CANAL, durable=True)


def callback(ch, method, properties, body):

    cmd = body.decode()

    with open('log'+CANAL+'.txt', 'w') as f:
        sys.stdout = f # Change the standard output to the file we created.
        print('cmd', cmd, CANAL, MICROSERVICIO)
        sys.stdout = original_stdout

    if cmd == 'financiero':
        print("imprime reporte financioer")
        channel.queue_declare(queue='canal_validador', durable=True)
        channel.basic_publish(
            exchange='',
            routing_key='canal_validador',
            body=CANAL + " = respuesta consulta base de datos sqlite",
            properties=pika.BasicProperties(
                delivery_mode=2,  # make message persistent
            ))
        # connection.close()
    else:
        print("Mensaaje = ", body)

    print(" [x] Ok")

    ch.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue=CANAL, on_message_callback=callback)
channel.start_consuming()
