import pandas as pd
import numpy as np

PAYOFF = pd.DataFrame(np.array([[5, -10], [10, -5]]), columns=[True, False], index=[True, False]) # True = good, False = bad

class Player:
    def __init__(self, payoff, friends=None):
        """Initialize a player"""
        self.score = 0
        self.history = {'own': [], 'other': []}
        self.payoff = payoff
        self.name = None
        self.friends = friends

    def __hash__(self):
        if self.friends is not None:
            return hash((self.name, tuple(self.friends)))
        return hash(self.name)

    def update_score(self, own_move, other_move):
        """Update the score of the player"""
        self.score += self.payoff.loc[own_move, other_move]
        self.history['own'].append(own_move)
        self.history['other'].append(other_move)


class GoodPlayer(Player):
    def __init__(self, payoff, friends=None):
        super().__init__(payoff, friends)
        self.name = "Good Player"

    def __str__(self):
        return self.name

    def make_move(self):
        """Make a move for a Good player"""
        return True


class BadPlayer(Player):
    def __init__(self, payoff, friends=None):
        super().__init__(payoff, friends)
        self.name = "Bad Player"

    def __str__(self):
        return self.name

    def make_move(self):
        """Make a move for a Bad player"""
        return False


class CopycatPlayer(Player):
    def __init__(self, payoff, friends=None):
        super().__init__(payoff, friends)
        self.name = "Copycat Player"

    def __str__(self):
        return self.name

    def make_move(self):
        """Make a move for a Copycat player"""
        if len(self.history['own']) == 0:
            return True
        else:
            return self.history['other'][-1]


class GrudgePlayer(Player):
    def __init__(self, payoff, friends=None):
        super().__init__(payoff, friends)
        self.name = "Grudge Player"
        self.betrayed = False

    def __str__(self):
        return self.name

    def make_move(self):
        """Make a move for a Grudge player"""
        if len(self.history['own']) == 0:
            return True
        if self.betrayed:
            return False
        elif self.history['other'][-1] == False:
            self.betrayed = True
            return False
        else:
            return True


class DetectivePlayer(Player):
    def __init__(self, payoff, friends=None):
        super().__init__(payoff, friends)
        self.name = "Detective Player"
        self.opening = [True, False, True, True]
        self.betrayed = False

    def __str__(self):
        return self.name

    def make_move(self):
        """Make a move for a Detective player"""
        if len(self.history['own']) != 0 and self.history['other'][-1] == False:
            self.betrayed = True
        if len(self.history['own']) < 4:
            return self.opening[len(self.history['own'])]
        elif self.betrayed:
            return self.history['other'][-1]
        else:
            return False

class RandomPlayer(Player):
    def __init__(self, payoff, friends=None):
        super().__init__(payoff, friends)
        self.name = "Random Player"

    def __str__(self):
        return self.name

    def make_move(self):
        """Make a move for a Random player"""
        return np.random.choice([True, False])

class Game:
    def __init__(self, player1, player2, payoff, num_turns=10):
        """
        Initialize a game
        player1: Player
        player2: Player
        payoff: DataFrame
        """
        self.player1 = player1(payoff)
        self.player2 = player2(payoff)
        self.num_turns = num_turns

    def play_turn(self):
        """Play a turn of the game"""
        move1 = self.player1.make_move()
        move2 = self.player2.make_move()
        self.player1.update_score(move1, move2)
        self.player2.update_score(move2, move1)

    def play_game(self):
        """Play a game"""
        for _ in range(self.num_turns):
            self.play_turn()
        return {'result': (self.player1.score, self.player2.score),
                'history': (self.player1.history, self.player2.history)
                }


def main():
    game = Game(DetectivePlayer, BadPlayer, PAYOFF)
    output = game.play_game()
    result = output['result']
    history = output['history']
    pretty_history = pd.DataFrame([history[0]['own'], history[1]['own']],
                                  index=[str(game.player1), str(game.player2)],
                                  columns=np.arange(1, 11)).T
    print("Result of the game:\n\tPlayer 1 ({}): {}\n\tPlayer 2 ({}): {}\n\nNote that values show score for the row player".format(
        game.player1, result[0], game.player2, result[1])
    )
    print("History of the game:\n{}".format(pretty_history))


if __name__ == '__main__':
    main()
