from pathlib import Path
import pygame
pygame.init()
def place_pieces(screen,board,sqr):
    i=sqr[0]
    j=sqr[1]
    piece=board[i][j]
    current_dir = Path(__file__).parent
    image=pygame.image.load(str(current_dir/"Pieces"/f"{piece}.png"))
    image=pygame.transform.scale(image,(50,50))
    imageRect=image.get_rect(center=(55+j*70,55+i*70))
    screen.blit(image, imageRect)