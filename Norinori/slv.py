#!/usr/bin/python3

import sys

from pysat.formula import CNF
from pysat.solvers import Solver

def sol(fichier, clauses):
    nom_fichier = fichier.split(".")
    resultat ="solution_" + nom_fichier[0]
    file = open(resultat, "w")

    #On crée une formule sous forme cnf avec nos clauses
    cnf = CNF(from_clauses=clauses)

    #Création d'un solveur pour notre problème:
    with Solver(bootstrap_with=cnf) as solver:
        if solver.solve(): #Si le solveur renvoie vraie alors c'est satisfiable
            file.write("SAT\n")
            res = solver.get_model()
            for case in res:
                file.write(str(case))
                if case != res[-1]:
                    file.write(" ")
        else:
            file.write("UNSAT")
        file.close()

def solveur():
    file = open(sys.argv[1], "r")
    info = file.read()
    tab_info = info.splitlines()
    file.close()

    #Comme il ne suit pas exactement le format Dimacs on prend seulement les clauses.
    clauses = []
    for tab in tab_info: 
        if tab[0] != 'c' and tab[0] != 'p':
            clause = tab.split(" ")
            clause = [int(case) for case in clause]
            del clause[-1]
            clauses.append(clause)
    sol(sys.argv[1], clauses)


if __name__ == "__main__":
    solveur()