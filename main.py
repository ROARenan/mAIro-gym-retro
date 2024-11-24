import retro
import numpy as np
from rominfo import getXY, getRam

# Lista de ações possíveis para Mario
ACTIONS = [
    [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],  # Direita
    [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],  # Pulo
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],  # Pulo rodando
    [0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0],  # Direita + Pulo
    [0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0],  # Direita + Pulo rodando
    [0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0],  # Correr + Direita
    [0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0],  # Correr + Direita + Pulo
    [0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 0],  # Correr + Direita + Pulo rodando
]

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

    while True:
        env.render()  # Mostra o jogo na tela

        # Escolhe uma ação aleatória da lista de ações definidas
        action = ACTIONS[np.random.randint(len(ACTIONS))]
        state, _, done, info = env.step(action)

        # Obtemos a RAM do jogo
        ram = getRam(env)

        # Calcula a recompensa baseada no deslocamento horizontal
        reward, last_x_position = calculate_reward(ram, last_x_position)
        total_reward += reward

        print(f"Reward: {reward}, Total Reward: {total_reward}, X Position: {last_x_position}")

        if done:
            print(f"Game over! Total Reward: {total_reward}")
            break

    env.close()
