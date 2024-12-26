#!/usr/bin/python3

import sys
from probleme import *
from slv import *
from interface import *

def main():
    #Partie problème
    nom_fichier = sys.argv[1]
    file = open(nom_fichier, "r")
    info = file.read()
    tab_info = info.splitlines()
    file.close()
    colonnes = int(tab_info[0])
    lignes = int(tab_info[1])
    probleme()
    
    #Partie generation avec solveur
    nom_solveur = nom_fichier + ".cnf"
    sys.argv[1] = nom_solveur
    solveur()
    
    #Partie affichage avec interface
    nom_affichage = "solution_" + nom_fichier
    sys.argv[1] = colonnes
    sys.argv.append(lignes)
    sys.argv.append(nom_affichage)
    solution()

if __name__ == "__main__":
    main()