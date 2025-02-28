import pygame
from constants import SIZE_WALL,TILE

class Ghost:
    def __init__(self, x, y, FileImage):
        self.x = x
        self.y = y
        self.image = pygame.image.load(FileImage).convert_alpha()
        self.image = pygame.transform.scale(self.image, (TILE["WIDTH"], TILE["HEIGHT"]))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

    def move(self, dx, dy):
        self.x += dx
        self.y += dy
        self.rect.topleft = (self.x, self.y)

    def collide(self, rect):
        return self.rect.colliderect(rect)
