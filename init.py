import redis
from kafka import KafkaConsumer
from kafka import KafkaProducer
import globals
import json
KAFKA_HOSTNAME = globals.KAFKA_HOSTNAME
KAFKA_PORT = globals.KAFKA_PORT
REDIS_HOSTNAME = globals.REDIS_HOSTNAME
REDIS_PORT = globals.KAFKA_PORT
REDIS_PASSWORD = globals.REDIS_PORT
RECEIVE_TOPIC = globals.RECEIVE_TOPIC



# Redis initialize
redis_obj = redis.StrictRedis(
    host=REDIS_HOSTNAME,
    port=REDIS_PORT,
    password=REDIS_PASSWORD,
    ssl=True
)

# Kafka initialize
consumer_obj = KafkaConsumer(
    RECEIVE_TOPIC,
    bootstrap_servers=[KAFKA_HOSTNAME + ':' + KAFKA_PORT],
    auto_offset_reset="earliest",
    enable_auto_commit=True,
    group_id="my-group",
    value_deserializer=lambda x: json.loads(x.decode("utf-8")),
)

producer_obj = KafkaProducer(
    bootstrap_servers=[KAFKA_HOSTNAME + ':' + KAFKA_PORT],
    value_serializer=lambda x: json.dumps(x).encode("utf-8"),
)
