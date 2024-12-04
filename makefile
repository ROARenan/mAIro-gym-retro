setup:
	conda create --name mairo python=3.8.0
	conda activate mairo
	pip install setuptools==65.5.0 wheel==0.38.4
	pip install pip==19.3.1
	pip install -r requirements.txt

test:
	python test.py

random:
	python -m retro.examples.random_agent --game SuperMarioWorld-Snes

brute:
	python -m retro.examples.brute --game SuperMarioWorld-Snes

replay:
	python replay.py

run:
	python run.py
