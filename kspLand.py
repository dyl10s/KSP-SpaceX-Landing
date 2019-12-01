import Game
import Learn
import GameState

#Trains and Runs the KSP Agent
game = Game.Game()
state = GameState.GameState(game)
model = Learn.buildModel(game)
Learn.train(model, state)
Learn.evaluate(model, state)

