from flask import Flask
import pika

app = Flask(__name__)


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

    
    channel.basic_publish(
        exchange='',
        routing_key='canal_contabilidad_1',
        body=cmd,
        properties=pika.BasicProperties(
            delivery_mode=2,  # make message persistent
        ))
    channel.basic_publish(
        exchange='',
        routing_key='canal_contabilidad_2',
        body=cmd,
        properties=pika.BasicProperties(
            delivery_mode=2,  # make message persistent
        ))
    channel.basic_publish(
        exchange='',
        routing_key='canal_contabilidad_3',
        body=cmd,
        properties=pika.BasicProperties(
            delivery_mode=2,  # make message persistent
        ))
    connection.close()
    return " [x] Sent: %s" % cmd


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
