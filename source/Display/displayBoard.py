from pathlib import Path
import pygame
from .displayPieces import place_pieces
pygame.init()
font = pygame.font.Font(None, 24)
WHTSQ=( 200, 200, 200)
BLKSQ=( 125, 125, 125)
Col=('A','B','C','D','E','F','G','H')
Row=('8','7','6','5','4','3','2','1')
def draw_board(screen,board):
    screen.fill((0,0,0))
    for i in range(8):
        text=font.render(Col[i], True, (255, 255, 255))
        text_rect = text.get_rect(center=(55+i*70, 10))
        screen.blit(text, text_rect)
        text_rect = text.get_rect(center=(55+i*70, 590))
        screen.blit(text, text_rect)
        text=font.render(Row[i], True, (255, 255, 255))
        text_rect = text.get_rect(center=(10, 55+i*70))
        screen.blit(text, text_rect)
        text_rect = text.get_rect(center=(590, 55+i*70))
        screen.blit(text, text_rect)
    for i in range(64):
        x=i//8;y=i%8
        draw_square(screen,(x,y),board)
    pygame.display.flip()
    
def draw_square(screen,sqr,board):
    x=sqr[0]
    y=sqr[1]
    if (x+y)%2==0: screen.fill(WHTSQ,(20+y*70,20+x*70,70,70))
    else: screen.fill(BLKSQ,(20+y*70,20+x*70,70,70))
    if board[x][y]!='.':place_pieces(screen,board,(x,y))
    pygame.display.update(20+y*70,20+x*70,70,70)

def promotion_display(screen):
    screen.fill((255,255,255))
    current_dir = Path(__file__).parent
    image=pygame.image.load(str(current_dir/"Pieces"/"wq.png"))
    image=pygame.transform.scale(image,(300,300))
    screen.blit(image,(0,0))
    image=pygame.image.load(str(current_dir/"Pieces"/"wr.png"))
    image=pygame.transform.scale(image,(300,300))
    screen.blit(image,(300,0))
    image=pygame.image.load(str(current_dir/"Pieces"/"wb.png"))
    image=pygame.transform.scale(image,(300,300))
    screen.blit(image,(0,300))
    image=pygame.image.load(str(current_dir/"Pieces"/"wn.png"))
    image=pygame.transform.scale(image,(300,300))
    screen.blit(image,(300,300))
    pygame.display.flip()