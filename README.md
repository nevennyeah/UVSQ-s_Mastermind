# UVSQ-s_Mastermind

## Français 🇫🇷

### Liste des élèves qui ont travailé sur le projet

Projet du Mastermind pour l'UVSQ (IN200N) / _MITD03_
- HERVÉ Neven
- FURTER Raphaël
- BOURAS Tarek
- MOHAMED SAID ALLAOUI Mohamed

### Pré-requis

Afin de faire fonctionner le Mastermind et son code principal, il y a besoin de plusieurs dépendances.
- TKinter ([Lien](https://docs.python.org/3/library/tkinter.html), normalement déjà présent sur votre machine, distribué avec l'installateur Python)
- Pillow ([Lien](https://pypi.org/project/pillow/))
- Pygame ([Lien](https://pypi.org/project/pygame/))

### C'est quoi le MasterMind ?

C'est :
- 11 tours pour trouver la solution
- 7 couleurs
- Un mode ordinateur
- Un mode 2 joueurs (codificateur et décodeur)

### Comment fonctionne le jeu

À chaque essai, le joueur qui décode acquiert l’information suivante :
- Le nombre de pions bien placés (mais il ne sait pas lesquels).
    - un pion est bien placé s’il a la même couleur que le pion qui est à la même position dans le code secret.
- Le nombre de pions mal placés.
    - Un pion est mal placé s’il a la même couleur qu’un pion du code secret qui n’est pas à une position d’un pion bien placé.

- De plus chaque pion du code secret peut compter pour au plus un pion mal placé

Cette information peut être matérialisée par deux nombres accolés au code essayé ou bien, comme sur le jeu de plateau, par des petits pions dont le nombre indique en rouge (resp. en blanc) le nombre de pions bien (resp. mal) placés.

- Si le joueur qui décode trouve le code secret en 11 essais ou moins, il gagne. Sinon, c’est son adversaire qui gagne.

### Anecdotes

La variante du jeu avec 4 pions et 6 couleurs permet 6⁴ = 1 296 combinaisons ; celle avec 5 pions et 8 couleurs 8⁵ = 32 768 combinaisons.

Inventé par Mordecai Meirowitz, expert en télécommunications israëlien, dans les années 1970, le jeu se base sur un jeu plus ancien : bulls and cows (taureaux et vaches) qui se jouait avec papier et crayon et des nombres au lieu de couleurs.

## English 🇬🇧

### List of students who worked on the project

Mastermind Project for the UVSQ (IN200N) / _MITD03_
- HERVÉ Neven
- FURTER Raphaël
- BOURAS Tarek
- MOHAMED SAID ALLAOUI Mohamed

### Prerequisites

To run Mastermind and its source code, the following dependencies are required:
- TKinter ([Link](https://docs.python.org/3/library/tkinter.html), Usually pre-installed with Python)
- Pillow ([Link](https://pypi.org/project/pillow/))
- Pygame ([Link](https://pypi.org/project/pygame/))

### What's the Mastermind ?

It's :
- 11 rounds to find the solution.
- 7 colors available.
- VS. computer mode
- 2 player local mode (codebreaker & codemaker)

### How does the game work ?

With each attempt, the Codebreaker receives the following information:
- The number of pawn well placed (but he doesn't know which one).
    - A pawn is well placed when he has the same color of the pawn in the same position in the solution
- The number of pawn wrongly placed (still doesn't know which one).
    - A pawn is wrongly placed if he doesn't have the same color of the pawn in the same position in the solution.

- Moreover, every pawn of the solution can count for only one wrongly placed pawn.

This information can be materialized by 2 numbers placed next to the attempt or, like the board game, by little pawns where the number of red little pawns represents the number of well placed pawns. The same goes for the white little pawns, except it represents the wrongly placed pawns.

- If the codebreaker find the answer in 11 attempts or less, he wins. Else, the codemaker wins.

### Fun Facts

The variation of the game with 4 pawns and 6 colors make space for 6⁴ = 1 296 combinaisons ; the one with 5 pawns and 8 colors 8⁵ = 32 768 combinaisons.

The Mastermind was created by Mordeacai Meirowitz, an Israeli post and telecommunications expert in the 70s. The original game take inspiration on an older game : bulls and cows, which was played with paper and pencils, and numbers as the role of colors.