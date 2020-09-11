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

    def __init__(self, get_data=False):
        # init model
        self.model = tf.keras.Sequential([
            tf.keras.layers.Dense(units=1000, activation='relu', input_shape=(500, )),
            tf.keras.layers.Dense(units=500, activation='relu'),
            tf.keras.layers.Dense(units=200, activation='relu'),
            tf.keras.layers.Dense(units=20, activation='relu'),
            tf.keras.layers.Dense(units=2, activation='softmax')
        ])
        # self.earlyStop = tf.keras.callbacks.EarlyStopping(monitor='val_loss', mode='min', verbose=1, patience=4, restore_best_weights=True)
        self.model_checkpoint = tf.keras.callbacks.ModelCheckpoint(filepath="checkpoint", monitor='val_accuracy', mode='max', verbose=1, save_best_only=True)
        self.model.compile(optimizer=tf.keras.optimizers.Adagrad(lr=0.2), loss='binary_crossentropy', metrics=['accuracy'])
        self.model.summary()

        if not get_data:
            self.train_X, self.train_Y, self.test_X, self.test_Y = None, None, None, None
        else:
            self.train_X, self.train_Y, self.test_X, self.test_Y = self.refine_data()

    def refine_data(self):
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
                    result_data[i].append(sentence)                     # X
                    result_data[i+1].append(np.eye(2)[int(line[2])])    # Y

                """
                j += 1
                if j == 100:
                    j = 0
                    break
                """
                
            result_data[i+1] = np.array(result_data[i+1])
            i += 2

        # delete empty things
        drop_data = [index for index, sentence in enumerate(result_data[0]) if len(sentence) < 1]
        result_data[0] = np.delete(result_data[0], drop_data, axis=0)
        result_data[1] = np.delete(result_data[1], drop_data, axis=0)

        # save raw_tokenized model (for better, faster use)
        np.save("checkpoint/raw1", result_data[0])
        np.save("checkpoint/raw2", result_data[1])
        np.save("checkpoint/raw3", result_data[2])
        np.save("checkpoint/raw4", result_data[3])

        print("finish tokenized")


        # pad_sequence things
        word2vec = Word2Vec(
            result_data[0],
            sg=1, size=500, window=3, min_count=3, workers=4
        )
        final_train_X, final_test_X = [], []
        for sentence in result_data[0]:
            test = np.zeros([500])
            for word in sentence:
                test += word2vec.wv[word]
            final_train_X.append(test)
        for sentence in result_data[2]:
            test = np.zeros([500])
            for word in sentence:
                test += word2vec.wv[word]
            final_test_X.append(test)
        final_train_X = np.array(final_train_X)
        final_test_X = np.array(final_test_X)

        # saving

        np.save("checkpoint/train_X", final_train_X)
        np.save("checkpoint/train_Y", result_data[1])
        np.save("checkpoint/test_X", final_test_X)
        np.save("checkpoint/test_Y", result_data[3])

            #  train_X         train_Y         test_X          test_Y
        return final_train_X, result_data[1], final_test_X, result_data[3]



    def train(self):
        self.model.fit(self.train_X, self.train_Y, epochs=15, callbacks=[self.model_checkpoint], batch_size=60, validation_split=0.2)

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
    test = Network(True)
    test.train()
    test.test()
    # test.test_ready()
    # test.get_tokenized_sentence("오늘은 날씨가 좋네")
