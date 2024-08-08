from pypp.parser import default_lexer


def _translate_gen(src, mapping):
    lex = default_lexer()
    lex.input(src)
    while tok := lex.token():
        value = tok.value
        yield mapping.get(value, value)


def translate(src, mapping):
    return "".join(_translate_gen(src, mapping))
