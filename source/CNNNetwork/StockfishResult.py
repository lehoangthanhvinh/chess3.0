import os,sys
import chess.engine
import numpy as np
import listMove

base_path = os.path.dirname(os.path.abspath(__file__))
stockfish_path = os.path.join(base_path, "stockfish-windows-x86-64-avx2.exe")
engine=None
def stock_fish_boost():
    global engine
    engine = chess.engine.SimpleEngine.popen_uci(stockfish_path)

def evaluate_fen(fen):
    board = chess.Board(fen)
    info = engine.analyse(board, limit=chess.engine.Limit(depth=10))
    score = info["score"].white().score(mate_score=10000)
    if score is None:
        return 0.0,0.0
    return max(min(score / 1000.0, 1), -1),1.0

def make_y_train(moveLog,flag):
    value_y=[]
    policy_y=[]
    value_w=[]
    policy_w=[]
    for x in moveLog:
        if flag=="all":
            value,weight=evaluate_fen(x)
            value_y.append(value)
            value_w.append(weight)
            policy,weight=make_move(x)
            policy_y.append(policy)
            policy_w.append(weight)
        elif flag=="score":
            value,weight=evaluate_fen(x)
            value_y.append(value)
            value_w.append(weight)
        elif flag=="move":
            policy,weight=make_move(x)
            policy_y.append(policy)
            policy_w.append(weight)
        else:
            print("ERROR: invalid flag")
            sys.exit()
    if value_y:
        value_y = np.array(value_y, dtype=np.float32)
        value_w = np.array(value_w, dtype=np.float32)
    else:
        value_y = None
        value_w = None

    if policy_y:
        policy_y = np.array(policy_y, dtype=np.float32)
        policy_w = np.array(policy_w, dtype=np.float32)
    else:
        policy_y = None
        policy_w = None
    return value_y,policy_y,value_w,policy_w

def make_move(fen):
    weight=1.0
    playingBoard=chess.Board(fen)
    result=np.zeros(1968)
    moveList=listMove.list_move()
    info=engine.analyse(playingBoard, chess.engine.Limit(depth=15,time=0.2), multipv=5)
    if "pv" not in info[0]:
        weight=0.0
        return result,weight
    for pv in info:
        if "pv" not in pv:
            continue
        if str(pv["pv"][0]) in moveList:
            result[moveList.index(str(pv["pv"][0]))]=1/int(pv["multipv"])
        else:
            print("Move not found in list",str(pv["pv"][0]))
            sys.exit()
    if result.sum()!=0:result=result/result.sum()
    return result,weight

def stock_fish_close():
    engine.quit()
