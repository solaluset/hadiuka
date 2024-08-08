import os
import json

from pypp.parser import default_lexer


with open(
    os.path.join(os.path.dirname(__file__), "mapping.json")
) as mapping_file:
    mapping = json.load(mapping_file)

string_modifiers = {
    "б": "b",
    "ф": "f",
    "с": "r",
    "ю": "u",
}
string_modifiers.update(
    {k.upper(): v.upper() for k, v in string_modifiers.items()}
)


def _translate_gen(src, word_mapping, letter_mapping):
    lex = default_lexer()
    lex.input(src)
    while tok := lex.token():
        value = tok.value
        if value in word_mapping:
            result = word_mapping[value]
            if isinstance(result, str):
                yield result
            else:
                next_tok = lex.token()
                if not next_tok:
                    return
                next_value = next_tok.value
                if not next_value.startswith("'"):
                    yield value
                    yield next_value
                else:
                    next_value = value + next_value
                    while not (
                        match := next(
                            (
                                (word, replacement)
                                for word, replacement in result
                                if next_value.startswith(word)
                            ),
                            None,
                        )
                    ):
                        next_tok = lex.token()
                        if not next_tok:
                            return
                        next_value += next_tok.value
                    yield match[1]
                    rest = ""
                    while tok := lex.token():
                        rest += tok.value
                    yield from _translate_gen(
                        next_value[len(match[0]) :] + rest,
                        word_mapping,
                        letter_mapping,
                    )
                    return
        elif set(value) <= set(letter_mapping):
            yield "".join(letter_mapping[c] for c in value)
        else:
            yield value


def translate(src, word_mapping, letter_mapping):
    return "".join(_translate_gen(src, word_mapping, letter_mapping))
