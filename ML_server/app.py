from flask import Flask, request, Response
from flask_cors import CORS, cross_origin
import NeuralNet1, NeuralNet2

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

AI1 = NeuralNet1.NeuralNet(None)
AI2 = NeuralNet2.Network(False)
AI2.test_ready()

def get_result(sentence):
    n1_result = AI1.sentiment_predict(sentence, True)
    n2_result = AI2.get_tokenized_sentence(sentence)
    print(n1_result, n2_result)
    if (n1_result + n2_result) / 2 > 0.5:
        return 1
    else:
        return 0



@app.route('/gamsung', methods=['GET', 'POST'])
def get_gamsung():
    if request.method == 'POST':
        get_string = request.json["text"]
        result = get_result(get_string)
        if result == 1:
            print(str(result), " ", get_string)
            return Response('{"result":"1"}', status=200, mimetype='application/json')
        elif result == 0:
            print("-1 ", get_string)
            return Response('{"result":"-1"}', status=200, mimetype='application/json')
    if request.method == 'GET':
        return Response('{"message":"Wrong Access"}', status=400, mimetype='application/json')


if __name__ == '__main__':


    app.run(host='0.0.0.0', port=8080)
