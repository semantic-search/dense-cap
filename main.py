import json
import subprocess
from dotenv import load_dotenv
import base64
import os
import uuid
import redis
import redis
from kafka import KafkaConsumer
from kafka import KafkaProducer
from json import loads
from base64 import decodestring
load_dotenv()

KAFKA_HOSTNAME = os.getenv("KAFKA_HOSTNAME")
KAFKA_PORT = os.getenv("KAFKA_PORT")
REDIS_HOSTNAME = os.getenv("REDIS_HOSTNAME")
REDIS_PORT = os.getenv("REDIS_PORT")
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD")
# kafka prerequisites
RECEIVE_TOPIC = 'DENSE_CAP'
SEND_TOPIC_FULL = "IMAGE_RESULTS"
SEND_TOPIC_TEXT = "TEXT"
print("kafka : " + KAFKA_HOSTNAME + ':' + KAFKA_PORT)
# Redis initialize
r = redis.StrictRedis(host=REDIS_HOSTNAME, port=REDIS_PORT,
                      password=REDIS_PASSWORD, ssl=True)
# Kafka initialize
consumer_easyocr = KafkaConsumer(
    RECEIVE_TOPIC,
    bootstrap_servers=[KAFKA_HOSTNAME + ':' + KAFKA_PORT],
    auto_offset_reset="earliest",
    enable_auto_commit=True,
    group_id="my-group",
    value_deserializer=lambda x: loads(x.decode("utf-8")),
)
# app = FastAPI()
producer = KafkaProducer(
    bootstrap_servers=[KAFKA_HOSTNAME + ':' + KAFKA_PORT],
    value_serializer=lambda x: json.dumps(x).encode("utf-8"),
)

result_dir = "vis/data/"
result_file = result_dir+"results.json"

# @app.post("/uploadfile/")
# def create_upload_file(file: UploadFile = File(...), image_id: str = Form(...)):
    # Redis Stuff
def predict(file_name,image_id):


    subprocess.call(["th", "run_model.lua", "-input_image", file_name])



    with open(result_file) as json_file:
        data = json.load(json_file)
    captions = []
    scores = []
    for items in data:
        if items == "results":
            for key, val in data[items][0].items():
                if key == "scores":
                    scores.append(val)
                elif key == "captions":
                    captions.append(val)
    captions = captions[0]
    scores = scores[0]
    response = {
        "image_id" : image_id,
        "captions" : captions,
        "scores": scores
    }


    os.remove(file_name)
    os.remove(result_dir + file_name)
    os.remove(result_file)
    # Redis Kafka Stuff
    producer.send('CONTAINER_TOPIC', value=response)
    return response

if __name__ == "__main__":
    for message in consumer_easyocr:
        print('xxx--- inside open images consumer---xxx')
        print(KAFKA_HOSTNAME + ':' + KAFKA_PORT)

        message = message.value
        print("MESSAGE RECEIVED consumer_densecap: ")
        image_id = message['image_id']
        # data = message['data']
        data = message['data']
        r.set(RECEIVE_TOPIC, image_id)
        file_name = str(uuid.uuid4()) + ".jpg"
        with open(file_name, "wb") as fh:
            fh.write(base64.b64decode(data.encode("ascii")))

        full_res = predict(file_name,image_id)
        text_res={
            "image_id": full_res["image_id"],
            "captions": full_res["captions"]
        }
        producer.send(SEND_TOPIC_FULL, value=json.dumps(full_res))
        producer.send(SEND_TOPIC_TEXT, value=json.dumps(text_res))

        producer.flush()
