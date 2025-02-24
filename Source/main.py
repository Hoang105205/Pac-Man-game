from Object.Board import Board

import pygame

def config():
    pygame.init()
    WIDTH = 900
    HEIGHT = 950
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    timer = pygame.time.Clock()
    fps = 60
    font = pygame.font.Font('freesansbold.ttf', 20)
    return screen, timer, fps, font


def main():
    screen, timer, fps, font = config()
    run = True
    while run:
        timer
        screen.fill('white')

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        pygame.display.flip()

    pygame.quit()
    
    input("Press Enter to continue...")

main()