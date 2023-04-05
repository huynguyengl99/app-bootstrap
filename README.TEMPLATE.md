# MYAPP

## Introduction

This is MYAPP

## Stack & Dependencies

- [Django](https://www.djangoproject.com/) - Batteries-included Python web framework.
- [PostgreSQL](https://www.postgresql.org/) - Well-know open source database system.

## Development

### Setup dev environment
- [Pyenv](https://github.com/pyenv/pyenv): python version management.
- [Docker](https://www.docker.com/products/docker-desktop/): docker app for launching services like db, redis, e.t.c.

### Getting Started
- Start docker `docker-compose up --detach`
- Installing Packages `pip install -r requirements/dev.txt`
- Run migrations `bin/manage.sh migrate`
- Start server `bin/manage.sh runserver 8000`
- (Optional) To set up pre-commit hook (to automatically code formatting before commit) run:
  ```bash
    pre-commit install
  ```
  (more info below)


### Code conventions and pre-commit hook
- For code convention we are using:
  - [Isort](https://pycqa.github.io/isort/): for automatically sorting dependency imports.
  - [Blake](https://black.readthedocs.io/en/stable): for code formatting.
  - [Flake8](https://flake8.pycqa.org/en/latest/): for style guide enforcement.
- The above tools have been wrapped with the executable script [bin/lint.sh](bin/lint.sh):
  - To lint only, run: `bin/lint.sh`
  - To automatically format, run: `bin/lint.sh --fix`
- To run these scripts automatically every time you commit, you need to install the pre-commit hooks:
  - Command: `pre-commit install`
  - [Pre-commit documentation](https://pre-commit.com/): Take a look at the documentation for more information.
  - After that, every time you commit, the `pre-commit` hooks will run the `bin/lint.sh --fix` for you.
### Running tests

- `pytest myapp`
- With coverage `pytest --cov-report term --cov=myapp myapp`
