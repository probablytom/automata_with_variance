from cells import Frame, Cell
from time import sleep
from pydysofu import fuzz_clazz
from pydysofu.core_fuzzers import on_condition_that
from pydysofu.core_fuzzers import replace_condition_with
import random
import math


class Conway(Cell):
    def rules(self, neighbours):
        if neighbours == 3 and self.state == 1:
            return 1
        if neighbours == 3 and self.state == 0:
            return 1
        if neighbours == 2 and self.state == 1:
            return 1
        return 0

    def generate_random_state(self):
        return int(random.choice([math.ceil, math.floor])(random.random()))


# Fuzzing instructions
randomly_ignore_rules = {
    Conway.rules:
    on_condition_that(lambda: random.random() > 0.95, replace_condition_with())
}

# Basic oscillator, should move between two
#   states when there's no variance.
initial_structure = [[0, 0, 0, 0, 0, 0], [0, 0, 1, 0, 0, 0],
                     [0, 0, 1, 1, 0, 0], [0, 0, 1, 1, 0, 0],
                     [0, 0, 0, 1, 0, 0], [0, 0, 0, 0, 0, 0]]

if __name__ == "__main__":
    print "Life without variation:"
    sleep(2)
    unvaried_game_of_life = Frame(initial_structure, Conway)
    unvaried_game_of_life.pretty_print_round(count=10, delay=0.5)

    fuzz_clazz(Conway, randomly_ignore_rules)  # Fuzz Conway's behaviour

    print
    print "=" * 25
    print
    print "Life with variation:"
    sleep(2)
    varied_game_of_life = Frame(initial_structure, Conway)
    varied_game_of_life.pretty_print_round(count=10, delay=0.5)
