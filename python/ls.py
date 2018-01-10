#!/usr/bin/env python3

from argparse import ArgumentParser
from pathlib import Path

parser = ArgumentParser(
    description='Ce script liste les fichiers Python et leur taille.')
parser.add_argument('chemin', default='.', nargs='?',
                    help='Chemin vers le fichier')
parser.add_argument('--afficher-taille', action='store_true',
                    help='Afficher la taille')
parser.add_argument('--limite', type=int, default=100)
args = parser.parse_args()
paths = Path(args.chemin).glob('**/*.py')

if args.afficher_taille:
    def show_path(path):
        print('%6d octets' % path.stat().st_size, path)
else:
    def show_path(path):
        print(path)


for i, path in enumerate(paths):
    if i == args.limite:
        break
    show_path(path)
