#!/usr/bin/env python3
import click
from pathlib import Path
from collections import Iterable
from parser import Config

# We'll use this as a default argument value.
# Allows us to diffrentiate between the user setting a config
# value to None, and when they didn't include a value at all.
MISSING = object()

def format_for_cli_display(value):
    """Formats given value for display in the CLI

    If it's a section, we'll display all it's options and their values.
    If it's an option, we'll display it's value.

    Arguments:
        value {mixed} -- Can be a section, or an option

    Returns:
        str -- String representation of given value
    """
    if isinstance(value, Iterable) and not isinstance(value, str):
        return '\n'.join(['{} = {}'.format(k, v) for (k, v) in value.items()])
    else:
        return str(value)


@click.command()
@click.argument('file_path')
@click.argument('key')
@click.argument('value', default=MISSING)
def cli(file_path, key, value):
    """This script works with the given config file to read/write values.

    If key/value contains spaces, wrap in quotes.

    Arguments:

        \b
        file_path {str} -- Path to the config file
        key {str} -- Option in question. Use dot notation (ex - header.option )
        value {mixed} -- Optional. If given, sets new value for given config option.

    Examples:

        \b
        Get value from section:
            cli.py ../path/config.txt header.budget
            cli.py ../path/config.txt "meta data.description"  # wrap with quotes if using spaces

        \b
        Get all values from section:
            cli.py ../path/config.txt header

        \b
        Set value for option:
            cli.py ../path/config.txt header.budget 12
            cli.py ../path/config.txt header.project "My new value that contains spaces"
    """
    file_path = Path(file_path).resolve()
    config = Config(str(file_path))

    if value is not MISSING:
        config.set(key, value)
        config.write()
        click.echo('{} = {}'.format(key, value))
    else:
        result = format_for_cli_display(config.get(key))
        click.echo(result)


if __name__ == '__main__':
    cli()
