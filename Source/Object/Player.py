import pygame
from constants import SPRITERATIO, SQUARE
class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.images = [pygame.image.load(f"Object/images/{i}.png") for i in range(1, 5)]  # 4 ảnh từ 1.png đến 4.png
        self.current_frame = 0  # Chỉ số frame hiện tại
        self.image = self.images[self.current_frame]  # Ảnh ban đầu
        self.image = pygame.transform.scale(self.image, (SQUARE * SPRITERATIO, SQUARE * SPRITERATIO))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.animation_speed = 10  # Số frame mỗi lần đổi ảnh
        self.frame_counter = 0  # Đếm số frame để đổi ảnh
    
    def update(self):
        self.frame_counter += 1
        if self.frame_counter >= self.animation_speed:
            self.frame_counter = 0  # Reset đếm frame
            self.current_frame = (self.current_frame + 1) % len(self.images)  # Chuyển ảnh tiếp theo
            self.image = self.images[self.current_frame]  # Cập nhật ảnh

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

    def move(self, dx, dy):
        self.x += dx
        self.y += dy
        self.rect.topleft = (self.x, self.y)

    def collide(self, rect):
        return self.rect.colliderect(rect)
       