import pika
import json
import os
from kafka import KafkaProducer

RABBITMQ_URL = os.getenv("RABBITMQ_URL", "amqp://guest:guest@localhost:5672/")
KAFKA_BOOTSTRAP = os.getenv("KAFKA_BOOTSTRAP", "localhost:9092")


def publicar_rabbitmq(pedido: dict):
    params = pika.URLParameters(RABBITMQ_URL)
    connection = pika.BlockingConnection(params)
    channel = connection.channel()
    channel.queue_declare(queue="pedidos_criados", durable=True)
    channel.basic_publish(
        exchange="",
        routing_key="pedidos_criados",
        body=json.dumps(pedido),
        properties=pika.BasicProperties(delivery_mode=2),
    )
    connection.close()


def publicar_kafka(pedido: dict):
    producer = KafkaProducer(
        bootstrap_servers=KAFKA_BOOTSTRAP,
        value_serializer=lambda v: json.dumps(v).encode("utf-8"),
    )
    producer.send("pedidos-criados", value=pedido)
    producer.flush()
    producer.close()
