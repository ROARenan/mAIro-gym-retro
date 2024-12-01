import sys
import retro
import numpy as np
import tensorflow as tf
import random
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.optimizers import Adam
import rominfo

# Converte número decimal para binário (utilizado para ações no ambiente)
def dec2bin(dec, num_bits):
    binN = [0] * num_bits
    idx = 0
    while dec != 0:
        binN[idx] = dec % 2
        dec //= 2
        idx += 1
    return binN

# Informações do Ambiente no Console
def update_console(episode, num_episodes, generation, score):
    sys.stdout.write(
        f"\rEpisódio {episode}/{num_episodes} | Geração: {generation} | Pontuação Atual: {score:.2f}"
    )
    sys.stdout.flush()

# Criação do ambiente de jogo
def createEnv():
    return retro.make(game='SuperMarioWorld-Snes', state='YoshiIsland2', record=False)

# Construção do modelo de rede neural
def build_model(input_shape, num_actions):
    model = Sequential()
    model.add(Dense(128, input_dim=input_shape, activation='relu'))  # Camada oculta
    model.add(Dense(64, activation='relu'))  # Camada oculta adicional
    model.add(Dense(num_actions, activation='linear'))  # Saída com Q-values
    model.compile(loss='mean_squared_error', optimizer=Adam())  # Otimizador Adam
    return model

# Geração de novos indivíduos (modelos) com mutação nos pesos
def generate_offspring(parents, input_shape, num_offspring=3):
    offspring = []
    for parent in parents:
        for _ in range(num_offspring):
            num_actions = parent.layers[-1].output_shape[1]  # Número de ações
            child = build_model(input_shape=input_shape, num_actions=num_actions)
            
            # Copiar pesos do modelo pai e aplicar mutação leve
            parent_weights = parent.get_weights()
            mutated_weights = [w + np.random.randn(*w.shape) * 0.1 for w in parent_weights]
            child.set_weights(mutated_weights)
            
            offspring.append(child)
    return offspring

# Recompensa personalizada baseada no progresso
def custom_reward(reward, info, previous_info):
    position_reward = 200 if info["x"] > previous_info["x"] + 1 else 0  # Progresso no eixo X
    position_reward = -1 if info["x"] <= previous_info["x"] else 0
    height_reward = 100 if info["y"] < previous_info["y"] else 0
    life_penalty = -1700 if info['lives'] < previous_info["lives"] else 0
    coin_reward = 50 if info["coins"] > previous_info["coins"] else 0
    score_reward = 75 if info["score"] > previous_info["score"] else 0
    
    total_reward = position_reward + life_penalty + coin_reward + score_reward + height_reward

    return total_reward

# Treinamento dos modelos
def training_model(env, num_episodes=1000, num_individuals=3, decision_interval=45):
    actions = [130, 128, 131, 386]  # Conjunto de ações possíveis
    num_actions = len(actions)
    input_shape = 11  # Aumente o número de entradas para incluir variáveis
    individuals = [build_model(input_shape=input_shape, num_actions=num_actions) for _ in range(num_individuals)]

    for episode in range(1, num_episodes + 1):
        scores = []  # Armazena pontuações dos indivíduos
        max_positions = []  # Armazena a maior posição X de cada indivíduo
        
        for individual in individuals:
            obs = env.reset()
            total_reward = 0
            done = False
            step_count = 0  # Contador para o intervalo de decisões
            previous_info = {'coins': 0, 'lives': 4, 'score': 0, 'x': 16, 'y': 352}
            current_action_bin = dec2bin(random.choice(actions), num_bits=9)  # Ação inicial
            max_x = previous_info['x']  # Rastreamento do maior progresso no eixo X

            # Variáveis para rastrear inatividade
            last_position_x = previous_info['x']
            inactivity_steps = 0  # Contador para rastrear os passos inativos
            inactivity_threshold = decision_interval * 3 + 10  # Limite de passos inativos

            while not done and rominfo.getLives(env) >= 5 and total_reward > -500:
                env.render()

                if step_count % decision_interval == 0:
                    # Obtenha o status de bloqueio e adicione ao estado
                    stuck_status = rominfo.getStuckStatus(env)
                    state_input = [
                        previous_info["x"],  # Posição X
                        previous_info["y"],
                        previous_info["coins"],
                        previous_info["score"],
                        previous_info["lives"],
                        stuck_status["up"],
                        stuck_status["down"],
                        stuck_status["left"],
                        stuck_status["right"],
                        stuck_status["middle"],
                        stuck_status["screen_side"],
                    ]
                    
                    # Use o modelo para escolher a próxima ação
                    action_idx = np.argmax(individual.predict(np.array([state_input])))
                    current_action_bin = dec2bin(actions[action_idx], num_bits=9)

                # Executa a ação atual
                obs, reward, done, info = env.step(current_action_bin)
                mario_pos = rominfo.getXY(rominfo.getRam(env))
                info["x"] = mario_pos[0]
                info["y"] = mario_pos[1]

                # Atualiza a maior posição X alcançada
                if info["x"] > max_x:
                    max_x = info["x"]

                # Verifique a inatividade no eixo X
                if info["x"] == last_position_x:
                    inactivity_steps += 1
                else:
                    inactivity_steps = 0  # Reset do contador se houver progresso

                # Penalize e encerre o episódio se o limite de inatividade for atingido
                if inactivity_steps >= inactivity_threshold:
                    total_reward -= 4000
                    done = True
                    print(f"\nInatividade detectada no episódio {episode}. Penalizando -4000.")

                last_position_x = info["x"]  # Atualiza a última posição X

                # Calcule a recompensa customizada
                my_reward = custom_reward(reward, info, previous_info)
                total_reward += my_reward

                # Atualize previous_info
                previous_info = info
                step_count += 1  # Incrementa o contador

                update_console(episode, num_episodes, generation=episode, score=total_reward)

                # Checa se finalizou e salva o modelo
                if rominfo.getCleared(env):
                  # Salve o modelo
                  save_path = f"model_cleared_episode_{episode}.h5"
                  individual.save(save_path)
                  print(f"Modelo salvo em {save_path} (Episódio: {episode})")
                  break  # Para salvar apenas o primeiro modelo que atender a condição

            scores.append(total_reward)
            max_positions.append(max_x)

        # Aplicar a grande recompensa ao indivíduo que foi mais longe no eixo X
        best_position_idx = np.argmax(max_positions)
        scores[best_position_idx] += 5000

        # Seleção dos melhores indivíduos e geração de descendentes
        best_individuals_idx = np.argsort(scores)[-3:]
        best_individuals = [individuals[idx] for idx in best_individuals_idx]
        offspring = generate_offspring(best_individuals, input_shape=input_shape)
        individuals = offspring  # Atualiza população

        print(f'\nEpisódio {episode}/{num_episodes} | Pontuações: {scores} | Melhor progresso no eixo X: {max_positions}')




# Inicialização do ambiente e treinamento do modelo
env = createEnv()
training_model(env, num_episodes=1000, num_individuals=3)
