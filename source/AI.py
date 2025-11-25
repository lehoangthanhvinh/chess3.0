import chess,random,listMove
from tensorflow.keras.models import Sequential, Model
from tensorflow.keras.layers import Conv2D, Flatten, Dense, Input, ReLU, BatchNormalization
import numpy as np

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

def AI_load_weight():
    global model
    try:
        model.load_weights('chess_ai.weights.h5')
        print("Loaded")
    except:pass

def AI_rate_board(fen):
    x_input=[fen]
    x_input=AI_input(x_input)
    value,policy=model.predict(x_input)
    return value.flatten()

def AI_rate_multiple_board(boardList):
    if not boardList: return
    x_input=AI_input(boardList)
    value,policy=model.predict(x_input)
    return value.flatten()

def AI_input(moveLog):
    piece_to_plane = {
        'P': 0, 'N': 1, 'B': 2, 'R': 3, 'Q': 4, 'K': 5,
        'p': 6, 'n': 7, 'b': 8, 'r': 9, 'q': 10, 'k': 11
    }
    output=[]
    for fen in moveLog:
        tensor=np.zeros((8, 8, 12), dtype=np.float32)
        board=chess.Board(fen)
        for rank in range(8):
            for file in range(8):
                square = chess.square(file, 7 - rank)
                piece = board.piece_at(square)
                if piece:
                    tensor[rank][file][piece_to_plane[piece.symbol()]]=1.0
                    pass
        output.append(tensor)
    return np.array(output, dtype=np.float32)
    
def AI_response(fen):
    x_input=[fen]
    x_input=AI_input(x_input)
    value,policy=model.predict(x_input)
    policy=policy[0]
    mask=np.zeros(1968)
    moveList=listMove.list_move()
    board=chess.Board(fen)
    move_index_map={move:i for i,move in enumerate(moveList)}
    for move in board.legal_moves:
        move_str=str(move)
        if move_str in move_index_map:
            mask[move_index_map[move_str]]=1
        else:
            print(f"Move not found in list: {move_str}")
    policy=policy*mask
    if policy.sum()==0:
        print("WARNING: Sum=0")
        try:return list(board.legal_moves)[0]
        except:pass
    policy=policy/policy.sum()
    temperature=0.01
    policy=np.power(policy,1/temperature)
    policy=policy/policy.sum()
    best_idx = np.random.choice(len(policy), p=policy)
    return moveList[best_idx]
