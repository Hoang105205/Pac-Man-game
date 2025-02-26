import pygame
import sys

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
        self.current_level = 0
        self.clicked = False
        self.map_name = []
        self.current_map = 0
        self.done = False
        self.current_screen = 1
        self.screen = screen

        menu_button_width = 150
        menu_button_height = 100

        self.btnStart = Button(WIDTH // 2 - menu_button_width // 2, HEIGHT // (2) + (menu_button_height + 10) * 0 - 50, menu_button_width, menu_button_height, screen, "Start", self.start_function)
        self.btnQuit = Button(WIDTH // 2 - menu_button_width // 2, HEIGHT // (2) + (menu_button_height + 10) * 1, menu_button_width, menu_button_height, screen, "Quit", self.quit_function)
        self.btnLevel1 = Button(WIDTH // 4 - menu_button_width // 2, HEIGHT // (2) + (menu_button_height + 10) * 0 - 50, menu_button_width, menu_button_height, screen, "Level 1")
        self.btnLevel2 = Button(WIDTH // 2 - menu_button_width // 2, HEIGHT // (2) + (menu_button_height + 10) * 0 - 50, menu_button_width, menu_button_height, screen, "Level 2")
        self.btnLevel3 = Button(WIDTH - menu_button_width * 2, HEIGHT // (2) + (menu_button_height + 10) * 0 - 50, menu_button_width, menu_button_height, screen, "Level 3")
        self.btnLevel4 = Button(WIDTH // 4 - menu_button_width // 2, HEIGHT // (2) + (menu_button_height + 10) * 1, menu_button_width, menu_button_height, screen, "Level 4")
        self.btnLevel5 = Button(WIDTH // 2 - menu_button_width // 2, HEIGHT // (2) + (menu_button_height + 10) * 1, menu_button_width, menu_button_height, screen, "Level 5")
        self.btnLevel6 = Button(WIDTH - menu_button_width * 2, HEIGHT // (2) + (menu_button_height + 10) * 1, menu_button_width, menu_button_height, screen, "Level 6")
        self.btnBack = Button(40, HEIGHT // 4 * 3 + 70, 150, 100, screen, "BACK", self.back_function)


    def start_function(self):
        self.current_screen = 2
        self.map_name = []
        self.current_map = 0
        self.current_level = 0

    def quit_function(self):
        pygame.quit()
        sys.exit(0)

    def back_function(self):
        self.current_screen = 1
        self.map_name = []
        self.current_map = 0
        self.current_level = 0

    def run(self):

        while not self.done:
            self.clicked = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit(0)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.clicked = True

            if self.current_screen == 1:
                self.screen.blit(bg, (0, 0))
                self.btnStart.process()
                self.btnQuit.process()

            elif self.current_screen == 2:
                self.screen.blit(bg, (0, 0))
                self.btnLevel1.process()
                self.btnLevel2.process()
                self.btnLevel3.process()
                self.btnLevel4.process()
                self.btnLevel5.process()
                self.btnLevel6.process()
                self.btnBack.process()

            pygame.display.update()  # Cập nhật màn hình



