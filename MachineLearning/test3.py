import csv
import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from konlpy.tag import Okt
from gensim.models.word2vec import Word2Vec
import pickle
import gensim


class Network:
    stopwords = ['의', '가', '이', '은', '들', '는', '좀', '잘', '걍', '과', '도', '를', '으로', '자', '에', '와', '한', '하다']
    okt = Okt()

    def __init__(self, get_data=1):
        # init model
        self.model = tf.keras.Sequential([
            tf.keras.layers.Dense(units=1000, activation='relu', input_shape=(2000,)),
            tf.keras.layers.Dense(units=500, activation='relu'),
            tf.keras.layers.Dense(units=2, activation='softmax')
        ])
        # self.earlyStop = tf.keras.callbacks.EarlyStopping(monitor='val_loss', mode='min', verbose=1, patience=4, restore_best_weights=True)
        self.model_checkpoint = tf.keras.callbacks.ModelCheckpoint(filepath="checkpoint", monitor='val_accuracy',
                                                                   mode='max', verbose=1, save_best_only=True)
        self.model.compile(optimizer=tf.keras.optimizers.Adam(lr=0.5), loss='binary_crossentropy', metrics=['accuracy'])
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
            train_X, train_Y, test_X, test_Y = self.get_embedding(train_X, train_Y, test_X, test_Y)

        elif get_data == 2:
            print("미리 토큰화된 배열을 읽어들인 후 임베딩을 수행합니다.")
            train_X, train_Y, test_X, test_Y = self.get_numpy_array("raw_tokenized")
            train_X, train_Y, test_X, test_Y = self.get_embedding(train_X, train_Y, test_X, test_Y)
        else:
            print("임베딩까지 완료된 데이터셋을 가져옵니다.")
            train_X, train_Y, test_X, test_Y = self.get_numpy_array("word2vec")
        print(train_Y)
        print("처리가 완료되었습니다.")
        return train_X, train_Y, test_X, test_Y

    def get_raw_tokenized(self):
        trainfile, testfile = open("./checkpoint/data/ratings_train.txt"), open("./checkpoint/data/ratings_test.txt")
        csv_data = [csv.reader(trainfile, delimiter='\t'), csv.reader(testfile, delimiter='\t')]
        result_data = [[], [], [], []]
        i, j = 0, 0
        for file in csv_data:
            file.__next__()
            for line in file:
                if line[1] == '' or line[2] == '':
                    pass
                else:
                    sentence = self.okt.morphs(line[1], stem=True)
                    sentence = [word for word in sentence if not word in self.stopwords]
                    result_data[i].append(sentence)  # X
                    result_data[i + 1].append(np.eye(2)[int(line[2])])  # Y

                j += 1
                if j == 100:
                    j = 0
                    break

            result_data[i + 1] = np.array(result_data[i + 1])
            i += 2

        # delete empty things
        drop_data = [index for index, sentence in enumerate(result_data[0]) if len(sentence) < 1]
        result_data[0] = np.delete(result_data[0], drop_data, axis=0)
        result_data[1] = np.delete(result_data[1], drop_data, axis=0)
        trainfile.close()
        testfile.close()

        np.save("checkpoint/raw_tokenized/raw1", result_data[0])
        np.save("checkpoint/raw_tokenized/raw2", result_data[1])
        np.save("checkpoint/raw_tokenized/raw3", result_data[2])
        np.save("checkpoint/raw_tokenized/raw4", result_data[3])

        return result_data[0], result_data[1], result_data[2], result_data[3]

    def get_embedding(self, train_X, train_Y, test_X, test_Y, vector=2000):
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
        np.save("checkpoint/word2vec/train_X", final_train_X)
        np.save("checkpoint/word2vec/train_Y", train_Y)
        np.save("checkpoint/word2vec/test_X", final_test_X)
        np.save("checkpoint/word2vec/test_Y", test_Y)
        return final_train_X, train_Y, final_test_X, test_Y

    def get_numpy_array(self, selection):
        train_X = np.load("checkpoint/" + selection + "/train_X.npy", allow_pickle=True)
        train_Y = np.load("checkpoint/" + selection + "/train_Y.npy", allow_pickle=True)
        test_X = np.load("checkpoint/" + selection + "/test_X.npy", allow_pickle=True)
        test_Y = np.load("checkpoint/" + selection + "/test_Y.npy", allow_pickle=True)
        return train_X, train_Y, test_X, test_Y

    def train(self):
        self.model.fit(self.train_X, self.train_Y, epochs=15, callbacks=[self.model_checkpoint], batch_size=60,
                       validation_split=0.2)

    def test(self):
        self.model.load_weights("checkpoint/variables/variables")
        self.model.evaluate(self.test_X, self.test_Y, batch_size=60, callbacks=[self.model_checkpoint])

    def test_ready(self):
        self.model.load_weights("checkpoint/variables/variables")
        with open('checkpoint/tokenizer.pickle', 'rb') as handle:
            self.tokenizer = pickle.load(handle)

    def get_tokenized_sentence(self, sentence):
        sentence = self.okt.morphs(sentence, stem=True)
        sentence = [word for word in sentence if not word in self.stopwords]
        encoded = self.tokenizer.texts_to_sequences([sentence])
        padding_sentence = pad_sequences(encoded, maxlen=30)
        score = self.model.predict(padding_sentence).argmax()
        # 1이 긍정, 0이 부정
        return score


if __name__ == "__main__":
    test = Network(3)
    test.train()
    test.test()
    # test.test_ready()
    # test.get_tokenized_sentence("오늘은 날씨가 좋네")

