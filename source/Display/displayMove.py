from pathlib import Path
import pygame
pygame.init()
def draw_move(screen,moveList,takeList):
    for move in moveList:
        current_dir = Path(__file__).parent
        image=pygame.image.load(str(current_dir/"Icons"/"Dots.png"))
        image=pygame.transform.scale(image,(50,50))
        imageRect=image.get_rect(center=(55+move[1]*70,55+move[0]*70))
        screen.blit(image, imageRect)
        pygame.display.update(imageRect)
    for move in takeList:
        current_dir = Path(__file__).parent
        image=pygame.image.load(str(current_dir/"Icons"/"Take.png"))
        image=pygame.transform.scale(image,(70,70))
        imageRect=image.get_rect(center=(55+move[1]*70,55+move[0]*70))
        screen.blit(image, imageRect)
        pygame.display.update(imageRect)