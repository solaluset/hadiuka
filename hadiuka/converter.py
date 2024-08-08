import os
import sys
import argparse

import pwcp

from .translator import mapping, string_modifiers, translate


mapping = {v: k for k, v in mapping.items()}
string_modifiers = {v: k for k, v in string_modifiers.items()}

parser = argparse.ArgumentParser(
    (
        "python -m " + __package__
        if sys.argv[0] == "-m"
        else os.path.basename(sys.argv[0])
    ),
    description="Пайтон українською (конвертація)",
)
parser.add_argument("target", type=argparse.FileType("r"))


def main(args=sys.argv[1:]):
    args = parser.parse_args(args)

    def preprocess(src, filename, preprocessor):
        preprocessor.disabled = True
        return translate(
            orig_preprocess(src, filename, preprocessor),
            mapping,
            string_modifiers,
        )

    orig_preprocess = pwcp.set_preprocessing_function(preprocess)

    print(
        pwcp.preprocessor.preprocess(args.target, args.target.name)[0], end=""
    )


if __name__ == "__main__":
    main()
