from math import log10, exp
from random import choice, randint
from time import sleep


class ActionImpossible(Exception):
    pass


class Personnage:
    nom = 'Humain'
    vie_max = 100
    endurance_max = 100
    force = 10
    agilite = 10
    attente_vie_regeneree = 10
    attente_endurance_regeneree = 10

    def __init__(self, niveau=1):
        self.vie = self.vie_max
        self.endurance = self.endurance_max
        self.experience = 10 ** niveau
        self.esquive = False

    def __str__(self):
        return '%s [Niv. %d Vie %d End. %d]' % (self.nom, self.niveau, self.vie,
                                                self.endurance)

    @property
    def niveau(self):
        return int(log10(self.experience))

    @property
    def mort(self):
        return self.vie <= 0

    def attendre(self):
        self.vie = min(self.vie_max, self.vie + self.attente_vie_regeneree)
        self.endurance = min(self.endurance_max,
                             self.endurance + self.attente_vie_regeneree)
        print('%s attend… Et récupère vie & endurance.' % self.nom)

    def frapper(self, other):
        cout = self.force
        if self.endurance < cout:
            raise ActionImpossible('Plus assez d’endurance !')
        self.endurance -= cout
        if other.esquive:
            other.esquive = False
            print('%s tente de frapper %s, mais est esquivé !'
                  % (self.nom, other.nom))
            return
        perte_vie = self.force * exp(self.niveau - other.niveau)
        other.vie -= perte_vie

        print('%s frappe ! %s perd %d de vie.'
              % (self.nom, other.nom, perte_vie))

        if other.mort:
            self.experience += other.experience

    def esquiver_prochain_coup(self):
        cout = 10 / self.agilite
        if self.endurance < cout:
            raise ActionImpossible('Plus assez d’endurance !')
        self.endurance -= cout
        self.esquive = True
        print('%s prépare une esquive pour le prochain coup.' % self.nom)

    def action_choisie(self, other):
        while True:
            choix = input('Que faire ? ').lower()
            try:
                if choix in ('attendre', 'attend', 'a'):
                    self.attendre()
                    break
                elif choix in ('frapper', 'frappe', 'f'):
                    self.frapper(other)
                    break
                elif choix in ('esquiver', 'esquive', 'e'):
                    self.esquiver_prochain_coup()
                    break
                else:
                    print('Choix invalide, taper attend, frappe ou esquive.')
            except ActionImpossible as e:
                print(str(e))

    def action_auto(self, other):
        try:
            self.frapper(other)
        except ActionImpossible:
            try:
                self.esquiver_prochain_coup()
            except ActionImpossible:
                self.attendre()


class ChauveSouris(Personnage):
    nom = 'Chauve-souris'
    vie_max = 10
    force = 1
    agilite = 3


class Gobelin(Personnage):
    nom = 'Gobelin'
    vie_max = 40
    force = 3
    agilite = 8


class Troll(Personnage):
    nom = 'Troll'
    vie_max = 200
    force = 20
    agilite = 3


TYPES_ENNEMIS = [ChauveSouris] * 10 + [Gobelin] * 30 + [Troll]
NIVEAU_OBJECTIF = 5
joueur = Personnage()

while joueur.niveau < NIVEAU_OBJECTIF:
    print('Vous êtes :')
    print(joueur)
    niveau_ennemi = randint(joueur.niveau - 3, joueur.niveau + 1)
    niveau_ennemi = max(1, niveau_ennemi)
    ennemi = choice(TYPES_ENNEMIS)(niveau=niveau_ennemi)
    print('%s vient d’apparaître !' % ennemi)
    while True:
        joueur.action_choisie(ennemi)
        sleep(1)
        if ennemi.mort:
            print('Ennemi mort !')
            print('-' * 50)
            print()
            break
        ennemi.action_auto(joueur)
        sleep(1)
        if joueur.mort:
            print()
            break
        print()
        print(joueur)
        print(ennemi)
    if joueur.mort:
        print('Vous êtes mort :( C’est fini…')
        break

if joueur.niveau == NIVEAU_OBJECTIF:
    print('Victoire, vous avez atteint le niveau %d !! :D' % NIVEAU_OBJECTIF)
