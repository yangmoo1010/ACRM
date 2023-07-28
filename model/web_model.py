import numpy as np
import os
import random as rn
import keras.backend as K
import tensorflow as tf
from tensorflow.keras.layers import (Dense, Embedding, 
                                     LayerNormalization, MultiHeadAttention, 
                                     GlobalAveragePooling1D, Flatten)
from tensorflow.keras.optimizers import Adam
from sklearn.model_selection import StratifiedKFold
from sklearn.model_selection import train_test_split
from sklearn import metrics
from tensorflow.keras.models import load_model
from tensorflow.keras.utils import to_categorical


os.environ["PYTHONHASHSEED"] = '0'
np.random.seed(11)
rn.seed(11)
tf.random.set_seed(42)
session_conf = tf.compat.v1.ConfigProto(
      intra_op_parallelism_threads=1,
      inter_op_parallelism_threads=1)
sess = tf.compat.v1.Session(graph=tf.compat.v1.get_default_graph(),config=session_conf)
K.set_session(sess)


class ClassificationModel(tf.keras.Model):
    def __init__(self, num_classes, hidden):
        super(ClassificationModel, self).__init__()

        self.h = hidden
        self.hidden_layers = []
        for i in range(self.h+1):
            self.hidden_layers.append(tf.keras.layers.Dense(64, activation='relu'))
        self.fc = Dense(num_classes, activation='softmax')

    def call(self, inputs):
        
        x = inputs
        for layer in self.hidden_layers:
            x = layer(x)
        outputs = self.fc(x)
        
        return outputs
    
class AntibioticAI():

    @classmethod
    def load_ABCD(cls, fingerprint):
        cls.model_test = ClassificationModel(num_classes=3, hidden=3)

        cls.optimizer_test = Adam(learning_rate=0.001)

        cls.model_test.compile(loss=tf.keras.losses.CategoricalCrossentropy(), 
                        optimizer=cls.optimizer_test, metrics=tf.keras.metrics.CategoricalAccuracy())
        cls.model_test.build((None, len(fingerprint), 334))
        cls.model_test.load_weights("/var/www/html/model/three_my_model.h5")

        cls.probs = []
        cls.risks = []
        for each_ddd in fingerprint:
            if "SORRY" in each_ddd:
                cls.probs.append(each_ddd)
                cls.risks.append(-1)
            else:
                cls.prob = cls.model_test.predict(tf.expand_dims(np.array(each_ddd), axis=0))
                cls.risk_map = np.argmax(cls.prob, axis=1)
                cls.probs.append(list(cls.prob[0]))
                cls.risks.append(list(cls.risk_map)[0])
        return cls.probs, cls.risks
    
