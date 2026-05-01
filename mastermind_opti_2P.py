import tkinter as tk

COULEURS = ('yellow', 'blue', 'red', 'green', 'white', 'black', 'purple')

# Phase: 'setup' pour le secret, 'guess' pour le joueur qui devine
phase = 'setup'
solution = None

tentatives = 11
début = 0

fenetre = tk.Tk()
fenetre.title("Mastermind 2 joueurs")

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
    global phase, solution

    tentative = obtenir_sequence()
    if tentative is None:
        label_resultat.config(text="Couleur invalide")
        return

    solution = tentative
    phase = 'guess'
    label_info.config(text="Joueur 2 : devinez la combinaison")
    label_resultat.config(text="Secret enregistré. Joueur 2, c'est à vous !")
    historique.insert(tk.END, "Secret défini. Joueur 2 commence.\n")
    reinitialiser_cases()
    btn_valider.config(text="Valider")


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
