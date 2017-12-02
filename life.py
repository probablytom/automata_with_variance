from cells import Frame, Cell
from time import sleep
from pydysofu import fuzz_clazz
from pydysofu.core_fuzzers import on_condition_that
from pydysofu.core_fuzzers import replace_condition_with
import random
import math


def print_output(func):
    def __wrap(*args, **kwargs):
        result = func(*args, **kwargs)
        print result
        return result

    return __wrap


def wait_after_for(time_secs):
    def wait_after_decorator(func):
        def __wrap(*args, **kwargs):
            result = func(*args, **kwargs)
            sleep(time_secs)
            return result

        return __wrap

    return wait_after_decorator


class Conway(Cell):

    def rules(self, garbage, neighbours):
        if neighbours == 3 and self.state == 1:
            return 1
        if neighbours == 3 and self.state == 0:
            return 1
        if neighbours == 2 and self.state == 1:
            return 1
        return 0

    def generate_random_state(self):
        return int(random.choice([math.ceil, math.floor])(random.random()))


randomly_ignore_rules = {
    Conway.rules:
    on_condition_that(lambda: random.random() > 0.95, replace_condition_with())
}

fuzz_clazz(Conway, randomly_ignore_rules)

# Basic oscillator, should move between two
#   states when there's no variance.
initial_structure = [[0, 0, 0, 0, 0, 0], [0, 0, 1, 0, 0, 0],
                     [0, 0, 1, 1, 0, 0], [0, 0, 1, 1, 0, 0],
                     [0, 0, 0, 1, 0, 0], [0, 0, 0, 0, 0, 0]]

game_of_life = Frame(initial_structure, Conway)

c = 10
while c > 0:
    c -= 1
    game_of_life.tick_all()
    print str(game_of_life)
    sleep(0.5)
