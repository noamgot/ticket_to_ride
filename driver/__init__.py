import time

import gui
from ai.greedy_ai.cheapest_path_ai import CheapestPathAI
from ai.greedy_ai.greedy_ai import GreedyAI
from ai.random_ai import RandomAI
from game import Game
from game.methods import find_paths_for_destinations
from game.board import create_board

p1 = RandomAI("P1")
# p2 = Player("P2")
p2 = GreedyAI("P2")

players = [p1, p2]

# game_gui = gui.GUI()
game = Game(players)

# Main game loop.  Tells players when to take their turn.
while not game.is_game_over()[0]:
    for player in players:
        if game.is_turn(player):
            player.take_turn(game)
            # game_gui.update(game)
            break

# Game's over.  Tell the players and print out some results.
for player in players:
    player.game_ended(game)

print "Game Over"
print "Winner: %s" % game.is_game_over()[1]
print "Final Scores: %s" % game.get_visible_scores()
# game_gui.update_game_ended(game)
