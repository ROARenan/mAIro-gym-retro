import retro
import numpy as np
from rominfo import getXY, getRam, getSprites, getLives, getTile

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
def heuristicAction(mario_pos, sprites, ram):
    mario_x, mario_y, _, _ = mario_pos

    # Heurística: Avance para a direita
    action = dec2bin(130)

    # Verifica se há sprites (como inimigos ou obstáculos) próximos
    for sprite in sprites:
        sprite_x, sprite_y = sprite['x'], sprite['y']
        if 0 < sprite_x - mario_x < 50 and sprite_y <= mario_y + 30:  # Obstáculo à frente
            action = dec2bin(131)  # Pular
            break

    # Verifica se há um bloco sólido no caminho de Mario
    for offset_x in range(16, 50, 16):  # Checa 16 a 50 pixels à frente
        tile = getTile(mario_x + offset_x, mario_y + 16, ram)  # Ponto um pouco abaixo de Mario
        if tile != 0:  # Se houver bloco sólido
            action = dec2bin(131)  # Pular
            break

    return action

if __name__ == "__main__":
    env = createEnv()
    state = env.reset()
    total_reward = 0

    for step in range(10000):  # Limite de passos
        env.render()
        ram = getRam(env)

        # Obtém informações do jogo
        mario_pos = getXY(ram)  # Posição do Mario
        sprites = getSprites(ram)  # Informações dos sprites na tela

        # Determina a ação usando heurística
        action = heuristicAction(mario_pos, sprites, ram)

        # Executa a ação no ambiente
        state, reward, done, info = env.step(action)
        total_reward += reward

        # Checa se Mario perdeu todas as vidas
        if getLives(env) < 5:
            print(f"Game Over! Total Reward: {total_reward}")
            break

    env.close()
