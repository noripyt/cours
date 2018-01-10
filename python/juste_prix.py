from random import choice, randint

objets_et_fourchettes_de_prix = {
    'téléphone portable': [15, 800],
    'aspirateur': [40, 1000],
    'ordinateur portable': [250, 3000],
    'frigo': [200, 5000],
    'voiture': [5000, 50000],
}
essais_max = 15

print('Bienvenue dans le juste prix !')
objet = choice(list(objets_et_fourchettes_de_prix))
prix_min, prix_max = objets_et_fourchettes_de_prix[objet]
prix = randint(prix_min, prix_max)
print('Aujourd’hui, vous pouvez gagner un(e) magnifique %s.' % objet)
prix_annonce = 0
essais = 0
while prix_annonce != prix:
    prix_annonce = int(input('À votre avis, combien cela coûte-t-il ? '))
    if prix_annonce > prix:
        print('C’est moins !')
    elif prix_annonce < prix:
        print('C’est plus !')
    else:
        print('Et c’est le juste priiiiix !!!')
        print('Félicitations, vous avez gagné un(e) %s !!!' % objet)
        break
    essais += 1
    if essais == essais_max:
        print('Comme c’est dommage… Vous avez dépassé le nombre d’essais :(')
        print('Cela coûtait %d €' % prix)
        break
