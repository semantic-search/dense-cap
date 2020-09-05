import os
SEND_TOPIC_FULL = "IMAGE_RESULTS"
SEND_TOPIC_TEXT = "TEXT"
KAFKA_HOSTNAME = os.getenv("KAFKA_HOSTNAME")
KAFKA_PORT = os.getenv("KAFKA_PORT")
REDIS_HOSTNAME = os.getenv("REDIS_HOSTNAME")
REDIS_PORT = os.getenv("REDIS_PORT")
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD")
RECEIVE_TOPIC = 'DENSE_CAP'
ALLOWED_IMAGE_TYPES = ["jpg", "png"]
KAFKA_USERNAME = os.getenv("KAFKA_USERNAME")
KAFKA_PASSWORD = os.getenv("KAFKA_PORT")
