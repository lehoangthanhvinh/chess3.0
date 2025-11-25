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
        sqr=0
        for i in fen:
            if i=="/":continue
            elif i==" ":break
            elif i.isdigit():sqr+=int(i)
            else:
                tensor[sqr//8][sqr%8][piece_to_plane[i]]=1.0
                sqr+=1
        output.append(tensor)
    return np.array(output, dtype=np.float32)

def CNN_weight_rate(moveLog,lastBoard):
    if lastBoard.is_seventyfive_moves():
        return 0,moveLog
    weight=1
    if (lastBoard.is_insufficient_material() or lastBoard.is_fivefold_repetition())\
    and len(moveLog)>100:
        return 0,moveLog
    if lastBoard.is_checkmate():
        weight+=1
    if len(moveLog)<=50:
        weight+=2
    elif len(moveLog)<=100:
        weight+=1
    if not lastBoard.is_checkmate():
        if len(moveLog)>250:
            moveLog=moveLog[:250]
        elif len(moveLog)>200:
            moveLog=moveLog[:-50]
        elif len(moveLog)>150:
            moveLog=moveLog[:-30]
    return weight,moveLog

def CNN_take_data(moveLog,lastBoard,flag):
    weight,moveLog=CNN_weight_rate(moveLog,lastBoard)
    if weight==0:return
    x_train=CNN_input_layer(moveLog)
    StockfishResult.stock_fish_boost()
    value_y,policy_y,value_w,policy_w=StockfishResult.make_y_train(moveLog,flag)
    policy_w*=weight
    value_w*=weight
    y_train = [value_y, policy_y]
    w_train = [value_w, policy_w]
    StockfishResult.stock_fish_close()
    CNNTraining.CNN_learn(x_train,y_train,w_train,flag)
