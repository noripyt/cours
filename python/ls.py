#!/usr/bin/env python3

from argparse import ArgumentParser, ArgumentTypeError
from itertools import islice
from pathlib import Path


def to_dir_path(path_str):
    dir_path = Path(path_str)
    if dir_path.is_dir():
        return dir_path
    raise ArgumentTypeError('Le chemin n’est pas un dossier valide.')


parser = ArgumentParser(
    description='Ce script liste les fichiers Python et leur taille.')
parser.add_argument('chemin', default='.', nargs='?', type=to_dir_path,
                    help='Chemin vers le dossier à lister')
parser.add_argument('--afficher-taille', action='store_true',
                    help='Affiche la taille de chaque fichier')
parser.add_argument('--limite', type=int, default=1000)
args = parser.parse_args()

for path in islice(args.chemin.glob('**/*.py'), args.limite):
    if args.afficher_taille:
        print('%6d octets' % path.stat().st_size, path)
    else:
        print(path)
