from flask import Flask, request
from flask.json import jsonify
import numpy as np
import pickle
import base64
import json
from teachable_code import predict_array

app = Flask(__name__)

@app.route('/cam', methods=['POST'])
def post_json():
    data = request.get_json()
#    print(data)
#    print(data["image"], "asdf`")
    decoded_thing = data["image"].encode("ascii")
#    print(decoded_thing)
   
    base64_bytes = base64.b64decode(decoded_thing)
    array = pickle.loads(base64_bytes)
    #array = np.fromstring(decoded_thing, dtype=np.uint8)
    print(array.shape)
    classname, confidence = predict_array(array)
    response_data = {'class': classname[:(len(classname)) - 1], 'confidence': str(confidence)}
    return jsonify(response_data)

if __name__ == '__main__':
    app.run(port=7649)

