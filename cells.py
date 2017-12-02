class Cell(object):
    '''
    A cell in a cellular automaton.

    Adjacency is handled by adjacency lists, and cells have .set_adjacent() and
      .no_longer_adjacent() methods to manage the adjacency lists.

    '''

    is_workflow = True

    def __init__(self, initial_state):
        self.state = initial_state
        self.adjacents = []
        self.future_state = None

    def generate_random_state(self):
        raise NotImplemented  ## Every type of cell might have different possible states, so we need to implement this separately for each class

    '''
    The rules function takes a count of live neighbours & the current cell,
    and outputs a bit indicating liveness.
    Note: this is intended to be overridden by a superclass!
    '''

    def rules(self, neighbours):
        return 0  ## Set states to 0

    # Sets this cell adjacent to another, and the other adjacent to this (two lists!)
    # If it's already adjacent, fail silently (it's already done so no harm!)
    def set_adjacent(self, other_cell, recursed=False):
        if other_cell not in self.adjacents:
            self.adjacents.append(other_cell)

        if not recursed:
            other_cell.set_adjacent(self, recursed=True)

    # Removes adjacency between this cell and the other cell supplied, for both adjacency lists.
    # If it's not already adjacent, fail silently (it's already done so no harm!)
    def no_longer_adjacent(self, other_cell, recursed=False):
        try:
            self.adjacents.remove(other_cell)
        except ValueError:
            pass

        if not recursed:
            other_cell.no_longer_adjacent(self, recursed=True)

    def determine_next_state(self):
        live_neighbours = 0

        # Work out how many neighbours are live
        for neighbour in self.adjacents:
            if neighbour.state == 1:
                live_neighbours += 1

        # Determine the future state based on the number of live neighbours.
        self.future_state = self.rules(self, live_neighbours)

    def tick(self):
        self.state = self.future_state
        self.future_state = None

    def __str__(self):
        return self.state


class Frame:
    '''
    A frame is the board that the automaton plays out on.

    For now, it takes a single cell class and creates cells of that class, but
      I think it would be really interesting to have different cells play by
      *different rules*. I wonder if that's been studied before!
      So, this is a work in progress. We should be able to provide some kind of structure, or a number of types of classes.
    '''

    def __init__(self, initial_state_matrix, cell_class):
        self.frame_size = len(initial_state_matrix)
        self.structure = initial_state_matrix
        self.__convert_structure_to_automaton(cell_class)

    def __convert_structure_to_automaton(self, cell_class):
        for y in range(self.frame_size):
            for x in range(len(self.structure[y])):
                self.structure[y][x] = cell_class(self.structure[y][x])
        self.__populate_adjacencies()

    def __populate_adjacencies(self):

        # Choose the first cell
        for y in range(self.frame_size):
            for x in range(len(self.structure[y])):
                current_cell = self.structure[y][x]
                adjacencies = self.__find_adjacencies(y, x)

                for b, a in adjacencies:
                    current_cell.set_adjacent(self.structure[b][a])

    def __find_adjacencies(self, y, x):
        current_cell = self.structure[y][x]
        adjacent_cells = []
        '''
        Populate adjacencies for the current cell ('c'):
        123
        4c5
        678
        '''

        # 1
        adjacent_cells.append((y - 1, x - 1))

        # 2
        adjacent_cells.append((y - 1, x))

        # 3
        adjacent_cells.append((y - 1, (x + 1) % self.frame_size))

        # 4
        adjacent_cells.append((y, x - 1))

        # 5
        adjacent_cells.append((y, (x + 1) % self.frame_size))

        # 6
        adjacent_cells.append(((y + 1) % self.frame_size, x - 1))

        # 7
        adjacent_cells.append(((y + 1) % self.frame_size, x))

        # 8
        adjacent_cells.append(((y + 1) % self.frame_size,
                               (x + 1) % self.frame_size))

        return adjacent_cells

    # TODO: Turn this into each cell acting asynchronously
    def tick_all(self):
        for line in self.structure:
            for cell in line:
                cell.determine_next_state()
        for line in self.structure:
            for cell in line:
                cell.tick()

    def __str__(self):
        output = ""
        for y in range(self.frame_size):
            for x in range(len(self.structure[y])):
                output += str(self.structure[y][x].state)
            output += "\n"
        return output
