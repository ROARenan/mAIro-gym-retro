# mAIro-gym-retro

## Introdução

**mAIro-gym-retro** é um projeto que utiliza aprendizado por reforço profundo para treinar uma IA a jogar _Super Mario World_ (SMW). O jogo é controlado através do framework **Gym-Retro**, que facilita a integração com emuladores de jogos retrô.

-   Baseado no projeto [MarioAStar](https://folivetti.github.io/courses/IA/Pratica/Mario/MarioAStar.zip) para leitura de inputs e dados da ROM do SMW.
-   Inspirado pelo artigo [Using Deep Reinforcement Learning To Play Atari Space Invaders](https://chloeewang.medium.com/using-deep-reinforcement-learning-to-play-atari-space-invaders-8d5159aa69ed).


## Requisitos

-   **Python 3.8**
-   Configuração de ambiente virtual com **Python 3.8**
-   Instalações de dependências:
    ```bash
    pip install gym==0.21.0
    pip install gym-retro
    ```


## Resumo de Instalação do Python 3.8

1. Faça o download do tarball do Python [aqui](https://www.python.org/downloads/release/python-3820/).
2. Extraia o arquivo para uma pasta.
3. Navegue até a pasta e instale dependências:
    ```bash
    sudo apt-get install -y build-essential
    ```
4. Configure e compile o código-fonte:
    ```bash
    ./configure --enable-optimizations
    make -j$(nproc)
    ```
5. Finalize a instalação:
    ```bash
    sudo make altinstall
    python3.8 --version
    ```

## Implementação

O projeto utiliza uma abordagem de **Aprendizado por Reforço Profundo** para treinar uma IA que controla o Mario no _Super Mario World_.

### Estrutura do Treinamento

1. **Ambiente**:
   O ambiente de simulação é configurado usando **gym-retro** para carregar o jogo _Super Mario World_. Um conjunto reduzido de ações possíveis é definido para simplificar o controle do personagem Mario.

2. **Modelo de IA**:
   A IA é baseada em uma rede neural construída com **Keras** e composta por:

    - Camadas densas (fully connected) com funções de ativação _ReLU_.
    - Saída linear para prever os _Q-values_ das ações disponíveis.
    - Otimização feita com o otimizador **Adam**.

3. **Recompensas Personalizadas**:
   O sistema de recompensa foi configurado para priorizar ações que maximizam:

    - Progresso horizontal no nível (posição `x`).
    - Coleta de moedas.
    - Aumento de pontuação.
    - Conservação de vidas.
      Penalidades são aplicadas para inatividade ou queda em buracos.

4. **Algoritmo Genético**:
   O treinamento utiliza uma abordagem evolutiva, onde:

    - Uma população inicial de redes neurais (indivíduos) é criada.
    - Os melhores indivíduos de cada geração (com base em pontuações) são cruzados e mutados para gerar descendentes.
    - A mutação adiciona variações aleatórias nos pesos das redes.

5. **Ciclo de Treinamento**:

    - Cada episódio treina um conjunto de indivíduos.
    - Os indivíduos executam ações no jogo com base em previsões da rede neural.
    - O desempenho de cada indivíduo é avaliado pelo total de recompensas acumuladas.
    - Redes com desempenho insuficiente são descartadas.

6. **Decisões da IA**:
    - O estado atual do jogo é convertido em uma entrada numérica para a rede neural.
    - A IA seleciona a ação com o maior valor predito (baseado em _Q-values_).
    - Ações são aplicadas no ambiente a cada intervalo de decisão.

### Resultados Esperados

O objetivo da IA é completar níveis do jogo, aprendendo de forma autônoma estratégias eficazes para superar obstáculos, coletar moedas e alcançar a bandeira final.

## Como Usar

1. Clone o repositório e configure o ambiente virtual:

    ```bash
    cd mAIro-gym-retro
    python3.8 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    ```

2. Certifique-se de ter a ROM de _Super Mario World_ configurada para **gym-retro**.

3. Inicie o treinamento:

    ```bash
    python play.py
    ```

4. Os modelos treinados serão salvos automaticamente ao atingir os critérios de desempenho.

## Como Treinar

É possível melhorar o desempenho do agente utilizando mais tempo de treinamento e melhores recompensas e inputs para a rede. Caso queira, realize as alterações e pode treiná-lo com:

   ```bash
   train.py
   ```

## Integrantes

- Arthur Norio Morita Osakawa _11202130323_
- Gabriel Rameh de Souza _11202021256_
- Karen Miky Sasai _11202130465_
- Marcelo Goulart Salinas Vega _11201921598_
- Matheus Marques _11201920383_
- Renan Santana Ferreira _11202131332_

---
# mAIro-gym-retro

## Introdução

**mAIro-gym-retro** é um projeto que utiliza aprendizado por reforço profundo para treinar uma IA a jogar _Super Mario World_ (SMW). O jogo é controlado através do framework **Gym-Retro**, que facilita a integração com emuladores de jogos retrô.

-   Baseado no projeto [MarioAStar](https://folivetti.github.io/courses/IA/Pratica/Mario/MarioAStar.zip) para leitura de inputs e dados da ROM do SMW.
-   Inspirado pelo artigo [Using Deep Reinforcement Learning To Play Atari Space Invaders](https://chloeewang.medium.com/using-deep-reinforcement-learning-to-play-atari-space-invaders-8d5159aa69ed).


## Requisitos

-   **Python 3.8**
-   Configuração de ambiente virtual com **Python 3.8**
-   Instalações de dependências:
    ```bash
    pip install gym==0.21.0
    pip install gym-retro
    ```


## Resumo de Instalação do Python 3.8

1. Faça o download do tarball do Python [aqui](https://www.python.org/downloads/release/python-3820/).
2. Extraia o arquivo para uma pasta.
3. Navegue até a pasta e instale dependências:
    ```bash
    sudo apt-get install -y build-essential
    ```
4. Configure e compile o código-fonte:
    ```bash
    ./configure --enable-optimizations
    make -j$(nproc)
    ```
5. Finalize a instalação:
    ```bash
    sudo make altinstall
    python3.8 --version
    ```

## Implementação

O projeto utiliza uma abordagem de **Aprendizado por Reforço Profundo** para treinar uma IA que controla o Mario no _Super Mario World_.

### Estrutura do Treinamento

1. **Ambiente**:
   O ambiente de simulação é configurado usando **gym-retro** para carregar o jogo _Super Mario World_. Um conjunto reduzido de ações possíveis é definido para simplificar o controle do personagem Mario.

2. **Modelo de IA**:
   A IA é baseada em uma rede neural construída com **Keras** e composta por:

    - Camadas densas (fully connected) com funções de ativação _ReLU_.
    - Saída linear para prever os _Q-values_ das ações disponíveis.
    - Otimização feita com o otimizador **Adam**.

3. **Recompensas Personalizadas**:
   O sistema de recompensa foi configurado para priorizar ações que maximizam:

    - Progresso horizontal no nível (posição `x`).
    - Coleta de moedas.
    - Aumento de pontuação.
    - Conservação de vidas.
      Penalidades são aplicadas para inatividade ou queda em buracos.

4. **Algoritmo Genético**:
   O treinamento utiliza uma abordagem evolutiva, onde:

    - Uma população inicial de redes neurais (indivíduos) é criada.
    - Os melhores indivíduos de cada geração (com base em pontuações) são cruzados e mutados para gerar descendentes.
    - A mutação adiciona variações aleatórias nos pesos das redes.

5. **Ciclo de Treinamento**:

    - Cada episódio treina um conjunto de indivíduos.
    - Os indivíduos executam ações no jogo com base em previsões da rede neural.
    - O desempenho de cada indivíduo é avaliado pelo total de recompensas acumuladas.
    - Redes com desempenho insuficiente são descartadas.

6. **Decisões da IA**:
    - O estado atual do jogo é convertido em uma entrada numérica para a rede neural.
    - A IA seleciona a ação com o maior valor predito (baseado em _Q-values_).
    - Ações são aplicadas no ambiente a cada intervalo de decisão.

### Resultados Esperados

O objetivo da IA é completar níveis do jogo, aprendendo de forma autônoma estratégias eficazes para superar obstáculos, coletar moedas e alcançar a bandeira final.

## Como Usar

1. Clone o repositório e configure o ambiente virtual:

    ```bash
    cd mAIro-gym-retro
    python3.8 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    ```

2. Certifique-se de ter a ROM de _Super Mario World_ configurada para **gym-retro**.

3. Inicie o treinamento:

    ```bash
    python play.py
    ```

4. Os modelos treinados serão salvos automaticamente ao atingir os critérios de desempenho.

## Como Treinar

É possível melhorar o desempenho do agente utilizando mais tempo de treinamento e melhores recompensas e inputs para a rede. Caso queira, realize as alterações e pode treiná-lo com:

   ```bash
   train.py
   ```

## Integrantes

- Arthur Norio Morita Osakawa _11202130323_
- Gabriel Rameh de Souza _11202021256_
- Karen Miky Sasai _11202130465_
- Marcelo Goulart Salinas Vega _11201921598_
- Matheus Marques _11201920383_
- Renan Santana Ferreira _11202131332_

---
