#!/usr/bin/python3

import sys
from tkinter import *

def affichage(colonne, ligne, tab_info):
    fenetre = Tk()
    #recuperer les valeurs de chaque case
    res = tab_info[1].split(" ")
    res = [int(case) for case in res]

    x = 75 * colonne + 20
    y = 75 * ligne + 20

    canvas = Canvas(fenetre, width=x, height=y, background='white')
    y0 = 10
    for i in range(ligne):
        x0 = 10
        for j in range(colonne):
            noire = j + (colonne * i)
            if res[noire] > 0: #si la valeur est supérieur à 0 alors case noir
                case = canvas.create_rectangle(x0,y0,x0+75,y0+75, fill="black")
            else: #si la valeur est inferieure à 0 alors case blanche
                case = canvas.create_rectangle(x0,y0,x0+75,y0+75, fill="white")
            x0 = x0 + 75
        y0 = y0 + 75

    canvas.pack()

    fenetre.mainloop()

def solution():
    colonne = int(sys.argv[1])
    ligne = int(sys.argv[2])
    file = open(sys.argv[3], "r")
    info = file.read()
    tab_info = info.splitlines()
    file.close()
    affichage(colonne, ligne, tab_info)

if __name__ == "__main__":
    solution()