try:
    import io
    import base64
    from PIL import Image
    from celery import Celery
    from flask import Flask, request

except Exception as e:
    print("Error  :{} ".format(e))

app = Flask(__name__)


simple_app = Celery('simple_worker',
                    broker='amqp://admin:mypass@rabbit:5672',
                    backend='rpc://')


@app.route('/task_status/<task_id>')
def get_status(task_id):
    status = simple_app.AsyncResult(task_id, app=simple_app)
    print("Invoking Method ")
    return "Status of the Task " + str(status.state)


@app.route('/task_result/<task_id>')
def task_result(task_id):
    result = simple_app.AsyncResult(task_id).result
    return "Result of the Task " + str(result)


@app.route("/predict-image/", methods=["POST"])
def predict_img():
    message = request.get_json(force=True)
    encoded = message["image"]
    decoded = base64.b64decode(encoded)
    image = Image.open(io.BytesIO(decoded))

    r = simple_app.send_task('tasks.predict', kwargs={'image': image})
    app.logger.info(r.backend)
    return r.id

