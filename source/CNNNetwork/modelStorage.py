from tensorflow.keras.models import Sequential,Model
from tensorflow.keras.layers import Conv2D, Flatten, Dense,InputLayer,\
    BatchNormalization,ReLU,Input,MaxPooling2D,Dropout
#--------------------------------------------------------------
inputs = Input(shape=(8,8,12))

x = Conv2D(64, 3, padding='same')(inputs)
x = BatchNormalization()(x)
x = ReLU()(x)

for _ in range(5):  # 5 residual blocks (tối thiểu)
    skip = x
    x = Conv2D(64, 3, padding='same')(x)
    x = BatchNormalization()(x)
    x = ReLU()(x)
    x = Conv2D(64, 3, padding='same')(x)
    x = BatchNormalization()(x)
    x = x + skip
    x = ReLU()(x)

# POLICY HEAD
p = Conv2D(2, 1)(x)
p = BatchNormalization()(p)
p = ReLU()(p)
p = Flatten()(p)
policy_out = Dense(4096, activation='softmax')(p)

model = Model(inputs, policy_out)
#-----------------------------------------------------------------
model = Sequential([
    InputLayer(input_shape=(8,8,12)),                # Input
    Conv2D(32, (3,3), padding='same', activation='relu'),
    Conv2D(64, (3,3), padding='same', activation='relu'),
    MaxPooling2D((2,2)),                              # => 4x4 spatial
    Dropout(0.2),
    Flatten(),                                        # flatten 4*4*64 = 1024
    Dense(256, activation='relu'),
    Dropout(0.3),
    Dense(1, activation='tanh')                      # output score in [-1,1]
])
#----------------------------------------------------------------
model = Sequential([
    Conv2D(64, 3, activation='relu', padding='same', input_shape=(8, 8, 12)),
    Conv2D(128, 3, activation='relu', padding='same'),
    Conv2D(256, 3, activation='relu', padding='same'),
    Flatten(),
    Dense(256, activation='relu'),
    Dense(1, activation='tanh')
])
#----------------------------------------------------------------
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

p=Conv2D(2,1)(x)
p=BatchNormalization()(p)
p=ReLU(p)
p=Flatten()(p)
outputData=Dense(1968,activation='softmax')(p)
model=Model(inputData,outputData)
