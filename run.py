import retro
import random

import rominfo
from utils import dec2bin
class Mario_AI():
    episodes = 400
    individuals = 2
    decision_interval = 45
    input_shape = 42
    max_steps = 5000
    actions_map = {'noop':0, 'down':32, 'up':16, 'jump':1, 'spin':3,
                    'left':64, 'jumpleft':65, 'runleft':66, 'runjumpleft':67,
                    'right':128, 'jumpright':129, 'runright':130, 'runjumpright':131,
                    'spin':256, 'spinright':384, 'runspinright':386, 'spinleft':320, 'spinrunleft':322
                    }

    def __init__(self, *args, **kwargs):
        self.env = self._createEnv()
        self.actions = self._getActions()

    def _createEnv(self):
        return retro.make(game='SuperMarioWorld-Snes', state='YoshiIsland2', record=False)

    def _getActions(self):
        # returns a subset of actions_map
        actions = [
            self.actions_map["runleft"],
            self.actions_map["runright"],
            self.actions_map["right"],
            self.actions_map["runjumpright"],
            self.actions_map["runspinright"],
        ]
        return actions


    def train(self, *args, **kwargs):
        episodes = kwargs.get("episodes", self.episodes)
        individuals = kwargs.get("individuals", self.individuals)
        decision_interval = kwargs.get("decision_interval", self.decision_interval)

        model_list = [self.build_model(input_shape=self.input_shape, num_actions=len(self.actions)) for _ in range(individuals)]

        for model in model_list:
            # Setting initial state
            self.env.reset()
            total_reward = 0
            done = False
            step_count = 0  # Contador para o intervalo de decisões
            previous_info = {'coins': 0, 'lives': 4, 'score': 0, 'x': 16}
            current_action_bin = dec2bin(random.choice(self.actions))  # Ação inicial

            while not done:
                if rominfo.getLives(self.env) < 5:
                    break
                if total_reward < -500:
                    break
                if step_count > max_steps:
                    break

                if step_count % 10 == 0:
                    self.env.render()

                state_input = self.get_input(previous_info)
                predictions = model.predict(np.array([state_input]))

                action_to_take = np.argmax(predictions)
                current_action_bin = dec2bin(actions[action_to_take])
                next_state, reward, done, info = self.env.step(current_action_bin)

    def get_input(self, previous_info):
        sprites = self.get_Sprites(self.env)
        stuck = rominfo.getStuckStatus(self.env)
        state_input = [
                    *previous_info,
                    *stuck,
                    *sprites,
                ]
        return state_input

    def get_sprites():
        sprites = rominfo.getSprites(rominfo.getRam(self.env))

        if len(sprites) > 12:
            sprites = sprites[:12]

        while len(sprites) < 12:
            empty_element = {
                "id": 0,
                "x": 0,
                "y": 0,
                "size": 0
            }
            sprites.append(empty_element)

        return sprites



    def build_model(self, input_shape, num_actions):
        # Construção do modelo de rede neural
        model = Sequential()
        model.add(Dense(128, input_dim=input_shape, activation='relu'))  # Camada oculta
        model.add(Dense(64, activation='relu'))  # Camada oculta adicional
        model.add(Dense(num_actions, activation='linear'))  # Saída com Q-values
        model.compile(loss='mean_squared_error', optimizer=Adam())  # Otimizador Adam
        return model




model = Mario_AI()
model.train()
