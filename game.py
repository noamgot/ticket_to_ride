from copy import copy

from board import create_board
from classes import Colors, Hand


class FailureCause:
    none, no_route, wrong_turn, missing_cards, incompatible_cards, already_drew, deck_empty, invalid_card_index = \
        range(8)


class Game:
    starting_hand_size = 5

    def __init__(self, players):
        self._city_edges, self._edges, self._deck, self._destinations, self._scoring = create_board()

        self._players = players

        # Set the first player to have the first turn.
        self._current_player_index = 0

        # Give each player a hand of 5 cards from the top of the deck.
        self._player_hands = {}
        for player in players:
            self._player_hands[player] = Hand([self._deck.pop() for x in range(self.starting_hand_size)])

        # Give each player a score of 0.
        self._player_scores = {player.name: 0 for player in self._players}

        # Give each player 3 destinations.
        self._player_destinations = {}
        for player in players:
            self._player_destinations[player] = [self._destinations.pop(), self._destinations.pop(),
                                                 self._destinations.pop()]

            # Reduce score by all incomplete destinations.
            for dest in self._player_destinations[player]:
                self._player_scores[player.name] -= dest.value()

        # Select 5 face up cards.
        self._face_up_cards = [self._deck.pop() for x in range(5)]

        # The number of actions the player has left to take this turn.
        self._num_actions_remaining = 2

        # Initialize edge claims
        self._edge_claims = {edge: None for edge in self._edges}

    def get_scoring(self):
        """
        :return: The scoring dictionary.
        """
        return dict(self._scoring)

    def get_edge_claims(self):
        """
        :return: All edge claims.
        """
        return dict(self._edge_claims)

    def get_face_up_cards(self):
        """
        See the face up cards.
        """
        return list(self._face_up_cards)

    def get_destinations(self, player):
        """
        Get the destinations for a player.

        :param player: The player.
        :return: The destinations of the player.
        """
        return list(self._player_destinations[player])

    def get_score(self, player):
        """
        See a player's score.

        :param player: The player.
        :return: The player's score.
        """
        return self._player_scores[player.name]

    def get_all_scores(self, player):
        """
        See the scores of all players.

        :param player: The player.
        :return: A dictionary of all opponents by name and their scores.
        """
        return dict(self._player_scores)

    def get_hand(self, player):
        """
        Get a player's hand.

        :param player: The player.
        :return: The hand of the player.
        """
        return list(self._player_hands[player])

    def is_turn(self, player):
        """
        Determine if it is this player's turn.

        :param player: The player.
        :return: True if it is this player's turn, false otherwise.
        """
        return player == self._players[self._current_player_index]

    def num_players(self):
        """
        Get the number of players.

        :return: The number of players.
        """
        return len(self._players)

    def in_hand(self, player, cards):
        """
        Determine if the given cards are in the player's hand.

        :param player: The player to check.
        :param cards: The cards to check for.
        :return: True if the cards are present, false otherwise.
        """
        return self._player_hands[player].contains_cards(cards)

    @staticmethod
    def cards_match(edge, cards):
        """
        Determine if a given list of cards match what the edge requires. Cards can be of the same color or have no
        color.

        :param edge: The edge to check.
        :param cards: The cards to check.
        :return: True if the cards are acceptable, False otherwise.
        """
        # Make sure there are the right number of cards.
        if len(cards) != edge.cost:
            return False

        # Figure out which color the cards need to match.  Since "None" is the highest possible color,
        # use the minimum of the list.
        if edge.color == Colors.none:
            color_to_match = min(cards)
        else:
            color_to_match = edge.color

        # Check the cards.
        for card in cards:
            if card != color_to_match and card != Colors.none:
                return False

        return True

    def lose_cards(self, player, cards):
        """
        Remove cards from a player's hand.  If the cards aren't in the player's hand, then those cards aren't affected.

        :param player: The player whose cards to remove.
        :param cards: The cards to remove.
        """
        hand = self._player_hands[player]

        for card in cards:
            hand.remove_card(card)

    def draw_face_up_card(self, player, card_index):
        """
        Have a player draw a card from the face up pile.

        :param player: The player who will be drawing.
        :param card_index: The index of the card being drawn.
        :return: A tuple containing a boolean and an int.  Boolean will be True if the action succeeded,
        False otherwise.  Integer will correspond to a failure cause in the FailureCause object.
        """
        # Make sure it is the correct turn.
        if not self.is_turn(player):
            return False, FailureCause.wrong_turn

        # Make sure index is valid.
        if card_index >= len(self._face_up_cards):
            return False, FailureCause.invalid_card_index

        card = self._face_up_cards[card_index]
        hand = self._player_hands[player]

        # Wilds require 2 actions.
        if card == Colors.none and self._num_actions_remaining == 1:
            return False, FailureCause.already_drew

        # Put card in hand.
        hand.add_card(card)

        # Replace face up card.
        self._face_up_cards[card_index] = self._deck.pop()

        # Complete action.
        self._use_actions(1 if card != Colors.none else 2)

        return True, FailureCause.none

    def draw_from_deck(self, player):
        """
        Have a player draw a card from the deck.

        :param player: The player who will be drawing.
        :return: A tuple containing a boolean and an int.  Boolean will be True if the action succeeded,
        False otherwise.  Integer will correspond to a failure cause in the FailureCause object.
        """
        # Make sure it is the correct turn.
        if not self.is_turn(player):
            return False, FailureCause.wrong_turn

        hand = self._player_hands[player]

        hand.add_card(self._deck.pop())

        self._use_actions(1)

        return True, FailureCause.none

    def connect_cities(self, player, city1, city2, edge_color, cards):
        """
        Connect 2 cities.  It must the player's turn to call this.

        :param player: The player who will be performing the connection.
        :param city1: The first city to connect.
        :param city2: The second city to connect.
        :param edge_color: The color of the connection.  This is important because some cities have multiple edges of
        different colors.
        :param cards: The cards from the player's hand to use when making the claim.
        :return: A tuple containing a boolean and an int.  Boolean will be True if the action succeeded,
        False otherwise.  Integer will correspond to a failure cause in the FailureCause object.
        """
        # Make sure it is the correct turn.
        if not self.is_turn(player):
            return False, FailureCause.wrong_turn

        # 2 Actions must remain
        if self._num_actions_remaining != 2:
            return False, FailureCause.already_drew

        # Find the edge and claim it if possible.
        for edge in city1.edges:
            if edge.contains_city(city2) and not self.edge_is_claimed(edge) and edge.color() == edge_color:
                # Player must have the given cards.
                if not self.in_hand(player, cards):
                    return False, FailureCause.missing_cards

                # Cards must match the edge's requirements.
                if not self.cards_match(edge, cards):
                    return False, FailureCause.incompatible_cards

                self._claim_edge(edge, player)
                self.lose_cards(player, cards)
                self._player_scores[player.name] = self._player_scores[player.name] + self._scoring[edge.cost]
                self._use_actions(2)

                return True, FailureCause.none

        return False, FailureCause.no_route

    def _claim_edge(self, edge, player):
        """
        Claim an edge for a player.

        :param edge:
        :param player:
        """
        self._edge_claims[edge] = player.name

    def edge_is_claimed(self, edge):
        """
        Determines if an edge is claimed.

        :param edge:
        :return: True if the edge is claimed, false otherwise.
        """
        return self._edge_claims[edge] is not None

    def _use_actions(self, num_actions):
        """
        Use up actions for the current player this turn.

        :param num_actions: The number of actions to use up.
        """
        self._num_actions_remaining -= num_actions

        # Running out of actions means the turn is over.
        if self._num_actions_remaining <= 0:
            self._num_actions_remaining = 2
            self._current_player_index = (self._current_player_index + 1) % len(self._players)
