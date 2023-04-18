# DJANGO REST BOOTSTRAP

### This project is for faster initialize app.

## 1. Prerequisites
- [Pyenv](https://github.com/pyenv/pyenv): python version management.

## 2. How to use
- Check if targeted python describe in [.python-version](.python-version) has been installed by using `python -V` or `which python`. If not, run `pyenv install`.
- Create virtual env:
```bash
    python -m venv .venv
```
- Sourcing the .venv:
```bash
    source .venv/bin/activate
```
- Install initial dependencies.
```bash
    pip install -r requirements-init.txt
```
- Bootstrap the code, input the target app name you want:
```bash
    python bootstrap.py
```
- The above command will rename app and remove util files, reset git and create other README file for you.
- After that, please continue with the project README.md (which previously name README.TEMPLATE.md)