import os
import chess.engine
import numpy as np

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
        return 0
    return max(min(score / 1000.0, 1), -1)

def make_y_train(moveLog):
    y_train=[]
    for x in moveLog:
        try:
            y_train.append(evaluate_fen(x))
        except:
            print(x)
            y_train.append(0)
    return np.array(y_train, dtype=np.float32)

def stock_fish_close():
    engine.quit()
