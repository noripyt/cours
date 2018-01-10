#!/usr/bin/env python3

from argparse import ArgumentParser
import datetime
import os.path


parser = ArgumentParser(description='Un journal intime en ligne de commande.')
subparsers = parser.add_subparsers(dest='commande')
subparsers.required = True
parser_ajout = subparsers.add_parser('ajout')
parser_ajout.add_argument('titre')
parser_ajout.add_argument('--date',
                          help='Utiliser une autre date '
                               'qu’aujourd’hui, au format AAAA-MM-JJ.')
parser_liste = subparsers.add_parser('liste')
parser_liste.add_argument('--date', help='Rechercher une date spécifique, '
                                         'au format AAAA-MM-JJ.')

args = parser.parse_args()

FILE_PATH = 'journal.txt'
if not os.path.exists(FILE_PATH):
    with open(FILE_PATH, 'w'):
        pass


def convert_date(date_str):
    return datetime.datetime.strptime(date_str, '%Y-%m-%d').date()


date = None if args.date is None else convert_date(args.date)

if args.commande == 'ajout':
    if date is None:
        date = datetime.date.today()
    with open(FILE_PATH, 'a') as f:
        f.write('%s %s\n' % (date, args.titre))
elif args.commande == 'liste':
    entrees = []
    with open(FILE_PATH) as f:
        for line in f.readlines():
            entree_date, entree_titre = line.strip().split(' ', 1)
            if date is not None and convert_date(entree_date) != date:
                continue
            entrees.append((entree_date, entree_titre))
    for entree_date, entree_titre in sorted(entrees, key=lambda e: e[0],
                                            reverse=True):
        print(entree_date, entree_titre)
