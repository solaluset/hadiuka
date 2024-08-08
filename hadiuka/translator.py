import os
import json

from pypp.parser import default_lexer


with open(os.path.join(os.path.dirname(__file__), "mapping.json")) as mapping_file:
    mapping = json.load(mapping_file)


def _translate_gen(src, mapping):
    lex = default_lexer()
    lex.input(src)
    while tok := lex.token():
        value = tok.value
        yield mapping.get(value, value)


def translate(src, mapping):
    return "".join(_translate_gen(src, mapping))
