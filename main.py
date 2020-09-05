import json
from dotenv import load_dotenv
import uuid
from db_models.mongo_setup import global_init
from db_models.models.cache_model import Cache
import init
from image_cap_service import predict
import globals

global_init()
load_dotenv()

RECEIVE_TOPIC = globals.RECEIVE_TOPIC
r = init.redis_obj
consumer = init.consumer_obj
producer = init.producer_obj
SEND_TOPIC_FULL = globals.SEND_TOPIC_FULL
SEND_TOPIC_TEXT = globals.SEND_TOPIC_TEXT


def send_to_topic(topic, value_to_send_dic):
    data_json = json.dumps(value_to_send_dic)
    producer.send(topic, value=data_json)


if __name__ == "__main__":
    for message in consumer:
        message = message.value
        db_key = str(message)
        db_object = Cache.objects.get(pk=db_key)
        file_name = db_object.file_name
        r.set(RECEIVE_TOPIC, file_name)
        if db_object.is_doc_type:
            """document"""
            images_array = []
            for image in db_object.files:
                pdf_image = str(uuid.uuid4()) + ".jpg"
                with open(pdf_image, 'wb') as file_to_save:
                    file_to_save.write(image.file.read())
                images_array.append(pdf_image)
            captions_list = []
            scores_list = []
            text_predictions = []
            for image in images_array:
                image_results = predict(image, doc=True)
                captions = image_results["captions"]
                scores = image_results["scores"]
                captions_list.append(captions)
                scores_list.append(scores)

            full_res = {
                "file_name": file_name,
                "captions": captions_list,
                "scores": scores_list
            }
            text_res = {
                "file_name": file_name,
                "captions": captions_list
            }
            send_to_topic(SEND_TOPIC_FULL, value_to_send_dic=full_res)
            send_to_topic(SEND_TOPIC_TEXT, value_to_send_dic=text_res)
            producer.flush()

        else:
            """image"""
            if db_object.mime_type in globals.ALLOWED_IMAGE_TYPES:
                with open(file_name, 'wb') as file_to_save:
                    file_to_save.write(db_object.file.read())
                full_res = predict(file_name)
                text_res = {
                    "file_name": full_res["file_name"],
                    "captions": full_res["captions"]
                }
                send_to_topic(SEND_TOPIC_FULL, value_to_send_dic=full_res)
                send_to_topic(SEND_TOPIC_TEXT, value_to_send_dic=text_res)
                producer.flush()
