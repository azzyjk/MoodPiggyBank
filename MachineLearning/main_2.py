import csv
import tensorflow as tf
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from konlpy.tag import Okt


class Network:
    stopwords = ['의', '가', '이', '은', '들', '는', '좀', '잘', '걍', '과', '도', '를', '으로', '자', '에', '와', '한', '하다']
    tokenizer = Tokenizer(19417, oov_token='OOV')
    okt = Okt()

    def __init__(self):
        # init model
        self.model = tf.keras.Sequential([
            tf.keras.layers.Embedding(19417, 100),
            tf.keras.layers.LSTM(128),
            tf.keras.layers.Dense(units=2, activation='softmax')
        ])
        self.earlyStop = tf.keras.callbacks.EarlyStopping(monitor='val_loss', mode='min', verbose=1, patience=4, restore_best_weights=True)
        self.model_checkpoint = tf.keras.callbacks.ModelCheckpoint(filepath="checkpoint", monitor='val_accuracy', mode='max', verbose=1, save_best_only=True)
        self.model.compile(optimizer='rmsprop', loss='binary_crossentropy', metrics=['accuracy'])
        self.model.summary()

        # init data
        self.train_X, self.train_Y, self.test_X, self.test_Y = self.refine_data()

    def refine_data(self):
        okt = Okt()
        trainfile, testfile = open("./ratings_train.txt"), open("./ratings_test.txt")
        csv_data = [csv.reader(trainfile, delimiter='\t'), csv.reader(testfile, delimiter='\t')]
        result_data = [[], [], [], []]
        i = 0

        for file in csv_data:
            file.__next__()
            for line in file:
                if line[1] == '' or line[2] == '':
                    pass
                else:
                    sentence = okt.morphs(line[1], stem=True)
                    sentence = [word for word in sentence if not word in self.stopwords]
                    result_data[i].append(sentence)             # X
                    result_data[i+1].append(float(line[2]))     # Y
            result_data[i] = self.tokenizer.fit_on_texts(result_data[i])
            result_data[i] = pad_sequences(result_data[i], maxlen=30)
            i += 2

            #  train_X         train_Y         test_X          test_Y
        return result_data[0], result_data[1], result_data[2], result_data[3]



    def train(self):
        self.model.fit(self.train_X, self.train_Y, epochs=15, callbacks=[self.earlyStop, self.model_checkpoint], batch_size=60, validation_split=0.2)
        self.model.save_weights("default_weight.weight")

    def test(self):
        self.model.load_weights("default_weight.weight")
        self.model.evaluate(self.test_X, self.test_Y, batch_size=60, callbacks=[self.earlyStop, self.model_checkpoint])

    def get_tokenized_sentence(self, sentence):
        self.model.load_weights("default_weight.weight")
        sentence = self.okt.morphs(sentence, stem=True)
        sentence = [word for word in sentence if not word in self.stopwords]
        encoded = self.tokenizer.texts_to_sequences([sentence])
        padding_sentence = pad_sequences(encoded, maxlen=30)
        score = self.model.test_step(padding_sentence)
        print(score)


if __name__ == "__main__":
    test = Network()
    test.train()
    test.test()
    test.get_tokenized_sentence("오늘은 날씨가 좋네")

