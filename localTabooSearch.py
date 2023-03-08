#Code de Yacin que j'ai légèrement modifié et dont je n'ai gardé que les
#parties qui m'intéressent
import math
import timeit
import utils
import random

def copy_list(liste : list):
    return [elem for elem in liste]

def add_star(ring : list, c_star, nb_vertices):
    star = []
    for i in range(1, nb_vertices+1):
        if i not in ring:
            j = 0
            minimum = math.inf
            for elem in ring:
                if c_star[i-1][elem-1] <= minimum : 
                    minimum = c_star[i-1][elem-1]
                    j = elem
            star.append([i,j])

    return star

def objective_function_ring(ring : list,c_ring, c_star):
    ring_size = len(ring)
    
    ring_cost = 0
    for i in range(ring_size-1):
        ring_cost += c_ring[ring[i]-1][ring[i+1]-1]
    ring_cost +=  c_ring[ring[-1]-1][ring[0]-1]

    return ring_cost 

def objective_function_star(star : list,c_ring, c_star):
    star_cost = 0   
    for elem in star:
        star_cost += c_star[elem[0]-1][elem[1]-1]
             
    return star_cost

def objective_function_global(ring : list, star : list,c_ring, c_star):
    return objective_function_ring(ring,c_ring, c_star) + objective_function_star(star,c_ring, c_star)


def particular_neighboorhood(ring, ring_size,nb_vertices):
    ring_temp = copy_list(ring)
    star_set = [elem for elem in range(2,nb_vertices+1) if elem not in ring_temp]
    x = random.choice(star_set)
    while True:
        index = random.randint(0, ring_size-1)
        if ring_temp[index] !=1 :
            ring_temp.pop(index)
            break

    ring_temp.insert(index, x)
    return ring_temp

def get_all_neighborhood_transposition(ring,ring_size, c_ring, c_star,nb_vertices):
    neighborhood = []
    for i in range(ring_size):
        for j in range(i+1,ring_size):
            ring_temp = [elem for elem in ring]
            temp = ring_temp[i]
            ring_temp[i] = ring_temp[j]
            ring_temp[j] = temp
            neighborhood.append([ring_temp, objective_function_global(ring_temp
                                            ,add_star(ring_temp, c_star,
                                            nb_vertices), c_ring, c_star),
                                            c_ring, c_star])
    
    neighborhood.sort(key=lambda x:x[1])
    return neighborhood

def local_search_tabou(starting_time, ring , ring_size,
                         input_file_name,time):

    c_ring, c_star, nb_vertices = utils.readingInput(input_file_name)
    TABOU = []
    tabou_size = 8
    best_ring = copy_list(ring)
    current_total_time = timeit.default_timer()-starting_time
    end_runtime = timeit.default_timer()-starting_time+time
    while(current_total_time < end_runtime):
        neighborhood = get_all_neighborhood_transposition(ring,ring_size,
                                                          c_ring,c_star,
                                                          nb_vertices)
        for neighbour in neighborhood:
            if neighbour[0] not in TABOU:
                star = add_star(neighbour[0], c_star,nb_vertices)
                star2 = add_star(best_ring, c_star,nb_vertices)
                if objective_function_global(neighbour[0],star,c_ring, c_star) <= objective_function_global(best_ring,star2,c_ring, c_star):
                    best_ring = copy_list(neighbour[0])
                    TABOU.append(best_ring)
                    if len(TABOU) > tabou_size:
                        TABOU.pop(0)
                    break
        else:
            break
        current_total_time = timeit.default_timer()-starting_time
        
    best_star = add_star(best_ring, c_star,nb_vertices)
    best_cost = objective_function_global(best_ring,best_star,c_ring, c_star)
    
    print(f"Local taboo search process finished {current_total_time} seconds " 
          +f"after the start with the following lowest cost : {best_cost}.")  
    
    return best_cost, best_ring, best_star

def local_search_tabou_classic(starting_time, max_runtime, ring , ring_size,
                         input_file_name):

    c_ring, c_star, nb_vertices = utils.readingInput(input_file_name)
    TABOU = []
    tabou_size = 8
    best_ring = copy_list(ring)
    current_total_time = timeit.default_timer()-starting_time
    while(current_total_time < max_runtime):
        neighborhood = get_all_neighborhood_transposition(ring,ring_size,
                                                          c_ring,c_star,
                                                          nb_vertices)
        for neighbour in neighborhood:
            if neighbour[0] not in TABOU:
                best_ring = copy_list(neighbour[0])
                TABOU.append(best_ring)
                if len(TABOU) > tabou_size:
                    TABOU.pop(0)
                break
        else:
            break
        current_total_time = timeit.default_timer()-starting_time
        
    best_star = add_star(best_ring, c_star,nb_vertices)
    best_cost = objective_function_global(best_ring,best_star,c_ring, c_star)
    
    print(f"Local classic (ring perms) search process finished {current_total_time} seconds" 
          +f" after the start with the following lowest cost : {best_cost}.")  
    
    return best_cost, best_ring, best_star

def local_search_ring_star_perm(starting_time, ring , ring_size,
                         input_file_name, time):

    c_ring, c_star, nb_vertices = utils.readingInput(input_file_name)

    best_ring = copy_list(ring)
    best_star = add_star(best_ring, c_star,nb_vertices)
    best_cost = objective_function_global(best_ring,best_star,c_ring, c_star)
    
    current_total_time = timeit.default_timer()-starting_time
    end_runtime = timeit.default_timer()-starting_time+time
    while(current_total_time < end_runtime):
        current_ring = particular_neighboorhood(ring, ring_size,nb_vertices)
        current_star = add_star(current_ring, c_star,nb_vertices)
        current_cost = objective_function_global(current_ring,current_star,c_ring, c_star)
        
        if current_cost < best_cost:
            best_ring = current_ring
            best_star = current_star
            best_cost = current_cost
        current_total_time = timeit.default_timer()-starting_time 
        
    print(f"Local classic (ring star perms) search process finished {current_total_time} seconds" 
          +f" after the start with the following lowest cost : {best_cost}.")  
    
    return best_cost, best_ring, best_star