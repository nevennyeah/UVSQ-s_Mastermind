import tkinter as tk
import random

COULEURS = ('yellow', 'blue', 'red', 'green', 'white', 'black', 'purple')

tentatives_max = 11
début = 0
partie_commencee = False
solution = None

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
btn_demarrer.pack(side=tk.LEFT)

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
    global tentatives_max, début, partie_commencee, solution
    try:
        tentatives_max = int(tentatives_var.get())
    except ValueError:
        label_resultat.config(text="Nombre de tentatives invalide")
        return

    début = 0
    solution = tuple(random.choice(COULEURS) for _ in range(4))
    partie_commencee = True
    historique.delete("1.0", tk.END)
    reinitialiser_cases()
    set_etat_controles(True)
    label_info.config(text=f"Partie lancée : {tentatives_max} tentatives")
    label_resultat.config(text="")


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
