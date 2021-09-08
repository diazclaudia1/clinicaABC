import pika
import time

sleepTime = 20
print(' [*] Inicia en  ', sleepTime, ' segundos.')
time.sleep(sleepTime)

connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
channel = connection.channel()
channel.queue_declare(queue='canal_validador', durable=True)

def callback(ch, method, properties, body):
    cmd = body.decode()
    print("respuesta microservicios contabilidad", body)

    ch.basic_ack(delivery_tag=method.delivery_tag)
    
channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='canal_validador', on_message_callback=callback)
channel.start_consuming()
