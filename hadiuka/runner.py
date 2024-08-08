import os
import sys
import argparse
from importlib import metadata
from collections import defaultdict

import pwcp

from . import config
from .translator import mapping, string_modifiers, translate


__version__ = metadata.version(__package__)

mapping_with_apostrophes = defaultdict(list)
for k, v in mapping.items():
    first_part, *rest = k.split("'")
    if rest:
        mapping_with_apostrophes[first_part].append((k, v))
        mapping_with_apostrophes[first_part].sort(
            key=lambda elem: len(elem[0]), reverse=True
        )
    else:
        mapping_with_apostrophes[first_part] = v

parser = argparse.ArgumentParser(
    (
        "python -m " + __package__
        if sys.argv[0] == "-m"
        else os.path.basename(sys.argv[0])
    ),
    description="Пайтон українською",
)
parser.add_argument(
    "--version", action="version", version=__package__ + " " + __version__
)
parser.add_argument(
    "-m", action="store_true", help="запустити target як модуль"
)
parser.add_argument("target", nargs=argparse.OPTIONAL)
parser.add_argument("args", nargs=argparse.ZERO_OR_MORE)


def main(args=sys.argv[1:]):
    args = parser.parse_args(args)

    pwcp.add_file_extension(config.EXTENSION)

    def preprocess(src, filename, preprocessor):
        preprocessor.disabled = True
        return translate(
            orig_preprocess(src, filename, preprocessor),
            mapping_with_apostrophes,
            string_modifiers,
        )

    orig_preprocess = pwcp.set_preprocessing_function(preprocess)

    if not args.target:
        args.m = True
        args.target = "code"

    pwcp.main_with_params(
        **vars(args),
        prefer_python=False,
        save_files=False,
        preprocess_unknown_sources=True,
    )
