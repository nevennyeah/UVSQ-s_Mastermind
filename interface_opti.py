import tkinter as tk
from PIL import Image, ImageTk

fenetre = tk.Tk()
fenetre.title("Mastermind")
fenetre.geometry("1280x720")
image = Image.open("Mastermind_menu1.png")
photo = ImageTk.PhotoImage(image)
background = tk.Label(fenetre, image=photo)
background.place(x=0, y=0, relwidth=1, relheight=1)
img = tk.PhotoImage(file = "bouton quitter.png")
img2 = tk.PhotoImage(file = "bouton_1_joueur.png")
def fermer_fenetre():
    fenetre.destroy()
def un_joueur():
    import mastermind_opti
for i in range(10):
    fenetre.grid_rowconfigure(i, weight=1)
    fenetre.grid_columnconfigure(i, weight=1)
button_fermer = tk.Button(fenetre, image = img,  command = fermer_fenetre)
button_fermer.grid(row = 10, column = 10, padx = 1, pady = 1)
button_un_joueur = tk.Button(fenetre, image = img2, command = un_joueur)
button_un_joueur.grid(row = 6, column = 2, padx = 1, pady = 1)
fenetre.mainloop()