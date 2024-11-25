import retro
import numpy as np
import random
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.optimizers import Adam
from rominfo import getXY, getRam

# Configurações do Algoritmo Genético
POPULATION_SIZE = 10
GENERATIONS = 20
MUTATION_RATE = 0.1
MAX_STEPS = 1000  # Número máximo de passos por agente

# Lista de ações possíveis para Mario
actions_map = {'noop':0, 'down':32, 'up':16, 'jump':1, 'spin':3, 
               'left':64, 'jumpleft':65, 'runleft':66, 'runjumpleft':67, 
               'right':128, 'jumpright':129, 'runright':130, 'runjumpright':131, 
               'spin':256, 'spinright':384, 'runspinright':386, 'spinleft':320, 'spinrunleft':322
               }

# Vamos usar apenas um subconjunto
actions_list = [130,128,131,386]

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

def get_lives(env):
    """
    Obtém o número de vidas do jogador no Super Mario World.
    O número de vidas está armazenado no endereço 0x7E0DBE.
    """
    lives_address = 0x0DBE  # Endereço de memória relativo para vidas no Super Mario World
    ram = env.get_ram()  # Obtém a memória RAM do jogo
    lives_minus_one = ram[lives_address]  # Lê o valor no endereço especificado
    return lives_minus_one + 1  # Ajusta para refletir o número correto de vidas

# Modelo da rede neural
def create_model(input_dim, output_dim):
    model = Sequential([
        Dense(128, input_dim=input_dim, activation='relu'),
        Dense(128, activation='relu'),
        Dense(output_dim, activation='softmax')  # Probabilidades para as ações
    ])
    return model

# Avaliação do agente
def evaluate_agent(env, model, max_steps=MAX_STEPS):
    state = env.reset()
    state = preprocess_state(state)
    total_reward = 0
    last_x_position = 0

    for step in range(max_steps):
        env.render()
        
        # Prediz a ação com base no estado atual
        q_values = model.predict(state.reshape(1, -1), verbose=0)
        action_index = np.argmax(q_values)
        action = actions_list[action_index]

        state, _, done, info = env.step(dec2bin(action))
        state = preprocess_state(state)

        # Calcula recompensa
        ram = getRam(env)
        reward, last_x_position = calculate_reward(ram, last_x_position)
        total_reward += reward

        # Finaliza se o Mario perder uma vida ou se o jogo acabar
        if get_lives(env) != 5 or done:
            break

    return total_reward

# Preprocessamento do estado (opcional)
def preprocess_state(state):
    return state.flatten() / 255.0  # Normaliza os valores da imagem

# Mutação dos pesos da rede
def mutate_weights(weights, mutation_rate):
    new_weights = []
    for layer in weights:
        if np.random.rand() < mutation_rate:
            noise = np.random.normal(0, 0.1, layer.shape)
            new_weights.append(layer + noise)
        else:
            new_weights.append(layer)
    return new_weights

# Reprodução (Crossover)
def crossover_weights(parent1, parent2):
    child_weights = []
    for layer1, layer2 in zip(parent1, parent2):
        mask = np.random.randint(0, 2, size=layer1.shape).astype(bool)
        child_layer = np.where(mask, layer1, layer2)
        child_weights.append(child_layer)
    return child_weights

# Main Loop do Algoritmo Genético
if __name__ == "__main__":
    env = create_env()
    input_dim = np.prod(env.observation_space.shape)
    output_dim = len(actions_list)

    # Cria população inicial
    population = [create_model(input_dim, output_dim) for _ in range(POPULATION_SIZE)]

    for generation in range(GENERATIONS):
        print(f"Generation {generation + 1}")

        # Avalia todos os agentes na população
        fitness_scores = []
        for agent in population:
            score = evaluate_agent(env, agent)
            fitness_scores.append(score)

        # Seleciona os melhores agentes
        sorted_indices = np.argsort(fitness_scores)[::-1]  # Ordem decrescente
        top_agents = [population[i] for i in sorted_indices[:POPULATION_SIZE // 2]]

        # Gera novos agentes (filhos)
        new_population = []
        for _ in range(POPULATION_SIZE // 2):
            parent1, parent2 = random.sample(top_agents, 2)
            child = create_model(input_dim, output_dim)
            child_weights = crossover_weights(parent1.get_weights(), parent2.get_weights())
            mutated_weights = mutate_weights(child_weights, MUTATION_RATE)
            child.set_weights(mutated_weights)
            new_population.append(child)

        # Atualiza a população
        population = top_agents + new_population

        # Mostra a melhor pontuação da geração
        print(f"Best score: {fitness_scores[sorted_indices[0]]}")

    env.close()
