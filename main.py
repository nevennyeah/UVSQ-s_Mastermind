import tkinter as tk
from PIL import Image, ImageTk
import pygame #pour pouvoir mettre de la musique, et ce uniquement sur le jeu. Sinon on avait une alternative avec playsound
import subprocess #pour pouvoir rouvrir les fichier une fois fermer. En créant des fenètres TkInter séparées
import sys #pour pouvoir fermer les fenetres TkInter séparées
import os
import random

fenetre = tk.Tk()
fenetre.title("Mastermind")
fenetre.geometry("1280x720")

image = Image.open("Media/Mastermind_menu1.png")
photo = ImageTk.PhotoImage(image)
background = tk.Label(fenetre, image=photo)
background.place(x=0, y=0, relwidth=1, relheight=1)

img = tk.PhotoImage(file="Media/bouton_quitter.png")
img2 = tk.PhotoImage(file="Media/bouton_1_joueur.png")
img3 = tk.PhotoImage(file="Media/bouton_2_joueur.png")
img4 = tk.PhotoImage(file="Media/parametre.png")

def fermer_fenetre():
    fenetre.destroy()

def un_joueur():
    subprocess.Popen([sys.executable, "mastermind_opti.py"])

def deux_joueurs():
    subprocess.Popen([sys.executable, "mastermind_opti_2P.py"])

# système de musique aléatoire
pygame.mixer.init() # on initialise l'audio de pygame

dossier_musiques = "Media/Musique"
# liste toutes les musiques mp3 présentes dans le dossier musique
musiques = [f for f in os.listdir(dossier_musiques) if f.endswith('.mp3')]
musique_actuelle = None

def jouer_musique_suivante():
    global musique_actuelle
    # filtre l'ancienne musique pour ne pas la jouer 2 fois de suite
    musiques_dispo = [m for m in musiques if m != musique_actuelle]
    musique_actuelle = random.choice(musiques_dispo)
    chemin_musique = os.path.join(dossier_musiques, musique_actuelle)
    pygame.mixer.music.load(chemin_musique)
    pygame.mixer.music.play()

def verifier_fin_musique():
    # .get_busy() renvoie False si la musique est terminée
    if not pygame.mixer.music.get_busy():
        jouer_musique_suivante()
    # rappelle la fonction toutes les 5000 millisecondes
    fenetre.after(5000, verifier_fin_musique)

# démarrage de la première musique et de la boucle de vérification
if musiques:
    jouer_musique_suivante()
    verifier_fin_musique()

def changer_volume(val):
    # Pygame prend une valeur entre 0.0 et 1.0, on divise donc la valeur du slider par 100
    volume = float(val) / 100
    pygame.mixer.music.set_volume(volume)
#

for i in range(10):
    fenetre.grid_rowconfigure(i, weight=1)
    fenetre.grid_columnconfigure(i, weight=1)

button_fermer = tk.Button(fenetre, image=img, command=fermer_fenetre)
button_fermer.grid(row=9, column=9, padx=1, pady=1)

button_un_joueur = tk.Button(fenetre, image=img2, command=un_joueur)
button_un_joueur.grid(row=5, column=0, padx=1, pady=1)

button_deux_joueur = tk.Button(fenetre, image=img3, command=deux_joueurs)
button_deux_joueur.grid(row=6, column=0, padx=1, pady=1)

button_skip = tk.Button(fenetre, text="Passer à la prochaine musique ⏭", command=jouer_musique_suivante)
button_skip.grid(row=9, column=1, padx=1, pady=10) # Placé juste au-dessus du slider de volume

slider_volume = tk.Scale(fenetre, from_=0, to=100, orient=tk.HORIZONTAL, 
                         command=changer_volume, label="Volume", length=150)
slider_volume.set(15) # On définit le volume initial à 30%
slider_volume.grid(row=9, column=0, padx=1, pady=1) # Placé en bas à droite, juste au-dessus du bouton quitter

fenetre.mainloop()
pygame.mixer.music.stop() # arret de la musique lors de la fermeture de la fenetre