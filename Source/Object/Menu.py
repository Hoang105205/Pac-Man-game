import pygame
import sys
from Object.Board import Board
from Object.Player import Player
import copy
import math
from constants import BOARD_HEIGHT, BOARD_WIDTH, SQUARE
from Object.Ghost import Ghost
import random

# ============ Class Algorithm ============
from Object.Algorithm import Algorithm
import time
import tracemalloc
import timeit



# Khởi tạo pygame
pygame.init()

# Kích thước màn hình
WIDTH, HEIGHT = BOARD_WIDTH * SQUARE, BOARD_HEIGHT * SQUARE
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game Menu")

# Load background
background = pygame.image.load("Object/images/home_bg.png")
background = pygame.transform.scale(background, (WIDTH, HEIGHT))
ending_background = pygame.image.load("Object/images/end_screen.jpg")
ending_background = pygame.transform.scale(ending_background, (WIDTH, HEIGHT))
win_background = pygame.image.load("Object/images/win.jpg")
win_background = pygame.transform.scale(win_background, (WIDTH, HEIGHT))
lose_background = pygame.image.load("Object/images/gameover_bg.png")
lose_background = pygame.transform.scale(lose_background, (WIDTH, HEIGHT))

# Fonts
font = pygame.font.SysFont('Arial', 40)

# Màu sắc
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

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
        self.current_map = 0
        self.done = False
        self.current_screen = 1
        self.screen = screen

        self.spritePosition = {
            # STT của map: {(tọa độ Pacman), (tọa độ Ghost)}
            1: {(4, 1), (17, 14)},
            2: {(22, 9), (29, 3)},
            3: {(4, 3), (29, 24)},
            4: {(25, 12), (21, 8)},
            5: {(31, 26), (31, 1)}, 
        }

        self.menu_button_size = (150, 100)

        self.screen_handlers = {
            1: self.draw_main_menu,
            2: self.draw_level_menu,
            3: self.draw_map_menu,
        }

        self.buttons = {
            "Start": Button(self.center_x(), self.pos_y(0), *self.menu_button_size, screen, "Start", self.start_function),
            "Quit": Button(self.center_x(), self.pos_y(1), *self.menu_button_size, screen, "Quit", self.quit_function),
            "Level1": Button(self.left_x(), self.pos_y(0), *self.menu_button_size, screen, "Level 1", self.select_map_level_1),
            "Level2": Button(self.center_x(), self.pos_y(0), *self.menu_button_size, screen, "Level 2", self.select_map_level_2),
            "Level3": Button(self.right_x(), self.pos_y(0), *self.menu_button_size, screen, "Level 3", self.select_map_level_3),
            "Level4": Button(self.left_x(), self.pos_y(1), *self.menu_button_size, screen, "Level 4", self.select_map_level_4),
            "Level5": Button(self.center_x(), self.pos_y(1), *self.menu_button_size, screen, "Level 5", self.level_5_ingame),
            "Level6": Button(self.right_x(), self.pos_y(1), *self.menu_button_size, screen, "Level 6", self.level_6_ingame),
            "Back": Button(40, HEIGHT // 4 * 3 + 70, 150, 100, screen, "BACK", self.back_function),
            "NextMap": Button(WIDTH - 70, 0, 70, 50, screen, ">", self.next_map),
            "PrevMap": Button(0, 0, 70, 50, screen, "<", self.prev_map),
            "PlayMap": Button(WIDTH // 2 + 20, 0, 100, 50, screen, "PLAY", self.play_map),
            "BackMap": Button(WIDTH // 3, 0, 100, 50, screen, "BACK", self.exit_map_select),
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

    def quit_function(self):
        pygame.quit()
        sys.exit(0)

    def back_function(self):
        self.current_screen = 1

    def select_map_level_1(self):
        self.current_screen = 3
        self.current_map = 1
        self.current_level = 1

    def select_map_level_2(self):
        self.current_screen = 3
        self.current_map = 1
        self.current_level = 2

    def select_map_level_3(self):
        self.current_screen = 3
        self.current_map = 1
        self.current_level = 3

    def select_map_level_4(self):
        self.current_screen = 3
        self.current_map = 1
        self.current_level = 4    

    def exit_map_select(self):
        self.current_screen = 2

    def next_map(self):
        self.current_map = self.current_map + 1
        if (self.current_map == 6):
            self.current_map = 1
        self.current_screen = 3

    def prev_map(self):
        self.current_map = self.current_map - 1
        if (self.current_map == 0):
            self.current_map = 5
        self.current_screen = 3

    def play_map(self):
        if (self.current_level == 1):
            self.level_1_ingame()
        elif (self.current_level == 2):
            self.level_2_ingame()
        elif (self.current_level == 3):
            self.level_3_ingame()
        elif (self.current_level == 4):
            self.level_4_ingame()

    def draw_food(self):
        for i in range(3, len(self.board.grid) - 2):
            for j in range(len(self.board.grid[0])):
                if(self.board.grid[i][j] == 2 or self.board.grid[i][j] == 6):
                    pygame.draw.circle(screen, (255, 255, 0), (j * SQUARE + SQUARE // 2, i * SQUARE + SQUARE // 2), 5)
    
    
    def level_1_ingame(self):
        # main_board = copy.deepcopy(self.board.grid) # Sao chép bảng để tránh thay đổi bảng gốc

        board = Board()
        main_board = copy.deepcopy(board.grid_algorithm)
        
        # --------------- Vị trí ban đầu của Pacman và Ghost ---------------
        
        Pacman = Player()
        Ghost1 = Ghost(31, 1, "Object/images/Inky.png")

        # --------------- Vẽ bảng ---------------
        screen.fill((0, 0, 0))
        self.draw_board()

        Pacman.draw(screen)
        Ghost1.draw(screen)

        pygame.display.update()
        pygame.time.wait(500)
        # --------------- Game loop ---------------
        start = Ghost1.get_position()
        end = Pacman.get_position()

        algorithm = Algorithm()

        #Calculate time cost
        execution_time = timeit.timeit(lambda: algorithm.BFS(main_board, start, end), number=1)

        #Calculate memory cost
        tracemalloc.start()

        [result, expaneded_nodes] = algorithm.BFS(main_board, start, end)

        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        memory_usage = peak # Bytes

        if result is not None:
            for i in range(len(result)):
                target_x = result[i][0]
                target_y = result[i][1]

                Ghost1.move(target_x, target_y, screen)

                # Vẽ lại màn hình
                screen.fill((0, 0, 0))
                self.draw_board()
                Pacman.draw(screen)
                Ghost1.draw(screen)
                pygame.display.update()

        pygame.time.wait(1000)
        
        self.draw_end_screen_algorithmTest(execution_time, memory_usage,expaneded_nodes, "BFS")
    
    
    def level_2_ingame(self):
        # main_board = copy.deepcopy(self.board.grid) # Sao chép bảng để tránh thay đổi bảng gốc

        board = Board()
        main_board = copy.deepcopy(board.grid_algorithm)
        
        # --------------- Vị trí ban đầu của Pacman và Ghost ---------------
        
        Pacman = Player()
        Ghost1 = Ghost(31, 1, "Object/images/Pinky.png")

        # --------------- Vẽ bảng ---------------
        screen.fill((0, 0, 0))
        self.draw_board()

        Pacman.draw(screen)
        Ghost1.draw(screen)

        pygame.display.update()
        pygame.time.wait(500)
        # --------------- Game loop ---------------
        start = Ghost1.get_position()
        end = Pacman.get_position()

        algorithm = Algorithm()
        #Calculate time cost
        execution_time = timeit.timeit(lambda: algorithm.DFS(main_board, start, end), number=1)

        #Calculate memory cost
        tracemalloc.start()

        [result, expanded_nodes] = algorithm.DFS(main_board, start, end)

        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        memory_usage = peak # Bytes

        if result is not None:
            for i in range(len(result)):
                target_x = result[i][0]
                target_y = result[i][1]
                Ghost1.move(target_x, target_y, screen)
                
                # Vẽ lại màn hình
                screen.fill((0, 0, 0))
                self.draw_board()
                Pacman.draw(screen)
                Ghost1.draw(screen)
                pygame.display.update()


        pygame.time.wait(1000)

        self.draw_end_screen_algorithmTest(execution_time, memory_usage, expanded_nodes, "DFS")
    
    
    def level_3_ingame(self):
         # main_board = copy.deepcopy(self.board.grid) # Sao chép bảng để tránh thay đổi bảng gốc

        board = Board()
        main_board = copy.deepcopy(board.grid_algorithm)
        
        # --------------- Vị trí ban đầu của Pacman và Ghost ---------------
        
        Pacman = Player()
        Ghost1 = Ghost(31, 1, "Object/images/Clyde.png")

        # --------------- Vẽ bảng ---------------
        screen.fill((0, 0, 0))
        self.draw_board()

        Pacman.draw(screen)
        Ghost1.draw(screen)

        pygame.display.update()
        pygame.time.wait(500)
        # --------------- Game loop ---------------
        start = Ghost1.get_position()
        end = Pacman.get_position()

        algorithm = Algorithm()
        #Calculate time cost
        execution_time = timeit.timeit(lambda: algorithm.UCS(main_board, start, end), number=1)

        #Calculate memory cost
        tracemalloc.start()

        [result, expanded_nodes] = algorithm.UCS(main_board, start, end)

        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        memory_usage = peak # Bytes

        if result is not None:
            for i in range(len(result)):
                target_x = result[i][0]
                target_y = result[i][1]
                Ghost1.move(target_x, target_y, screen)

                # Vẽ lại màn hình
                screen.fill((0, 0, 0))
                self.draw_board()
                Pacman.draw(screen)
                Ghost1.draw(screen)
                pygame.display.update()

        pygame.time.wait(1000)

        self.draw_end_screen_algorithmTest(execution_time, memory_usage,expanded_nodes, "UCS")
    
    
    def level_4_ingame(self):
         # main_board = copy.deepcopy(self.board.grid) # Sao chép bảng để tránh thay đổi bảng gốc

        board = Board()
        main_board = copy.deepcopy(board.grid_algorithm)
        
        # --------------- Vị trí ban đầu của Pacman và Ghost ---------------
        
        Pacman = Player()
        Ghost1 = Ghost(31, 1, "Object/images/Blinky.png")

        # --------------- Vẽ bảng ---------------
        screen.fill((0, 0, 0))
        self.draw_board()

        Pacman.draw(screen)
        Ghost1.draw(screen)

        pygame.display.update()
        pygame.time.wait(500)
        # --------------- Game loop ---------------
        start = Ghost1.get_position()
        end = Pacman.get_position()

        algorithm = Algorithm()
        #Calculate time cost
        execution_time = timeit.timeit(lambda: algorithm.ASTAR(main_board, start, end), number=1)

        #Calculate memory cost
        tracemalloc.start()

        [result, expanded_nodes] = algorithm.ASTAR(main_board, start, end)

        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        memory_usage = peak # Bytes

        if result is not None:
            for i in range(len(result)):
                target_x = result[i][0]
                target_y = result[i][1]

                Ghost1.move(target_x, target_y, screen)

                # Vẽ lại màn hình
                screen.fill((0, 0, 0))
                self.draw_board()
                Pacman.draw(screen)
                Ghost1.draw(screen)
                pygame.display.update()

        pygame.time.wait(1000)

        self.draw_end_screen_algorithmTest(execution_time, memory_usage, expanded_nodes, "A*")
        
    
    def level_5_ingame(self):
         # main_board = copy.deepcopy(self.board.grid) # Sao chép bảng để tránh thay đổi bảng gốc

        board = Board()
        main_board = copy.deepcopy(board.grid_algorithm)
        
        # --------------- Vị trí ban đầu của Pacman và Ghost ---------------
        
        Pacman = Player()
        Blue_Ghost = Ghost(17, 15, "Object/images/Inky.png")
        Pink_Ghost = Ghost(17, 12, "Object/images/Pinky.png")
        Orange_Ghost = Ghost(16, 15, "Object/images/Clyde.png")
        Red_Ghost = Ghost(16, 12, "Object/images/Blinky.png")

        # --------------- Vẽ bảng ---------------
        screen.fill((0, 0, 0))
        self.draw_board()

        Pacman.draw(screen)
        Blue_Ghost.draw(screen)
        Pink_Ghost.draw(screen)
        Orange_Ghost.draw(screen)
        Red_Ghost.draw(screen)

        pygame.display.update()
        pygame.time.wait(500)
        # --------------- Game loop ---------------
        Blue_start = Blue_Ghost.get_position()
        Pink_start = Pink_Ghost.get_position()
        Orange_start = Orange_Ghost.get_position()
        Red_start = Red_Ghost.get_position()
        end = Pacman.get_position()

        algorithm = Algorithm()
        [Blue_result, blue_expanded_nodes] = algorithm.BFS(main_board, Blue_start, end)
        [Pink_result, pink_expanded_nodes] = algorithm.DFS(main_board, Pink_start, end, path = None)
        [Orange_result, orange_expanded_nodes] = algorithm.UCS(main_board, Orange_start, end)
        [Red_result, red_expanded_nodes] = algorithm.ASTAR(main_board, Red_start, end)

        if Blue_result is not None or Pink_result is not None or Orange_result is not None or Red_result is not None:
            blue_step = 1
            pink_step = 1
            orange_step = 1
            red_step = 1
            while blue_step < len(Blue_result) or pink_step < len(Pink_result) or orange_step < len(Orange_result) or red_step < len(Red_result):
                # Di chuyển từng Ghost nếu còn đường đi
                if blue_step < len(Blue_result):
                    if(Blue_Ghost.check_collision(
                            Blue_result[blue_step],
                            Pink_result, pink_step,
                            Orange_result, orange_step, 
                            Red_result, red_step)):
                        blue_step -= 1
                        
                    target_x = Blue_result[blue_step][0]
                    target_y = Blue_result[blue_step][1]    
                    Blue_Ghost.move(target_x, target_y, screen)
                    blue_step += 1

                if pink_step < len(Pink_result):
                    if(Pink_Ghost.check_collision(
                            Pink_result[pink_step], 
                            Blue_result, blue_step,
                            Orange_result, orange_step,
                            Red_result, red_step)):
                        pink_step -= 1
                    
                    target_x = Pink_result[pink_step][0]
                    target_y = Pink_result[pink_step][1]
                    Pink_Ghost.move(target_x, target_y, screen)
                    pink_step += 1

                if orange_step < len(Orange_result):
                    if(Orange_Ghost.check_collision(
                            Orange_result[orange_step], 
                            Blue_result, blue_step,
                            Pink_result, pink_step,
                            Red_result, red_step)):
                        orange_step -= 1
            
                    target_x = Orange_result[orange_step][0]
                    target_y = Orange_result[orange_step][1]
                    Orange_Ghost.move(target_x, target_y, screen)
                    orange_step += 1

                if red_step < len(Red_result):
                    if(Red_Ghost.check_collision(
                            Red_result[red_step], 
                            Blue_result, blue_step,
                            Pink_result, pink_step,
                            Orange_result, orange_step)):
                        red_step -= 1
                    
                    target_x = Red_result[red_step][0]
                    target_y = Red_result[red_step][1]
                    Red_Ghost.move(target_x, target_y, screen)
                    red_step += 1
                
                # Vẽ lại màn hình
                screen.fill((0, 0, 0))
                self.draw_board()
                Pacman.draw(screen)
                Blue_Ghost.draw(screen)
                Pink_Ghost.draw(screen)
                Orange_Ghost.draw(screen)
                Red_Ghost.draw(screen)
                pygame.display.update()

        pygame.time.wait(100)

        self.draw_lose_screen()
        
    def level_6_ingame(self):
         # main_board = copy.deepcopy(self.board.grid) # Sao chép bảng để tránh thay đổi bảng gốc

        board = Board()
        main_board = copy.deepcopy(board.grid_algorithm)
        
        # --------------- Vị trí ban đầu của Pacman và Ghost ---------------
        
        Pacman = Player()
        Blue_Ghost = Ghost(16, 15, "Object/images/Inky.png")
        Pink_Ghost = Ghost(16, 12, "Object/images/Pinky.png")
        Orange_Ghost = Ghost(17, 15, "Object/images/Clyde.png")
        Red_Ghost = Ghost(17, 12, "Object/images/Blinky.png")

        # --------------- Vẽ bảng ---------------
                    
        screen.fill((0, 0, 0))
        self.draw_food()
        self.draw_board()

        Pacman.draw(screen)
        Blue_Ghost.draw(screen)
        Pink_Ghost.draw(screen)
        Orange_Ghost.draw(screen)
        Red_Ghost.draw(screen)

        pygame.display.update()
        pygame.time.wait(500)
        # --------------- Game loop ---------------
        Blue_start = Blue_Ghost.get_position()
        Pink_start = Pink_Ghost.get_position()
        Orange_start = Orange_Ghost.get_position()
        Red_start = Red_Ghost.get_position()
        current_step = 0
        end = Pacman.get_position()
        board = Board()
        algorithm = Algorithm()
        [Blue_result, blue_expanded_nodes] = algorithm.BFS(main_board, Blue_start, end)
        [Pink_result, pink_expanded_nodes] = algorithm.DFS(main_board, Pink_start, end, path = None)
        [Orange_result, orange_expanded_nodes] = algorithm.UCS(main_board, Orange_start, end)
        [Red_result, red_expanded_nodes] = algorithm.ASTAR(main_board, Red_start, end)
        new_end = end
        clock = pygame.time.Clock()
        
        # Vẽ màn hình
        screen.fill((0, 0, 0))
        self.draw_board()
        Pacman.draw(screen)
        Blue_Ghost.draw(screen)
        Pink_Ghost.draw(screen)
        Orange_Ghost.draw(screen)
        Red_Ghost.draw(screen)
        pygame.display.update()
        running = True
        food_remain = 244
        player_score = 0
        font = pygame.font.Font(None, 36)
        blue_step = 1
        pink_step = 1
        orange_step = 1
        red_step = 1
        result = False
        start_time = time.time()
        play_time = start_time
        
        while running:
            text = font.render("SCORE: " + str(player_score), True, WHITE)
            text_rect = text.get_rect()
            text_rect.topleft = (30, 50)
            screen.blit(text, text_rect)
            
            # Tính thời gian chơi
            elapsed_time = time.time() - start_time
            minutes = int(elapsed_time // 60)
            seconds = int(elapsed_time % 60)
            
            # Tạo chuỗi hiển thị
            time_text = f"{minutes:02}:{seconds:02}"
            text_surface = font.render("PLAY TIME:  " + str(time_text), True, GREEN)
            text_rect = text_surface.get_rect()
            text_rect.topleft = (300, 50)
            screen.blit(text_surface, text_rect)
            
            # Xử lý sự kiện
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key in (pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT):
                        Pacman.change_direction(event.key)
            
            Pacman.update()                     
            # Di chuyển Pac-Man
            Pacman.move(screen)
            new_end = Pacman.get_position()
            if(self.board.grid[new_end[0]][new_end[1]] == 2 or self.board.grid[new_end[0]][new_end[1]] == 6):
                self.board.grid[new_end[0]][new_end[1]] = 1
                food_remain -= 1
                player_score += 1
            
            # Nếu Pac-Man thay đổi vị trí, cập nhật đường đi mới của Ghosts
            if new_end != end:
                current_step = 1
                end = new_end
                
                # Xử lí vị trí delay lâu của Pink Ghost
                if(end == (8, 4) or end == (8, 3)):
                    if(Pacman.direction == "LEFT"):
                        end = (8, 2)
                    if(Pacman.direction == "RIGHT"):
                        end = (8, 5)
                
                [Pink_result, pink_expanded_nodes] = algorithm.DFS(main_board, Pink_start, end, path = None)
                end  = new_end
                
                # Tính toán đường đi mới cho Ghosts
                [Blue_result, blue_expanded_nodes] = algorithm.BFS(main_board, Blue_start, end)
                [Orange_result, orange_expanded_nodes] = algorithm.UCS(main_board, Orange_start, end)
                [Red_result, red_expanded_nodes] = algorithm.ASTAR(main_board, Red_start, end)
                blue_step = 1
                pink_step = 1
                orange_step = 1
                red_step = 1

            # Di chuyển từng Ghost nếu còn đường đi
            if blue_step < len(Blue_result):
                if(Blue_Ghost.check_collision(
                        Blue_result[blue_step],
                        Pink_result, pink_step,
                        Orange_result, orange_step,
                        Red_result, red_step)):
                    blue_step -= 1
                target_x = Blue_result[blue_step][0]
                target_y = Blue_result[blue_step][1]
                Blue_Ghost.move(target_x, target_y, screen)
                Blue_start = Blue_Ghost.get_position()
                blue_step += 1

            if pink_step < len(Pink_result):
                if(Pink_Ghost.check_collision(
                        Pink_result[current_step], 
                        Blue_result, blue_step,
                        Orange_result, orange_step,
                        Red_result, red_step)):
                    pink_step -= 1
                    
                target_x = Pink_result[pink_step][0]
                target_y = Pink_result[pink_step][1]
                Pink_Ghost.move(target_x, target_y, screen)
                Pink_start = Pink_Ghost.get_position()
                pink_step += 1

            if orange_step < len(Orange_result):
                if(Orange_Ghost.check_collision(
                        Orange_result[orange_step], 
                        Blue_result, blue_step,
                        Pink_result, pink_step,
                        Red_result, red_step)):
                    orange_step -= 1
            
                target_x = Orange_result[orange_step][0]
                target_y = Orange_result[orange_step][1]
                Orange_Ghost.move(target_x, target_y, screen)
                Orange_start = Orange_Ghost.get_position()
                orange_step += 1

            if red_step < len(Red_result):
                if(Red_Ghost.check_collision(
                        Red_result[red_step], 
                        Blue_result, blue_step,
                        Pink_result, pink_step,
                        Orange_result, orange_step)):
                    red_step -= 1
                
                target_x = Red_result[red_step][0]
                target_y = Red_result[red_step][1]
                Red_Ghost.move(target_x, target_y, screen)
                Red_start = Red_Ghost.get_position()
                red_step += 1


            # Vẽ lại màn hình
            screen.fill((0, 0, 0))
            self.draw_food()
            self.draw_board()
            Pacman.draw(screen)
            Blue_Ghost.draw(screen)
            Pink_Ghost.draw(screen)
            Orange_Ghost.draw(screen)
            Red_Ghost.draw(screen)
            pygame.display.update()
            
            if(blue_step == len(Blue_result) or pink_step == len(Pink_result) or orange_step == len(Orange_result) or red_step == len(Red_result) or food_remain == 0):
                running = False
                if(food_remain == 0):
                    result = True
                else:
                    result = False
                play_time = elapsed_time

            # Giới hạn tốc độ game (60 FPS)
            clock.tick(60)
            
        # Trả về bảng ban đầu
        self.board.grid = copy.deepcopy(board.grid)
        if(result == True):
            if(play_time < 60):
                player_score += 100
            elif(play_time < 120):
                player_score += 50
            self.draw_win_screen(player_score)
        else:
            self.draw_win_screen(player_score)
        pygame.time.wait(30)


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

    def draw_map_menu(self):
        screen.fill((0, 0, 0))
        self.buttons["NextMap"].process()
        self.buttons["PrevMap"].process()
        self.buttons["PlayMap"].process()
        self.buttons["BackMap"].process()
        self.draw_select_map_test(self.current_map)

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

# ============ Hàm màn hình kết thúc ============    
    def draw_end_screen_algorithmTest(self, time, memory, expanded_nodes, algorithm_name):
        screen.fill(BLACK)  # Background color
        game_over_text = font.render(f"STATS", True, RED)
        algorithm_name_text = font.render(f"Algorithm: {algorithm_name}", True, WHITE)
        time_text = font.render(f"Execution time: {time:.10f} seconds", True, WHITE)
        memory_text = font.render(f"Memory usage: {memory} bytes", True, WHITE)
        expanded_node_text = font.render(f"Expanded nodes: {expanded_nodes}", True, WHITE)
        continue_text = font.render("Press Enter to Continue", True, WHITE)

        # Position text in the center
        screen.blit(ending_background, (0, 0))
        screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - 150))
        screen.blit(algorithm_name_text, (WIDTH // 2 - algorithm_name_text.get_width() // 2, HEIGHT // 2 - 50))
        screen.blit(time_text, (WIDTH // 2 - time_text.get_width() // 2, HEIGHT // 2))
        screen.blit(memory_text, (WIDTH // 2 - memory_text.get_width() // 2, HEIGHT // 2 + 50))
        screen.blit(expanded_node_text, (WIDTH // 2 - expanded_node_text.get_width() // 2, HEIGHT // 2 + 100))
        screen.blit(continue_text, (WIDTH // 2 - continue_text.get_width() // 2, HEIGHT - 100))

        pygame.display.flip()  # Update the screen

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit(0)
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        return
                    
    def draw_win_screen(self, score):
        screen.fill(BLACK)  # Background color
        game_over_text = font.render(f"YOU WIN", True, RED)
        Score_text = font.render(f"SCORE: {score}", True, WHITE)
        continue_text = font.render("Press Enter to Continue", True, WHITE)

        # Position text in the center
        screen.blit(win_background, (0, 0))
        screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - 150))
        screen.blit(Score_text, (WIDTH // 2 - Score_text.get_width() // 2, HEIGHT // 2))
        screen.blit(continue_text, (WIDTH // 2 - continue_text.get_width() // 2, HEIGHT - 60))

        pygame.display.flip()  # Update the screen

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit(0)
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        return
                    
    def draw_lose_screen(self):
        screen.fill(BLACK)
        continue_text = font.render("Press Enter to Continue", True, WHITE)

        # Position text in the center
        screen.blit(lose_background, (0, 0))
        screen.blit(continue_text, (WIDTH // 2 - continue_text.get_width() // 2, HEIGHT - 100))

        pygame.display.flip()  # Update the screen

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit(0)
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        return
                

    # ============ Hàm vẽ màn hình chọn map ============            
    def draw_select_map_test(self, map):
        position = list(self.spritePosition[map])
        self.draw_board()
        pacman = Player()
        ### hàm set tọa độ của Pacman
        ghost = Ghost(position[1][0], position[1][1], "Object/images/Inky.png")
        pacman.draw(screen)
        ghost.draw(screen)

