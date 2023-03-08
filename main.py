#Mehdi Hannoteau
import math
import utils
import timeit
import recuit
import fourmis
import localTabooSearch as lts
      
if __name__ == "__main__":
    """
    Paramètres pour fourmis
    ----------
    input_file_name : string
        Nom du fichier de lecture sans le ".txt".
    output_file_name : string
        Nom du fichier d'écriture sans le ".txt".
    max_runtime : int
        Nombre de secondes au-delà de laquelle l'exécution doit s'arrêter.
    N : int
        Nombre de fourmis qui passent avant évaporation. Max 2000 pour ne pas
        trop dépasser sur le runtime max. C'est le seul paramètre sur lequel
        nous allons jouer pour l'examen. Plus il y a de fourmis qui passent et
        plus la quantité de phéromones laissées par itéré t est grande. En
        fonction des problèmes, on veut plus ou moins de phéromones. 
    alpha : int
        Positif non nul fixé à 7.
        Importance des phéromones dans le choix du chemin.
        Augmenter = intensification
        Diminuer = diversification
    beta : int
        Positif non nul fixé à 7.
        Importance de la visibilité (qui  est comprise entre 0 et 1) dans le
        choix du chemin.
        Augmenter = intensification
        Diminuer = diversification
    Q : int
        Positif non nul fixé à 100.
        Poids des phéromones déposées.         
        Augmenter = intensification
        Diminuer = diversification
    rho : float
        Compris entre 0 et 1 fixé à 0.3.
        Intensité de l'évaporation des phéromones.
        Augmenter = diversification
        Diminuer = intensification
           
    """
    #Préparation de la variable temporelle pour garantir que l'algorithme
    #tourne pendant max_runtime secondes.
    starting_time = timeit.default_timer()
    
    #Les jeux de paramètres : (N[i],alpha[i],beta[i],Q[i],rho[i])
    
    input_file_name = "challenge2"
    
    output_file_name = "Groupe[5iG3]-Challenge1"
    max_runtime = 840
    N = [2000,20,1000,1000,100]
    alpha = [1,7,1,5,7]
    beta = [7,7,10,10,7]
    Q = [100,100,100,100,100]
    rho = [0,0.3,0,0,0.3]
    
    #Codage de la solution
    best_L = math.inf
    best_ring = []
    best_star = []
    
        
    print("PHASE 1 : ANALYSIS OF THE PROBLEM")
    best_L_r = math.inf
    best_ring_r = []
    best_s_r = []
    ring_size = 1
    goForAnts = True
    
    #On utilise le recuit de Merouane pour trouver le meilleur ring size et on
    #garde aussi sa meilleure solution.
    #tc, iterations, alpha, temps, fichier d'entrée
    for i in range(4) :
        tmp, r, s, ri = recuit.recuit(1000,10,0.99,0.5,input_file_name,
                                      starting_time)
        if tmp < best_L_r :
            best_L_r = tmp
            best_ring_r = r
            best_s_r = s
            ring_size = ri
            
    
    #Indice du meilleur jeu de paramètres
    best_i = 0   
    #On lance plusieurs algos fourmis pendant 20s avec différents paramètres
    #pour trouver le meilleur jeu de paramètres.
    for i in range(len(N)):
        tmp_max_runtime = timeit.default_timer()-starting_time+20
        tmp, r, s = fourmis.antSystemAlgorithm(starting_time,
                            tmp_max_runtime,N[i], alpha[i], beta[i], Q[i],
                            rho[i],input_file_name,output_file_name,
                            ring_size,math.inf,[],[],False)
        if tmp <= best_L:
            best_L = tmp
            best_ring = r
            best_star = s
            best_i = i           
    
    if best_L_r < best_L:
        best_L = best_L_r
        best_ring = best_ring_r
        best_star = best_s_r
        goForAnts = False
    print("")
    
    print("PHASE 2 : BEST SOLUTION WITH ACO AND TABOU LOCAL SEARCH")
    #On lance plusieurs algos fourmis pendant 20s avec différents paramètres
    #pour trouver le meilleur jeu de paramètres.
    if goForAnts == True:
        for j in range(2):    
            for i in range(len(N)):
                tmp_max_runtime = timeit.default_timer()-starting_time+20
                tmp, r, s = fourmis.antSystemAlgorithm(starting_time,
                                    tmp_max_runtime,N[i], alpha[i], beta[i], Q[i],
                                    rho[i],input_file_name,output_file_name,
                                    ring_size,math.inf,[],[],False)
                if tmp <= best_L:
                    best_L = tmp
                    best_ring = r
                    best_star = s
                    best_i = i
        for i in range(10):
            tmp_max_runtime = timeit.default_timer()-starting_time+30
            tmp, r, s = fourmis.antSystemAlgorithm(starting_time
                           ,tmp_max_runtime, N[best_i], alpha[best_i], beta[best_i]
                           ,Q[best_i],rho[best_i],input_file_name, output_file_name
                           ,ring_size,math.inf,[],[],True)
            if tmp < best_L :
                best_L = tmp
                best_ring = r
                best_star = s
            #Dernière recherche tabou sur la meilleure solution du for[i]
            tmp, r, s = lts.local_search_tabou(starting_time,r,
                                    ring_size,input_file_name,30)
            if tmp < best_L :
                best_L = tmp
                best_ring = r
                best_star = s
    print("")
    
    print("PHASE 2 BIS : BEST SOLUTION WITH SA AND TABOU LOCAL SEARCH")
    #Appel de l'algorithme recuit avec choix des paramètres

    t0 = [1000,1000,1000,1000]
    step = [10,10,1,1]
    alpha = [0.99,0.998,0.99,0.998]
    time = [0.5,0.5,2,2]
    best_i = 0

    if goForAnts == False:
        for i in range(4):
            tmp, r, s, ri = recuit.recuit(t0[i],step[i],alpha[i],time[i],input_file_name,
                                          starting_time)
            if tmp < best_L_r:
                best_L_r = tmp
                best_ring_r = r
                best_star_r = s
                ring_size_r = ri
                best_i = i
 
            #Dernière recherche tabou sur la meilleure solution du for[i]
            tmp, r, s = lts.local_search_tabou(starting_time,r,
                                    ri,input_file_name,30)
            if tmp < best_L :
                best_L = tmp
                best_ring = r
                best_star = s

        if best_L_r < best_L:
            best_L = best_L_r
            best_ring = best_ring_r
            best_star = best_star_r
            ring_size = ring_size_r

        tmp, r, s, ri = recuit.recuit(t0[best_i],step[best_i],alpha[best_i],3,input_file_name,
                                            starting_time)
        if tmp < best_L :
            best_L = tmp
            best_ring = r
            best_star = s
            ring_size = ri

        tmp, r, s = lts.local_search_tabou(starting_time,r,
                                        ri,input_file_name,30)
        if tmp < best_L :
            best_L = tmp
            best_ring = r
            best_star = s   
    print("")

    print("PHASE 3 : LOCAL SEARCH OF THE BEST SOLUTION")
    #Écriture de la solution
    if goForAnts == False:
        if len(best_star) != 0:
            tmp, r, s = lts.local_search_ring_star_perm(starting_time, best_ring,
                                     ring_size, input_file_name,120)
            if tmp <= best_L:
                best_L = tmp
                best_ring = r
                best_star = s
    else:
        tmp, r, s = lts.local_search_tabou_classic(starting_time, max_runtime, 
                                 best_ring,ring_size, input_file_name)
        if tmp <= best_L:
            best_L = tmp
            best_ring = r
            best_star = s
    
    utils.writing(best_L,best_ring,best_star,output_file_name)
    print(f"Complete process finished {timeit.default_timer()-starting_time} "
          +f"seconds after the start with the following lowest cost : {best_L}"
          +".")   
