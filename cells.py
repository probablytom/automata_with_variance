import theatre_ag as theatre


# TODO: actually convert this to Theatre!
class Cell:

    '''
    A cell in a cellular automaton.

    Adjacency is handled by adjacency lists, and cells have .set_adjacent() and
      .no_longer_adjacent() methods to manage the adjacency lists.

    The rule mapping function takes a count of live neighbours & the current cell,
      and outputs a bit indicating liveness.
    '''

    def __init__(self, initial_state, rule_mapping_function):
        self.state = initial_state
        self.rules = rule_mapping_function
        self.adjacents = []
        self.future_state = None

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
        print(live_neighbours)

        # Determine the future state based on the number of live neighbours.
        self.future_state = self.rules(self, live_neighbours)

    def tick(self):
        self.state = self.future_state
        self.future_state = None

    def __str__(self):
        return self.state
