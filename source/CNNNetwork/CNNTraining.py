from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, Flatten, Dense
import os

model = Sequential([
    Conv2D(64, 3, activation='relu', padding='same', input_shape=(8, 8, 12)),
    Conv2D(128, 3, activation='relu', padding='same'),
    Conv2D(256, 3, activation='relu', padding='same'),
    Flatten(),
    Dense(256, activation='relu'),
    Dense(1, activation='tanh')
])

rootPath=os.path.dirname(os.path.abspath(__file__))
def init_path(path):
    global rootPath
    rootPath=path

def CNN_load():
    try:
        loadPath=os.path.join(rootPath,'chess_ai.weights.h5')
        model.load_weights(loadPath)
        print("Loaded")
    except:pass

def CNN_learn(x_train,y_train):
    CNN_load()
    model.compile(optimizer='adam', loss='mean_squared_error')

    model.fit(x_train, y_train, epochs=5, batch_size=32)

    loadPath=os.path.join(rootPath,'chess_ai.weights.h5')
    model.save_weights(loadPath)
