import pygame
import sys
from Object.Board import Board
import copy
import math

# Khởi tạo pygame
pygame.init()

# Kích thước màn hình
WIDTH, HEIGHT = 900, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game Menu")

# Load background
background = pygame.image.load("Object/images/home_bg.png")
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

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
            'normal': '#03A9F4',   # Xanh dương nhạt
            'hover': '#0288D1',    # Xanh dương đậm hơn
            'pressed': '#0277BD',  # Xanh biển đậm
        }



        self.buttonSurface = pygame.Surface((self.width, self.height))
        self.buttonRect = pygame.Rect(self.x, self.y, self.width, self.height)

        self.buttonText = font.render(buttonText, True, WHITE)


    def default_function(self):
        print(f"Button '{self.buttonText}' clicked (but no function set)")

    def process(self):
        mousePos = pygame.mouse.get_pos()
        self.buttonSurface.fill(self.fillColors['normal'])

        if self.buttonRect.collidepoint(mousePos):  # Nếu chuột nằm trên nút
            self.buttonSurface.fill(self.fillColors['hover'])
            if pygame.mouse.get_pressed()[0]:  # Nếu nhấn chuột trái
                self.buttonSurface.fill(self.fillColors['pressed'])
                self.onClickFunction()

        # Vẽ chữ lên nút
        self.buttonSurface.blit(self.buttonText, [
            self.buttonRect.width / 2 - self.buttonText.get_width() / 2,
            self.buttonRect.height / 2 - self.buttonText.get_height() / 2
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

        self.menu_button_size = (150, 100)

        self.screen_handlers = {
            1: self.draw_main_menu,
            2: self.draw_level_menu
        }

        self.buttons = {
            "Start": Button(self.center_x(), self.pos_y(0), *self.menu_button_size, screen, "Start", self.start_function),
            "Quit": Button(self.center_x(), self.pos_y(1), *self.menu_button_size, screen, "Quit", self.quit_function),
            "Level1": Button(self.left_x(), self.pos_y(0), *self.menu_button_size, screen, "Level 1", self.load_map_level_1),
            "Level2": Button(self.center_x(), self.pos_y(0), *self.menu_button_size, screen, "Level 2", None),
            "Level3": Button(self.right_x(), self.pos_y(0), *self.menu_button_size, screen, "Level 3", None),
            "Level4": Button(self.left_x(), self.pos_y(1), *self.menu_button_size, screen, "Level 4", None),
            "Level5": Button(self.center_x(), self.pos_y(1), *self.menu_button_size, screen, "Level 5", None),
            "Level6": Button(self.right_x(), self.pos_y(1), *self.menu_button_size, screen, "Level 6", None),
            "Back": Button(40, HEIGHT // 4 * 3 + 70, 150, 100, screen, "BACK", self.back_function)
        }

        self.board = Board()

    # ============ Các hàm hỗ trợ vị trí nút ============
    def center_x(self):
        """Vị trí giữa màn hình theo chiều ngang."""
        return WIDTH // 2 - self.menu_button_size[0] // 2

    def left_x(self):
        """Vị trí 1/4 màn hình."""
        return WIDTH // 4 - self.menu_button_size[0] // 2

    def right_x(self):
        """Vị trí phía bên phải màn hình."""
        return WIDTH - self.menu_button_size[0] * 2

    def pos_y(self, row):
        """Tính vị trí theo hàng dọc."""
        return HEIGHT // 2 + (self.menu_button_size[1] + 10) * row - 50


    # ============ Các hàm xử lý sự kiện ============
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

    def load_map_level_1(self):
        screen.fill((0, 0, 0))
        self.draw_board()
        pygame.display.update()
        pygame.time.wait(3000)


    # ============ Các hàm vẽ màn hình ============
    def draw_main_menu(self):
        self.screen.blit(background, (0, 0))
        self.buttons["Start"].process()
        self.buttons["Quit"].process()

    def draw_level_menu(self):
        self.screen.blit(background, (0, 0))
        self.buttons["Level1"].process()
        self.buttons["Level2"].process()
        self.buttons["Level3"].process()
        self.buttons["Level4"].process()
        self.buttons["Level5"].process()
        self.buttons["Level6"].process()
        self.buttons["Back"].process()

    
    # ============ Hàm chạy chính ============
    def run(self):

        while not self.done:
            self.clicked = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit(0)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.clicked = True

            self.screen_handlers[self.current_screen]()

            pygame.display.update()  # Cập nhật màn hình
            
    # ============ Hàm vẽ bảng ============      
    def draw_board(self):
        level = copy.deepcopy(self.board.grid)
        color = 'blue'
        flicker = False
        PI = math.pi
        num1 = ((HEIGHT - 50) // 32)
        num2 = (WIDTH // 30)
        for i in range(len(level)):
            for j in range(len(level[i])):
                if level[i][j] == 1:
                    pygame.draw.circle(screen, 'white', (j * num2 + (0.5 * num2), i * num1 + (0.5 * num1)), 4)
                if level[i][j] == 2 and not flicker:
                    pygame.draw.circle(screen, 'white', (j * num2 + (0.5 * num2), i * num1 + (0.5 * num1)), 10)
                if level[i][j] == 3:
                    pygame.draw.line(screen, color, (j * num2 + (0.5 * num2), i * num1),
                                    (j * num2 + (0.5 * num2), i * num1 + num1), 3)
                if level[i][j] == 4:
                    pygame.draw.line(screen, color, (j * num2, i * num1 + (0.5 * num1)),
                                    (j * num2 + num2, i * num1 + (0.5 * num1)), 3)
                if level[i][j] == 5:
                    pygame.draw.arc(screen, color, [(j * num2 - (num2 * 0.4)) - 2, (i * num1 + (0.5 * num1)), num2, num1],
                                    0, PI / 2, 3)
                if level[i][j] == 6:
                    pygame.draw.arc(screen, color,
                                    [(j * num2 + (num2 * 0.5)), (i * num1 + (0.5 * num1)), num2, num1], PI / 2, PI, 3)
                if level[i][j] == 7:
                    pygame.draw.arc(screen, color, [(j * num2 + (num2 * 0.5)), (i * num1 - (0.4 * num1)), num2, num1], PI,
                                    3 * PI / 2, 3)
                if level[i][j] == 8:
                    pygame.draw.arc(screen, color,
                                    [(j * num2 - (num2 * 0.4)) - 2, (i * num1 - (0.4 * num1)), num2, num1], 3 * PI / 2,
                                    2 * PI, 3)
                if level[i][j] == 9:
                    pygame.draw.line(screen, 'white', (j * num2, i * num1 + (0.5 * num1)),
                                    (j * num2 + num2, i * num1 + (0.5 * num1)), 3)
        
