#Mehdi Hannoteau
import timeit
import random
import math
import utils
import localTabooSearch as lts

def antSystemAlgorithm(starting_time,max_runtime, N, alpha, beta, Q, rho, 
                       input_file_name, output_file_name, ring_size,
                       best_L,best_ring,best_star, doLocalTabooSearch):
    #Les matrices de données (matrices de distances)
    ring_matrix = []
    assignment_matrix = []
    
    #Remplissage des matrices    
    ring_matrix, assignment_matrix, matrix_size = utils.readingInput(
        input_file_name)
    
    #Visiblité, matrice des distances où on remplace chaque valeur par son
    #inverse. Il y a donc deux matrices de visibilité.
    ring_visibility, assignment_visibility = utils.calculateVisibility(
    matrix_size,ring_matrix, assignment_matrix)
    
    #L'intensité définit l'attractivité d'une arrête entre deux villes. On
    #parle aussi de phéromones.
    ring_intensity = [[1]*matrix_size]*matrix_size
    
    #Liste d'endroits (nécessaire car rand.choices() ne renvoie pas d'index et
    #je n'ai pas la force de la recoder)
    places = []
    for i in range(matrix_size):
        places.append(i+1)
    
    #Préparation de la variable temporelle pour garantir que l'algorithme
    #tourne pendant max_runtime secondes.
    current_total_time = 0
    
    #Les meilleurs résultats issus la recherche locale si elle a lieu
    best_tmp = math.inf
    best_r = []
    best_s = []
        
    #Tant qu'on est pas au temps max ça tourne.
    while(current_total_time < max_runtime):
        #Phéromones laissées par toutes les fourmis sur l'itéré temporel
        ring_intensity_t = [[0]*matrix_size]*matrix_size
                        
        #Pour chaque fourmi
        for i in range(N):
            #Chemin de la fourmi
            ring = []
            star = []
            
            #Endroits déjà visités par la fourmi
            visited_places = [False]*matrix_size
                             
            #Choix obligatoire du premier point
            current_place = 1
            visited_places[0] = True
            ring.append(current_place)
            
            
            #Passage de la fourmi pour chaque endroit restant
            for j in range(ring_size-1): 
                
                #Calcul des poids
                weights = [] 
                for k in range(matrix_size):
                    if visited_places[k] == False :
                        #Pas besoin de diviser par la somme car cela est géré
                        #par random.choices(places, weights)
                        weight = (ring_intensity[current_place-1][k]**alpha)*(
                            ring_visibility[current_place-1][k]**beta)
                        weights.append(weight)
                    else :
                        weights.append(0)
                        
                #Choix aléatoire pondéré par les poids d'un endroit
                current_place = random.choices(places, weights)[0]
                #Endroit considéré comme visité
                visited_places[current_place-1] = True
                #Il est ajouté au chemin parcouru par la fourmi
                ring.append(current_place)
            
            #Calcul du coût du ring
            L = 0
            for j in range(len(ring)-1):
                L += ring_matrix[ring[j]-1][ring[j+1]-1]
            #Dernière arrête
            if len(ring) != 1:
                L += ring_matrix[ring[0]-1][ring[len(ring)-1]-1]
                
            #Calcul du coût du star    
            for j in range(matrix_size):
                if visited_places[j] == False :
                    dist = math.inf
                    for k in range(len(ring)):
                        if (dist > assignment_matrix[j][ring[k]-1]):
                            dist = assignment_matrix[j][ring[k]-1]
                            point = ring[k]
                    L += dist
                    star.append([j+1,point])

            #On ajoute les phéromones
            for j in range(len(ring)-1):
                ring_intensity[ring[j]-1][ring[j+1]-1] += Q/L
                ring_intensity[ring[j+1]-1][ring[j]-1] += Q/L
                ring_intensity_t[ring[j]-1][ring[j+1]-1] += Q/L
                ring_intensity_t[ring[j+1]-1][ring[j]-1] += Q/L
            #Dernière arrête
            ring_intensity[ring[0]-1][ring[len(ring)-1]-1] += Q/L
            ring_intensity[ring[len(ring)-1]-1][ring[0]-1] += Q/L
            ring_intensity_t[ring[0]-1][ring[len(ring)-1]-1] += Q/L
            ring_intensity_t[ring[len(ring)-1]-1][ring[0]-1] += Q/L

           
            #Conserver la meilleure solution
            if (L < best_L):
                best_L = L
                best_ring = ring
                best_star = star
                if doLocalTabooSearch == True :
                    tmp, r, s = lts.local_search_tabou(starting_time,best_ring,
                                            ring_size,input_file_name,10)
                    if (tmp < best_tmp):
                        best_tmp = tmp
                        best_r = r
                        best_s = s
        #Évaporation des phéromones
        for i in range(matrix_size):
            for j in range(matrix_size):
                ring_intensity[i][j] = (1-rho)*ring_intensity[i][j] 
                + ring_intensity_t[i][j]

        current_total_time = timeit.default_timer()-starting_time
    
    #On regarde si on a eu une meilleure solution par recherche tabou que par
    #l'algorithme des fourmis.
    if (best_tmp < best_L):
        best_L = best_tmp
        best_ring = best_r
        best_star = best_s
    
    #Affichage de la solution
    print(f"ACO process finished {current_total_time} seconds after the start " 
          +f"with the following lowest cost : {best_L}.")    
    
    return best_L,best_ring,best_star
