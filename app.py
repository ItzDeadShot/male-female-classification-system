from flask import Flask, request, render_template, Response
import tensorflow as tf
import numpy as np
from io import BytesIO
import sass

app = Flask(__name__)

# load the model
model = tf.keras.models.load_model('model.h5')

# @app.route('/css/style.css')
# def serve_css():
#   # read the SCSS file
#   with open('static/scss/style.scss', 'r') as f:
#     scss = f.read()

#   # compile the SCSS to CSS
#   css = sass.compile(string=scss)

#   # return the CSS as a response
#   return Response(css, mimetype='text/css')


@app.route('/')
def home():
    # render the template with a form for uploading an image
    return render_template('index.html')


@app.route('/upload')
def upload():
    # render the template with a form for uploading an image
    return render_template('upload.html')


@app.route('/capture')
def capture():
    # render the template with a form for uploading an image
    return render_template('capture.html')


@app.route('/about')
def about():
    # render the template with a form for uploading an image
    return render_template('about.html')


@app.route('/predict', methods=['POST'])
def predict():
    # get the uploaded image file
    print(request.get_data())
    image_file = request.files['fileup']

    # read the image file as a binary stream
    image_binary_stream = BytesIO(image_file.read())

    # read the image file and preprocess it for the model
    image = tf.keras.preprocessing.image.load_img(
        image_binary_stream, target_size=(128, 128))
    image = tf.keras.preprocessing.image.img_to_array(image)
    image = tf.keras.applications.mobilenet.preprocess_input(image)
    image = np.expand_dims(image, axis=0)

    # make a prediction using the model
    prediction = model.predict(image)
    
    title = ""
    if int(prediction*2) >= 1:
        percentage = (round(float(((prediction[0]-0.5) + 0.5) * 100), 2))
        title = f"Male ({percentage}%)"
    else:
        percentage = (round(float(((0.5-prediction[0])+0.5) * 100), 2))
        title = f"Female ({percentage}%)"

    # save the image to a file
    with open('static/temp.jpg', 'wb') as f:
        f.write(image_binary_stream.getvalue())

    # return the prediction and image to the template
    return render_template('index.html', prediction=title, image='static/temp.jpg')


if __name__ == '__main__':
    app.run(debug=True)
