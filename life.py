from cells import Frame
from time import sleep

initial_structure = [[0,0,0,0,0,0],
                     [0,0,1,0,0,0],
                     [0,0,1,1,0,0],
                     [0,0,1,1,0,0],
                     [0,0,0,1,0,0],
                     [0,0,0,0,0,0]]

def conway_rules(self, neighbours):
    new_state = 0
    if neighbours == 3 and self.state == 1:
        new_state = 1
    if neighbours == 3 and self.state == 0:
        new_state = 1
    if neighbours == 2 and self.state == 1:
        new_state = 1
    return new_state

game_of_life = Frame(initial_structure, conway_rules)

while True:
    game_of_life.tick_all()
    print str(game_of_life)
    sleep(0.5)
