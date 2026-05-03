import tkinter as tk

COULEURS = ('yellow', 'blue', 'red', 'green', 'white', 'black', 'purple')

# Phase: 'setup' pour le secret, 'guess' pour le joueur qui devine
phase = 'setup'
solution = None

tentatives = 11
début = 0
historique_parties = [] # liste pour stocker les données brutes de la partie

# Fenêtre
fenetre = tk.Tk()
fenetre.title("Mastermind 2 joueurs")
frame_boutons = tk.Frame(fenetre)
frame_boutons.pack(pady=5)

def sauvegarder_partie():
    global phase, tentatives, début, solution, historique_parties
    
    # on bloque au cas ou, mais le bouton est grisé dans tout les cas
    if phase == 'setup':
        label_resultat.config(text="Vous n'êtes pas en train de jouer, à quoi bon sauvegarder ??")
        return
    
    # on ouvre le fichier pour écrire dedans
    f_output = open('sauvegarde_mastermind_2P.csv', 'w')

    # 1ere ligne: les paramètres et la phase
    f_output.write(f"{phase},{tentatives},{début}\n")

    # 2eme ligne: le code secret
    f_output.write(','.join(solution) + '\n')

    # le reste c'est l'historique des essais
    for tour in historique_parties:
        ligne = ','.join(tour["tentative"]) + ',' + str(tour["bien"]) + ',' + str(tour["mal"]) + ',' + str(tour["mauvaises"])
        f_output.write(ligne + '\n')

    # on ferme le fichier
    f_output.close() 
    label_resultat.config(text="Partie sauvegardée !")

def charger_partie():
    global phase, tentatives, début, solution, historique_parties
    try:
        # on lit le fichier de save
        f_input = open('sauvegarde_mastermind_2P.csv', 'r')

        # on lit la ligne 1
        ligne1 = f_input.readline().strip().split(',')
        phase = ligne1[0]
        tentatives = int(ligne1[1])
        début = int(ligne1[2])

        # on lit la ligne 2 pour chopper la soluce
        ligne2 = f_input.readline().strip()
        solution = tuple(ligne2.split(','))

        # on vide l'historique interne s'il y avait déjà une sauvegarde
        historique_parties.clear()
        historique.delete("1.0", tk.END) 
        
        # Réinitilaisation des cases
        reinitialiser_cases()
        
        # on recrée la memoire du jeu
        li = f_input.readline()
        while li != '':
            data = li.strip().split(',')
            tentative = tuple(data[0:4])
            bien = int(data[4])
            mal = int(data[5])
            mauvaises = int(data[6])

            historique_parties.append({
                "tentative": tentative, "bien": bien, "mal": mal, "mauvaises": mauvaises
            })

            tour_actuel = len(historique_parties)
            historique.insert(tk.END, f"{tour_actuel}: ")
            for c in tentative:
                ajouter_carre_historique(c)
            historique.insert(tk.END, f" → ✓{bien} O{mal} X{mauvaises}\n")

            li = f_input.readline()

        f_input.close() 

        # maj de l'interface parce qu'on est dans la phase guess
        btn_valider.config(state="normal")
        btn_sauvegarder.config(state="normal") # on réactive la save parce qu'on joue
        label_info.config(text="Joueur 2 : devinez la combinaison")
        btn_valider.config(text="Valider")
            
        # check si la partie chargée était déià finie
        if len(historique_parties) > 0:
            dernier_tour = historique_parties[-1]
            if dernier_tour["bien"] == 4:
                label_resultat.config(text="Le joueur 2 a déjà gagné")
                btn_valider.config(state="disabled")
                btn_sauvegarder.config(state="disabled")
                label_info.config(text=f"La réponse était : {' '.join(solution)}")
            elif début >= tentatives:
                label_resultat.config(text=f"Perdu ! la réponse était : {' '.join(solution)}")
                btn_valider.config(state="disabled")
                btn_sauvegarder.config(state="disabled")
            else:
                label_resultat.config(text="Partie chargée, au tour du joueur 2")
        else:
            label_resultat.config(text="Partie chargée, au tour du joueur 2")

    except FileNotFoundError:
        label_resultat.config(text="y a pas de sauvegarde frero")

# on grise le bouton de save au debut avec tk.DISABLED
btn_sauvegarder = tk.Button(frame_boutons, text="Sauvegarder", command=sauvegarder_partie, state=tk.DISABLED)
btn_sauvegarder.pack(side=tk.LEFT, padx=5)

# ajout des boutons 'sauvegarder' et 'charger' a côté de 'démarrer'
btn_charger = tk.Button(frame_boutons, text="Charger", command=charger_partie)
btn_charger.pack(side=tk.LEFT, padx=5)

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

frame_couleurs = tk.Frame(fenetre)
frame_couleurs.pack()
for c in COULEURS:
    btn = tk.Button(frame_couleurs, text=c, command=lambda col=c: ajouter_couleur(col))
    btn.pack(side=tk.LEFT)

historique = tk.Text(fenetre, height=14, width=60)
historique.pack()

label_info = tk.Label(fenetre, text="Joueur 1 : choisissez la combinaison secrète")
label_info.pack()

label_resultat = tk.Label(fenetre, text="")
label_resultat.pack()


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


def reinitialiser_cases():
    for lbl in entries:
        lbl.couleur = ""
        lbl.config(bg="white")


def evaluer_secret(tentative):
    global début

    début += 1
    bien_placees = sum(t == s for t, s in zip(tentative, solution))

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

    if bien_placees == 4:
        label_resultat.config(text="Joueur 2 gagne !")
        btn_valider.config(state="disabled")
        label_info.config(text=f"La combinaison était : {' '.join(solution)}")
        return

    if début == tentatives:
        label_resultat.config(text=f"GAME OVER ! La solution était : {' '.join(solution)}")
        btn_valider.config(state="disabled")


def enregistrer_secret():
    global phase, solution, historique_parties

    tentative = obtenir_sequence()
    if tentative is None:
        label_resultat.config(text="Couleur invalide")
        return

    solution = tentative
    phase = 'guess'
    # on vide l'historique interne s'il y avait déjà une sauvegarde
    historique_parties.clear() 
    historique.delete("1.0", tk.END)
    label_info.config(text="Joueur 2 : devinez la combinaison")
    label_resultat.config(text="Secret enregistré. Joueur 2, c'est à vous !")
    historique.insert(tk.END, "Secret défini. Joueur 2 commence.\n")
    reinitialiser_cases()

    btn_valider.config(text="Valider")
    btn_sauvegarder.config(state="normal") # le vrai jeu commence, on debug le bouton save

def verifier():
    global solution

    if phase == 'setup':
        enregistrer_secret()
        return

    if début >= tentatives:
        label_resultat.config(text="Plus de tentatives !")
        return

    tentative = obtenir_sequence()
    if tentative is None:
        label_resultat.config(text="Couleur invalide")
        return

    evaluer_secret(tentative)
    
    reinitialiser_cases()


btn_valider = tk.Button(fenetre, text="Enregistrer le secret", command=verifier)
btn_valider.pack(pady=10)

fenetre.mainloop()
