# UVSQ-s_Mastermind

## Liste d'élèves

Projet du Mastermind pour l'UVSQ (IN200N) / _MITD03_
- HERVÉ Neven
- FURTER Raphaël
- BOURAS Tarek
- MOHAMED SAID ALLAOUI Mohamed

## C'est quoi le MasterMind ?

C'est :
- 11 tours pour trouver la solution
- 7 couleurs
- Un mode ordinateur
- Un mode 2 joueurs (codificateur et décodeur)

## Comment fonctionne le jeu

À chaque essai, le joueur qui décode acquiert l’information suivante :
- Le nombre de pions bien placés (mais il ne sait pas lesquels).
    - un pion est bien placé s’il a la même couleur que le pion qui est à la même position dans le code secret.
- Le nombre de pions mal placés.
    - Un pion est mal placé s’il a la même couleur qu’un pion du code secret qui n’est pas à une position d’un pion bien placé.

- De plus chaque pion du code secret peut compter pour au plus un pion mal placé

Cette information peut être matérialisée par deux nombres accolés au code essayé ou bien, comme sur le jeu de plateau, par des petits pions dont le nombre indique en rouge (resp. en blanc) le nombre de pions bien (resp. mal) placés.

- Si le joueur qui décode trouve le code secret en 11 essais ou moins, il gagne. Sinon, c’est son adversaire qui gagne.

## Anecdotes

La variante du jeu avec 4 pions et 6 couleurs permet 6⁴ = 1 296 combinaisons ; celle avec 5 pions et 8 couleurs 8⁵ = 32 768 combinaisons.

Inventé par Mordecai Meirowitz, expert en télécommunications israëlien, dans les années 1970, le jeu se base sur un jeu plus ancien : bulls and cows (taureaux et vaches) qui se jouait avec papier et crayon et des nombres au lieu de couleurs.