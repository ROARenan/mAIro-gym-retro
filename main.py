import retro
import numpy as np
from rominfo import *

def dec2bin(dec):
    binN = []
    while dec != 0:
        binN.append(dec % 2)
        dec = dec / 2
    return binN

# Função para criar o ambiente
def createEnv():
    return retro.make(game='SuperMarioWorld-Snes', state='YoshiIsland2', record=False)

# Função para determinar a próxima ação baseada na posição de Mario e nos sprites
def heuristicAction(mario_pos, sprites, ram, env):
    """
    Determina a ação de Mario baseada na heurística:
    - Move para a direita.
    - Pula se houver obstáculos, degraus ou bloqueio à direita.
    - Se estiver bloqueado à direita, faz um long jump (pulo normal seguido de um pulo longo).

    Args:
        mario_pos (tuple): Posição de Mario (x, y, layer1x, layer1y).
        sprites (list): Lista de sprites na tela.
        ram (numpy.array): Memória RAM do jogo.
        env: Ambiente Retro para leitura da RAM.

    Returns:
        action (list): Lista de ações para o ambiente Retro (duas ações se for long jump).
    """
    mario_x, mario_y, _, _ = mario_pos

    # Ação padrão: mover para a direita
    action = [dec2bin(130)]  # Primeira ação: mover para a direita

    # Verifica bloqueios usando a função getStuckInWall
    stuck_status = getStuckStatus(env)
    if stuck_status["right"]:  # Bloqueado à direita
        # Pulo normal e, em seguida, pulo longo
        action = [dec2bin(131), dec2bin(131)]  # Executa dois pulos
        return action

    # Verifica se há sprites (inimigos ou obstáculos) próximos
    for sprite in sprites:
        sprite_x, sprite_y = sprite['x'], sprite['y']
        if 0 < sprite_x - mario_x < 50 and sprite_y <= mario_y + 30:  # Obstáculo à frente
            action = [dec2bin(131)]  # Pular
            return action

    return action

if __name__ == "__main__":
    env = createEnv()
    state = env.reset()
    total_reward = 0

    for step in range(10000):  # Limite de passos
        env.render()
        ram = getRam(env)

        # Obtém informações do jogo
        mario_pos = getXY(ram)  # Posição de Mario
        sprites = getSprites(ram)  # Informações dos sprites na tela
        print(mario_pos)
        # Determina a ação usando heurística
        actions = heuristicAction(mario_pos, sprites, ram, env)  # Recebe uma lista de ações

        # Executa as ações no ambiente
        for action in actions:
            state, reward, done, info = env.step(action)
            total_reward += reward
        print("Score:",getScore(env))
        print("Cleared: ", getCleared(env))
        # Checa se Mario perdeu todas as vidas
        if getLives(env) < 5 or env.data.is_done():
            print(f"Game Over! Total Reward: {total_reward}")
            break

    env.close()

# Lista de ações possíveis para Mario
# actions_map = {'noop':0, 'down':32, 'up':16, 'jump':1, 'spin':3, 
#                'left':64, 'jumpleft':65, 'runleft':66, 'runjumpleft':67, 
#                'right':128, 'jumpright':129, 'runright':130, 'runjumpright':131, 
#                'spin':256, 'spinright':384, 'runspinright':386, 'spinleft':320, 'spinrunleft':322
#                }