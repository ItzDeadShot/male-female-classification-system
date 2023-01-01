from flask import Flask, request, render_template, Response
import tensorflow as tf
import numpy as np
from io import BytesIO
import base64
import os

app = Flask(__name__)

# load the model
model = tf.keras.models.load_model('model.h5')


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@app.route('/')
def home():
    # render the template with a form for home page
    return render_template('index.html')


@app.route('/upload')
def upload():
    # render the template with a form for uploading an image
    return render_template('upload.html')


@app.route('/capture')
def capture():
    # render the template with a form for capturing an image
    return render_template('capture.html')


@app.route('/about')
def about():
    # render the template with a form for about page
    return render_template('about.html')


@app.route('/predict', methods=['POST'])
def predict():
    upload = True
    if (request.content_type.split(';')[0] == "application/x-www-form-urlencoded"):
        # get the uploaded image file
        image_file = request.form['image'].split(',')[1]
        # read the image file as a binary stream
        image_binary_stream = BytesIO(base64.b64decode(image_file))
        upload = False
    else:
        # get the uploaded image file
        image_file = request.files['fileup']
        # read the image file as a binary stream
        image_binary_stream = BytesIO(image_file.read())
        upload = True

    if os.path.exists("static/temp.jpg"):
        os.remove("static/temp.jpg")
    else:
        print("The file does not exist")

    # save the image to a file
    with open('static/temp.jpg', 'wb') as f:
        f.write(image_binary_stream.getvalue())

    # read the image file and preprocess it for the model
    image = tf.keras.preprocessing.image.load_img(
        image_binary_stream, target_size=(128, 128))
    image = tf.keras.preprocessing.image.img_to_array(image)
    image = tf.keras.applications.mobilenet.preprocess_input(image)
    image = np.expand_dims(image, axis=0)

    # make a prediction using the model
    prediction = model.predict(image)

    title = "Null"
    if int(prediction*2) >= 1:
        percentage = (round(float(((prediction[0]-0.5) + 0.5) * 100), 2))
        title = f"Male ({percentage}%)"
    else:
        percentage = (round(float(((0.5-prediction[0])+0.5) * 100), 2))
        title = f"Female ({percentage}%)"

    if upload:
        # return the prediction and image to the template
        return render_template('upload.html', prediction=title, image='static/temp.jpg')
    else:
        # return the prediction and image to the template
        results = {'prediction': title, 'image': 'static/temp.jpg'}
        return results


if __name__ == '__main__':
    app.run(debug=True)
