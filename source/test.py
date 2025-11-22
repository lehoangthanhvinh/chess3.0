import chess
board=chess.Board("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
for move in board.legal_moves:
    if str(move)=="e2e4":print("check")