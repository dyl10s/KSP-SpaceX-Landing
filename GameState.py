class GameState:
    def __init__(self, game):
        self.game = game
    
    def getState(self, actions):
        score = self.game.getScore()
        reward = 10 * score
        isOver = False

        self.game.Pitch(actions[0])
        self.game.Yaw(actions[1])
        self.game.Roll(actions[2])
        self.game.Throttle(actions[3])

        if self.game.isDead():
            self.game.restart()
            reward = -10/(score + .00001)
            isOver = True
        
        return self.game.getState(), reward, isOver
