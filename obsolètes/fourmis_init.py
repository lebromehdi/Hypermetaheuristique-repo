#Mehdi Hannoteau
import timeit
import random
import math
import utils

def modifiedAntSystemAlgorithm(N, alpha, beta, Q, rho, input_file_name, 
                               ant_passages, starting_time):
    #Les matrices de données (matrices de distances)
    ring_matrix = []
    assignment_matrix = []
    
    #Remplissage des matrices    
    ring_matrix, assignment_matrix, matrix_size = utils.readingInput(input_file_name)
    
    #Visiblité, matrice des distances où on remplace chaque valeur par son
    #inverse. Il y a donc deux matrices de visibilité.
    ring_visibility, assignment_visibility = utils.calculateVisibility(
    matrix_size,ring_matrix, assignment_matrix)
    
       
    #Liste d'endroits (nécessaire car rand.choices() ne renvoie pas d'index et
    #je n'ai pas la force de la recoder)
    places = []
    for i in range(matrix_size):
        places.append(i)
    
    #Meilleure score
    best_L = math.inf
    best_ring = []
    
    #Pour chaque taille de ring.
    for r in range(3,matrix_size):
        #L'intensité définit l'attractivité d'une arrête entre deux villes. On
        #parle aussi de phéromones.
        ring_intensity = [[1]*matrix_size]*matrix_size
        
        #Les fourmis passent p fois
        for p in range(ant_passages):
            #Phéromones laissées par toutes les fourmis sur l'itéré du while
            ring_intensity_t = [[0]*matrix_size]*matrix_size
                            
            #Pour chaque fourmi
            for i in range(N):
                #Chemin de la fourmi
                ring = []
                star = []
                
                #Endroits déjà visités par la fourmi
                visited_places = [False]*matrix_size
                                 
                #Choix obligatoire du premier point
                current_place = 0
                visited_places[current_place] = True
                ring.append(current_place)
                
                
                #Passage de la fourmi pour chaque endroit restant
                for j in range(r): 
                    
                    #Calcul des poids
                    weights = [] 
                    for k in range(matrix_size):
                        if visited_places[k] == False :
                            #Pas besoin de diviser par la somme car cela est géré
                            #par random.choices(places, weights)
                            weight = (ring_intensity[current_place][k]**alpha)*(
                                ring_visibility[current_place][k]**beta)
                            weights.append(weight)
                        else :
                            weights.append(0)
                            
                    #Choix aléatoire pondéré par les poids d'un endroit
                    current_place = random.choices(places, weights)[0]
                    #Endroit considéré comme visité
                    visited_places[current_place] = True
                    #Il est ajouté au chemin parcouru par la fourmi
                    ring.append(current_place)
                
                #Calcul du coût du ring
                L = 0
                for j in range(len(ring)-1):
                    L += ring_matrix[ring[j]][ring[j+1]]
                    
                L += ring_matrix[ring[0]][ring[len(ring)-1]]
                    
                #Calcul du coût du star    
                for j in range(matrix_size):
                    if visited_places[j] == False :
                        dist = math.inf
                        for k in range(len(ring)-1):
                            if (dist > assignment_matrix[j][ring[k]]):
                                dist = assignment_matrix[j][ring[k]]
                                point = ring[k]
                        L += dist
                        star.append([j,point])
    
                #On ajoute les phéromones
                for j in range(len(ring)-1):
                    ring_intensity[ring[j]][ring[j+1]] += Q/L
                    ring_intensity[ring[j+1]][ring[j]] += Q/L
                    ring_intensity_t[ring[j]][ring[j+1]] += Q/L
                    ring_intensity_t[ring[j+1]][ring[j]] += Q/L
                ring_intensity[ring[0]][ring[len(ring)-1]] += Q/L
                ring_intensity[ring[len(ring)-1]][ring[0]] += Q/L
               
                #Conserver la meilleure solution
                if (L < best_L):
                    best_L = L
                    best_ring = ring  
                    
            #Évaporation des phéromones
            for i in range(matrix_size):
                for j in range(matrix_size):
                    ring_intensity[i][j] = (1-rho)*ring_intensity[i][j] 
                    + ring_intensity_t[i][j]
    
                    
    print(f"ACO_init process finished {timeit.default_timer()-starting_time} "
          +"seconds after start with the following best ring size: "
          +f"{len(best_ring)-1}.") 
    return len(best_ring)-1
