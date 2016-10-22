

def get_positions_in_grid(object, grid, map):
    '''Returns the tiles ocupied by this object in the collision grid.'''
    positions = list()

    #grid_tile_width = (map.width * map.tilewidth) / len(grid)
    #grid_tile_height = (map.height * map.tileheight) / len(grid)

    #diffs = [(x * grid_tile_width, y * grid_tile_height) for x in [-1, 0, 1] for y in [-1, 0, 1]]
    diffs = [(0,0)]
    for diff in diffs:
        try:
            x = object.position[0]
            y = object.position[1]
        except AttributeError:
            x = object[0]
            y = object[1]
        x = (x + diff[0] * 0.5) // (map.width * map.tilewidth)
        y = (x + diff[1] * 0.5) // (map.height * map.tileheight)
        x = int(max(0, min(len(grid) - 1, x)))
        y = int(max(0, min(len(grid) - 1, y)))
        positions.append((x, y))

    return positions


def get_objects_in_range(object, grid, map):
    '''Iterator that returns all objects close to one object in one grid.'''
    for pos in get_positions_in_grid(object, grid, map):
        for other in grid[pos[0]][pos[1]]:
            yield other


def get_collision_grid(objects, map, size=5):
    '''Returns a collision grid from a set of objects'''
    grid = [[list() for x in range(size)] for y in range(size)]

    for obj in objects:
        for pos in get_positions_in_grid(obj, grid, map):
            grid[pos[0]][pos[1]].append(obj)

    return grid
