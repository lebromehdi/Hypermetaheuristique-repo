#Mehdi Hannoteau
import utils



if __name__ == "__main__":
    
    input_file_name = "data4"
    output_file_name = "Groupe[5iG3]-Challenge1"
    
    ring_matrix, assignment_matrix, matrix_size = utils.readingInput(input_file_name)
    
    ring_size, ring, star, cost = utils.readingOutput(output_file_name, matrix_size)
    
    print("Check 1 - Taille du ring est bien celle écrite dans le fichier : ")    
    if (len(ring) == ring_size):
        print("OK\n")
    else :
        print("PROBLEM\n")
    
    print('Check 2 - Taille star est bien égale à "taille totale - taille du ring" : ')  
    if (len(star) == matrix_size-ring_size and len(star) == matrix_size-len(ring)):
        print("OK\n")
    else :
        print("PROBLEM\n")
    
    print("Check 3 - Coût écrit est bien celui obtenu depuis les arrêtes écrites dans .txt  : ")
    calculated_cost = 0
    for i in range(len(ring)):
        if i != len(ring)-1:
            calculated_cost += ring_matrix[ring[i]-1][ring[i+1]-1]
        else :
            calculated_cost += ring_matrix[ring[i]-1][ring[0]-1]
        
    for i in range(len(star)):
        calculated_cost += assignment_matrix[star[i][0]-1][star[i][1]-1]
    
    if (calculated_cost == cost):
        print("OK\n")
    else :
        print("PROBLEM\n")
        
    print("Check 4 - Entrepôt bien : ")
    isIn = False
    for i in range(len(ring)):
        if ring[i] ==1:
           isIn = True
           
    if (isIn == True):
        print("OK")
    else :
        print("PROBLEM")