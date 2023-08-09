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

## Pyinstaller

After activate venv in terminal, run this in terminal:
```
$env:PLAYWRIGHT_BROWSERS_PATH="0" 
playwright install chromium
pyinstaller --specpath ./. -n choose -F choose_gui.py
```

Then you will find a `choose.spec` file, now open it and find the line:
```c
hiddenimports=[],
```

We should add the text to the list, make sure it looks like:
```c
hiddenimports=["babel.numbers"],
```

Store and close the `choose.spec` file.  Now run this in terminal:

```
pyinstaller choose.spec
```

## Test it

You will find the compiled app in `dist/` folder, try to run it. 

