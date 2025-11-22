from tensorflow.keras.models import Sequential,Model
from tensorflow.keras.layers import Conv2D, Flatten, Dense, Input, ReLU, BatchNormalization
import os,sys

inputData=Input(shape=(8,8,12))

x = Conv2D(64, 3, padding='same')(inputData)
x = BatchNormalization()(x)
x = ReLU()(x)

for _ in range(5):
    skip=x
    x=Conv2D(64,3,padding='same')(x)
    x=BatchNormalization()(x)
    x=ReLU()(x)
    x=Conv2D(64,3,padding='same')(x)
    x=BatchNormalization()(x)
    x=x+skip
    x=ReLU()(x)

#Value head
v = Conv2D(1, 1)(x)
v = BatchNormalization()(v)
v = ReLU()(v)
v = Flatten()(v)
value_out = Dense(256, activation='relu')(v)
value_out = Dense(1, activation='tanh')(value_out)

#Policy head
p = Conv2D(2, 1)(x)
p = BatchNormalization()(p)
p = ReLU()(p)
p = Flatten()(p)
policy_out = Dense(1968, activation='softmax')(p)


model=Model(inputData,[value_out,policy_out])

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

def CNN_learn(x_train,y_train,w_train,flag):
    CNN_load()
    if flag == "score":
        model.compile(optimizer='adam', loss=['mean_squared_error', None])
        y = [y_train[0], None]
        w = [w_train[0], None]

    elif flag == "move":
        model.compile(optimizer='adam', loss=[None, 'categorical_crossentropy'])
        y = [None, y_train[1]]
        w = [None, w_train[1]]

    elif flag == "all":
        model.compile(optimizer='adam', loss=['mean_squared_error', 'categorical_crossentropy'])
        y = y_train
        w = w_train
    model.fit(x_train, y, sample_weight=w, epochs=5, batch_size=32)

    loadPath=os.path.join(rootPath,'chess_ai.weights.h5')
    model.save_weights(loadPath)
