import tensorflow as tf
import tensorflowjs as tfjs
import numpy as np
import pandas as pd

import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

TRAIN_DATA_URL = "data.csv"

pandaData = pd.read_csv(TRAIN_DATA_URL)
pandaData = pandaData.to_numpy()
pre_train_data = list(pandaData[:, 1])
train_label = pandaData[:, -1]
train_data = []
for i in pre_train_data:
    train_data.append([0, i, 0, 0])

train_data = np.array(train_data)

model = tf.keras.Sequential([
    tf.keras.layers.Dense(16, input_shape=(4,), activation=tf.keras.activations.relu),
    tf.keras.layers.Dense(32, activation=tf.keras.activations.sigmoid),
    tf.keras.layers.Dense(64, activation=tf.keras.activations.relu),
    tf.keras.layers.Dense(30, activation=tf.keras.activations.softmax)
])

model.compile(
    optimizer='adam',
    loss=tf.keras.losses.sparse_categorical_crossentropy,
    metrics=['accuracy']
)

train_data = tf.convert_to_tensor(train_data, dtype=tf.float32)
train_label = tf.convert_to_tensor(train_label, dtype=tf.float32)

epochs = 100
model.fit(train_data,
          train_label,
          epochs=epochs)

predicted_label = np.argmax(model.predict(np.array([[0,-50,0,0]])))
print(predicted_label)

export_dir = 'saved_model/model'

# tf.saved_model.save(model, export_dir)
tfjs.converters.save_keras_model(model, export_dir)
