from configparser import ConfigParser
from wrapt import ObjectProxy
import re

def nested_set(dic, keys, value):
    for key in keys[:-1]:
        dic = dic.setdefault(key, {})
    dic[keys[-1]] = value

class CustomParser(ConfigParser):
    """Custom ConfigParser to hold our own rules

    Extends:
        ConfigParser
    """
    _FLAGS = re.MULTILINE | re.VERBOSE

    # Regular expressions for parsing section headers and options
    _SECTION_HEADER = r"""
        ^\[                                # [ in col 0
        \s*                                # leading whitespace
            (?P<header>[^\]\n]+?)              # get chars until close,
                                               # match as few as possible
        \s*                                # trailing whitespace
        \]                                 # ]
        """

    _OPTION = r"""
        ^(?P<option>\w.*?)                 # key starts in col 0
        \s*(?P<vi>\:)\s*                   # colon surrounded by whitespace
        (?P<value>                         # match value as...
            (?:                                # for each line...
                (?:.|\n)                           # get all chars/newlines,
                (?!^[^\s]+)                        # until the next non-continued line
                                                   # (match lines until it starts with space)
            )*                                 # non-capture to hold negative lookahead
        )$                               # everything up to eol
        """

    # Compiled regular expression for matching sections
    SECTCRE = re.compile(_SECTION_HEADER, _FLAGS)

    # Compiled regular expression for matching options
    OPTCRE = re.compile(_OPTION, _FLAGS)

    def __init__(self, *args, **kwargs):
        kwargs['delimiters'] = (':',)
        super().__init__(*args, **kwargs)


class Config(ObjectProxy):
    """Helper class to make working with the config file easier

    Acts as a proxy to our CustomParser class, adding a few
    helper functions on top of it.

    Extends:
        wrapt.ObjectProxy

    Variables:
        __slots__ {tuple} -- So the ObjectProxy knows not to forward these
    """
    __slots__ = ('parsed', 'file_path')

    def __init__(self, file_path):
        self.file_path = file_path
        self.parsed = CustomParser()
        self.parsed.read(self.file_path)
        super().__init__(self.parsed)

    def get(self, key):
        value = self.parsed
        for k in key.split('.'):
            value = value[k]
        return value

    def set(self, key, value):
        nested_set(self.parsed, key.split('.'), value)

    def write(self):
        with open(self.file_path, 'w') as config_file:
            self.parsed.write(config_file)
