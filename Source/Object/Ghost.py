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
    
    def check_collision(self, des, Ghost1_path, Ghost1_step, Ghost2_path, Ghost2_step, Ghost3_path, Ghost3_step): 
        if(des == Ghost1_path[Ghost1_step - 1] or des == Ghost2_path[Ghost2_step - 1] or des == Ghost3_path[Ghost3_step - 1]):
            current_position = self.get_position()
            if(Ghost1_step == len(Ghost1_path)):
                Ghost1_step -= 1
            if(Ghost2_step == len(Ghost2_path)):
                Ghost2_step -= 1
            if(Ghost3_step == len(Ghost3_path)):
                Ghost3_step -= 1
            
            # Khi 2 con ma di chuyển vào ô nhau
            if(current_position == Ghost1_path[Ghost1_step] or current_position == Ghost2_path[Ghost2_step] or current_position == Ghost3_path[Ghost3_step]):
                return False
            
            # Khi 2 con ma di chuyển vào ô Pacman
            if(des == Ghost1_path[Ghost1_step] and Ghost1_step == len(Ghost1_path) - 1):
                return False
            if(des == Ghost2_path[Ghost2_step] and Ghost2_step == len(Ghost2_path) - 1):
                return False
            if(des == Ghost3_path[Ghost3_step] and Ghost3_step == len(Ghost3_path) - 1):
                return False
            
            return True
        return False
