import Game
import Learn
import GameState

game = Game.Game()
state = GameState.GameState(game)
model = Learn.buildModel()
Learn.train(model, state)
