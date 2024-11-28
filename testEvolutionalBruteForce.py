import retro
import numpy as np
import tensorflow as tf
import random
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.optimizers import Adam
from rominfo import *

# Função para converter número decimal para binário (exemplo para ações)
def dec2bin(dec, num_bits):
    binN = [0] * num_bits
    idx = 0
    while dec != 0:
        binN[idx] = dec % 2
        dec = dec // 2
        idx += 1
    return binN

# Criação do ambiente
def createEnv():
    return retro.make(game='SuperMarioWorld-Snes', state='YoshiIsland2', record=False)

# Função para construir o modelo
def build_model(input_shape, num_actions):
    model = Sequential()
    
    # Primeira camada densa
    model.add(Dense(128, input_dim=input_shape, activation='relu'))
    
    # Camada de saída com num_actions neurônios (um para cada ação possível)
    model.add(Dense(num_actions, activation='linear'))  # Saída contínua para Q-values
    
    model.compile(loss='mean_squared_error', optimizer=Adam())  # Usando MSE para Q-learning
    return model

# Função para gerar filhos (cópias ou mutação simples nos pesos)
def generate_offspring(parents, num_offspring=3):
    offspring = []
    for parent in parents:
        for _ in range(num_offspring):
            # Criar um filho com uma nova arquitetura igual ao modelo pai
            num_actions = parent.layers[-1].output_shape[1]  # Extrair o número de ações da camada de saída
            child = build_model(input_shape=4, num_actions=num_actions)  # Novo modelo com a mesma arquitetura
            
            # Copiar pesos do modelo pai para o modelo filho
            parent_weights = parent.get_weights()
            child.set_weights(parent_weights)
            
            # Pequena mutação aleatória nos pesos
            mutated_weights = []
            for weight in parent_weights:
                mutated_weights.append(weight + np.random.randn(*weight.shape) * 0.1)  # Pequena mutação
            child.set_weights(mutated_weights)
            
            offspring.append(child)
    return offspring

# Função para treinar o modelo no jogo
def training_model(env, num_episodes=1000, num_individuals=3):
    actions = [66, 130, 128, 131, 386]  # As possíveis ações
    num_actions = len(actions)
    individuals = [build_model(input_shape=4, num_actions=num_actions) for _ in range(num_individuals)]  # Inicializar modelos
    
    # Treinar por um número fixo de episódios
    for episode in range(1, num_episodes + 1):
        scores = []  # Lista para armazenar as pontuações de cada indivíduo
        
        # Cada indivíduo joga o episódio
        for individual in individuals:
            env.reset()
            total_reward = 0
            done = False

            while not done and getLives(env) >= 5:
                env.render()
                
                # Selecionando a ação aleatoriamente
                action = random.choice(actions)
                
                # Convertendo a ação para binário usando a função dec2bin
                action_bin = dec2bin(action, num_bits=9)  # Número de bits dependendo da representação binária da ação
                
                # Tomando a ação no ambiente
                next_state, reward, done, info = env.step(action_bin)
                total_reward += reward  # Acumulando a recompensa
                
            scores.append(total_reward)
        
        # Seleção dos melhores indivíduos
        best_individuals_idx = np.argsort(scores)[-3:]  # Índices dos 3 melhores indivíduos
        best_individuals = [individuals[idx] for idx in best_individuals_idx]  # Melhores indivíduos
        
        # Gerar filhos com base nos melhores indivíduos
        offspring = generate_offspring(best_individuals)
        
        # Substituir os indivíduos antigos pelos novos
        individuals = offspring
        
        # Mostrar as pontuações dos indivíduos
        print(f'Episódio {episode}/{num_episodes} | Pontuação dos indivíduos: {scores}')

# Criando o ambiente
env = createEnv()

# Treinando o modelo com múltiplos indivíduos e avaliação de desempenho
training_model(env, num_episodes=1000, num_individuals=3)
