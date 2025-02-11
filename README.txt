1. Координаты и градусы - целочисленные.
2. Диапазон координат - от -5 до 5.
3. Запуск: python3.9 xiaomi_test.py
4. 4 и 5 действия сохраняют результат в папку result.
5. Реализовано на основе задачки из pdf. 

OS Linux:
	sudo apt update
	sudo apt install software-properties-common
	sudo add-apt-repository ppa:deadsnakes/ppa
	sudo apt install python3.9
	
OS Windows:
	https://bangbangeducation.ru/point/razrabotka/kak-ustanovit-python/
	
OS MacOS:
	$ /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
	$ brew install python[version]
```

#### Установка окружения (python v.3.9):
```commandline

C помощью vrtualenv:
	pip3.9 install virtualenv
	python3.9 -m virtualenv .venv
	source .venv/bin/activate
	pip3.9 install -r ./requirements.txt
	
C помощью venv:
	sudo apt install python3-venv
	python3.9 -m venv kitty
	source kitty/bin/activate
	pip3.9 install -r ./requirements.txt
	
С помощью conda:
	wget https://repo.anaconda.com/archive/Anaconda3-2024.02-1-Linux-x86_64.sh
	bash Anaconda3-2024.02-1-Linux-x86_64.sh
	source ~/.bashrc
	rm Anaconda3-2024.02-1-Linux-x86_64.sh 
	conda env create -n kitty -f environment.yml  
	conda activate kitty
```
