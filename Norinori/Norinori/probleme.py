#!/usr/bin/python3

import sys
from clauses import *

def format_Dimacs(nom_fichier, clauses, nb_cases):
    nom_fichier = nom_fichier + ".cnf"
    fichier = open(nom_fichier, "w")
    fichier.write("c Projet Norinori\n")
    fichier.write("p cnf " + str(len(clauses)) + " " + str(nb_cases) + "\nc\nc\n")
    for clause in clauses:
        i = 0
        while i != len(clause):
            fichier.write(str(clause[i]))
            i = i + 1
            if (i < len(clause)):
                fichier.write(" ")
        fichier.write(" 0\n")
    fichier.close()

def bonne_region(region, coord):
    for case in region:
        i = 0
        for voisin in region:
            if case != voisin and est_voisin(coord[case], coord[voisin]):
                i = i + 1
        if i == 0:
            return False
    return True

def coordo_tab(regions, lignes, colonnes):
    #On associe une case à des coordonnée
    coord = {}
    tab = []
    for i in range(0, (lignes*colonnes)):
        tab.append([i//(colonnes), i%colonnes])
    for t in regions:
        for i in t:
            coord[i] = tab[int(i)-1]
    return coord

def probleme():
    file = open(sys.argv[1], "r")
    info = file.read()
    tab_info = info.splitlines()
    file.close()
    colonnes = int(tab_info[0])
    lignes = int(tab_info[1])
    nb_regions = int(tab_info[2])

    if colonnes < 3 and lignes < 3 and nb_regions < 2:
        file.close()
        exit(-1)
    if len(tab_info) < 3 + nb_regions:
        print("erreur")
        file.close()
        exit(-1)

    regions = tab_info[3:]
    nb_case = 0
    for i in range(0, len(regions)):
        regions[i] = regions[i].split(" ")
        nb_case = nb_case + len(regions[i])
    if nb_case != colonnes * lignes:
        print("Le nombre de case dans les régions est diffèrent du nombre de case calculé avec les lignes et colonnes")

    coord = coordo_tab(regions, lignes, colonnes)
    for region in regions:
        if not bonne_region(region, coord):
            print("Une region a un problème, toute les cases ne se touchent pas")
            file.close()
            exit(-1)
    clauses = deux_case_noires_par_regions(regions)
    voisin = un_voisin_case_noir_par_case_noir(coord)
    clauses = clauses + voisin
    format_Dimacs(sys.argv[1], clauses, nb_case)

if __name__ == "__main__":
    probleme()