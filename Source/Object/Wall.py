import pygame

from Object.Board import Board
from constants import SQUARE, SPRITEOFFSET



class Wall:
    def __init__(self, board):
        self.walls = []
        for row in range(len(board.grid)):
            for col in range(len(board.grid[0])):
                if board.grid[row][col] == 3:
                    wall_rect = pygame.Rect(SPRITEOFFSET + col * SQUARE, SPRITEOFFSET + row * SQUARE, SQUARE, SQUARE)
                    self.walls.append(wall_rect)

    def check_collision(self, rect):
        return any(wall.colliderect(rect) for wall in self.walls)
