import sys
import retro
import numpy as np
import tensorflow as tf
import rominfo

# Função para converter número decimal para binário (utilizado para ações no ambiente)
def dec2bin(dec, num_bits):
    binN = [0] * num_bits
    idx = 0
    while dec != 0:
        binN[idx] = dec % 2
        dec //= 2
        idx += 1
    return binN

# Função para criar o ambiente de jogo
def createEnv():
    return retro.make(game='SuperMarioWorld-Snes', state='YoshiIsland2', record=False)

# Atualizar o console com informações do progresso
def update_console(step, total_reward, done):
    sys.stdout.write(
        f"\rPasso: {step} | Pontuação Total: {total_reward:.2f} | Concluído: {'Sim' if done else 'Não'}"
    )
    sys.stdout.flush()

# Função principal para executar o modelo salvo
def run_model(model_path, num_episodes=1, decision_interval=45):
    # Carregar o modelo salvo
    model = tf.keras.models.load_model(model_path)
    print(f"Modelo {model_path} carregado com sucesso!")

    # Criar o ambiente
    env = createEnv()
    actions = [130, 128, 131, 386]  # Conjunto de ações possíveis
    num_bits = 9  # Número de bits para representar ações

    for episode in range(1, num_episodes + 1):
        obs = env.reset()
        done = False
        step = 0
        total_reward = 0
        previous_info = {'coins': 0, 'lives': 4, 'score': 0, 'x': 16, 'y': 352}
        current_action_bin = dec2bin(actions[0], num_bits)  # Ação inicial

        print(f"\nIniciando o Episódio {episode}")

        while not done:
            env.render()
            step += 1

            # Apenas decide a cada `decision_interval` passos
            if step % decision_interval == 0:
                # Obter informações do ambiente
                stuck_status = rominfo.getStuckStatus(env)
                mario_pos = rominfo.getXY(rominfo.getRam(env))

                state_input = [
                    mario_pos[0],  # Posição X
                    mario_pos[1],  # Posição Y
                    previous_info["coins"],  # Moedas
                    previous_info["score"],  # Pontuação
                    previous_info["lives"],  # Vidas restantes
                    stuck_status["up"],
                    stuck_status["down"],
                    stuck_status["left"],
                    stuck_status["right"],
                    stuck_status["middle"],
                    stuck_status["screen_side"],
                ]

                # Prever a próxima ação
                action_idx = np.argmax(model.predict(np.array([state_input])))
                current_action_bin = dec2bin(actions[action_idx], num_bits)

            # Executar a ação no ambiente
            obs, reward, done, info = env.step(current_action_bin)

            # Atualizar informações do ambiente
            mario_pos = rominfo.getXY(rominfo.getRam(env))
            info["x"] = mario_pos[0]
            info["y"] = mario_pos[1]

            # Acumular a recompensa
            total_reward += reward
            previous_info = info

            # Atualizar o console
            update_console(step, total_reward, done)

            # Verificar condição de conclusão
            if rominfo.getCleared(env):
                print("\nNível concluído com sucesso!")
                break

        print(f"\nEpisódio {episode} finalizado com pontuação total: {total_reward:.2f}")

    env.close()

# Nome do arquivo do modelo salvo
model_file = "model_cleared_episode_1.h5"  # Atualize com o nome correto do arquivo salvo

# Executar o modelo
run_model(model_path=model_file, num_episodes=3)
