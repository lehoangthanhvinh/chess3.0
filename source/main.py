import chess,pygame
import os
import AI
from CNNNetwork import CNNProcessor
from Display import displayBoard,displayMove
rootPath=os.path.dirname(os.path.abspath(__file__))
pygame.init()
screen = pygame.display.set_mode((1000,600))
pygame.display.set_caption("Chess Board")
clock = pygame.time.Clock()
file=['a','b','c','d','e','f','g','h']
rank=['8','7','6','5','4','3','2','1']
running=True
try:
    CNNProcessor.init_path(rootPath)
except:pass
def main():
    global running
    [playingBoard,moveLog]=set_starting_board(screen)
    AITurn=[]
    AITurn.append('b')
    AITurn.append('w')
    selected=None
    AI.AI_load_weight()
    AI.AI_boost("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
    while running:
        if playingBoard.fen().split()[1] in AITurn:
            if playingBoard.is_game_over():
                CNNProcessor.CNN_take_data(moveLog)
                [playingBoard,moveLog]=set_starting_board(screen)
                continue
            AI_move(playingBoard,moveLog)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if playingBoard.is_game_over():
                    CNNProcessor.CNN_take_data(moveLog)
                    [playingBoard,moveLog]=set_starting_board(screen)
                    continue
                (y,x)=pygame.mouse.get_pos()
                if x<580 and y<580 and x>20 and y>20 and playingBoard.fen().split()[1] not in AITurn:
                    selected=player_click_move(x,y,selected,playingBoard,moveLog)
                elif y>600:
                    pass

def player_click_move(x,y,selected,playingBoard,moveLog):
    x=(x-20)//70
    y=(y-20)//70
    sqr=file[y]+rank[x]
    if selected and selected!=sqr:
        move=chess.Move.from_uci(selected+sqr)
        moveEx=chess.Move.from_uci(selected+sqr+'q')
        if move in playingBoard.legal_moves or moveEx in playingBoard.legal_moves:
            if moveEx in playingBoard.legal_moves:
                displayBoard.promotion_display(screen)
                move=chess.Move.from_uci(selected+sqr+promotion_handling())
            playingBoard.push(move)
            moveLog.append(playingBoard.fen())
            board=to_2D_array(playingBoard)
            displayBoard.draw_board(screen,board)
            return None
        else:
            move_handling(screen,playingBoard,selected,sqr)
            return sqr
    else:
        move_handling(screen,playingBoard,selected,sqr)
        return sqr

def AI_move(playingBoard,moveLog):
    AI.AI_to_next_move(moveLog)
    move=AI.AI_response()
    playingBoard.push(move)
    moveLog.append(playingBoard.fen())
    board=to_2D_array(playingBoard)
    displayBoard.draw_board(screen,board)

def set_starting_board(screen):
    playingBoard=chess.Board("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
    board=to_2D_array(playingBoard)
    moveLog=["rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"]
    displayBoard.draw_board(screen,board)
    return[playingBoard,moveLog]

def move_handling(screen,playingBoard,selected,sqr):
    board=to_2D_array(playingBoard)
    if selected:
        square=chess.parse_square(selected)
        curMoveList=[m for m in playingBoard.legal_moves if m.from_square==square]
        for move in curMoveList:
            displayBoard.draw_square(screen,(7-(move.to_square//8),move.to_square%8),board)
    takeList=[]
    moveList=[]
    square=chess.parse_square(sqr)
    moves=[m for m in playingBoard.legal_moves if m.from_square==square]
    for move in moves:
        if playingBoard.is_capture(move):
            takeList.append((7-(move.to_square//8),move.to_square%8))
        else:
            moveList.append((7-(move.to_square//8),move.to_square%8))
    displayMove.draw_move(screen,moveList,takeList)

def promotion_handling():
    global running
    promo=[
        ['q','r'],
        ['b','n']
    ]
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                (y,x)=pygame.mouse.get_pos()
                if x<600 and y<600:
                    x=x//300
                    y=y//300
                    return promo[x][y]
            

def to_2D_array(playingBoard):
    array=[['.' for _ in range(8)] for _ in range(8)]
    changeTable={
        'P':'wp', 'N':'wn', 'B':'wb', 'R':'wr', 'Q':'wq', 'K':'wk', 
        'p':'bp', 'n':'bn', 'b':'bb', 'r':'br', 'q':'bq', 'k':'bk'
    }
    for i in range(64):
        piece=playingBoard.piece_at(i)
        if piece:
            array[7-(i//8)][i%8]=changeTable[piece.symbol()]
    return array

main()
