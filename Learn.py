import tensorflow as tf
import numpy as np
from tensorflow import keras

LEARNING_RATE = .01

def buildModel():
    model = keras.Sequential()

    model.add(keras.layers.Dense(
        6,
        activation='relu',
        input_dim=4,
    ))

    model.add(keras.layers.Dense(
        8,
        activation='relu'
    ))

    model.add(keras.layers.Dense(
        4,
        activation='sigmoid'
    ))

    adam = keras.optimizers.Adam(lr=LEARNING_RATE)
    model.compile(loss='mse', optimizer=adam)
    return model

def train(model, gameState):
    doNothing = (0, 0, 0, 0)
    
    curState, reward, isOver = gameState.getState(doNothing)
    while True:
        q = model.predict((curState,))
        model.fit([gameState.game.getState()], [[1, 0, 0, .1]])
        curState, reward, isOver = gameState.getState(q[0])
        if isOver:
            gameState.game.restart()
            model.save('ksp.h5')


