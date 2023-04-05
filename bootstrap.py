import fileinput
import os
import shutil

import click


@click.command()
@click.option("--app_name", prompt="Your app name", help="The app name would be use instead of `myapp`.")
def cli(app_name):
    """Simple program that greets NAME for a total of COUNT times."""
    replace_files = (
        'bin/manage.sh',
        'bin/lint.sh',
        'pyproject.toml',
        'myapp/config/settings/base.py'
    )

    with fileinput.FileInput(files=replace_files, inplace=True) as file:
        for line in file:
            print(line.replace('myapp', app_name), end='')

    shutil.move('myapp', app_name)

    shutil.copyfile('.env.TEMPLATE', '.env')

    bootstrap_file = 'bootstrap.py'
    if os.path.isfile(bootstrap_file):
        os.remove(bootstrap_file)


if __name__ == '__main__':
    cli()
