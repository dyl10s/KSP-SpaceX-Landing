import tensorflow as tf
import numpy as np
from tensorflow import keras

LEARNING_RATE = .01

#This is where we construct our model's shape
#as well as details about how it should optomize / train
def buildModel(game):
    model = keras.Sequential()

    model.add(keras.layers.Dense(
        16,
        activation='sigmoid',
        input_dim=len(game.getState()),
    ))

    model.add(keras.layers.Dense(
        1,
        activation='sigmoid'
    ))

    adam = keras.optimizers.Adam(lr=LEARNING_RATE)
    model.compile(loss='mse', optimizer=adam)
    return model

#This function generates and then trains on 1000
#data points for 100 cycles. We use the getOptimalVelocityFromHeight
#function to generate the data
def train(model, gameState):
    trainInput = []
    trainOutput = []
    for x in range(0, 1000):
        trainInput.append(x)
        trainOutput.append(gameState.game.getOptimalVelocityFromHeight(x))

    for x in range(0, 100):
        model.fit(trainInput, trainOutput)

#This function will run the KSP simulation with
#the results from our trained model
def evaluate(model, gameState):
    curState = gameState.game.getState()
    while True:
        q = model.predict((curState,))
        print([curState])
        curState, isOver = gameState.getState(q[0])

        if isOver:
            gameState.game.restart()
            model.save('ksp.h5')