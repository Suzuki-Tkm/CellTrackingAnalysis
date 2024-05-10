import random

def dfs(grid, visited, row, col):
    if (row < 0 or row >= len(grid) or col < 0 or col >= len(grid[0]) or grid[row][col] == 0 or visited[row][col]):
        return 0, 1

    visited[row][col] = True

    area = 1  # 島の面積
    perimeter = 0  # 外周の長さ

    for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        new_row, new_col = row + dr, col + dc
        a, p = dfs(grid, visited, new_row, new_col)
        area += a
        perimeter += p

    return area, perimeter

def cellSizes(grid):
    if not grid:
        return []

    rows, cols = len(grid), len(grid[0])
    visited = [[False] * cols for _ in range(rows)]  # 訪問済み

    islands = []

    for row in range(rows):
        for col in range(cols):
            if grid[row][col] == 1 and not visited[row][col]:
                area, perimeter = dfs(grid, visited, row, col)
                islands.append((area, perimeter))

    return islands


rows = 5
cols = 5
cell_matrix = [[random.choice([0, 1]) for _ in range(cols)] for _ in range(rows)]

for row in cell_matrix:
    print(row)

print(cellSizes(cell_matrix))