def track_islands(time_series):
    def dfs(grid, row, col, island_id):
        if row < 0 or col < 0 or row >= len(grid) or col >= len(grid[0]) or grid[row][col] != 1 or grid[row][col] == island_id:
            return
        grid[row][col] = island_id
        dfs(grid, row + 1, col, island_id)
        dfs(grid, row - 1, col, island_id)
        dfs(grid, row, col + 1, island_id)
        dfs(grid, row, col - 1, island_id)


    all_islands = []
    island_id = 2  # Start island numbering from 2
    island_map = None

    for grid in time_series:
        if island_map is None:
            island_map = [row[:] for row in grid]  # Copy the grid for marking islands
        else:
            for i in range(len(grid)):
                for j in range(len(grid[0])):
                    if grid[i][j] == 1 and island_map[i][j] != 0:
                        dfs(island_map, i, j, island_map[i][j])

        islands = {}
        for i in range(len(grid)):
            for j in range(len(grid[0])):
                if grid[i][j] == 1:
                    if island_map[i][j] not in islands:
                        islands[island_map[i][j]] = sum(row.count(island_map[i][j]) for row in island_map)
                    else:
                        islands[island_map[i][j]] += 1

        all_islands.append(islands)

    return all_islands

# Example usage:
time_series = [
    [
        [1, 0, 1, 0, 1],
        [0, 0, 1, 0, 0],
        [1, 0, 1, 0, 1],
        [0, 0, 0, 0, 1],
        [0, 0, 0, 0, 0]
    ],
    [
        [1, 0, 1, 0, 1],
        [0, 0, 1, 0, 0],
        [0, 0, 1, 0, 1],
        [1, 0, 0, 0, 1],
        [0, 0, 0, 0, 0]
    ],
    [
        [1, 0, 1, 0, 1],
        [0, 0, 1, 0, 0],
        [0, 0, 1, 0, 0],
        [1, 0, 0, 0, 1],
        [0, 0, 0, 0, 1]
    ]
]

all_islands = track_islands(time_series)
print(all_islands)
