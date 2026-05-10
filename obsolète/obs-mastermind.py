import random
def mastermind():
    ...

possibilités = ['jaune', 'bleu', 'rouge', 'vert', 'blanc', 'noir', 'violet']

def Solution_auto():
    '''on va créer une séquence solution de manière aléatoire'''
    solution = []
    for i in range(4):
        i = random.choice(possibilités)
        solution.append(i)
    return solution

def Solution_manuel():
    '''on va séléctionner la séquence solution'''
    solution = []
    for i in range(4):
        i = str(input('choisir une couleur dans jaune, bleu, rouge, vert, blanc, noir, violet :\n'))
        if str(i) not in possibilités:
            return 'erreur'
            '''si le texte entré ne figure pas dans l'ensemble des posibilités de solution'''
        solution.append(i)
    return solution

def essai():
    '''on donne une liste correspondant a une tentative de trouver la liste solution'''
    tentative = []
    for i in range(4):
        i = str(input('choisir une couleur dans jaune, bleu, rouge, vert, blanc, noir, violet :\n'))
        if str(i) not in possibilités:
            return 'erreur'
            '''si le texte entré ne figure pas dans l'ensemble des posibilités de solution'''
        tentative.append(i)
    return tentative

def passage_en_int(list):
    '''on convertit les listes de chaine de caractères en liste de valeurs pour simplifier la comparaison'''
    nouvelle_list = []
    for couleurs in list:
        if couleurs == "bleu":
            nouvelle_list.append(0)
        if couleurs == "rouge":
            nouvelle_list.append(1)
        if couleurs == "vert":
            nouvelle_list.append(2)
        if couleurs == "jaune":
            nouvelle_list.append(3)
        if couleurs == "blanc":
            nouvelle_list.append(4)
        if couleurs == "noir":
            nouvelle_list.append(5)
        if couleurs == "violet":
            nouvelle_list.append(6)
    return nouvelle_list

def vérification():
    '''on vérifie la correspondance entre le tentative utilisateur et la solution'''
    tentative = passage_en_int(essai())
    '''on execute les fonctions associées'''
    couleur_bien_placees = 0
    couleur_mal_placees = 0
    mauvaise_couleur = 0
    for i in range(len(tentative)):
        if tentative[i] == solution[i]:
            couleur_bien_placees += 1
        else:
            if tentative[i] in solution:
                couleur_mal_placees += 1
            else:
                mauvaise_couleur += 1
    return ("il y a " ,mauvaise_couleur, "mauvaise couleur",
            couleur_mal_placees, "couleur bonne mais au mauvais endroit",
            couleur_bien_placees, "couleur au bon endroit")
