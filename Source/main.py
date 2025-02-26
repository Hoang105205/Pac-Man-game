from Object.Menu import Button, Menu, WIDTH, HEIGHT

import pygame


# Initial Pygame --------------------------
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('PacMan')
clock = pygame.time.Clock()

pygame.font.init()
my_font = pygame.font.SysFont('Comic Sans MS', 30)
my_font_2 = pygame.font.SysFont('Comic Sans MS', 100)


def main():
    # Chạy menu
    menu = Menu(screen)
    menu.run()
    pygame.quit()


main()