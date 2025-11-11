from CNNNetwork import StockfishResult,CNNTraining
import chess
import numpy as np
import os
rootPath=os.path.dirname(os.path.abspath(__file__))
def init_path(path):
    global rootPath
    rootPath=path
    try:
        CNNTraining.init_path(rootPath)
    except:pass
    
def CNN_input_layer(moveLog):
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

def CNN_take_data(moveLog):
    x_train=CNN_input_layer(moveLog)
    StockfishResult.stock_fish_boost()
    y_train=StockfishResult.make_y_train(moveLog)
    StockfishResult.stock_fish_close()
    CNNTraining.CNN_learn(x_train,y_train)
