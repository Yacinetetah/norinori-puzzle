#!/usr/bin/python3



def est_voisin(coord1, coord2):
    x = coord1[0] - coord2[0]
    y = coord1[1] - coord2[1]
    if x == 1 and y == 0:
        return True
    elif x == -1 and y == 0:
        return True
    elif x == 0 and y == 1:
        return True
    elif x == 0 and y == -1:
        return True
    else:
        return False


def negatif(clauses):
    #On rend les clauses en negatif dans le cas de la contrainte des au plus 2 cases noires
    for i in range(len(clauses)):
        if (len(clauses[i]) > 2): #si on a plus que deux cases dans la regions alors on rend tout ça en négatif pour garder le sens de la contrainte correcte
            for j in range(len(clauses[i])):
                clauses[i][j] = "-" + clauses[i][j]
    return clauses

def clause_voisin(case, voisins):
    if len(voisins) > 2: #calcul du nombre de clause
        nb_clause = 3 * (len(voisins)-2)
    else:
        nb_clause = 1
    clauses = []
    for i in range(nb_clause): #pour toute les clause on ajoute la case actuel
        tab = []
        tab.append(case)
        clauses.append(tab)
    nb_fois = len(voisins) - 1 #un voisin est dans nb_fois de clause
    for voisin in voisins:
        i = 0
        while i != nb_fois:
            for clause in clauses:
                ajout = True
                if len(clause) == 3: #si la clause est complète on ajoute pas le voisin
                    ajout = False
                if len(clause) == 2: #si il reste une place pour la close alors
                    cp = clause.copy()
                    cp.append(voisin)
                    if cp in clauses: #on regarde si elle existe déjà, si c'est le cas on l'ajoute pas
                        ajout = False
                if len(clause) == 1: #s'il n'y a que le case actuelle on ajoute le voisin
                    ajout = True
                if ajout == True and i < nb_fois:
                    i = i + 1
                    clause.append(voisin)
    #on crée la clause ou on au moins 1 voisin ou que la case actuelle n'est pas une case noir
    voisins.append("-" + case)
    #on transforme les clauses pour les rendre conforme a ce que l'on veut
    # [-x, -y, -z] ou il faut que soit x soit une case normal ou bien que y ou z soit une case noir
    clauses = negatif(clauses)
    clauses.append(voisins)
    return clauses

def un_voisin_case_noir_par_case_noir(coord):
    #On va regarder pour chaque case leurs coordonnées et trouver leurs voisins
    #ensuite on va crée les clauses pour dire que si on est une case noir
    #alors on a un unique voisin case noire.
    clause = []
    for case in coord:
        voisins = []
        for voisin in coord:
            if est_voisin(coord[case], coord[voisin]):
                voisins.append(voisin)
        clause = clause + clause_voisin(case, voisins)
    return clause


def au_moins_deux_case(region):
    #On va prendre n-1 element de la région pour voir s'il y a au moins deux cases noires
    #On décale de 1 a chaque fois par exemple notre région à [1,2,3,4] On va d'abord avoir
    # [1,2,3] puis [2,3,4] puis [3,4,1] et [4,1,2] donc on a tout les groupes de clauses
    #ou il manque un élèment a chaque fois, si une clauses n'est pas bonne alors on n'a
    #pas assez de cases noires
    l = len(region)
    t = []
    for i in range(l):
        tab = []
        for j in range(i, i+l-1): # On décales de 1 pour commencer à une nouvelle variable 
            tab.append(region[j % l]) #on veut les elements de la region donc si on dépasse le nombre de région au fait le modulo
        t.append(tab)
    return t

#def nb_fois_apparition(region, n):
#    if len(region) == 2:
#        return n
#    else:
#        cp = region.copy(region)
#        del region[0]
#        return n + nb_fois_apparition(region, n+1)

def au_plus_deux_case(region):
    #On va faire tout les groupe de 3 variables possible pour voir si on a plus de 3 cases noires dans la région
    #si la clause est bonne alors on a moins de 3 cases noires dans la région.
    if len(region) == 2 or len(region) == 3: #si on a 2 ou 3 cases par région on a pas besoin de chercher tout les couples et on renvoie la region
        return [region]
    nb_clauses = 1 +  pow(3, len(region)-3) #Pour savoir combien de clauses possible on a dans une region en fonction du nombre de cases
    nb_fois = nb_clauses/2 +1 #une cases apparait un certain nombre de fois
    tab = []
    for i in range(nb_clauses):
        tab.append([])
    for x in region:
        #le dictionnaire autre_case nous dit combien de fois on a associé notre case actuelle à une autre case
        #étant donné qu'on veut faire tout les clauses on doit avoir le même nombre d'apparition pour chaque case.
        autre_case = {}
        for y in region:
            if x != y:
                autre_case[y] = 0
        i = 0
        while (i != nb_fois):
            #On va regarder dans toute les clauses qu'on a crée si on doit ajouter notre case ou pas
            for clause in tab:
                ajout = True
                #Si on a déjà 3 cases alors on doit pas ajouter notre case dans cette clause
                if len(clause) == 3:
                    ajout = False
                #Si on a déjà 2 cases alors on regarde si on a déjà un clause qui contient ces deux cases + notre case actuel
                #si c'est le cas on l'ajoute pas sinon on va l'ajouter
                if len(clause) == 2:

                    if x in clause:
                        ajout = False
                    else:
                        cp = clause.copy()
                        cp.append(x)
                        if cp in tab:
                            ajout = False
                #Si on a qu'une case dans notre clause on regarde si c'est pas notre case actuelle pour eviter les doublons
                if len(clause) == 1:
                    if clause[0] == x:
                        ajout = False
                    else: #si c'est pas la même case on regarde si on a pas déjà associé notre case avec le maximum qu'on puisse associé a une autre
                        if autre_case[clause[0]] >= nb_fois/2:
                            ajout = False
                #Si la clause ne contient rien alors on peut l'ajouter
                if len(clause) == 0:
                    ajout = True
                #Si on peut ajouter notre case on regarde toute les autres variable et on incremente le nombre de fois
                # que on les a rencontrer dans la clause ou on les ajouter
                if ajout == True and i < nb_fois:
                    for var in clause:
                        autre_case[var] = autre_case[var] + 1
                    clause.append(x)
                    i = i + 1
    return tab

def deux_case_noires_par_regions(regions):
    #On a la règle d'avoir uniquement deux cases noires dans une région
    #On va la traduire par :
        #- au moins deux cases noires
        #- au plus deux cases noires
    clauses = []
    for r in regions:
        clauses = clauses + au_moins_deux_case(r)
        a_modif = au_plus_deux_case(r)
        if not (len(a_modif) == 1 and len(a_modif[0]) < 3):
            clauses = clauses + negatif(a_modif)
    return clauses