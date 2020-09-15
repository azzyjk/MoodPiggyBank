import csv
import numpy as np
import tensorflow as tf
from gensim.models import Word2Vec
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from konlpy.tag import Okt
import pickle

class Network:
    stopwords = ['의', '가', '이', '은', '들', '는', '좀', '잘', '걍', '과', '도', '를', '으로', '자', '에', '와', '한', '하다']
    tokenizer = Tokenizer(19417, oov_token='OOV')
    okt = Okt()

    def __init__(self, get_data=3):
        """/
        # init model 0번째 모델
        layer1 = tf.keras.layers.Embedding(19417, 200),
        layer2 = tf.keras.layers.GRU(units=128),
        layer3 = tf.keras.layers.Dropout(rate=0.2),
        layer4 = tf.keras.layers.GRU(units=64),
        layer5 = tf.keras.layers.Flatten(),
        layer6 = tf.keras.layers.BatchNormalization(axis=1, epsilon=1.001e-5),
        layer7 = tf.keras.layers.Dropout(rate=0.2),
            # tf.keras.layers.LSTM(units=64, return_sequences=False),

        layer_plus = tf.keras.layers.Add()([layer1, layer2])
        
        layer8 = tf.keras.layers.Dense(units=2, activation='softmax')[layer_plus]
        """

        """ 1번째 모델
        input1 = tf.keras.layers.Input(shape=(30, ))
        x1 = tf.keras.layers.Embedding(19417, 200)(input1)
        x2 = tf.keras.layers.GRU(units=128, return_sequences=True)(x1)
        x2 = tf.keras.layers.GRU(units=64)(x2)
        x2 = tf.keras.layers.Dropout(rate=0.3)(x2)
        x1 = tf.keras.layers.Flatten()(x1)
        x1 = tf.keras.layers.Dense(units=64)(x1)
        added = tf.keras.layers.Add()([x1, x2])
        # x3 = tf.keras.layers.BatchNormalization(axis=1, epsilon=1.001e-5)(added)
        out = tf.keras.layers.Dense(units=2, activation='softmax')(added)
        """

        """ 2번째 모델
        input1 = tf.keras.layers.Input(shape=(30, ))
        x1 = tf.keras.layers.Embedding(19417, 200)(input1)
        x1 = tf.keras.layers.GRU(units=200, return_sequences=True)(x1)
        x1 = tf.keras.layers.GRU(units=100, return_sequences=False)(x1)
        x1 = tf.keras.layers.Dropout(rate=0.3)(x1)
        out = tf.keras.layers.Dense(units=2, activation='softmax')(x1)
        """

        """ 3번째 코드
        input1 = tf.keras.layers.Input(shape=(30, ))
        x1 = tf.keras.layers.Embedding(19417, 200)(input1)
        x2 = tf.keras.layers.LSTM(units=200, return_sequences=True)(x1)
        x1 = tf.keras.layers.Add()([x1, x2])
        x1 = tf.keras.layers.Flatten()(x1)
        out = tf.keras.layers.Dense(units=2, activation='softmax')(x1)
        """
    
        """    # 4번째 코드 (basic)
        input1 = tf.keras.layers.Input(shape=(30, ))
        x1 = tf.keras.layers.Embedding(19417, 200)(input1)
        x1 = tf.keras.layers.LSTM(128)(x1)
        out = tf.keras.layers.Dense(2, activation='softmax')(x1)
        """
        """# 5번째 코드
        input1 = tf.keras.layers.Input(shape=(30,))
        x = tf.keras.layers.Embedding(19417, 200)(input1)
        x = tf.keras.layers.Dropout(rate=0.5)(x)
        
        x1 = tf.keras.layers.Conv1D(filters=128, kernel_size=3, padding="valid", activation="relu", strides=1)(x)
        x1 = tf.keras.layers.GlobalMaxPooling1D()(x1)
        x1 = tf.keras.layers.Flatten()(x1)

        x2 = tf.keras.layers.Conv1D(filters=128, kernel_size=3, padding="valid", activation="relu", strides=1)(x)
        x2 = tf.keras.layers.GlobalMaxPooling1D()(x2)
        x2 = tf.keras.layers.Flatten()(x2)

        x3 = tf.keras.layers.Conv1D(filters=128, kernel_size=3, padding="valid", activation="relu", strides=1)(x)
        x3 = tf.keras.layers.GlobalMaxPooling1D()(x3)
        x3 = tf.keras.layers.Flatten()(x3)

        x = tf.keras.layers.Concatenate()([x1, x2, x3])
        x = tf.keras.layers.Dropout(rate=0.8)(x)
        x = tf.keras.layers.Dense(128)(x)
        out = tf.keras.layers.Dense(2, activation="softmax")(x)"""

        # 6번째 코드
        input1 = tf.keras.layers.Input(shape=(30,))
        x = tf.keras.layers.Embedding(2979, 200)(input1)
        x = tf.keras.layers.Dropout(rate=0.5)(x)

        x = tf.keras.layers.Conv1D(filters=200, kernel_size=3, padding="valid", activation="relu", strides=1)(x)
        x1 = tf.keras.layers.BatchNormalization(epsilon=1.001e-5)(x)
        x1 = tf.keras.layers.Activation('relu')(x1)

        x = tf.keras.layers.Add()([x, x1])
        x = tf.keras.layers.Activation('relu')(x)

        x = tf.keras.layers.Conv1D(filters=100, kernel_size=3, padding="valid", activation="relu", strides=1)(x)
        x2 = tf.keras.layers.BatchNormalization(epsilon=1.001e-5)(x)
        x2 = tf.keras.layers.Activation('relu')(x2)

        x = tf.keras.layers.Add()([x, x2])
        x = tf.keras.layers.Activation('relu')(x)

        x = tf.keras.layers.Conv1D(filters=50, kernel_size=3, padding="valid", activation="relu", strides=1)(x)
        x3 = tf.keras.layers.BatchNormalization(epsilon=1.001e-5)(x)
        x3 = tf.keras.layers.Activation('relu')(x3)

        x = tf.keras.layers.Add()([x, x3])
        x = tf.keras.layers.Activation('relu')(x)

        x = tf.keras.layers.Dropout(rate=0.5)(x)
        x = tf.keras.layers.Flatten()(x)
        # x = tf.keras.layers.Dense(300, 'relu')(x)
        out = tf.keras.layers.Dense(2, activation='softmax')(x)

        self.model = tf.keras.models.Model(inputs=[input1], outputs=out)
        self.earlyStop = tf.keras.callbacks.EarlyStopping(monitor='val_loss', mode='min', verbose=1, patience=4, restore_best_weights=True)
        self.model_checkpoint = tf.keras.callbacks.ModelCheckpoint(filepath="checkpoint", monitor='val_accuracy', mode='max', verbose=1, save_best_only=True)
        self.model.compile(optimizer='rmsprop', loss='binary_crossentropy', metrics=['accuracy'])
        self.model.summary()

        if not get_data:
            self.train_X, self.train_Y, self.test_X, self.test_Y = None, None, None, None
        else:
            self.train_X, self.train_Y, self.test_X, self.test_Y = self.refine_data(get_data)

    def refine_data(self, get_data=1):
        """
        :param get_raw: 데이터를 어느 방식까지 처리된 것을 불러오고, 나머지를 자동화할 것인지
                1일 경우에는 처음부터 끝까지 처리를 시작한다. (파일에서 읽어서 전처리 후 임베딩까지)
                2일 경우에는 임베딩만 수행한다 (토크나이즈 된 배열을 읽어들여와 임베딩만 처리)
                3일 경우에는 정제된 데이터셋만 넘겨준다 (train, test 저장된 데이터셋을 그냥 넘겨준다)
        :return: train, test 데이터
        """

        # get raw data
        if get_data == 1:
            print("파일에서 직접 읽어들인 후 임베딩까지 수행합니다.")
            train_X, train_Y, test_X, test_Y = self.get_raw_tokenized()
            train_X, train_Y, test_X, test_Y = self.get_embedding_tfTokenizer(train_X, train_Y, test_X, test_Y)

        elif get_data == 2:
            print("미리 토큰화된 배열을 읽어들인 후 임베딩을 수행합니다.")
            train_X, train_Y, test_X, test_Y = Network.get_numpy_array("raw_tokenized")
            train_X, train_Y, test_X, test_Y = self.get_embedding_tfTokenizer(train_X, train_Y, test_X, test_Y)
        else:
            print("임베딩까지 완료된 데이터셋을 가져옵니다.")
            train_X, train_Y, test_X, test_Y = Network.get_numpy_array("tfTokenizer")
        print("처리가 완료되었습니다.")
        return train_X, train_Y, test_X, test_Y

    def get_raw_tokenized(self):
        trainfile, testfile = open("checkpoint/data/ratings_train.txt", encoding='UTF8'), open("checkpoint/data/ratings_test.txt", encoding='UTF8')
        # Naver sentimental movie corpus에 있는 데이터를 로컬에 미리 저장한 후 긁어옵니다. 원본은 커밋하지 않았습니다.

        csv_data = [csv.reader(trainfile, delimiter='\t'), csv.reader(testfile, delimiter='\t')]
        result_data = [[], [], [], []]
        i, j = 0, 0
        print(csv_data[0])
        for file in csv_data:
            file.__next__()
            for line in file:
                if line[1] == '' or line[2] == '':
                    pass
                else:
                    word_list = []
                    line[1] = line[1].replace("[^ㄱ-ㅎㅏ-ㅣ가-힣 ]", "")
                    for letter in line[1]:
                        word_list.append(letter)
                    result_data[i].append(word_list)  # X
                    result_data[i + 1].append(np.eye(2)[int(line[2])])  # Y
            result_data[i + 1] = np.array(result_data[i + 1])
            i += 2

        # delete empty things
        drop_data = [index for index, sentence in enumerate(result_data[0]) if len(sentence) < 1]
        result_data[0] = np.delete(result_data[0], drop_data, axis=0)
        result_data[1] = np.delete(result_data[1], drop_data, axis=0)
        trainfile.close()
        testfile.close()

        Network.save_numpy_array("raw_tokenized", result_data[0], result_data[1], result_data[2], result_data[3])

        return result_data[0], result_data[1], result_data[2], result_data[3]

    def get_embedding_W2V(self, train_X, train_Y, test_X, test_Y, vector=2000):
        word2vec = Word2Vec(
            train_X,
            sg=1, size=vector, window=3, min_count=3, workers=4
        )
        final_train_X, final_test_X = [], []
        a, b, c = 0, 0, 0
        test2 = np.zeros([vector])

        print("데이터 다듬기 시작")
        for sentence in train_X:
            test = np.zeros([vector])

            for word in sentence:
                try:
                    test += word2vec.wv[word]
                    a += 1
                except KeyError:
                    b += 1
            if (test == test2).all():
                c += 1
            final_train_X.append(test)
        for sentence in test_X:
            test = np.zeros([vector])
            for word in sentence:
                try:
                    test += word2vec.wv[word]
                    a += 1
                except KeyError:
                    b += 1
            if (test == test2).all():
                c += 1
            final_test_X.append(test)
        final_train_X = np.array(final_train_X)
        final_test_X = np.array(final_test_X)

        final_train_X = (final_train_X - final_train_X.min()) / (final_train_X.min() - final_train_X.max())
        final_test_X = (final_test_X - final_test_X.min()) / (final_test_X.min() - final_test_X.max())

        print(a, b, c)

        # exit()
        # saving
        Network.save_numpy_array("word2vec", final_test_X, train_Y, final_test_X, test_Y)
        return final_train_X, train_Y, final_test_X, test_Y

    def get_embedding_tfTokenizer(self, train_X, train_Y, test_X, test_Y):

        # pad_sequence things
        self.tokenizer.fit_on_texts(train_X)
        train_X = pad_sequences(self.tokenizer.texts_to_sequences(train_X), maxlen=30)
        test_X = pad_sequences(self.tokenizer.texts_to_sequences(test_X), maxlen=30)

        # saving
        with open('tokenizer.pickle', 'wb') as handle:
            pickle.dump(self.tokenizer, handle, protocol=pickle.HIGHEST_PROTOCOL)
        Network.save_numpy_array("tfTokenizer", train_X, train_Y, test_X, test_Y)

            #  train_X         train_Y         test_X          test_Y
        return train_X, train_Y, test_X, test_Y

    @staticmethod
    def get_numpy_array(selection):
        train_X = np.load("checkpoint/" + selection + "/train_X.npy", allow_pickle=True)
        train_Y = np.load("checkpoint/" + selection + "/train_Y.npy", allow_pickle=True)
        test_X = np.load("checkpoint/" + selection + "/test_X.npy", allow_pickle=True)
        test_Y = np.load("checkpoint/" + selection + "/test_Y.npy", allow_pickle=True)
        return train_X, train_Y, test_X, test_Y

    @staticmethod
    def save_numpy_array(selection, train_X, train_Y, test_X, test_Y):
        np.save("checkpoint/" + selection + "/train_X.npy", train_X)
        np.save("checkpoint/" + selection + "/train_Y.npy", train_Y)
        np.save("checkpoint/" + selection + "/test_X.npy", test_X)
        np.save("checkpoint/" + selection + "/test_Y.npy", test_Y)





    def train(self):
        self.model.fit(self.train_X, self.train_Y, epochs=15, callbacks=[self.earlyStop, self.model_checkpoint], batch_size=60, validation_split=0.2)

    def test(self):
        self.model.load_weights("checkpoint/variables/variables")
        self.model.evaluate(self.test_X, self.test_Y, batch_size=60, callbacks=[self.model_checkpoint])

    def test_ready(self):
        self.model.load_weights("checkpoint/variables/variables")
        with open('checkpoint/tokenizer.pickle', 'rb') as handle:
            self.tokenizer = pickle.load(handle)

    def get_tokenized_sentence(self, sentence):
        word_list = []
        sentence = sentence.replace("[^ㄱ-ㅎㅏ-ㅣ가-힣 ]", "")
        for word in sentence:
            word_list.append(word)
        encoded = self.tokenizer.texts_to_sequences([word_list])
        padding_sentence = pad_sequences(encoded, maxlen=30)
        print(padding_sentence)
        score = self.model.predict(padding_sentence)
        print(score)
        # 1이 긍정, 0이 부정
        return score.argmax()


if __name__ == "__main__":
    test = Network(3)

    tf.keras.utils.plot_model(test.model, to_file="test.png", show_shapes=True)

    # test.train()
    # test.test()
    # test.test_ready()
    # print(test.get_tokenized_sentence("오늘은 날씨가 좋네"))

