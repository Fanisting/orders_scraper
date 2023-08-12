# README

## Installation

Git clone this project by running in terminal:

```
git clone https://github.com/Fanisting/orders-scraper.git
```

Set up a virtual env with `python venv`. Run this in terminal:

```
python -m venv env
```

It creates the `venv` with name = env. Please **activate the env in terminal**. 

Now install pre-requisites listed in `requirements.txt`.

```
pip install requirements.txt
```

Here we should set up more in playwright, run this in terminal:

```
playwright install
```

## Make your own app with Pyinstaller

After activate `venv` in terminal, run command to compile the app/exe in terminal.

### Windows

```powershell
# powershell
$env:PLAYWRIGHT_BROWSERS_PATH="0" 
playwright install chromium
pyinstaller -n choose -F --windowed choose.py
```

### Mac OS

```bash
PLAYWRIGHT_BROWSERS_PATH=0 playwright install chromium
pyinstaller -n choose -F --windowed choose.py
```

You will find the compiled app in `dist/` folder, try to run it. 

