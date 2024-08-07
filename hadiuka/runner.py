import os
import sys
import json
import argparse
from importlib import metadata

import pwcp

from . import config


__version__ = metadata.version(__package__)

with open(os.path.join(os.path.dirname(__file__), "mapping.json")) as mapping_file:
    mapping = json.load(mapping_file)


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
parser.add_argument("-m", action="store_true", help="запустити target як модуль")
parser.add_argument("target", nargs=argparse.OPTIONAL)
parser.add_argument("args", nargs=argparse.ZERO_OR_MORE)


def main(args=sys.argv[1:]):
    args = parser.parse_args(args)

    def preprocess(src, filename, preprocessor):
        for key, value in mapping.items():
            preprocessor.define(f"{key} {value}")
        return orig_preprocess(src, filename, preprocessor)

    orig_preprocess = pwcp.set_preprocessing_function(preprocess)

    if not args.target:
        args.m = True
        args.target = "code"
    else:
        # for some reason this prevents `code` module from working
        pwcp.add_file_extension(config.EXTENSION)

    pwcp.main_with_params(
        **vars(args),
        prefer_python=False,
        save_files=False,
        preprocess_unknown_sources=True,
    )
