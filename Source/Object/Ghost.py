import pygame
from constants import SPRITERATIO, SQUARE, SPEED, SPRITEOFFSET

class Ghost:
    def __init__(self, x, y, FileImage):
        self.row_index = x
        self.col_index = y
        self.x = y * SQUARE + SPRITEOFFSET
        self.y = x * SQUARE + SPRITEOFFSET
        self.image = pygame.image.load(FileImage).convert_alpha()
        self.image = pygame.transform.scale(self.image, (int(SQUARE * SPRITERATIO), int(SQUARE * SPRITERATIO)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.x, self.y)

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

    def move(self, target_x, target_y, screen):
        if(self.row_index == 17 and self.col_index == 0 and target_y == 27):
            self.col_index = 27
            target_x = 27 * SQUARE + SPRITEOFFSET
            self.x = target_x
            self.remove_ghost(screen)
            self.rect.topleft = (self.x, self.y)
            self.draw(screen)
            pygame.display.update()
        elif(self.row_index == 17 and self.col_index == 27 and target_y == 0):
            self.col_index = 0
            target_x = 0 * SQUARE + SPRITEOFFSET
            self.x = target_x
            self.remove_ghost(screen)
            self.rect.topleft = (self.x, self.y)
            self.draw(screen)
            pygame.display.update()
        else:
            if(self.row_index < target_x):
                self.row_index += 1
            elif(self.row_index > target_x):
                self.row_index -= 1
            if(self.col_index < target_y):
                self.col_index += 1
            elif(self.col_index > target_y):
                self.col_index -= 1
                
            target_x = self.col_index * SQUARE + SPRITEOFFSET
            target_y = self.row_index * SQUARE + SPRITEOFFSET
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
    
    def get_position(self):
        return (self.row_index, self.col_index)
