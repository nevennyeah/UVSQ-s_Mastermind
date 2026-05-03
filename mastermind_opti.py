import tkinter as tk
import random

COULEURS = ('yellow', 'blue', 'red', 'green', 'white', 'black', 'purple')

tentatives_max = 11
début = 0
partie_commencee = False
solution = None
historique_parties = [] # liste pour stocker les données brutes de la partie

# Fenêtre
fenetre = tk.Tk()
fenetre.title("Mastermind")

tentatives_var = tk.IntVar(value=11)

frame_parametres = tk.Frame(fenetre)
frame_parametres.pack(pady=5)

tk.Label(frame_parametres, text="Tentatives :").pack(side=tk.LEFT)
spin_tentatives = tk.Spinbox(frame_parametres, from_=1, to=20, width=3, textvariable=tentatives_var)
spin_tentatives.pack(side=tk.LEFT, padx=(0, 10))

btn_demarrer = tk.Button(frame_parametres, text="Démarrer la partie")
btn_demarrer.pack(side=tk.LEFT, padx=5)

label_info = tk.Label(fenetre, text="Réglez les tentatives puis démarrez la partie.")
label_info.pack()

entries = []
frame_entries = tk.Frame(fenetre)
frame_entries.pack()

def creer_case():
    lbl = tk.Label(frame_entries, width=6, height=3, relief="solid", bg="white")
    lbl.couleur = ""
    return lbl

for i in range(4):
    lbl = creer_case()
    lbl.grid(row=0, column=i, padx=5)
    entries.append(lbl)


def ajouter_couleur(couleur):
    for lbl in entries:
        if lbl.couleur == "":
            lbl.couleur = couleur
            lbl.config(bg=couleur)
            break

def reinitialiser_cases():
    for lbl in entries:
        lbl.couleur = ""
        lbl.config(bg="white")


def set_etat_controles(actif: bool):
    etat = tk.NORMAL if actif else tk.DISABLED
    for btn in color_buttons:
        btn.config(state=etat)
    btn_valider.config(state=etat)


def demarrer_partie():
    global tentatives_max, début, partie_commencee, solution, historique_parties
    try:
        tentatives_max = int(tentatives_var.get())
    except ValueError:
        label_resultat.config(text="Nombre de tentatives invalide")
        return

    début = 0
    solution = tuple(random.choice(COULEURS) for _ in range(4))
    partie_commencee = True
    historique_parties.clear() # on vide l'historique interne s'il y avait déjà une sauvegarde
    historique.delete("1.0", tk.END)
    reinitialiser_cases()
    set_etat_controles(True)
    label_info.config(text=f"Partie lancée : {tentatives_max} tentatives")
    label_resultat.config(text="")

def sauvegarder_partie():
    global tentatives_max, début, solution, partie_commencee, historique_parties
    
    if not partie_commencee:
        label_resultat.config(text="Vous n'êtes pas en train de jouer, à quoi bon sauvegarder ??")
        return
    
    f_output = open('sauvegarde_mastermind.csv', 'w')

    # ligne 1 : paramètres de base
    f_output.write(str(tentatives_max) + ',' + str(début) + '\n')

    # ligne 2 : la solution secrète
    f_output.write(','.join(solution) + '\n')

    # lignes suivantes : l'historique des essais
    for tour in historique_parties:
        ligne = ','.join(tour["tentative"]) + ',' + str(tour["bien"]) + ',' + str(tour["mal"]) + ',' + str(tour["mauvaises"])
        f_output.write(ligne + '\n')

    f_output.close() # fermeture du fichier
    label_resultat.config(text="Partie sauvegardée avec succès !")

def charger_partie():
    global tentatives_max, début, solution, partie_commencee, historique_parties
    try:
        # ouverture du fichier en lecture ('r')
        f_input = open('sauvegarde_mastermind.csv', 'r')

        # lecture ligne 1 : tentatives_max, début
        ligne1 = f_input.readline().strip().split(',')
        tentatives_max = int(ligne1[0])
        début = int(ligne1[1])
        tentatives_var.set(tentatives_max) # met à jour la Spinbox

        # lecture ligne 2 : solution
        ligne2 = f_input.readline().strip().split(',')
        solution = tuple(ligne2)

        # réinitialisation de l'interface et des variables
        historique_parties.clear()
        historique.delete("1.0", tk.END) 
        
        # lecture de l'historique ligne par ligne
        li = f_input.readline()
        while li != '':
            data = li.strip().split(',')
            tentative = tuple(data[0:4])
            bien = int(data[4])
            mal = int(data[5])
            mauvaises = int(data[6])

            # recréation de la mémoire du jeu
            historique_parties.append({
                "tentative": tentative, "bien": bien, "mal": mal, "mauvaises": mauvaises
            })

            # recréation de l'interface visuelle (historique textuel)
            # on simule le numéro du tour pour l'affichage
            tour_actuel = len(historique_parties)
            historique.insert(tk.END, f"{tour_actuel}: ")
            for c in tentative:
                ajouter_carre_historique(c)
            historique.insert(tk.END, f" → ✓{bien} O{mal} X{mauvaises}\n")

            li = f_input.readline()

        f_input.close() # fermeture du fichier

        # mettre à jour l'état global de la partie
        partie_commencee = True
        set_etat_controles(True)
        reinitialiser_cases()
        label_info.config(text=f"Partie chargée : {tentatives_max} tentatives")
        label_resultat.config(text="Partie chargée avec succès !")

    except FileNotFoundError:
        label_resultat.config(text="Aucun fichier de sauvegarde trouvé.")

# ajout des boutons 'sauvegarder' et 'charger' a côté de 'démarrer'
btn_sauvegarder = tk.Button(frame_parametres, text="Sauvegarder", command=sauvegarder_partie)
btn_sauvegarder.pack(side=tk.LEFT, padx=5)

btn_charger = tk.Button(frame_parametres, text="Charger", command=charger_partie)
btn_charger.pack(side=tk.LEFT, padx=5)

frame_couleurs = tk.Frame(fenetre) #bouton de couleur
frame_couleurs.pack()

color_buttons = []
for c in COULEURS:
    btn = tk.Button(frame_couleurs, text=c, command=lambda col=c: ajouter_couleur(col))
    btn.pack(side=tk.LEFT)
    color_buttons.append(btn)


historique = tk.Text(fenetre, height=12, width=60) # initialisation de l'historique, tah c'est dans le nom
historique.pack()

def ajouter_carre_historique(couleur):
    carre = tk.Label(historique, width=2, height=1, bg=couleur, relief="solid")
    historique.window_create(tk.END, window=carre)
    historique.insert(tk.END, " ")


def obtenir_sequence():
    seq = []
    for lbl in entries:
        if lbl.couleur not in COULEURS:
            return None
        seq.append(lbl.couleur)
    return tuple(seq)

def verifier():
    global début

    if not partie_commencee:
        label_resultat.config(text="Démarrez la partie d'abord")
        return

    # Vérifier limite
    if début >= tentatives_max:
        label_resultat.config(text="❌ Plus de tentatives !")
        return

    tentative = obtenir_sequence()

    if tentative is None:
        label_resultat.config(text="Couleur invalide")
        return

    début += 1  # On compte la tentative

    # Bien placées
    bien_placees = sum(t == s for t, s in zip(tentative, solution))

    # Mal placées
    indices = [i for i in range(4) if tentative[i] != solution[i]]
    sol_reste = [solution[i] for i in indices]
    tent_reste = [tentative[i] for i in indices]

    mal_placees = 0
    for c in tent_reste:
        if c in sol_reste:
            mal_placees += 1
            sol_reste.remove(c)

    mauvaises = len(tent_reste) - mal_placees

    # sauvegarde de la tentative en mémoire pour l'exportation
    historique_parties.append({
        "tentative": tentative, 
        "bien": bien_placees, 
        "mal": mal_placees, 
        "mauvaises": mauvaises
    })
   
    historique.insert(tk.END, f"{début}: ")
    for c in tentative:
        ajouter_carre_historique(c)

    historique.insert(tk.END, f" → ✓{bien_placees} O{mal_placees} X{mauvaises}\n")


    label_resultat.config(text=f"✓{bien_placees} O{mal_placees} X{mauvaises}")

    # Victoire
    if bien_placees == 4:
        label_resultat.config(text="🎉 VICTOIRE !")
        btn_valider.config(state="disabled")
        return

    # Défaite après le nombre de tentatives défini
    if début == tentatives_max:
        label_resultat.config(text=f"GAME OVER! il fallait trouver {solution}")
        btn_valider.config(state="disabled")

    # Réinitilaisation des cases
    for lbl in entries:
        lbl.couleur = ""
        lbl.config(bg="white")


btn_valider = tk.Button(fenetre, text="Valider", command=verifier)
btn_valider.pack()

label_resultat = tk.Label(fenetre, text="")
label_resultat.pack()

btn_demarrer.config(command=demarrer_partie)
set_etat_controles(False)

fenetre.mainloop()
