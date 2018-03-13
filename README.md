# parser_demo

A demo project for parsing data from a file.

Uses python 3. It's just a demo, so there's no tests or pip editable install or setuptools to deal with. Just clone it and run.

To start:

```bash
$ git clone https://github.com/haydenbbickerton/parser_demo.git
$ cd parser_demo
$ pip3 install -r requirements.txt
$ ./cli.py --help
Usage: cli.py [OPTIONS] FILE_PATH KEY [VALUE]

  This script works with the given config file to read/write values.

  If key/value contains spaces, wrap in quotes.

  Arguments:

          file_path {str} -- Path to the config file
          key {str} -- Option in question. Use dot notation (ex - header.option )
          value {mixed} -- Optional. If given, sets new value for given config option.

  Examples:

          Get value from section:
              cli.py ../path/config.txt header.budget
              cli.py ../path/config.txt "meta data.description"  # wrap with quotes if using spaces

          Get all values from section:
              cli.py ../path/config.txt header

          Set value for option:
              cli.py ../path/config.txt header.budget 12
              cli.py ../path/config.txt header.project "My new value that contains spaces"

Options:
  --help  Show this message and exit.
```
