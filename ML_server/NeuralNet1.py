import pickle
import sys
import pandas as pd
import numpy as np
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.optimizers import *
from tensorflow.keras.losses import *
from tensorflow.keras.layers import *
from tensorflow.keras.models import Model

class NeuralNet:

    tokenizer = Tokenizer()

    def __init__(self, filename, fetch_data=False):

        self.model = self.init_neuralnet()

        if fetch_data:
            self.X_train, self.Y_train, self.X_test, self.Y_test = self.get_data()

        if filename is not None:
            self.test_inputdata(filename)
        elif filename is None:
            with open('checkpoint/ML1/tokenizer.pickle', 'rb') as handle:
                self.tokenizer = pickle.load(handle)
            self.model.load_weights('checkpoint/ML1/best_model.h5')
            print("Load model complete")


    def get_data(self):
        train_data = pd.read_table('ratings_train.txt')
        test_data = pd.read_table('ratings_test.txt')

        train_data = NeuralNet.preprocessing(train_data)
        test_data = NeuralNet.preprocessing(test_data)

        X_train = NeuralNet.Token(train_data)
        X_test = NeuralNet.Token(test_data)


        self.tokenizer.fit_on_texts(X_train)
        with open('checkpoint/ML1/tokenizer.pickle', 'wb') as handle:
            pickle.dump(self.tokenizer, handle, protocol=pickle.HIGHEST_PROTOCOL)

        # label 데이터 생성
        Y_train = np.array(train_data['label'])
        Y_test = np.array(test_data['label'])

        X_train, Y_train = NeuralNet.rmEmpty(X_train, Y_train)

        # padding
        X_train = pad_sequences(X_train, maxlen=100, padding='post')
        X_test = pad_sequences(X_test, maxlen=100, padding='post')

        return X_train, Y_train, X_test, Y_test

    def test_inputdata(self, filename):
        # 한 줄에 문장이 하나 있다고 가정,
        # 데이터 형식은 해당 데이터 형식을 따름
        """
        id      document         label
        19238   영화가 재밌네요    1
        1234    재미없어요        0...
        -> 단, predict해야하는 경우 label은 빈칸으로 둠.
        """
        test_data = pd.read_table(filename)
        with open('checkpoint/ML1/tokenizer.pickle', 'rb') as handle:
            self.tokenizer = pickle.load(handle)
        self.model.load_weights('checkpoint/ML1/best_model.h5')
        print("Load tokenizer and model complete, will predict data")

        # print(test_data)
        for i in range(len(test_data)):
            result = self.sentiment_predict(test_data['document'][i])
            test_data.loc[i, ['label']] = result

        test_data.to_csv("result.txt", sep='	', float_format='%.0f')



    def init_neuralnet(self):
        # 하이퍼파라미터는 여기서 조절
        embedding_dim = 256
        hidden_dim = 512
        dropout_rate = 0.6

        # Model
        input = Input(shape=(100,))
        x = Embedding(2542, embedding_dim)(input)
        x = Dropout(dropout_rate)(x)
        x = Conv1D(hidden_dim, 5, padding="same")(x)
        x = BatchNormalization()(x)
        x = LeakyReLU()(x)
        x_res = x
        x = Bidirectional(LSTM(int(hidden_dim / 2), return_sequences=True))(x)
        x = x + x_res
        x = LeakyReLU()(x)
        x = LSTM(hidden_dim, return_sequences=True)(x)
        x = GlobalMaxPool1D()(x)
        x = Dropout(dropout_rate)(x)
        output = Dense(1, activation='sigmoid')(x)

        model = Model(inputs=[input], outputs=output)

        optimizer = Adam(learning_rate=0.001)
        loss_function = BinaryCrossentropy()
        model.compile(optimizer=optimizer, loss=loss_function, metrics=['acc'])
        # model.summary()
        return model

    @staticmethod
    def preprocessing(data):
        data = data.drop_duplicates(subset=['document'])
        data = data.dropna(how='any')
        data['document'] = data['document'].str.replace("[^ㄱ-ㅎㅏ-ㅣ가-힣 ]", "")
        data['document'] = data['document'].replace('', np.nan)
        data = data.dropna(how='any')
        return data

    @staticmethod
    def Token(data):
        now = 0
        res = list()

        print("start token")
        for sentence in data['document']:
            if now % 10000 == 0:
                print(f"token : {now}/{len(data)}")
            now = now + 1
            temp = list()
            for i in range(len(sentence)):
                temp.append(sentence[i])
            res.append(temp)
        print("end token")
        return res

    @staticmethod
    def Tokenizing(data, tokenizer):
        return tokenizer.texts_to_sequences(data)

    @staticmethod
    def rmEmpty(data, label):
        drop_data = [index for index, sentence in enumerate(data) if len(sentence) < 1]
        data = np.delete(data, drop_data, axis=0)
        label = np.delete(label, drop_data, axis=0)
        return data, label

    def sentiment_predict(self, sentence, justone=False):
        word_list = []
        for letter in sentence:
            word_list.append(letter)
        encoded = self.tokenizer.texts_to_sequences([word_list])
        padding_sentence = pad_sequences(encoded, maxlen=100)
        score = float(self.model.predict(padding_sentence))

        if not justone:
            if score > 0.5:
                return 1
            else:
                return 0
        elif justone:
            return score




if __name__ == "__main__":

    nn = NeuralNet(None)
    nn.sentiment_predict("test")

    """
    if len(sys.argv) == 1:
        print("아무 값도 인자로 주지 않았습니다. 프로그램을 종료합니다.")
    elif len(sys.argv) == 2:
        nn = NeuralNet(sys.argv[1])
        print("result.txt로 저장되었습니다.")
    else:
        print("비정상적인 입력입니다. 프로그램을 종료합니다.")
    """