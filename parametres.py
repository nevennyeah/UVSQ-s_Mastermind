import tkinter as tk

def sauvegarder():
    tentatives = spin_tentatives.get()
    f_output = open("Sauvegarde/config.csv", "w")
    f_output.write("Parametre,Valeur\n")
    f_output.write("Tentatives," + str(tentatives))
    f_output.close()
    label_status.config(text="Sauvegardé !")

root = tk.Tk()
root.title("paramètres")
root.geometry("300x200")

label_info = tk.Label(root, text="Nombre de tentatives :")
label_info.pack(pady=10)
spin_tentatives = tk.Spinbox(root, from_=1, to=20)
spin_tentatives.delete(0, tk.END)
spin_tentatives.insert(0, "11")
spin_tentatives.pack()

try:
    f_input = open("Sauvegarde/config.csv", "r")
    f_input.readline()
    ligne = f_input.readline()
    
    if ligne != "":
        donnees = ligne.strip().split(',')
        valeur_tentatives = donnees[1]
        spin_tentatives.delete(0, tk.END)
        spin_tentatives.insert(0, valeur_tentatives)
        
    f_input.close()
except FileNotFoundError:
    pass

btn_save = tk.Button(root, text="Sauvegarder", command=sauvegarder)
btn_save.pack(pady=10)

label_status = tk.Label(root, text="")
label_status.pack()

root.mainloop()
