import pika
import os
import time
import sys

sleepTime = 5
print(' [*] Inicia en  ', sleepTime, ' segundos.')
CANAL = 'canal_contabilidad_' + os.getenv('MICROSERVICIO')

time.sleep(sleepTime)

connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
channel = connection.channel()
channel.queue_declare(queue=CANAL, durable=True)
original_stdout = sys.stdout

def callback(ch, method, properties, body):

    cmd = body.decode()

    with open('log'+CANAL+'.txt', 'w') as f:
        sys.stdout = f # Change the standard output to the file we created.
        print('cmd', cmd, CANAL, os.getenv('MICROSERVICIO'))
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
