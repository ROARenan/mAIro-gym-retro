import retro
import numpy as np
import tensorflow as tf
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

# Função para treinar o modelo no jogo
def training_model(model, env, num_episodes=1000):
    actions = [66, 130, 128, 131, 386]  # As possíveis ações
    num_actions = len(actions)
    
    for episode in range(num_episodes):
        env.reset()
        ram_data = getRam(env)  # Obtendo a memória do jogo
        state = getXY(ram_data)  # Obtendo as posições de Mario e outros elementos
        state_input = np.array(state).reshape((1, -1))  # Transformando o estado em um formato adequado
        total_reward = 0
        done = False
        pos_count = 0
        mario_last_pos = (state[0],state[1])
        
        while not done and getLives(env) >= 5:
            env.render()
            # Selecionando a ação usando a rede neural
            q_values = model.predict(state_input)  # Obtendo Q-values para cada ação
            action = np.argmax(q_values[0])  # Escolhendo a ação com maior Q-value
            
            # Convertendo a ação para binário usando a função dec2bin
            action_bin = dec2bin(actions[action], num_bits=9)  # Número de bits dependendo da representação binária da ação
            
            # Tomando a ação no ambiente
            next_state, reward, done, info = env.step(action_bin)
            
            # Coletando os dados para treinamento
            total_reward += reward
            next_ram_data = getRam(env)  # Obtendo a memória para o próximo estado
            next_state_input = getXY(next_ram_data)  # Obtendo as posições para o próximo estado
            if mario_last_pos[0] == next_state_input[0] and mario_last_pos[1] == next_state_input[1]:
                pos_count += 1
                if pos_count >= 60:
                    done = True
            else:
                pos_count = 0
            mario_last_pos = (next_state_input[0],next_state_input[1])
            print(f"Parado a {pos_count} frames")

            next_state_input = np.array(next_state_input).reshape((1, -1))  # Formatando para o modelo
            
            

            # Estimando o Q-value target
            next_q_values = model.predict(next_state_input)
            target = reward + 0.99 * np.max(next_q_values)  # Estimativa de Q-value
            
            # Atualizando o Q-value da ação tomada
            q_values[0][action] = target
            
            # Treinando o modelo
            model.fit(state_input, q_values, epochs=1, verbose=0)
            
            # Atualizando o estado
            state_input = next_state_input
        
        print(f'Episódio {episode + 1}/{num_episodes} | Recompensa total: {total_reward}')


# Criando o ambiente e o modelo
env = createEnv()
input_shape = 4  # Ajuste para o formato do seu estado
actions = [130,128,131,386]

model = build_model(input_shape, len(actions))

# Treinando o modelo
training_model(model, env)
