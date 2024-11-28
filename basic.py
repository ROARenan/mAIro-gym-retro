import retro
import numpy as np
import random
from rominfo import *

def dec2bin(dec):
    binN = []
    while dec != 0:
        binN.append(dec % 2)
        dec = dec / 2
    return binN

def createEnv():
    return retro.make(game='SuperMarioWorld-Snes', state='YoshiIsland2', record=False)

env = createEnv()

actions = [66,130,128,131,386]

episodes = 5
for episode in range(1, episodes+1):
    state = env.reset()
    done = False
    score = 0 
    
    while not done and getLives(env) >= 5:
        env.render()
        action = dec2bin(random.choice(actions))
        n_state, reward, done, info = env.step(action)
        score+=reward
    print('Episode:{} Score:{}'.format(episode, score))
env.close()

# actions_map = {'noop':0, 'down':32, 'up':16, 'jump':1, 'spin':3, 
#                'left':64, 'jumpleft':65, 'runleft':66, 'runjumpleft':67, 
#                'right':128, 'jumpright':129, 'runright':130, 'runjumpright':131, 
#                'spin':256, 'spinright':384, 'runspinright':386, 'spinleft':320, 'spinrunleft':322
#                }