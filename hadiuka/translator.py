import os
import json

from pypp.parser import default_lexer


with open(os.path.join(os.path.dirname(__file__), "mapping.json")) as mapping_file:
    mapping = json.load(mapping_file)

string_modifiers = {
    "б": "b",
    "ф": "f",
    "с": "r",
    "ю": "u",
}
string_modifiers.update({k.upper(): v.upper() for k, v in string_modifiers.items()})


def _translate_gen(src, word_mapping, letter_mapping):
    lex = default_lexer()
    lex.input(src)
    while tok := lex.token():
        value = tok.value
        if value in word_mapping:
            yield word_mapping[value]
        elif set(value) <= set(letter_mapping):
            yield "".join(letter_mapping[c] for c in value)
        else:
            yield value


def translate(src, word_mapping, letter_mapping):
    return "".join(_translate_gen(src, word_mapping, letter_mapping))
