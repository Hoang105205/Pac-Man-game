import pygame
import sys
from Object.Board import Board
from Object.Player import Player
import copy
import math
from constants import EMPTY, FOOD, GHOST, START_X, START_Y, BOARD_HEIGHT, BOARD_WIDTH, SQUARE
from Object.Ghost import Ghost

# ============ Class Algorithm ============
from Object.Algorithm import Algorithm



# Khởi tạo pygame
pygame.init()

# Kích thước màn hình
WIDTH, HEIGHT = BOARD_WIDTH * SQUARE, BOARD_HEIGHT * SQUARE
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
        self.clicked = False

        self.fillColors = {
            'normal': '#03A9F4',   # Xanh dương nhạt
            'hover': '#0288D1',    # Xanh dương đậm hơn
            'pressed': '#0277BD',  # Xanh biển đậm
        }



        self.buttonSurface = pygame.Surface((self.width, self.height))
        self.buttonRect = pygame.Rect(self.x, self.y, self.width, self.height)

        self.buttonText = font.render(buttonText, True, WHITE)


    def default_function(self):
        print(f"Button {self.buttonText} clicked (but no function set)")

    def process(self):
        mousePos = pygame.mouse.get_pos()
        self.buttonSurface.fill(self.fillColors['normal'])

        if self.buttonRect.collidepoint(mousePos):  # Nếu chuột nằm trên nút
            self.buttonSurface.fill(self.fillColors['hover'])
            

            if not pygame.mouse.get_pressed()[0] and self.clicked == True:  # Khi chuột NHẢ, thực thi hàm
                self.buttonSurface.fill(self.fillColors['pressed'])
                self.onClickFunction()
                self.clicked = False  # Reset trạng thái click để tránh double-click
            # Khi chuột NHẤN, đánh dấu là đã click
            elif pygame.mouse.get_pressed()[0]:
                self.clicked = True

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
            "Level1": Button(self.left_x(), self.pos_y(0), *self.menu_button_size, screen, "Level 1", self.level_1_ingame),
            "Level2": Button(self.center_x(), self.pos_y(0), *self.menu_button_size, screen, "Level 2", self.level_2_ingame),
            "Level3": Button(self.right_x(), self.pos_y(0), *self.menu_button_size, screen, "Level 3", self.level_3_ingame),
            "Level4": Button(self.left_x(), self.pos_y(1), *self.menu_button_size, screen, "Level 4", self.level_4_ingame),
            "Level5": Button(self.center_x(), self.pos_y(1), *self.menu_button_size, screen, "Level 5", self.level_5_ingame),
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
        return WIDTH - self.menu_button_size[0] * 1.5

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

    def level_1_ingame(self):
        # main_board = copy.deepcopy(self.board.grid) # Sao chép bảng để tránh thay đổi bảng gốc

        board = Board()
        main_board = copy.deepcopy(board.grid_algorithm)
        
        # --------------- Vị trí ban đầu của Pacman và Ghost ---------------
        i_ghost = 17
        j_ghost = 14
        spawn_ghost = (j_ghost, i_ghost)
        Pacman = Player(0,0)
        spawn_pacman = Pacman.random_spawn()
        Ghost1 = Ghost(spawn_ghost[0] * SQUARE + START_X, spawn_ghost[1] * SQUARE + START_Y, "Object/images/Inky.png")

        # --------------- Vẽ bảng ---------------
        screen.fill((0, 0, 0))
        self.draw_board()

        Pacman.draw(screen)
        Ghost1.draw(screen)

        pygame.display.update()

        # --------------- Game loop ---------------
        start = (i_ghost, j_ghost)
        end = spawn_pacman

        algorithm = Algorithm()
        result = algorithm.BFS(main_board, start, end)

        if result is not None:
            for i in range(len(result)):
                target_y = result[i][0] * SQUARE + START_Y
                target_x = result[i][1] * SQUARE + START_X

                Ghost1.move(target_x, target_y)

                # Vẽ lại màn hình
                screen.fill((0, 0, 0))
                self.draw_board()
                Pacman.draw(screen)
                Ghost1.draw(screen)
                pygame.display.update()

        pygame.time.wait(3000)
    
    
    def level_2_ingame(self):
        # main_board = copy.deepcopy(self.board.grid) # Sao chép bảng để tránh thay đổi bảng gốc

        board = Board()
        main_board = copy.deepcopy(board.grid_algorithm)
        
        # --------------- Vị trí ban đầu của Pacman và Ghost ---------------
        i_ghost = 17
        j_ghost = 14
        spawn_ghost = (j_ghost, i_ghost)
        Pacman = Player(0,0)
        spawn_pacman = Pacman.random_spawn()
        Ghost1 = Ghost(spawn_ghost[0] * SQUARE + START_X, spawn_ghost[1] * SQUARE + START_Y, "Object/images/Pinky.png")

        # --------------- Vẽ bảng ---------------
        screen.fill((0, 0, 0))
        self.draw_board()

        Pacman.draw(screen)
        Ghost1.draw(screen)

        pygame.display.update()

        # --------------- Game loop ---------------
        start = (i_ghost, j_ghost)
        end = spawn_pacman

        algorithm = Algorithm()
        result = algorithm.DFS(main_board, start, end, path = None)

        if result is not None:
            for i in range(len(result)):
                target_y = result[i][0] * SQUARE + START_Y
                target_x = result[i][1] * SQUARE + START_X

                Ghost1.move(target_x, target_y)

                # Vẽ lại màn hình
                screen.fill((0, 0, 0))
                self.draw_board()
                Pacman.draw(screen)
                Ghost1.draw(screen)
                pygame.display.update()

        pygame.time.wait(3000)
    
    
    def level_3_ingame(self):
         # main_board = copy.deepcopy(self.board.grid) # Sao chép bảng để tránh thay đổi bảng gốc

        board = Board()
        main_board = copy.deepcopy(board.grid_algorithm)
        
        # --------------- Vị trí ban đầu của Pacman và Ghost ---------------
        
        i_ghost = 17
        j_ghost = 14
        spawn_ghost = (j_ghost, i_ghost)
        Pacman = Player(0,0)
        spawn_pacman = Pacman.random_spawn()
        Ghost1 = Ghost(spawn_ghost[0] * SQUARE + START_X, spawn_ghost[1] * SQUARE + START_Y, "Object/images/Clyde.png")

        # --------------- Vẽ bảng ---------------
        screen.fill((0, 0, 0))
        self.draw_board()

        Pacman.draw(screen)
        Ghost1.draw(screen)

        pygame.display.update()

        # --------------- Game loop ---------------
        start = (i_ghost, j_ghost)
        end = spawn_pacman

        algorithm = Algorithm()
        result = algorithm.UCS(main_board, start, end)

        if result is not None:
            for i in range(len(result)):
                target_y = result[i][0] * SQUARE + START_Y
                target_x = result[i][1] * SQUARE + START_X

                Ghost1.move(target_x, target_y)

                # Vẽ lại màn hình
                screen.fill((0, 0, 0))
                self.draw_board()
                Pacman.draw(screen)
                Ghost1.draw(screen)
                pygame.display.update()

        pygame.time.wait(3000)
    
    
    def level_4_ingame(self):
         # main_board = copy.deepcopy(self.board.grid) # Sao chép bảng để tránh thay đổi bảng gốc

        board = Board()
        main_board = copy.deepcopy(board.grid_algorithm)
        
        # --------------- Vị trí ban đầu của Pacman và Ghost ---------------
        
        i_ghost = 17
        j_ghost = 14
        spawn_ghost = (j_ghost, i_ghost)
        Pacman = Player(0,0)
        spawn_pacman = Pacman.random_spawn()
        Ghost1 = Ghost(spawn_ghost[0] * SQUARE + START_X, spawn_ghost[1] * SQUARE + START_Y, "Object/images/Blinky.png")

        # --------------- Vẽ bảng ---------------
        screen.fill((0, 0, 0))
        self.draw_board()

        Pacman.draw(screen)
        Ghost1.draw(screen)

        pygame.display.update()

        # --------------- Game loop ---------------
        start = (i_ghost, j_ghost)
        end = spawn_pacman

        algorithm = Algorithm()
        result = algorithm.ASTAR(main_board, start, end)

        if result is not None:
            for i in range(len(result)):
                target_y = result[i][0] * SQUARE + START_Y
                target_x = result[i][1] * SQUARE + START_X

                Ghost1.move(target_x, target_y)

                # Vẽ lại màn hình
                screen.fill((0, 0, 0))
                self.draw_board()
                Pacman.draw(screen)
                Ghost1.draw(screen)
                pygame.display.update()

        pygame.time.wait(3000)
        
    
    def level_5_ingame(self):
         # main_board = copy.deepcopy(self.board.grid) # Sao chép bảng để tránh thay đổi bảng gốc

        board = Board()
        main_board = copy.deepcopy(board.grid_algorithm)
        
        # --------------- Vị trí ban đầu của Pacman và Ghost ---------------
        
        #Blue Ghost
        i_blue_ghost = 16
        j_blue_ghost = 15
        
        #Pink Ghost
        i_pink_ghost = 16
        j_pink_ghost = 12
        
        #Orange Ghost
        i_orange_ghost = 17
        j_orange_ghost = 15
        
        #Red Ghost
        i_red_ghost = 17
        j_red_ghost = 12
        
        spawn_blue_ghost = (j_blue_ghost, i_blue_ghost)
        spawn_pink_ghost = (j_pink_ghost, i_pink_ghost)
        spawn_orange_ghost = (j_orange_ghost, i_orange_ghost)
        spawn_red_ghost = (j_red_ghost, i_red_ghost)
        
        Pacman = Player(0,0)
        spawn_pacman = Pacman.random_spawn()
        Blue_Ghost = Ghost(spawn_blue_ghost[0] * SQUARE + START_X, spawn_blue_ghost[1] * SQUARE + START_Y, "Object/images/Inky.png")
        Pink_Ghost = Ghost(spawn_pink_ghost[0] * SQUARE + START_X, spawn_pink_ghost[1] * SQUARE + START_Y, "Object/images/Pinky.png")
        Orange_Ghost = Ghost(spawn_orange_ghost[0] * SQUARE + START_X, spawn_orange_ghost[1] * SQUARE + START_Y, "Object/images/Clyde.png")
        Red_Ghost = Ghost(spawn_red_ghost[0] * SQUARE + START_X, spawn_red_ghost[1] * SQUARE + START_Y, "Object/images/Blinky.png")

        # --------------- Vẽ bảng ---------------
        screen.fill((0, 0, 0))
        self.draw_board()

        Pacman.draw(screen)
        Blue_Ghost.draw(screen)
        Pink_Ghost.draw(screen)
        Orange_Ghost.draw(screen)
        Red_Ghost.draw(screen)

        pygame.display.update()

        # --------------- Game loop ---------------
        Blue_start = (i_blue_ghost, j_blue_ghost)
        Pink_start = (i_pink_ghost, j_pink_ghost)
        Orange_start = (i_orange_ghost, j_orange_ghost)
        Red_start = (i_red_ghost, j_red_ghost)
        end = spawn_pacman

        algorithm = Algorithm()
        Blue_result = algorithm.BFS(main_board, Blue_start, end)
        Pink_result = algorithm.DFS(main_board, Pink_start, end, path = None)
        Orange_result = algorithm.UCS(main_board, Orange_start, end)
        Red_result = algorithm.ASTAR(main_board, Red_start, end)
        max_length = max(len(Blue_result), len(Pink_result), len(Orange_result), len(Red_result))

        if Blue_result is not None or Pink_result is not None or Orange_result is not None or Red_result is not None:
            for i in range(max_length):
                if i < len(Blue_result):
                    target_y = Blue_result[i][0] * SQUARE + START_Y
                    target_x = Blue_result[i][1] * SQUARE + START_X
                    Blue_Ghost.move(target_x, target_y)
                    
                if i < len(Pink_result):
                    target_y = Pink_result[i][0] * SQUARE + START_Y
                    target_x = Pink_result[i][1] * SQUARE + START_X
                    Pink_Ghost.move(target_x, target_y)
                    
                if i < len(Orange_result):
                    target_y = Orange_result[i][0] * SQUARE + START_Y
                    target_x = Orange_result[i][1] * SQUARE + START_X
                    Orange_Ghost.move(target_x, target_y)
                    
                if i < len(Red_result):
                    target_y = Red_result[i][0] * SQUARE + START_Y
                    target_x = Red_result[i][1] * SQUARE + START_X
                    Red_Ghost.move(target_x, target_y)

                # Vẽ lại màn hình
                screen.fill((0, 0, 0))
                self.draw_board()
                Pacman.draw(screen)
                Blue_Ghost.draw(screen)
                Pink_Ghost.draw(screen)
                Orange_Ghost.draw(screen)
                Red_Ghost.draw(screen)
                pygame.display.update()

        pygame.time.wait(3000)
        
       # ============ Dang hoan thien ============ 
    # def level_6_ingame(self):
    #      # main_board = copy.deepcopy(self.board.grid) # Sao chép bảng để tránh thay đổi bảng gốc

    #     board = Board()
    #     main_board = copy.deepcopy(board.grid_algorithm)
        
    #     # --------------- Vị trí ban đầu của Pacman và Ghost ---------------
        
    #     #Blue Ghost
    #     i_blue_ghost = 16
    #     j_blue_ghost = 15
        
    #     #Pink Ghost
    #     i_pink_ghost = 16
    #     j_pink_ghost = 12
        
    #     #Orange Ghost
    #     i_orange_ghost = 17
    #     j_orange_ghost = 15
        
    #     #Red Ghost
    #     i_red_ghost = 17
    #     j_red_ghost = 12
        
    #     spawn_blue_ghost = (j_blue_ghost, i_blue_ghost)
    #     spawn_pink_ghost = (j_pink_ghost, i_pink_ghost)
    #     spawn_orange_ghost = (j_orange_ghost, i_orange_ghost)
    #     spawn_red_ghost = (j_red_ghost, i_red_ghost)
        
    #     Pacman = Player(0,0)
    #     spawn_pacman = Pacman.random_spawn()
    #     Blue_Ghost = Ghost(spawn_blue_ghost[0] * SQUARE + START_X, spawn_blue_ghost[1] * SQUARE + START_Y, "Object/images/Inky.png")
    #     Pink_Ghost = Ghost(spawn_pink_ghost[0] * SQUARE + START_X, spawn_pink_ghost[1] * SQUARE + START_Y, "Object/images/Pinky.png")
    #     Orange_Ghost = Ghost(spawn_orange_ghost[0] * SQUARE + START_X, spawn_orange_ghost[1] * SQUARE + START_Y, "Object/images/Clyde.png")
    #     Red_Ghost = Ghost(spawn_red_ghost[0] * SQUARE + START_X, spawn_red_ghost[1] * SQUARE + START_Y, "Object/images/Blinky.png")

    #     # --------------- Vẽ bảng ---------------
    #     screen.fill((0, 0, 0))
    #     self.draw_board()

    #     Pacman.draw(screen)
    #     Blue_Ghost.draw(screen)
    #     Pink_Ghost.draw(screen)
    #     Orange_Ghost.draw(screen)
    #     Red_Ghost.draw(screen)

    #     pygame.display.update()

    #     # --------------- Game loop ---------------
    #     Blue_start = (i_blue_ghost, j_blue_ghost)
    #     Pink_start = (i_pink_ghost, j_pink_ghost)
    #     Orange_start = (i_orange_ghost, j_orange_ghost)
    #     Red_start = (i_red_ghost, j_red_ghost)
    #     end = spawn_pacman

    #     algorithm = Algorithm()
    #     Blue_result = algorithm.BFS(main_board, Blue_start, end)
    #     Pink_result = algorithm.DFS(main_board, Pink_start, end, path = None)
    #     Orange_result = algorithm.UCS(main_board, Orange_start, end)
    #     Red_result = algorithm.ASTAR(main_board, Red_start, end)
    #     max_length = max(len(Blue_result), len(Pink_result), len(Orange_result), len(Red_result))

    #     if Blue_result is not None or Pink_result is not None or Orange_result is not None or Red_result is not None:
    #         for i in range(max_length):
    #             if i < len(Blue_result):
    #                 target_y = Blue_result[i][0] * SQUARE + START_Y
    #                 target_x = Blue_result[i][1] * SQUARE + START_X
    #                 Blue_Ghost.move(target_x, target_y)
                    
    #             if i < len(Pink_result):
    #                 target_y = Pink_result[i][0] * SQUARE + START_Y
    #                 target_x = Pink_result[i][1] * SQUARE + START_X
    #                 Pink_Ghost.move(target_x, target_y)
                    
    #             if i < len(Orange_result):
    #                 target_y = Orange_result[i][0] * SQUARE + START_Y
    #                 target_x = Orange_result[i][1] * SQUARE + START_X
    #                 Orange_Ghost.move(target_x, target_y)
                    
    #             if i < len(Red_result):
    #                 target_y = Red_result[i][0] * SQUARE + START_Y
    #                 target_x = Red_result[i][1] * SQUARE + START_X
    #                 Red_Ghost.move(target_x, target_y)

    #             # Vẽ lại màn hình
    #             screen.fill((0, 0, 0))
    #             self.draw_board()
    #             Pacman.draw(screen)
    #             Blue_Ghost.draw(screen)
    #             Pink_Ghost.draw(screen)
    #             Orange_Ghost.draw(screen)
    #             Red_Ghost.draw(screen)
    #             pygame.display.update()

    #     pygame.time.wait(3000)


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
        currentTile = 0
        for i in range(3, len(self.board.grid) - 2):
            for j in range(len(self.board.grid[0])):
                if self.board.grid[i][j] == 3: # Draw wall
                    imageName = str(currentTile)
                    if len(imageName) == 1:
                        imageName = "00" + imageName
                    elif len(imageName) == 2:
                         imageName = "0" + imageName
                    # Get image of desired tile
                    imageName = "tile" + imageName + ".png"
                    tileImage = pygame.image.load("Assets/BoardImages/" + imageName)
                    tileImage = pygame.transform.scale(tileImage, (SQUARE, SQUARE))

                    #Display image of tile
                    screen.blit(tileImage, (j * SQUARE, i * SQUARE, SQUARE, SQUARE))
                
                currentTile += 1


