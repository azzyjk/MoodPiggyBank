from flask import Flask, request, Response
from flask_cors import CORS, cross_origin
import ML_server.ML as ML

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

AI = ML.Network()
AI.test_ready()


@app.route('/gamsung', methods=['GET', 'POST'])
def get_gamsung():
    if request.method == 'POST':
        get_string = request.json["text"]
        result = AI.get_tokenized_sentence(get_string)
        if result == 1:
            print(str(result), " ", get_string)
            return Response('{"result":"1"}', status=200, mimetype='application/json')
        elif result == 0:
            print("-1 ", get_string)
            return Response('{"result":"-1"}', status=200, mimetype='application/json')
    if request.method == 'GET':
        return Response('{"message":"Wrong Access"}', status=400, mimetype='application/json')


if __name__ == '__main__':

    app.run(host='0.0.0.0', port=80)
