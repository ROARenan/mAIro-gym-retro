import retro
import numpy as np
from rominfo import getXY, getRam, getSprites, getLives

# Lista de ações possíveis para Mario
actions_map = {'noop':0, 'down':32, 'up':16, 'jump':1, 'spin':3, 
               'left':64, 'jumpleft':65, 'runleft':66, 'runjumpleft':67, 
               'right':128, 'jumpright':129, 'runright':130, 'runjumpright':131, 
               'spin':256, 'spinright':384, 'runspinright':386, 'spinleft':320, 'spinrunleft':322
               }

# Vamos usar apenas um subconjunto
actions_list = [66,130,128,131,386]

def dec2bin(dec):
    binN = []
    while dec != 0:
        binN.append(dec % 2)
        dec = dec / 2
    return binN

# Função para criar o ambiente
def create_env():
    return retro.make(game='SuperMarioWorld-Snes', state='YoshiIsland2', record=False)

# Recompensa baseada no deslocamento
def calculate_reward(ram, last_x_position):
    marioX, _, _, _ = getXY(ram)  # Obtém a posição X de Mario
    delta_x = marioX - last_x_position  # Diferença no deslocamento horizontal

    # Recompensa positiva para deslocamento à direita, penalidade para esquerda ou falta de movimento
    if delta_x > 0:
        reward = delta_x  # Movimento positivo gera recompensa proporcional
    elif delta_x <= 0:
        reward = -1  # Movimento para a esquerda ou falta de movimento gera penalidade fixa

    return reward, marioX

# Main
if __name__ == "__main__":
    env = create_env()
    state = env.reset()
    
    last_x_position = 0  # Posição inicial do Mario no eixo X
    total_reward = 0
    reset_live = 5

    while True:
        env.render()  # Mostra o jogo na tela

        # Escolhe uma ação aleatória da lista de ações definidas
        action = actions_list[np.random.randint(len(actions_list))]
        state, _, done, info = env.step(dec2bin(action))

        # Obtemos a RAM do jogo
        ram = getRam(env)
        if getLives(env) != 5:
            done = True

        # Calcula a recompensa baseada no deslocamento horizontal
        reward, last_x_position = calculate_reward(ram, last_x_position)
        total_reward += reward
        print(getXY(ram))
        #print(getSprites(ram))
        #print(f"Reward: {reward}, Total Reward: {total_reward}, X Position: {last_x_position}")

        if done:
            print(f"Game over! Total Reward: {total_reward}")
            break

    env.close()
