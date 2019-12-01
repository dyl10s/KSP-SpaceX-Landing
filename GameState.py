class GameState:
    def __init__(self, game):
        self.game = game
    
    #Get the current state of the game as well as running the specified actions
    #on the game client. Returns the state and a value that says if the
    #vessel has exploded or not
    def getState(self, actions):
        isOver = False

        self.game.Throttle(actions[0].item())

        if self.game.isDead():
            isOver = True
        
        return self.game.getState(), isOver
