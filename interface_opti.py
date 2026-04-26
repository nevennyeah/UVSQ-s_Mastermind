import tkinter as tk
from PIL import Image, ImageTk
import pygame #pour pouvoir mettre de la musique, et ce uniquement sur le jeu. Sinon on avait une alternative avec playsound

fenetre = tk.Tk()
fenetre.title("Mastermind")
fenetre.geometry("1280x720")
image = Image.open("Mastermind_menu1.png")
photo = ImageTk.PhotoImage(image)
background = tk.Label(fenetre, image=photo)
background.place(x=0, y=0, relwidth=1, relheight=1)
img = tk.PhotoImage(file = "bouton quitter.png")
img2 = tk.PhotoImage(file = "bouton_1_joueur.png")
img3 = tk.PhotoImage(file = "bouton_2_joueur.png")
img4 = tk.PhotoImage(file = "parametres.png")
def fermer_fenetre():
    fenetre.destroy()
def un_joueur():
    import finalmastermind_v2
def deux_joueurs():
    ...
def parametres():
    import parametres.py
for i in range(10):
    fenetre.grid_rowconfigure(i, weight=1)
    fenetre.grid_columnconfigure(i, weight=1)
button_fermer = tk.Button(fenetre, image = img,  command = fermer_fenetre)
button_fermer.grid(row = 9, column = 9, padx = 1, pady = 1)
button_un_joueur = tk.Button(fenetre, image = img2, command = un_joueur)
button_un_joueur.grid(row = 5, column = 0, padx = 1, pady = 1)
button_deux_joueur = tk.Button(fenetre, image = img3, command = deux_joueurs)
button_deux_joueur.grid(row = 6, column = 0, padx = 1, pady = 1)
button_parametres = tk.Button(fenetre, image = img4, command = parametres)
button_parametres.grid(row = 9, column = 0, padx = 1, pady = 1)
pygame.mixer.init() #on initialise l'audio de pygame
pygame.mixer.music.load("Come on! — Retro 8-Bit Arcade Music.mp3")
pygame.mixer.music.play(-1) #on initialise pygame en boucle infinie
fenetre.mainloop()
pygame.mixer.music.stop() #arret de la musique lors de la fermeture de la fenetre
