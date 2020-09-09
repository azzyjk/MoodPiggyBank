from flask import Flask, render_template, request, Response
from flask_cors import CORS, cross_origin
from MachineLearning import main_2
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

AI = main_2.Network()
AI.test_ready()


@app.route('/gamsung', methods=['GET', 'POST'])
def get_gamsung():
    if request.method == 'POST':
        result = AI.get_tokenized_sentence(request.json["text"])
        if result == 1:
            return Response('{"result":"1"}', status=200, mimetype='application/json')
        elif result == 0:
            return Response('{"result":"-1"}', status=200, mimetype='application/json')
    if request.method == 'GET':
        return Response('{"message":"Wrong Access"}', status=400, mimetype='application/json')


if __name__ == '__main__':

    app.run(host='localhost', port=80)
