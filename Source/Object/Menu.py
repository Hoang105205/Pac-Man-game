import pygame

# Khởi tạo pygame
pygame.init()

# Kích thước màn hình
WIDTH, HEIGHT = 900, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game Menu")

# Load background
bg = pygame.image.load("Object/images/home_bg.png")
bg = pygame.transform.scale(bg, (WIDTH, HEIGHT))

# Fonts
font = pygame.font.SysFont('Arial', 40)

# Màu sắc
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)


class Button:
    def __init__(self, x, y, width, height, screen, buttonText="Button", onClickFunction=None):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.onClickFunction = onClickFunction if onClickFunction else self.default_function
        self.screen = screen

        self.fillColors = {
            'normal': '#FF4500',
            'hover': '#FF6347',
            'pressed': '#FF7F50',
        }

        self.buttonSurface = pygame.Surface((self.width, self.height))
        self.buttonRect = pygame.Rect(self.x, self.y, self.width, self.height)

        self.buttonSurf = font.render(buttonText, True, WHITE)

    def default_function(self):
        print(f"Button '{self.buttonSurf}' clicked (but no function set)")

    def process(self):
        mousePos = pygame.mouse.get_pos()
        self.buttonSurface.fill(self.fillColors['normal'])

        if self.buttonRect.collidepoint(mousePos):  # Nếu chuột nằm trên nút
            self.buttonSurface.fill(self.fillColors['hover'])
            if pygame.mouse.get_pressed()[0]:  # Nếu nhấn chuột trái
                self.buttonSurface.fill(self.fillColors['pressed'])
                self.onClickFunction()

        # Vẽ chữ lên nút
        self.buttonSurface.blit(self.buttonSurf, [
            self.buttonRect.width / 2 - self.buttonSurf.get_width() / 2,
            self.buttonRect.height / 2 - self.buttonSurf.get_height() / 2
        ])
        pygame.draw.rect(self.buttonSurface, BLUE, (0, 0, self.width, self.height), 5)

        # Hiển thị nút lên màn hình
        self.screen.blit(self.buttonSurface, self.buttonRect)


class Menu:
    def __init__(self, screen):
        self.screen = screen

        menu_button_width = 150
        menu_button_height = 100

        self.btnLevel1 = Button(WIDTH // 2 - menu_button_width // 2, HEIGHT // (2) + (menu_button_height + 10) * 0 - 50, menu_button_width, menu_button_height, screen, "Level 1")
        self.btnLevel2 = Button(WIDTH // 2 - menu_button_width // 2, HEIGHT // (2) + (menu_button_height + 10) * 1 - 50, menu_button_width, menu_button_height, screen, "Level 2")
        self.btnLevel3 = Button(WIDTH // 2 - menu_button_width // 2, HEIGHT // (2) + (menu_button_height + 10) * 2 - 50, menu_button_width, menu_button_height, screen, "Level 3")
        self.btnLevel4 = Button(WIDTH // 2 - menu_button_width // 2, HEIGHT // (2) + (menu_button_height + 10) * 3 - 50, menu_button_width, menu_button_height, screen, "Level 4")


        self.buttons = [self.btnLevel1, self.btnLevel2, self.btnLevel3, self.btnLevel4]

    def run(self):
        running = True
        while running:
            screen.blit(bg, (0, 0))  # Hiển thị background

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            for button in self.buttons:
                button.process()  # Vẽ các nút

            pygame.display.update()  # Cập nhật màn hình



