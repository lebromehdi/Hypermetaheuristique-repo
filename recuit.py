#Code de Merouane que j'ai légèrement modifié
import random
import utils
import math
import time
import timeit

# Permet de stocker tout les sommet qui ne sont pas dans le ring
def calculAllStar(ring,verticesNum):  

    Vertices = []    
    for i in range(verticesNum):
        i= i+1
        if i not in ring:
            Vertices.append(i)
    return Vertices

#Permet d'associer les Stars à leur ring les plus proches
def calculStarToAssigne(ring,starMatrix,verticesNum):
    Vertices = calculAllStar(ring,verticesNum)
    RingStar  =[]
    for vertice in Vertices:
        # On assigne à l'entrepot au debut
        minCost = starMatrix[vertice -1][ring[0]-1]
        ringVertice = ring[0]
        """ On check pour tout les points du ring 
         pour lui associer le meilleur"""
        for secVertice in ring:
            # Calcul du cout avec le nouveau sommet du ring
            cost  = starMatrix[vertice -1][secVertice-1]  
            # Si c'est meilleur on assigne      
            if cost < minCost:
                minCost = cost
                ringVertice = secVertice
        #on stock la paire ring Star dans un tableau
        RingStar.append([vertice, ringVertice])
    return RingStar

# Calcul le cout des elements dans le ring
def calculRingCost(ring,ringMatrix):
    
    ringCost = 0
    for i in range(len(ring)-1):              
        ringCost = ringCost+ringMatrix[ring[i]-1][ring[i+1]-1]        

    ringCost = ringCost + ringMatrix[ring[-1]-1][ring[0]-1]
    return ringCost

# Calcul du cout des Star
def calculStarCost(ringStar,starMatrix):
    #calcul du cout des star
    starCost = 0
    for i in ringStar:
        starCost = starCost + starMatrix[i[0]-1][i[1]-1]
    return starCost

def calculCost(ring,verticesNum,ringMatrix,starMatrix):
    # retourne le cout total
    ringCost = calculRingCost(ring,ringMatrix)
    starCost = calculStarCost(calculStarToAssigne(ring,starMatrix,verticesNum),
                              starMatrix)
    return ringCost+starCost

#Défini un ring totalement aleatoire d'une taille fixé
def initialisationDuRingtaille(n,verticesNum):
   
    ring = [1]   
    chooseList = []
    for i in range(2, verticesNum+1):
        chooseList.append(i)

    for i in range(n):
        vertice = random.choice(chooseList)
        ring.append(vertice)
        chooseList.remove(vertice)

    return ring

# Generation de plusieru ring de départ et on prend le meilleur
def meilleurRingRandom(verticesNum,ringMatrix,starMatrix):
    
    rings = []    
    rings.append([1])
    rings.append(initialisationDuRingtaille(int((verticesNum-1) * 0.1),verticesNum))    
    rings.append(initialisationDuRingtaille(int((verticesNum-1) * 0.25),
                 verticesNum))    
    rings.append(initialisationDuRingtaille(int((verticesNum-1) * 0.4),
                 verticesNum))
    rings.append(initialisationDuRingtaille((verticesNum-1)// 2,verticesNum))
    rings.append(initialisationDuRingtaille(int((verticesNum-1) * 0.6),
                 verticesNum))   
    rings.append(initialisationDuRingtaille(int((verticesNum-1) * 0.75),
                 verticesNum))    
    rings.append(initialisationDuRingtaille(int((verticesNum-1) * 0.9),
                 verticesNum))
    rings.append(initialisationDuRingtaille(verticesNum-1,verticesNum))
    
    cost = []
    for ring in rings:
        x = calculCost(ring,verticesNum,ringMatrix,starMatrix)
        cost.append(x)
    bestCost = min(cost)
    index = cost.index(bestCost)
    bestRing = rings[index]
    return [bestRing, bestCost]

def permutation(ring):
    
    output = []
    for i in range(1,len(ring)):
        for e in range(i + 1, len(ring)):
            ring2 = ring.copy()
            save = ring2[i]
            ring2[i] = ring2[e]
            ring2[e] = save
            output.append(ring2)
    return output
     
def addVertice(ring,verticesNum):
    #Permet de faire plusieur ring ou l'on ajoute un point
    n = verticesNum - len(ring)
    news = []
    ajout = calculAllStar(ring,verticesNum)    
    for i in range(n):
        tmp = ring.copy()
        ni = random.choice(ajout)        
        ajout.remove(ni)
        m = random.randint(1, len(ring))
        tmp.insert(m, ni)
        news.append(tmp)
    return news

def deleteVertices(ring, n):
    # Supprime un point du ring 
    news = []
    for i in range(n):
        tmp = ring.copy()
        n = random.choice(ring[1:])
        tmp.remove(n)
        news.append(tmp)
    return news

def Modification(ring, n,verticesNum):
    res = []
    if n == 1:
        m = 1
    if n > 1:
        m = n // 2
    # adding
    assign = calculAllStar(ring,verticesNum)
    for i in range(n):
        ring2 = ring.copy()
        n = random.choice(assign)
        m = random.randint(1, len(ring))
        ring2.insert(m, n)
        res.append(ring2)
    # removing
    for i in range(n):
        ring2 = ring.copy()
        n = random.choice(ring[1:])
        ring2.remove(n)
        res.append(ring2)

    return res

def neighbourhood(ring,verticesNum):
    # Retourne le voisinage
    perm = permutation(ring)    
    nbperm = len(perm)    
    if perm != []:
        max = verticesNum
        if len(ring) == max:
            # on retire un point 
            modification = deleteVertices(ring, nbperm)

        if len(ring) != max:
            # on ajoute et retire un point
            modification = Modification(ring, nbperm,verticesNum)

    if perm == []:        
        # on ajoute un point 
        modification = addVertice(ring,verticesNum)

    tmp = modification + perm    
    #augmente l'aleatoire en melangeant 
    random.shuffle(tmp)
    return tmp

def recuit(tc,step, alpha, temps, input_file_name,starting_time):
    #Redéfinition des variables globales
    ringMatrix,starMatrix,verticesNum= utils.readingInput(input_file_name)
    
    ringD, bestCost = meilleurRingRandom(verticesNum,ringMatrix,starMatrix)     
    timeout = time.time() + 60*temps

    while time.time() < timeout:

      for i in range(step):
        ring = random.choice(neighbourhood(ringD,verticesNum))
        cost = calculCost(ring,verticesNum,ringMatrix,starMatrix)
        delta = cost - bestCost
        if delta <=0:
            ringD = ring
            bestCost = cost
        else:
            probably = math.exp(-delta/tc)
            x = random.random()
            if x <= probably:
                ringD = ring
                bestCost = cost
       
      tc = tc * alpha
      
    print(f"SA process finished {timeit.default_timer() - starting_time} " 
          +"seconds after the start with the following lowest cost : "
          +f"{bestCost}.")
    print(f"The best size of ring found : {len(ringD)}.")
    
    return  bestCost, ringD, calculStarToAssigne(ring,starMatrix,verticesNum), len(ringD)

