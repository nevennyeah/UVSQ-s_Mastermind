import random

couleur = ["bleu", "rouge", "vert", "jaune", "noir", "violet", "blanc", "orange"]
couleur_a_trouver = []

def generation_de_couleurs():
    return random.choices(couleur, k=4)

def evaluer_proposition(combinaison, tentative):
    bien_places = 0
    mal_places = 0
    
    combinaison_restante = []
    tentative_restante = []

    for c, t in zip(combinaison, tentative):
        if c == t:
            bien_places += 1
        else:
            combinaison_restante.append(c)
            tentative_restante.append(t)

    for t in tentative_restante:
        if t in combinaison_restante:
            mal_places += 1
            combinaison_restante.remove(t)
    return bien_places, mal_places

def jouer_mastermind():
    tentative_max = 11

    solution = generation_de_couleurs()
    
    print("Couleurs disponibles :", couleur, sep=" ")
    print("Trouvez la combinaison en 11 essais.")
    print("Exemple de réponse : rouge vert vert noir")
    print()

    for essai in range(1, tentative_max + 1):
        while True:
            entree_raw = input(f"Essai {essai}/{tentative_max} : ").lower()     
            proposition = entree_raw.replace(",", " ").split()
            if len(proposition) == 4 and all(c in couleur for c in proposition):
                break
            print(f"Invalide ! Entrez 4 couleurs parmi {couleur}.")

        bien, mal = evaluer_proposition(solution, proposition)

        if bien == 4:
            print(f"Bravo ! Vous avez trouvé la combinaison {entree_raw} en {essai} essais.")
            return

        print(f"-> {bien} bien placé(s), {mal} mal placé(s)\n")

    print(f"Dommage ! Vous avez perdu. La solution était : {' '.join(solution)}")

jouer_mastermind()