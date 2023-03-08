#Mehdi Hannoteau
def calculateVisibility(matrix_size,ring_matrix, assignment_matrix):
    mat1 = []
    mat2 = []
    
    for i in range(2*matrix_size):
        tmp = []
        for j in range(matrix_size):
            if (i < matrix_size):
                if (i != j):                 
                    tmp.append(1/ring_matrix[i][j])
                if (i == j):
                    tmp.append(0)
            else :
                if (i-matrix_size != j):
                    tmp.append(1/assignment_matrix[i-matrix_size][j])
                if (i-matrix_size == j):
                    tmp.append(0)
                    
        if (i < matrix_size):
            mat1.append(tmp)
        else :
            mat2.append(tmp)
    
    return mat1,mat2


def readingInput(file_name):
    mat1 = []
    mat2 = []
    with open(file_name+".txt") as f:        
        N = int(f.readline())
        for i in range(2*N):
            tmp = f.readline().split(" ")
            del tmp[0] #Enlever le caractère espace
            tmp[len(tmp)-1] = tmp[len(tmp)-1][:-1] #Enlever le \n
            for j in range(len(tmp)): #Cast en int
                tmp[j] = int(tmp[j])
            
            if (i < N):
                mat1.append(tmp)
            else :
                mat2.append(tmp)
                
        return mat1,mat2,N
    

def writing(best_L, best_ring, best_star, output_file_name):
    with open(output_file_name+".txt", "w") as f:
        f.write(f"RING {len(best_ring)}\n")
        for i in range(len(best_ring)):
            if i != len(best_ring)-1:
                f.write(f"{best_ring[i]} ")
            else :
                f.write(f"{best_ring[i]}\n")
        f.write("STAR\n")
        for i in range(len(best_star)):
            f.write(f"{best_star[i][0]} {best_star[i][1]}\n")
        f.write(f"COST {best_L}")
        

def readingOutput(output_file_name, matrix_size):
    with open(output_file_name+".txt") as f:
        ring_size = int(f.readline().split(" ")[1][:-1])
        ring = f.readline().split(" ")
        
        for i in range(len(ring)):
            if i != len(ring):
                ring[i] = int(ring[i])
            else:
                ring[i] = int(ring[i][:-1])
        f.readline()
        star = []
        for i in range(matrix_size-len(ring)):
            tmp = f.readline().split(" ")
            tmp[0] = int(tmp[0])
            tmp[1] = int(tmp[1][:-1])
            star.append(tmp)
        cost = int(f.readline().split(" ")[1])    
        return ring_size, ring, star, cost
    