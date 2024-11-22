# mAIro-gym-retro
mAIro-gym-retro

[MarioAStar Base](https://folivetti.github.io/courses/IA/Pratica/Mario/MarioAStar.zip) projeto base do para ler os inputs e dados da ROM do SMW

## Requirements
- Python 3.8
- Configurar Venv com o Python 3.8
- pip install gym==0.21.0
- pip install gym-retro

## Install Python 3.8
1. Download Tarball from [Python.org](https://www.python.org/downloads/release/python-3820/)
2. Unzip to folder
3. On the folder run ```sudo apt-get install -y build-essential```
4. Run ```./configure --enable-optimizations``` to build
5. Run ```make -j$(nproc)```, now compilling the source
6. Run ```sudo make install```, to fish installation
7. Check the version ```python3.8 --version```

```bash
wget https://www.python.org/ftp/python/3.8.20/Python-3.8.20.tgz
sudo apt-get install -y build-essential
./configure --enable-optimizations
make -j$(nproc)
sudo make install
python3.8 --version
```

## Config Env
```bash
python3.8 -m venv marioenv #Create env named marioenv
source marioenv/bin/activate #Activate marioenv
python --version #To check if Python is 3.8
```

### REQUIREMENTS
We will need some libs
- ```pip install gym==0.21.0```
- ```pip install gym-retro``` 