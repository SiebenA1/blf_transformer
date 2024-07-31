# -*- coding: utf-8 -*-
import argparse
from pathlib import Path

parser = argparse.ArgumentParser(description='A simple command line tool to convert BLF file to a normal file which '
                                             'can be checked easily.')
parser.add_argument('--blf-file', type=Path, help='The input BLF file path.')
parser.add_argument('--dbc-file', type=Path, nargs='+', help='The input DBC file paths.')
parser.add_argument('--signal-list', type=str, nargs='+', help='The name of signals which need to be extracted.')
