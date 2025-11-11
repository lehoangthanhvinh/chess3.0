import chess
boardTree=None
searchDepth=3
quienceDepth=4

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

def AI_boost(FENCode):
    global boardTree
    newNode=Node(FENCode,None,0)
    boardTree=newNode
    for i in range(searchDepth+1):
        AI_build(boardTree,0,i)
        print(f"After search No {i}")
        AI_print(boardTree,"  ")

def AI_print(curNode,padding):
    print(f"{padding}{curNode.FENCode}")
    for i in curNode.next:
        AI_print(i,padding+"  ")

def AI_build(curNode,depth,maxDepth):
    playingBoard=chess.Board(curNode.FENCode)
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
AI_boost("n6k/2P5/8/8/8/8/2p5/N6K w - - 0 1")