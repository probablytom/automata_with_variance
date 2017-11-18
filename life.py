from cells import Cell
import time

structure = [[0,0,0,0,0,0],
             [0,0,1,0,0,0],
             [0,0,1,1,0,0],
             [0,0,1,1,0,0],
             [0,0,0,1,0,0],
             [0,0,0,0,0,0]]
frame_size = len(structure) 

def conway_rules(self, neighbours):
    if neighbours == 3 or (self.state == 1 and neighbours == 2):
        return 1
    else:
        return 0

def convert_structure_to_life_game():
    for y in range(frame_size):
        for x in range(len(structure[y])):
            structure[y][x] = Cell(structure[y][x], conway_rules)
    populate_adjacencies()

def populate_adjacencies():

    # Choose the first cell
    for y in range(frame_size):
        for x in range(len(structure[y])):
            current_cell = structure[y][x]
            adjacencies = find_adjacencies(y, x)

            # Actually populate the adjacent cells
            for b, a in adjacencies:
                print y, x,
                print " -> ",
                print b, a
                current_cell.set_adjacent(structure[b][a])

def find_adjacencies(y, x):
    current_cell = structure[y][x]
    adjacent_cells = []
    '''
    Populate adjacencies for the current cell ('c'):
    123
    4c5
    678
    '''

    # 1
    adjacent_cells.append((y-1,x-1))

    # 2
    adjacent_cells.append((y-1,x))

    # 3
    adjacent_cells.append((y-1, (x+1) % frame_size))

    # 4
    adjacent_cells.append((y, x-1))

    # 5
    adjacent_cells.append((y, (x+1) % frame_size))

    # 6
    adjacent_cells.append(((y+1) % frame_size, x-1))

    # 7
    adjacent_cells.append(((y+1) % frame_size, x))

    # 8
    adjacent_cells.append(((y+1) % frame_size, (x+1) % frame_size))

    return adjacent_cells

def tick_all():
    for line in structure:
        for cell in line:
            cell.determine_next_state()
    for line in structure:
        for cell in line:
            cell.tick()

def pretty_print_states():
    for y in range(len(structure)):
        for x in range(len(structure[y])):
            print structure[y][x].state,
        print

convert_structure_to_life_game()

while True:
    tick_all()
    pretty_print_states()
    print
    print "=" * frame_size 
    print
    time.sleep(1)
