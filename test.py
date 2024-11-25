import retro
import numpy as np
import random
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from rominfo import getXY, getRam
import time

# Configurações do Algoritmo Genético
POPULATION_SIZE = 10
GENERATIONS = 20
MUTATION_RATE = 0.1
MAX_STEPS = 1000  # Número máximo de passos por agente
FRAME_SKIP = 4  # Avaliar a cada 4 frames

# Lista de ações possíveis para Mario
actions_list = [66, 130, 128, 131, 386]

def dec2bin(dec):
    binN = []
    while dec != 0:
        binN.append(dec % 2)
        dec = dec // 2
    return binN

def create_env():
    return retro.make(game='SuperMarioWorld-Snes', state='YoshiIsland2', record=False)

def calculate_reward(ram, last_x_position):
    marioX, _, _, _ = getXY(ram)
    delta_x = marioX - last_x_position
    return delta_x if delta_x > 0 else -1, marioX

def get_lives(env):
    lives_address = 0x0DBE
    ram = env.get_ram()
    return ram[lives_address] + 1

def create_model(input_dim, output_dim):
    model = Sequential([
        Dense(128, input_dim=input_dim, activation='relu'),
        Dense(128, activation='relu'),
        Dense(output_dim, activation='softmax')
    ])
    return model

def evaluate_agent(env, model, max_steps=MAX_STEPS, frame_skip=FRAME_SKIP):
    state = env.reset()
    state = preprocess_state(state)
    total_reward = 0
    last_x_position = 0

    for step in range(max_steps):
        if step % frame_skip == 0:
            q_values = model.predict(state.reshape(1, -1), verbose=0)
            action_index = np.argmax(q_values)
            action = actions_list[action_index]
        else:
            action = 0  # "No operation" nos frames intermediários

        state, _, done, info = env.step(dec2bin(action))
        state = preprocess_state(state)

        if step % frame_skip == 0:
            ram = getRam(env)
            reward, last_x_position = calculate_reward(ram, last_x_position)
            total_reward += reward

        if get_lives(env) != 5 or done:
            break

        time.sleep(0.02)  # Intervalo para manter o fluxo do jogo

    return total_reward

def preprocess_state(state):
    return state.flatten() / 255.0

def mutate_weights(weights, mutation_rate):
    return [layer + np.random.normal(0, 0.1, layer.shape) if np.random.rand() < mutation_rate else layer for layer in weights]

def crossover_weights(parent1, parent2):
    return [np.where(np.random.randint(0, 2, size=l1.shape).astype(bool), l1, l2) for l1, l2 in zip(parent1, parent2)]

if __name__ == "__main__":
    env = create_env()
    input_dim = np.prod(env.observation_space.shape)
    output_dim = len(actions_list)

    population = [create_model(input_dim, output_dim) for _ in range(POPULATION_SIZE)]

    for generation in range(GENERATIONS):
        print(f"Generation {generation + 1}")

        fitness_scores = []
        for agent in population:
            score = evaluate_agent(env, agent, frame_skip=FRAME_SKIP)
            fitness_scores.append(score)

        sorted_indices = np.argsort(fitness_scores)[::-1]
        top_agents = [population[i] for i in sorted_indices[:POPULATION_SIZE // 2]]

        new_population = []
        for _ in range(POPULATION_SIZE // 2):
            parent1, parent2 = random.sample(top_agents, 2)
            child = create_model(input_dim, output_dim)
            child_weights = crossover_weights(parent1.get_weights(), parent2.get_weights())
            mutated_weights = mutate_weights(child_weights, MUTATION_RATE)
            child.set_weights(mutated_weights)
            new_population.append(child)

        population = top_agents + new_population

        print(f"Best score: {fitness_scores[sorted_indices[0]]}")

    env.close()
