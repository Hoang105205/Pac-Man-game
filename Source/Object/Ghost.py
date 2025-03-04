import pygame
from constants import SPRITERATIO, SQUARE, SPEED

class Ghost:
    def __init__(self, x, y, FileImage):
        self.x = x
        self.y = y
        self.image = pygame.image.load(FileImage).convert_alpha()
        self.image = pygame.transform.scale(self.image, (SQUARE * SPRITERATIO, SQUARE * SPRITERATIO))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

    def move(self, target_x, target_y, screen):
        # Di chuyển từng bước nhỏ
        while(self.x, self.y) != (target_x, target_y):
            if self.x < target_x: #qua phải
                self.x += SPEED
            elif self.x > target_x: # qua trái
                self.x -= SPEED
            if self.y < target_y: # xuống
                self.y += SPEED
            elif self.y > target_y: # lên
                self.y -= SPEED
            self.remove_ghost(screen)
            self.rect.topleft = (self.x, self.y)
            self.draw(screen)
            pygame.display.update()

    def remove_ghost(self, screen):
        pygame.draw.rect(screen, (0, 0, 0), self.rect)

    def collide(self, rect):
        return self.rect.colliderect(rect)
