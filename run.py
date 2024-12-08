import sys
import retro
import random
import rominfo
import numpy as np
import itertools

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.optimizers import Adam

from utils import dec2bin



class Mario_AI():
    episodes = 20
    individuals = 8
    decision_interval = 20
    input_shape = 15
    max_steps = 5000
    max_sprites = 5
    inactivity_threshold = 40
    actions_map = {'noop':0, 'down':32, 'up':16, 'jump':1, 'spin':3,
                    'left':64, 'jumpleft':65, 'runleft':66, 'runjumpleft':67,
                    'right':128, 'jumpright':129, 'runright':130, 'runjumpright':131,
                    'spin':256, 'spinright':384, 'runspinright':386, 'spinleft':320, 'spinrunleft':322
                    }

    reward_weights = {
        "x_pos": 5,
        "jump": 200,
        "coin": 100,
        "score": 50,
        "lives": 4000,
    }

    def __init__(self, *args, **kwargs):
        self.env = self._createEnv()
        self.actions = self._getActions()
        self.input_shape += self.max_sprites *4

    def update_console(self, episode, model, score):
        sys.stdout.write(
            f"\rEpisódio {episode}/{self.episodes} | Individuo: {model} | Pontuação Atual: {score:.2f} | Pontuacao Maxima: {self.max_score:.2f}"
        )
        sys.stdout.flush()

    def _createEnv(self):
        return retro.make(game='SuperMarioWorld-Snes', state='YoshiIsland2', record=False)

    def _getActions(self):
        # returns a subset of actions_map
        actions = [
            self.actions_map["jump"],
            self.actions_map["runright"],
            self.actions_map["runjumpright"],
            # self.actions_map["runspinright"],
        ]
        return actions


    def train(self, *args, **kwargs):
        episodes = kwargs.get("episodes", self.episodes)
        individuals = kwargs.get("individuals", self.individuals)
        decision_interval = kwargs.get("decision_interval", self.decision_interval)

        model_list = [self.build_model() for _ in range(individuals)]
        for episode in range(1, self.episodes+1):
            generation = []
            model_n = 0
            self.max_score = 0
            for model in model_list:
                # Setting initial state
                self.env.reset()
                self.inactivity_steps = 0
                model_n += 1
                total_reward = 0
                done = False
                step_count = 0  # Contador para o intervalo de decisões
                previous_info = {'coins': 0, 'lives': 4, 'score': 0, 'x': 16, 'y': 0}
                current_action_bin = dec2bin(random.choice(self.actions))  # Ação inicial

                while not done:
                    step_count += 1
                    if rominfo.getLives(self.env) < 5:
                        print("\n Died!")
                        break
                    if total_reward < -400:
                        print("\n Bad Score!")
                        break
                    if step_count > self.max_steps:
                        print("\n Took too long!")
                        break
                    if self.inactivity_steps > self.inactivity_threshold * self.decision_interval:
                        self.inactivity_steps = 0
                        print("\n Inactive!")
                        break

                    if step_count % 20 == 0:
                        self.env.render()

                    if step_count % self.decision_interval == 0:
                        current_action_bin = self.decide(model, previous_info)

                    next_state, reward, done, info = self.env.step(current_action_bin)

                    total_reward += reward + self.custom_reward(info, previous_info)
                    if total_reward >= self.max_score:
                        self.max_score = total_reward
                    previous_info.update(info)

                    self.update_console(episode, model=model_n, score=total_reward)

                    # Verifique se a condição foi atendida
                    if rominfo.getCleared(self.env):
                        # Salve o modelo
                        save_path = f"model_cleared_episode_{episode}.h5"
                        individual.save(save_path)
                        print(f"Modelo salvo em {save_path} (Episódio: {episode})")
                        break  # Para salvar apenas o primeiro modelo que atender a condição

                generation.append({"model": model, "score": total_reward})

            model_list = self.generate_offspring(generation, individuals)

    def generate_offspring(self, generation, individuals):
        generation_sorted = sorted(generation, key=lambda x:x["score"], reverse=True)
        # Gets the best N-1 models from generation
        parents = generation_sorted[:3]
        # Adds a random model for mutability
        while len(parents) < individuals:
            parents.append(random.choice(parents))

        new_generation = []
        while len(new_generation) < individuals:
            parent = random.choice(parents)
            child = self.build_model()

            parent_weights = parent["model"].get_weights()
            mutated_weights = [w + np.random.randn(*w.shape) * 0.1 for w in parent_weights]
            child.set_weights(mutated_weights)

            new_generation.append(child)

        return new_generation

    def custom_reward(self, info, previous_info):
        reward = 0
        mario_pos = rominfo.getXY(rominfo.getRam(self.env))
        info["x"] = mario_pos[0]
        # Positional rewards

        mario_x = info["x"]
        old_x = previous_info["x"]

        delta_pos = (mario_x - old_x)
        if delta_pos == 0:
            self.inactivity_steps += 1
        else:
            self.inactivity_steps = 0

        reward += delta_pos * self.reward_weights["x_pos"]

        # Coins and score
        coin_reward = (info["coins"] - previous_info["coins"]) * self.reward_weights["coin"]
        reward += coin_reward

        score_reward = (info["score"] - previous_info["score"]) * self.reward_weights["score"]
        reward += score_reward

        return reward

    def decide(self, model, previous_info):
        state_input = self._build_input(previous_info)
        predictions = model.predict(np.array([state_input]))
        action_to_take = np.argmax(predictions)
        return dec2bin(self.actions[action_to_take])

    def _build_input(self, previous_info):
        inputs = self.get_input(previous_info)
        state_input = list(itertools.chain(*inputs))
        return state_input

    def get_input(self, previous_info):
        mario_pos = rominfo.getXY(rominfo.getRam(self.env))
        sprites = list(itertools.chain(*[list(sprite.values()) for sprite in self.get_sprites()])) # turns dict in to a list of lists and flattens it
        stuck = list(rominfo.getStuckStatus(self.env).values())
        previous = list(previous_info.values())

        inputs = [mario_pos, sprites, stuck, previous]
        return inputs

    def get_sprites(self):
        sprites = rominfo.getSprites(rominfo.getRam(self.env))

        if len(sprites) > self.max_sprites:
            sprites = sprites[:self.max_sprites]

        while len(sprites) < self.max_sprites:
            empty_element = {
                "id": 0,
                "x": 0,
                "y": 0,
                "size": 0
            }
            sprites.append(empty_element)

        return sprites



    def build_model(self):
        input_shape= self.input_shape
        num_actions= len(self.actions)
        # Construção do modelo de rede neural
        model = Sequential()
        model.add(Dense(128, input_dim=input_shape, activation='relu'))  # Camada oculta
        model.add(Dense(64, activation='relu'))  # Camada oculta adicional
        model.add(Dense(64, activation='relu'))  # Camada oculta adicional
        model.add(Dense(num_actions, activation='linear'))  # Saída com Q-values
        model.compile(loss='mean_squared_error', optimizer=Adam())  # Otimizador Adam
        return model




model = Mario_AI()
model.train()
