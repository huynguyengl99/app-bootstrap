import fileinput
import os
import re
import shutil
import subprocess

import click

from builders.process_modules import process_modules


def validate_app_name(ctx, param, value):
    app_name_pattern = re.compile("^[a-z0-9_]+$")
    if not app_name_pattern.match(value):
        raise click.BadParameter("App name should contain only alphanumeric and underscore.")
    return value


@click.command()
@click.option(
    "--app_name",
    prompt="Enter your app name (only lowercase alphanumeric and underscore)",
    help="The app name would be use instead of `myapp`.",
    callback=validate_app_name,
)
def cli(app_name):
    """Simple program that greets NAME for a total of COUNT times."""
    process_modules("myapp")

    replace_files = (
        "bin/manage.sh",
        "bin/lint.sh",
        "docs/channels-websocket.md",
        "pyproject.toml",
        "myapp/config/settings/base.py",
        "myapp/config/asgi.py",
        "myapp/config/urls.py",
        "myapp/config/wsgi.py",
        ".coveragerc",
        "README.TEMPLATE.md",
    )

    with fileinput.FileInput(files=replace_files, inplace=True) as file:
        for line in file:
            print(line.replace("myapp", app_name).replace("MYAPP", app_name.upper()), end="")

    remove_line_include_content_files = (
        "requirements-init.txt",
        ".gitignore",
    )
    remove_line_contents = (
        "click",
        "Temporary ignore",
        "poetry.lock",
    )
    with fileinput.FileInput(files=remove_line_include_content_files, inplace=True) as file:
        for line in file:
            if not any(remove_content in line for remove_content in remove_line_contents):
                print(line, end="")

    shutil.move("myapp", app_name)

    shutil.copyfile(".env.TEMPLATE", ".env")

    builder_dirs = "builders"
    if os.path.isdir(builder_dirs):
        shutil.rmtree(builder_dirs)

    shutil.move("README.TEMPLATE.md", "README.md")
    shutil.rmtree(".git")

    subprocess.run(["git", "init", "-b", "main"])


if __name__ == "__main__":
    cli()
