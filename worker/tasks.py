import time
from celery import Celery
from celery.utils.log import get_task_logger

import numpy as np
from keras.models import load_model
from keras.preprocessing.image import ImageDataGenerator, img_to_array

from flask import jsonify

logger = get_task_logger(__name__)

app = Celery('tasks',
             broker='amqp://admin:mypass@rabbit:5672',
             backend='rpc://')

classes = ["apple", "banana", "grapes", "pineapple"]


def get_model():
    global model
    model = load_model("fruits.h5")
    print("Model Loaded")


def preprocess_img(image, target_size, inv):
    image = image.convert("L")
    image = image.resize(target_size)
    if inv:
        image = np.invert(image)
    image = img_to_array(image)
    image = np.expand_dims(image, axis=0)
    return image


print("loading model...")
get_model()


@app.task()
def predict(image):
    logger.info('Got Request - Starting work ')
    time.sleep(4)

    processed_img = preprocess_img(image, target_size=(28, 28), inv=False)
    pred = model.predict(processed_img)
    idx = np.argmax(np.array(pred[0]))
    response = {
        'predictionImg': str(classes[idx])
    }

    logger.info('Work Finished ')
    return jsonify(response)
