import tkinter as tk

COULEURS = ('yellow', 'blue', 'red', 'green', 'white', 'black', 'purple')

début = 0
partie_commencee = False
solution = None
historique_parties = []  # liste pour stocker les données brutes de la partie

# Phase: 'setup' pour le secret, 'guess' pour le joueur qui devine
phase = 'setup'
solution = None

tentatives = 11  # valeur par défaut

# Lecture éventuelle de la config
try:
    f_input = open("Sauvegarde/config.csv", "r")
    f_input.readline()
    ligne = f_input.readline()
    if ligne != "":
        donnees = ligne.strip().split(',')
        tentatives = int(donnees[1])
    f_input.close()
except FileNotFoundError:
    pass

fenetre = tk.Tk()
fenetre.title("Mastermind 2 joueurs")

tentatives_var = tk.IntVar(value=tentatives)

frame_parametres = tk.Frame(fenetre)
frame_parametres.pack(pady=5)

tk.Label(frame_parametres, text="Tentatives :").pack(side=tk.LEFT)
spin_tentatives = tk.Spinbox(frame_parametres, from_=1, to=20, width=3, textvariable=tentatives_var)
spin_tentatives.pack(side=tk.LEFT, padx=(0, 10))

def demarrer_partie():
    global tentatives, début, phase, solution, historique_parties
    tentatives = tentatives_var.get()
    début = 0
    phase = 'setup'
    solution = None
    historique_parties.clear()
    historique.delete("1.0", tk.END)
    reinitialiser_cases()
    btn_valider.config(state="normal", text="Enregistrer le secret")
    btn_sauvegarder.config(state=tk.DISABLED)
    label_info.config(text="Joueur 1 : choisissez la combinaison secrète")
    label_resultat.config(text="")

btn_demarrer = tk.Button(frame_parametres, text="Démarrer la partie", command=demarrer_partie)
btn_demarrer.pack(side=tk.LEFT, padx=5)

label_info = tk.Label(fenetre, text="Réglez les tentatives puis démarrez la partie.")
label_info.pack()

entries = []
frame_entries = tk.Frame(fenetre)
frame_entries.pack()

frame_boutons = tk.Frame(fenetre)
frame_boutons.pack(pady=5)

def sauvegarder_partie():
    global phase, tentatives, début, solution, historique_parties

    if phase == 'setup':
        label_resultat.config(text="Vous n'êtes pas en train de jouer, à quoi bon sauvegarder ??")
        return

    f_output = open('Sauvegarde/sauvegarde_mastermind_2P.csv', 'w')

    # 1ere ligne: les paramètres et la phase
    f_output.write(f"{phase},{tentatives},{début}\n")

    # 2eme ligne: le code secret
    f_output.write(','.join(solution) + '\n')

    # le reste c'est l'historique des essais
    for tour in historique_parties:
        ligne = (
            ','.join(tour["tentative"]) + ',' +
            str(tour["bien"]) + ',' +
            str(tour["mal"]) + ',' +
            str(tour["mauvaises"])
        )
        f_output.write(ligne + '\n')

    f_output.close()
    label_resultat.config(text="Partie sauvegardée !")

def charger_partie():
    global phase, tentatives, début, solution, historique_parties
    try:
        f_input = open('Sauvegarde/sauvegarde_mastermind_2P.csv', 'r')

        # ligne 1
        ligne1 = f_input.readline().strip().split(',')
        phase = ligne1[0]
        tentatives_lues = int(ligne1[1])
        début_lu = int(ligne1[2])

        # on met à jour les variables globales
        tentatives_var.set(tentatives_lues)
        tentatives = tentatives_lues
        début = début_lu

        # ligne 2 : solution
        ligne2 = f_input.readline().strip()
        solution_lue = tuple(ligne2.split(','))
        solution = solution_lue

        # reset historique
        historique_parties.clear()
        historique.delete("1.0", tk.END)
        reinitialiser_cases()

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
            
            historique.insert(tk.END, " → ")
            ajouter_resultat_couleurs(bien, mal, mauvaises)
            historique.insert(tk.END, "\n")

            li = f_input.readline()

        f_input.close()

        btn_valider.config(state="normal")
        btn_sauvegarder.config(state="normal")
        label_info.config(text="Joueur 2 : devinez la combinaison")
        btn_valider.config(text="Valider")

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

btn_sauvegarder = tk.Button(frame_boutons, text="Sauvegarder", command=sauvegarder_partie, state=tk.DISABLED)
btn_sauvegarder.pack(side=tk.LEFT, padx=5)

btn_charger = tk.Button(frame_boutons, text="Charger", command=charger_partie)
btn_charger.pack(side=tk.LEFT, padx=5)

def ajouter_resultat_couleurs(bien, mal, mauvaises):
    # Carrés verts
    for _ in range(bien):
        carre = tk.Label(historique, width=2, height=1, bg="green", relief="solid")
        historique.window_create(tk.END, window=carre)
        historique.insert(tk.END, " ")

    # Carrés orange
    for _ in range(mal):
        carre = tk.Label(historique, width=2, height=1, bg="orange", relief="solid")
        historique.window_create(tk.END, window=carre)
        historique.insert(tk.END, " ")

    # Carrés rouges
    for _ in range(mauvaises):
        carre = tk.Label(historique, width=2, height=1, bg="red", relief="solid")
        historique.window_create(tk.END, window=carre)
        historique.insert(tk.END, " ")
        
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

label_info.config(text="Joueur 1 : choisissez la combinaison secrète")

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

    historique_parties.append({
        "tentative": tentative,
        "bien": bien_placees,
        "mal": mal_placees,
        "mauvaises": mauvaises
    })

    historique.insert(tk.END, f"{début}: ")
    for c in tentative:
        ajouter_carre_historique(c)
    
    historique.insert(tk.END, " → ")
    ajouter_resultat_couleurs(bien_placees, mal_placees, mauvaises)
    historique.insert(tk.END, "\n")

    label_resultat.config(text=f"{bien_placees} verts, {mal_placees} oranges, {mauvaises} rouges")

    if bien_placees == 4:
        label_resultat.config(text="Joueur 2 gagne !")
        btn_valider.config(state="disabled")
        btn_sauvegarder.config(state="disabled")
        label_info.config(text=f"La combinaison était : {' '.join(solution)}")
        return

    if début == tentatives:
        label_resultat.config(text=f"GAME OVER ! La solution était : {' '.join(solution)}")
        btn_valider.config(state="disabled")
        btn_sauvegarder.config(state="disabled")

def enregistrer_secret():
    global phase, solution, historique_parties

    tentative = obtenir_sequence()
    if tentative is None:
        label_resultat.config(text="Couleur invalide")
        return

    solution = tentative
    phase = 'guess'
    historique_parties.clear()
    historique.delete("1.0", tk.END)
    label_info.config(text="Joueur 2 : devinez la combinaison")
    label_resultat.config(text="Secret enregistré. Joueur 2, c'est à vous !")
    historique.insert(tk.END, "Secret défini. Joueur 2 commence.\n")
    reinitialiser_cases()

    btn_valider.config(text="Valider")
    btn_sauvegarder.config(state="normal")

def verifier():
    global solution, phase

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
