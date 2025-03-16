from collections import deque
import heapq
class Algorithm:
    def __init__(self):
        pass


    def BFS(self, grid, start, end):
        rows = len(grid)
        cols = len(grid[0])

        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        queue = deque([(start[0], start[1], [])])
        visited = set()

        while queue:
            # pop phần tử đầu tiên ra khỏi queue
            x, y, path = queue.popleft()

            # kiểm tra xem (x, y) có phải là điểm kết thúc không
            if (x, y) == end:
                return [path + [(x, y)], len(visited)]
            
            # nếu (x, y) đã được thăm rồi thì bỏ qua
            if (x, y) in visited:
                continue

            visited.add((x, y))

            # thêm các điểm xung quanh (x, y) vào queue
            for dx, dy in directions:
                nx = x + dx
                ny = y + dy
                
                if(nx == 17 and ny == 28):
                    ny = 0
                
                if(nx == 17 and ny == -1):
                    ny = 27

                if 0 <= nx < rows and 0 <= ny < cols and grid[nx][ny] != 0 and (nx, ny) not in visited:
                    if((nx, ny) == end):
                        return [path + [(x, y), (nx, ny)], len(visited)]
                    queue.append((nx, ny, path + [(x, y)]))

        return None
    
    
    def DFS(self, grid, start, end, path=None, expanded_nodes = 0):
        if path is None:
            path = [start]  # Danh sách lưu đường đi hiện tại

        x, y = start
        if start == end:
            return path  # Nếu đến điểm đích, trả về đường đi

        rows, cols = len(grid), len(grid[0])
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Lên, Xuống, Trái, Phải
        
        
        for index, (dx, dy) in enumerate(directions):
            nx, ny = x + dx, y + dy
            if nx == 17 and ny == 28:
                ny = 0
            elif nx == 17 and ny == -1:
                ny = 27
            if 0 <= nx < rows and 0 <= ny < cols and grid[nx][ny] != 0 and (nx, ny) not in path:
                if((nx, ny) == end):
                    return [path + [(nx, ny)], expanded_nodes + index + 1]

        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if nx == 17 and ny == 28:
                ny = 0
            elif nx == 17 and ny == -1:
                ny = 27
            # Kiểm tra nếu ô hợp lệ và chưa xuất hiện trong đường đi hiện tại
            if 0 <= nx < rows and 0 <= ny < cols and grid[nx][ny] != 0 and (nx, ny) not in path:
                [new_path, expanded_nodes]  = self.DFS(grid, (nx, ny), end, path + [(nx, ny)], expanded_nodes + 1)
                if new_path:  # Nếu tìm thấy đường đi, trả về ngay
                    return [new_path, expanded_nodes]

        return [None, expanded_nodes]  # Nếu không tìm được đường đi nào
    
    def get_ghost_cost(self, x, y, path):
        # Trọng số cơ bản cho mỗi ô là 1
        cost = 1
        
        # Ưu tiên đường tắt qua hầm (nếu có)
        if (x, y) == (17, 0) or (x, y) == (17, 27):
            cost = 0.5
            
        #Khúc cua sẽ tốn nhiều chi phí hơn
        if(len(path) > 1):
            previous = path[-2]
            if (x != previous[0] and abs(y - previous[1] == 1)) or (abs(x - previous[0] == 1) and y != previous[1]):
                cost = 3
        return cost 

    
    def UCS(self, grid, start, end):
        priority_queue = [(0, start, [])]  # (cost, (x, y), path)
        visited = set()
        rows = len(grid)
        cols = len(grid[0])
        # Các hướng di chuyển: Lên, Xuống, Trái, Phải
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        while priority_queue:
            path_cost, (x, y), path = heapq.heappop(priority_queue)

            # Nếu đã đến đích, trả về đường đi
            if (x, y) == end:
                return [path + [(x, y)], len(visited)]

            # Nếu đã thăm ô này, bỏ qua
            if (x, y) in visited:
                continue

            visited.add((x, y))

            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                if nx == 17 and ny == 28:
                    ny = 0
                elif nx == 17 and ny == -1:
                    ny = 27
                # Kiểm tra ô hợp lệ
                if 0 <= nx < rows and 0 <= ny < cols and grid[nx][ny] != 0:
                    cost = self.get_ghost_cost(nx, ny, path)
                    heapq.heappush(priority_queue, (path_cost + cost, (nx, ny), path + [(x, y)]))

        return None  # Không tìm thấy đường đi
    
    def heuristic(self, start, end):
        return abs(start[0] - end[0]) + abs(start[1] - end[1])
    
    def ASTAR(self, grid, start, end):
        """Thuật toán A* tìm đường đi ngắn nhất"""
        rows = len(grid)
        cols = len(grid[0])
        priority_queue = [(0, 0, start, [])]  # (f = g + h, g, (x, y), path)
        visited = set()

        while priority_queue:
            _, g, (x, y), path = heapq.heappop(priority_queue)

            # Nếu đã đến đích, trả về đường đi
            if (x, y) == end:
                return [path + [(x, y)], len(visited)]

            # Nếu đã thăm ô này, bỏ qua
            if (x, y) in visited:
                continue

            visited.add((x, y))

            # Các hướng di chuyển: Lên, Xuống, Trái, Phải
            directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                if nx == 17 and ny == 28:
                    ny = 0
                elif nx == 17 and ny == -1:
                    ny = 27

                # Kiểm tra ô hợp lệ
                if 0 <= nx < rows and 0 <= ny < cols and grid[nx][ny] != 0:
                    h = self.heuristic((nx, ny), end)
                    cost = self.get_ghost_cost(nx, ny, path)
                    heapq.heappush(priority_queue, (g + cost + h, g + cost, (nx, ny), path + [(x, y)]))

        return None  # Không tìm thấy đường đi
