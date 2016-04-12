import time

from ai.cf_ai.cf_adversarial_ai import AdversarialAI
from ai.cf_ai.cheapest_path_ai import CheapestPathAI
from ai.random_ai import RandomAI
from ai.cf_ai.cf_random_ai import CFRandomAI
from ai.cf_ai.cf_base_ai import CFBaseAI
from drivers.driver import Driver
from drivers.log_driver import LogDriver
from game import Game
from game.classes import FailureCause, Colors
from human_player.console_player import ConsolePlayer


# for i in range(6):
p1 = CFRandomAI("CF Random AI")
# p1 = RandomAI("R1")
# p1 = ConsolePlayer("Human")
# p2 = Player("P2")

p2 = CFBaseAI("CF Base AI")
# p2 = RandomAI("R2")
# p2 = GreedyAI("P2")
p3 = AdversarialAI("Adversarial AI")
players = [p3, p2]

driver = LogDriver(use_gui=False, players=players, print_debug=False, iterations=1, switch_order=True,
                   replay_deck=True, replay_destinations=True)

# driver = Driver(use_gui=False, players=players, print_debug=False)

driver.run_game()
