# mAIro-gym-retro
mAIro-gym-retro

[MarioAStar Base](https://folivetti.github.io/courses/IA/Pratica/Mario/MarioAStar.zip) projeto base do para ler os inputs e dados da ROM do SMW
[Using Deep Reinforcement Learning To Play Atari Space Invaders](https://chloeewang.medium.com/using-deep-reinforcement-learning-to-play-atari-space-invaders-8d5159aa69ed)


## Requirements
- Python 3.8
- Config Venv with Python 3.8
- pip install gym==0.21.0
- pip install gym-retro

## Summary
1. Download Tarball from [Python.org](https://www.python.org/downloads/release/python-3820/)
2. Unzip to folder
3. On the folder run ```sudo apt-get install -y build-essential```
4. Run ```./configure --enable-optimizations``` to build
5. Run ```make -j$(nproc)```, now compilling the source
6. Run ```sudo make altinstall```, to fish installation
7. Check the version ```python3.8 --version```

### Terminal
```bash
sudo apt update
sudo apt install build-essential zlib1g-dev libncurses5-dev libgdbm-dev libnss3-dev libssl-dev libreadline-dev libffi-dev
```

```bash
wget https://www.python.org/ftp/python/3.8.20/Python-3.8.20.tgz
sudo apt-get install -y build-essential
./configure --enable-optimizations
make -j$(nproc)
sudo make altinstall
python3.8 --version
```
---

## Install Python 3.8

When installing Python 3.8 from source on Linux, you may want to **altinstall** it rather than simply installing it. This ensures that Python 3.8 is installed without overwriting the default `python` or `python3` versions on your system, which could break system dependencies.

To **altinstall** Python 3.8, follow these steps:

### 1. **Download Python 3.8 Source Code**
   First, you need to download the Python 3.8 source code. You can do this from the official Python website or by using `wget`:

   ```bash
   cd /tmp
   wget https://www.python.org/ftp/python/3.8.20/Python-3.8.20.tgz
   ```

   (Replace `3.8.10` with the desired version if necessary.)

### 2. **Extract the Tarball**

   After downloading the Python tarball, extract it:

   ```bash
   tar -xvzf Python-3.8.10.tgz
   ```

### 3. **Install Dependencies**

   Before you can compile Python from source, make sure you have the necessary build dependencies installed. On a Debian-based system (like Ubuntu), you can install them with:

   ```bash
   sudo apt update
   sudo apt install build-essential zlib1g-dev libncurses5-dev libgdbm-dev libnss3-dev libssl-dev libreadline-dev libffi-dev
   ```

   These are common dependencies for building Python. Some systems may require additional dependencies depending on the configuration.

### 4. **Configure the Build**

   Navigate to the extracted Python source directory:

   ```bash
   cd Python-3.8.20
   ```

   Run the `./configure` script. You can use the `--prefix` option to specify the installation directory if you don't want to use the default `/usr/local/` path. But for `altinstall`, you won't need to change the prefix unless you have a custom location.

   Run:

   ```bash
   ./configure --enable-optimizations
   ```

   The `--enable-optimizations` flag is optional, but it speeds up Python's runtime performance by optimizing the build.

### 5. **Altinstall Python 3.8**

   Now, you can install Python 3.8 using `altinstall` to avoid overwriting the system’s default `python` or `python3` binary:

   ```bash
   sudo make altinstall
   ```

   This will install Python 3.8 as `python3.8` without replacing the default system `python3`.

### 6. **Verify the Installation**

   After the installation is complete, verify that Python 3.8 is installed correctly:

   ```bash
   python3.8 --version
   ```

   This should output something like `Python 3.8.20`.

### 7. **Install `pip` for Python 3.8**

   Python 3.8 should come with `ensurepip`, which can install `pip` if it's missing. To install `pip` for Python 3.8, you can use the following command:

   ```bash
   python3.8 -m ensurepip --upgrade
   ```

   This ensures that `pip` is available for your new Python installation.

   Afterward, you can verify `pip` for Python 3.8:

   ```bash
   python3.8 -m pip --version
   ```

### 8. **Optional: Set Up Virtual Environments**

   You can also set up a virtual environment using Python 3.8. First, install `venv` (if it's not already installed):

   ```bash
   python3.8 -m pip install --upgrade pip
   ```

   Then, create a virtual environment:

   ```bash
   python3.8 -m venv myenv
   ```

   This will create a `myenv` virtual environment using Python 3.8.

---

## Config Env
```bash
python3.8 -m venv marioenv #Create env named marioenv
source marioenv/bin/activate #Activate marioenv
python --version #To check if Python is 3.8
```

### Libs
We will need some libs
- ```pip install --upgrade pip``` Before running other pip commands
- ```pip install gym==0.21.0```
- ```pip install gym-retro``` 
- ```pip install tensorflow``` 

---

## Uninstall Pyton 3.8
If you've installed Python 3.8 from source, uninstalling it is a bit more involved than with packages installed via a package manager (like `apt` on Ubuntu). Python doesn't include an automatic uninstall command when you install from source, so you'll need to manually remove the files associated with the installation.

Here’s how you can uninstall Python 3.8 that was built from source:

### 1. **Locate the Installation Directory**
   When you built Python from source, you likely specified a directory where it was installed (or it used the default). The default location is usually `/usr/local/`, but it could also be another directory if you specified it during the `./configure` step.

   If you don't remember where Python was installed, you can try running the following to check where the Python 3.8 binary is located:
   
   ```bash
   which python3.8
   ```

   This should give you the full path to the Python binary, for example: `/usr/local/bin/python3.8`.

   You can also check the prefix you used when building:

   ```bash
   cd /path/to/python/source/
   make install
   ```

   If you didn’t specify a custom directory during the build, it should have installed to `/usr/local/`.

### 2. **Remove Python Files**

   If Python was installed with the default `prefix` of `/usr/local/`, you'll need to remove Python 3.8 files from the following locations:

   - **Binaries:**

     ```bash
     sudo rm -rf /usr/local/bin/python3.8
     sudo rm -rf /usr/local/bin/python3.8-config
     sudo rm -rf /usr/local/bin/pip3.8
     ```

   - **Libraries:**

     ```bash
     sudo rm -rf /usr/local/lib/python3.8
     ```

   - **Include Files:**

     ```bash
     sudo rm -rf /usr/local/include/python3.8
     ```

   - **Man Pages:**

     ```bash
     sudo rm -rf /usr/local/share/man/man1/python3.8.1
     ```

   - **Site Packages:**

     If you used `pip` to install packages into this Python installation, you may also want to remove the site packages:
   
     ```bash
     sudo rm -rf /usr/local/lib/python3.8/site-packages
     ```

### 3. **Remove Configuration Files (Optional)**
   
   If you configured the build with a custom prefix or installation location, you'll need to remove files from that location. For example, check the configuration directory (typically `/usr/local/lib` or a similar directory):

   ```bash
   sudo rm -rf /usr/local/lib/python3.8
   ```

### 4. **Check for Leftover Files**
   
   After removing the main files, it’s a good idea to search for any remaining Python 3.8 files on your system that might have been installed outside the standard directories:

   ```bash
   sudo find / -name "python3.8*" -exec rm -rf {} \;
   ```

   This command will search your entire filesystem for files or directories related to Python 3.8 and remove them.

### 5. **Remove the Build Files (Optional)**

   If you still have the source directory where you built Python, you can remove it as well:

   ```bash
   rm -rf /path/to/python-source-directory
   ```

### 6. **Verify the Uninstallation**
   
   After removing the files, check if Python 3.8 has been successfully removed:

   ```bash
   python3.8 --version
   ```

   If the command returns an error saying that `python3.8` is not found, it means the uninstallation was successful.

---