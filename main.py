import os
from PIL import Image
from flask import Flask, request

# For inference
from tensorflow.keras.applications.resnet50 import ResNet50
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.resnet50 import preprocess_input, decode_predictions
import numpy as np

model = ResNet50(weights='imagenet')

UPLOAD_FOLDER="/home/test/servertest/uploads"
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# CHECK EXTENSION
@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file1' not in request.files:
            return 'there is no file1 in form!'
        file1 = request.files['file1']
        
        img = Image.open(file1)  # load with Pillow
        img = img.resize((224,224))
        print(img.size)          # show image size (width, height)
        x = image.img_to_array(img)[:, :, :3]
        print(x.shape)
        x = np.expand_dims(x, axis=0)
        x = preprocess_input(x)
        preds = model.predict(x)
        print('Predicted:', decode_predictions(preds, top=3)[0])

        #path = os.path.join(app.config['UPLOAD_FOLDER'], file1.filename)
        #file1.save(path)
        bestPred = decode_predictions(preds, top=3)[0][0][1]
        return "Is this a <b>{}</b>?".format(bestPred)
        #return "Predicted: {}".format(decode_predictions(preds, top=3)[0])
    
    return '''
    <h1>Upload new File</h1>
    <form method="post" enctype="multipart/form-data">
      <input type="file" name="file1">
      <input type="submit">
    </form>
    '''
# main driver function
if __name__ == '__main__':
 
    # run() method of Flask class runs the application
    # on the local development server.
    app.run( host='0.0.0.0', port=80 )