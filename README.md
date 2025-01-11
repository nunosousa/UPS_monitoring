# TelescopeMirrorTester
This is an application intended to provide useful tools to perform Foucault or Wire testing on reflective telescope mirrors

## Notes on setting up the Python virtual environment

### Creating a virtual environment
To create a virtual environment, run venv.
```
python3 -m venv .venv
```

### Activating a virtual environment
```
source .venv/bin/activate
```

### Ensure pip, setuptools, and wheel are up to date
```
python3 -m pip install --upgrade pip setuptools wheel
```

### Installing packages using requirements file
```
python3 -m pip install -r requirements.txt
```

### Starting JupyterLab
Start JupyterLab using:
```
jupyter lab
```

### Leaving the virtual environment
If you want to switch projects or otherwise leave your virtual environment, simply run:
```
deactivate
```
### Update project dependencies
If new dependencies where installed, run:
```
python3 -m pip freeze > requirements.txt
```

Check all installed packages with:
```
python3 -m pip list
```
