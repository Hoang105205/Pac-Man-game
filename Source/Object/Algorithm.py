from collections import deque
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
                return path + [(x, y)]
            
            # nếu (x, y) đã được thăm rồi thì bỏ qua
            if (x, y) in visited:
                continue

            visited.add((x, y))

            # thêm các điểm xung quanh (x, y) vào queue
            for dx, dy in directions:
                nx = x + dx
                ny = y + dy

                if 0 <= nx < rows and 0 <= ny < cols and grid[nx][ny] != 0 and (nx, ny) not in visited:
                    queue.append((nx, ny, path + [(x, y)]))

        return None