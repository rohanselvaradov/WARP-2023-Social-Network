from classes import *
import itertools

players = [GoodPlayer, BadPlayer, CopycatPlayer, GrudgePlayer, DetectivePlayer]
names = [str(player(None)) for player in players]

outcomes = pd.DataFrame(index=names, columns=names)

# Go through all possible combinations of players and add scores to dataframe
for p1, p2 in itertools.combinations_with_replacement(players, 2):
    game = Game(p1, p2, PAYOFF)
    result = game.play_game()['result']
    outcomes.loc[str(game.player1), str(game.player2)] = result[0]
    outcomes.loc[str(game.player2), str(game.player1)] = result[1]

print(outcomes)