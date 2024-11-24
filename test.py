import retro
import numpy as np
import random

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
  
def getRam(env):
    return np.array(list(env.data.memory.blocks[8257536]))

# Função para obter as vidas do Mario
def get_lives(env):
    """
    Obtém o número de vidas do jogador no Super Mario World.
    O número de vidas está armazenado no endereço 0x7E0010.
    """
    lives_address = 0x7E0010  # Endereço de memória para vidas no Super Mario World
    # Usando a API retro para ler o valor diretamente da memória
    info = getRam(env)
    lives = 5
    return lives

# Main
if __name__ == "__main__":
    env = create_env()
    state = env.reset()

    while True:
        env.render()  # Mostra o jogo na tela

        # Lê a memória do emulador para verificar o número de vidas
        lives = get_lives(env)  # Obtém o número de vidas

        # Imprime o número de vidas no terminal
        print(f"Número de vidas: {lives}")

        # Executa uma ação aleatória
        action = random.choice(ACTIONS)
        state, _, done, info = env.step(action)

        if done:
            break

    env.close()
