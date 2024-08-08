import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from hadiuka import main


def test_hadiuka():
    main(["tests/спіраль.пай"])
