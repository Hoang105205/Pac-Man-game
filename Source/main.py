from Object.Menu import Button, Menu, WIDTH, HEIGHT

import pygame


# Initial Pygame --------------------------
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('PacMan')
# -----------------------------------------


from Object.Board import Board
from Object.Algorithm import Algorithm

def main():
    # Chạy menu
    menu = Menu(screen)
    menu.run()
    pygame.quit()

main()