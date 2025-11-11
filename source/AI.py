import chess,random
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, Flatten, Dense
import numpy as np

boardTree=None
searchDepth=1
quienceDepth=2

class Node:
    def __init__(self,FENCode,move,cont):
        self.FENCode=FENCode
        self.score=0
        self.response=None
        self.cont=cont
        self.move=move
        self.next=[]
    def update_response(self,move):
        self.response=move


model = Sequential([
    Conv2D(64, 3, activation='relu', padding='same', input_shape=(8, 8, 12)),
    Conv2D(128, 3, activation='relu', padding='same'),
    Conv2D(256, 3, activation='relu', padding='same'),
    Flatten(),
    Dense(256, activation='relu'),
    Dense(1, activation='tanh')
])

def AI_load_weight():
    global model
    try:
        model.load_weights('chess_ai.weights.h5')
        print("Loaded")
    except:pass

def AI_boost(FENCode):
    global boardTree
    newNode=Node(FENCode,None,0)
    boardTree=newNode
    for i in range(searchDepth+1):AI_build(boardTree,0,i)

def AI_build(curNode,depth,maxDepth):
    global model
    playingBoard=chess.Board(curNode.FENCode)
    if playingBoard.is_game_over():
        if playingBoard.result()=="1-0":curNode.score=1
        elif playingBoard.result()=="0-1":curNode.score=-1
        else:curNode.score=0
        return
    curNode.score=AI_rate_board(playingBoard)
    if (depth<maxDepth or (curNode.cont==1 and depth<maxDepth+quienceDepth)):
        if not curNode.next:
            AI_input_take(curNode)
            if depth<maxDepth:
                AI_input_move(curNode)
                curNode.cont=0
        elif depth<maxDepth and curNode.cont==1:
            AI_input_move(curNode)
            curNode.cont=0
        for node in curNode.next:
            AI_build(node,depth+1,maxDepth)
        if curNode.next:
            if is_maxing(curNode.FENCode):curNode.next.sort(key=lambda x:x.score,reverse=True)
            else:curNode.next.sort(key=lambda x:x.score)
            if maxDepth-depth>2:
                curNode.next=curNode.next[:5]
            elif maxDepth-depth>1:
                curNode.next=curNode.next[:7]
            elif maxDepth-depth>0:
                curNode.next=curNode.next[:10]
            curNode.response=curNode.next[0].move
            curNode.score=curNode.next[0].score

def is_maxing(FENCode):
    turn=FENCode.split()[1]
    if turn=='w': return True
    return False

def AI_input_take(curNode):
    playingBoard=chess.Board(curNode.FENCode)
    for move in playingBoard.legal_moves:
        cont=playingBoard.is_capture(move)
        playingBoard.push(move)
        newNode=Node(playingBoard.fen(),move,cont)
        if cont:curNode.next.append(newNode)
        playingBoard.pop()

def AI_input_move(curNode):
    playingBoard=chess.Board(curNode.FENCode)
    for move in playingBoard.legal_moves:
        cont=playingBoard.is_capture(move)
        playingBoard.push(move)
        newNode=Node(playingBoard.fen(),move,cont)
        if not cont:curNode.next.append(newNode)
        playingBoard.pop()

def AI_rate_board(playingBoard):
    x_input=[playingBoard.fen()]
    x_input=AI_input(x_input)
    return model.predict(x_input)[0][0]

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

def AI_to_next_move(moveLog):
    global boardTree
    found=False
    for fen in moveLog:
        if found:
            for node in boardTree.next:
                if node.FENCode==fen:
                    boardTree=node
        if fen==boardTree.FENCode:
            found=True
    if boardTree.FENCode!=moveLog[-1]:
        newNode=Node(moveLog[-1],None,0)
        boardTree=newNode
        print("Not found")
    for i in range(searchDepth+1):AI_build(boardTree,0,i)
    
def AI_response():
    return boardTree.response