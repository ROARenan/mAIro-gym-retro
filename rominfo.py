import numpy as np
from itertools import product


'''
Extração de atributos da memória RAM do jogo Super Mario World
Informações retiradas de: https://www.smwcentral.net/?p=nmap&m=smwram
'''
def getXY(ram):
    '''
    getXY(ram): retorna informação da posição do agente
    embora layer1? não seja utilizada no momento, pode ser útil em algumas 
    alterações do algoritmo de aprendizado.
    '''
    
    # Coordenadas x, y em relação a fase inteira 
    # Elas estão armazenadas em 2 bytes cada
    # no formato little endian
    marioX = ram[0x95]*256 + ram[0x94]
    marioY = ram[0x97]*256 + ram[0x96]
    
    # Coordenada da parte visível do site
    layer1x = ram[0x1B]*256 + ram[0x1A]
    layer1y = ram[0x1D]*256 + ram[0x1C]
    
    return (marioX.astype(np.int16), marioY.astype(np.int16), layer1x.astype(np.int16), layer1y.astype(np.int16))

def getSprites(ram):
  '''
  getSprites(ram): retorna os sprites (blocos, inimigos, itens) exibidos na tela.
  '''
  
  sprites = []
  extsprites = []
  
  # Podem existir até 12 sprites na tela
  for slot in range(12):
    # se o status é 0, não tem sprite nesse slot
    status = ram[0x14C8+slot]
    if status != 0:
      # posição x,y do sprite
      spriteX    = ram[0xE4+slot] + ram[0x14E0+slot]*256
      spriteY    = ram[0xD8+slot] + ram[0x14D4+slot]*256
      
      spriteSize = ram[0x0420+ram[0x15EA+slot]]  # tamanho do sprite
      spriteId   = ram[0x15EA+slot]              # qual é o sprite?
      
      # se for item (44) ou bloco ? (216), não insere nas informações
      if spriteId != 44 and spriteId != 216:
        # ou ele é 1x1 ou 4x4 blocos da nossa janela
        size = 1
        if spriteSize == 0:
          size = 4
        sprites.append({'id':spriteId,'x': spriteX, 'y': spriteY, 'size': size})
      
  return sprites
      
def getTile(dx,dy,ram):
  '''
  getTile(dx, dy, ram): retorna se tem um bloco que o mario possa pisar na posição dx, dy
  '''
  x = np.floor(dx/16)
  y = np.floor(dy/16)
  
  # 0x1C800 indica para cada pixel se é um obstáculo ou não
  # como obter o ponto certo foi retirado daqui: https://www.smwcentral.net/?p=viewthread&t=78887
  # return ram[0x1C800 + int(np.floor(x/16)*432 + y*16 + x%16)]

  # O endereço correto é 0x1F000, contribuição de Fernando Teixeira
  return ram[0x1F000 + int(np.floor(x/16)*432 + y*16 + x%16)]
  
def getInputs(ram, radius=6):
  '''
  getInputs(ram): retorna uma nd.array de inimigos, obstáculos dentro de um raio em torno do agente
  '''
  
  marioX, marioY, layer1x, layer1y = getXY(ram)
  sprites = getSprites(ram)

  # tamanho do vetor
  maxlen = (radius*2+1)*(radius*2+1)
  inputs = np.zeros(maxlen, dtype=int)
  
  # cada bloco de imagem representa 16x16 pixesl
  # portanto tendo um x,y de referência do Mario
  # devemos camihar de 16 em 16
  window = (-radius*16, radius*16 + 1, 16)
  j = 0

  def withinLimits(idx, ds1, ds2, r, maxlen):
    return (idx%(2*r + 1) + ds2 < 2*r + 1) and (idx + ds1*(2*r + 1) + ds2 < maxlen)
  
  for dy, dx in product(range(*window), repeat=2):
    # verifica se tem obstáculo na posição x+dx, y+dy
    # o +8 é para começar a medir a partir do meio do Mario
    tile = getTile(marioX+dx+8, marioY+dy, ram)
    
    # O Mario está sempre no meio, 
    # deve checar se o y está dentro do limite
    if tile==1 and marioY+dy < 0x1B0:
      inputs[j] = 1
    
    # Para cada sprite  
    for i in range(len(sprites)):
      # Se estiver dentro do bloco de 16 x 16 (-8, +8)
      distx = np.abs(sprites[i]['x'] - marioX - dx)
      disty = np.abs(sprites[i]['y'] - marioY - dy)
      size = sprites[i]['size']
      if distx <= 8 and disty <= 8:
        # se estiver dentro dos limites, insira -1
        for s1, s2 in product(range(size), repeat=2):
          if withinLimits(j, s1, s2, radius, maxlen):
            inputs[j + s1*(radius*2 + 1) + s2] = -1
    j = j + 1
  return inputs, marioX, marioY
  
# Recupera o estado atual como uma string
def getState(ram, radius):
  state, x, y = getInputs(ram, radius=radius)
  return ','.join(map(str,state)), x, y  
  
def getRam(env):
    return np.array(list(env.data.memory.blocks[8257536]))
    

def getLives(env):
    """
    Obtém o número de vidas do jogador no Super Mario World.
    O número de vidas está armazenado no endereço 0x7E0DBE.
    """
    lives_address = 0x0DBE  # Endereço de memória relativo para vidas no Super Mario World
    ram = env.get_ram()  # Obtém a memória RAM do jogo
    lives_minus_one = ram[lives_address]  # Lê o valor no endereço especificado
    return lives_minus_one + 1  # Ajusta para refletir o número correto de vidas

def getScore(env):
  """
  Obtem o score do jogador atual em 0x7E0F34.
  O valor eh salvo em HEX e precisa ser convertido

  return:
    score_dec: O score atual do jogador convertido para decimal
  """

  score_address = 0x0F34
  ram = env.get_ram()
  score_hex = ram[score_address]
  score_dec = int(str(score_hex), 16)

  return score_dec

# Retorna True se na animacao de vitoria no fim da fase
def getCleared(env):

  cc_address = 0x1493
  ram = env.get_ram()
  cc = ram[cc_address]

  return cc!=0

def getStuckStatus(env):
    """
    Verifica se Mario está em contato com uma parede ou bloqueado em qualquer direção.
    Utiliza o status de bloqueio armazenado no endereço 0x7E0077.
    
    Retorna:
        stuck_status (dict): Um dicionário com o status booleano de bloqueio em cada direção:
            - "up": Bloqueado acima.
            - "down": Bloqueado abaixo.
            - "left": Bloqueado à esquerda.
            - "right": Bloqueado à direita.
            - "middle": Mario está no meio de um bloco.
            - "screen_side": Mario está tocando a lateral da tela.
    """
    status_address = 0x0077  # Endereço na RAM para o status de bloqueio
    ram = env.get_ram()  # Obtém a memória RAM do jogo
    status = ram[status_address]  # Lê o valor no endereço especificado

    # Decodifica os bits do status
    stuck_status = {
        "up": bool(status & 0b00001000),         # Bloqueado acima (U)
        "down": bool(status & 0b00000100),       # Bloqueado abaixo (D)
        "left": bool(status & 0b00000010),       # Bloqueado à esquerda (L)
        "right": bool(status & 0b00000001),      # Bloqueado à direita (R)
        "middle": bool(status & 0b00100000),     # No meio de um bloco (M)
        "screen_side": bool(status & 0b10000000) # Tocando a lateral da tela (S)
    }

    return stuck_status

def getTimer(env):
    """
    Obtém o valor atual do timer do jogo.
    O timer está localizado em 0x7E0F31 (centenas), 0x7E0F32 (dezenas), e 0x7E0F33 (unidades).

    return:
        timer_value: O valor do timer como um número decimal.
    """
    # Endereços do timer
    hundreds_address = 0x0F31
    tens_address = 0x0F32
    ones_address = 0x0F33

    # Acessando a memória RAM do jogo
    ram = env.get_ram()

    # Obtendo os valores individuais
    hundreds = ram[hundreds_address]
    tens = ram[tens_address]
    ones = ram[ones_address]

    # Calculando o valor total do timer
    timer_value = (hundreds * 100) + (tens * 10) + ones

    return timer_value

# Retorna True se na animacao de vitoria no fim da fase
def getCleared(env):

  cc_address = 0x1493
  ram = env.get_ram()
  cc = ram[cc_address]

  return cc!=0

def getBonusStars(env):
    """
    Obtém a contagem de estrelas bonus vermelhas do Mario $7E0F48

    return:
        star_counter: contagem de estrelas bonus do Mario
    """
    star_adress = 0x0F48

    # Acessando a memória RAM do jogo
    ram = env.get_ram()

    star_counter = ram[star_adress]

    return star_counter