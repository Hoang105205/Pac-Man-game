import pygame
from constants import SPRITERATIO, SQUARE, SPRITEOFFSET, SPEED
from Object.Board import Board
import random
import asyncio
class Player:
    def __init__(self):
        
        # Random vị trí ban đầu
        self.board = Board()
        while True:
            self.row_index = random.randint(0, len(self.board.grid) - 1)
            self.col_index = random.randint(0, len(self.board.grid[0]) - 1)
            if self.board.grid[self.row_index][self.col_index] != 3 and self.board.grid[self.row_index][self.col_index] != 4:
                self.x = self.col_index * SQUARE + SPRITEOFFSET
                self.y = self.row_index *  SQUARE + SPRITEOFFSET
                break
            else:
                continue
            
        # Xác định hướng đi ban đầu
        self.rotation_angle = 0
        if self.board.grid[self.row_index][self.col_index - 1] != 3:
            self.direction = "LEFT"
            self.rotation_angle = 180
        elif self.board.grid[self.row_index][self.col_index + 1] != 3:
            self.direction = "RIGHT"
            self.rotation_angle = 0
        elif self.board.grid[self.row_index - 1][self.col_index] != 3:
            self.direction = "UP"
            self.rotation_angle = 90
        elif self.board.grid[self.row_index + 1][self.col_index] != 3:
            self.direction = "DOWN"
            self.rotation_angle = -90

        # Load ảnh
        self.images = [pygame.image.load(f"Object/images/{i}.png").convert_alpha() for i in range(1, 5)]  # 4 ảnh từ 1.png đến 4.png
        self.original_images = [img.copy() for img in self.images] # Sao chép ảnh gốc
        self.current_frame = 0  # Chỉ số frame hiện tại
        self.image = self.images[self.current_frame]  # Ảnh hiện tại
        self.image = pygame.transform.scale(self.image, (int(SQUARE * SPRITERATIO), int(SQUARE * SPRITERATIO)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.x, self.y)
        self.animation_speed = 0.5  # Số frame mỗi lần đổi ảnh
        self.frame_counter = 0  # Đếm số frame để đổi ảnh
        self.rotate() # Xoay ảnh theo hướng đi ban đầu
    
    def update(self):
        self.frame_counter += 1
        if self.frame_counter >= self.animation_speed:
            self.frame_counter = 0  # Reset đếm frame
            self.current_frame = (self.current_frame + 1) % len(self.images)  # Chuyển ảnh tiếp theo
            self.image = self.images[self.current_frame]  # Cập nhật ảnh
            self.rotate()
            self.image = pygame.transform.scale(self.image, (int(SQUARE * SPRITERATIO), int(SQUARE * SPRITERATIO)))

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

    def move(self, screen):
        if self.direction == "LEFT" and self.row_index == 17 and self.col_index == 0:
            self.x = 27 * SQUARE + SPRITEOFFSET
            self.col_index = 27
        elif self.direction == "RIGHT" and self.row_index == 17 and self.col_index == 27:
            self.x = 0 * SQUARE + SPRITEOFFSET
            self.col_index = 0
        else:
            target_x = self.x
            target_y = self.y
            if self.direction == "UP" and self.board.grid[self.row_index - 1][self.col_index] != 3:
                target_y = self.y - SQUARE
                self.row_index -= 1
            elif self.direction == "DOWN" and self.board.grid[self.row_index + 1][self.col_index] != 3:
                target_y = self.y + SQUARE
                self.row_index += 1
            elif self.direction == "LEFT" and self.board.grid[self.row_index][self.col_index - 1] != 3:
                target_x = self.x - SQUARE
                self.col_index -= 1
            elif self.direction == "RIGHT" and self.board.grid[self.row_index][self.col_index + 1] != 3:
                target_x = self.x + SQUARE
                self.col_index += 1
                
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
                self.remove_player(screen)
                self.rect.topleft = (self.x, self.y)
                self.draw(screen)
                pygame.display.update()


    def collide(self, rect):
        return self.rect.colliderect(rect)
    
    def get_position(self):
        return (self.row_index, self.col_index)
    
    def remove_player(self, screen):
        pygame.draw.rect(screen, (0, 0, 0), self.rect)
        
    def change_direction(self, keys):
        if keys == pygame.K_UP and self.board.grid[self.row_index - 1][self.col_index] != 3 and self.direction != "UP":
            self.direction = "UP"
            self.rotation_angle = 90
        elif keys == pygame.K_DOWN and self.board.grid[self.row_index + 1][self.col_index] != 3 and self.direction != "DOWN":
            self.direction = "DOWN"
            self.rotation_angle = -90
        elif keys == pygame.K_LEFT and self.col_index > 0 and self.direction != "LEFT":
            if(self.board.grid[self.row_index][self.col_index - 1] != 3):
                self.direction = "LEFT"
                self.rotation_angle = 180
        elif keys == pygame.K_RIGHT and self.col_index < 27 and self.direction != "RIGHT":
            if(self.board.grid[self.row_index][self.col_index + 1] != 3):
                self.direction = "RIGHT"
                self.rotation_angle = 0
        self.rotate()
                
    def rotate(self):
        self.image = pygame.transform.rotate(self.original_images[self.current_frame], self.rotation_angle)