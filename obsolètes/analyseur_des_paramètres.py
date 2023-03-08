import matplotlib.pyplot as plt
import fourmis
import math

#Tests de variation de N et Q sur données
file_names = ["data1","data2","data3","data4","data5","data6","data7","data8",
              "data9"]
file_rings = [50,16,5,75,31,11,99,54,20]
file_sizes = [51,51,51,76,76,76,100,100,100]


N_range = [1,10,20,50,100,200,500,1000,2000]
Q_range = [1,10,20,50,100,200,500,1000,2000,5000,10000,12000,15000,20000,50000]

best_N = []
score_best_N = []
best_Q = []
score_best_Q = []
score_combined = []

estimated_optimality = []

#Runtime en s (le temps de calcul augmente beaucoup en fonction de t)
t = 90

for i in range(len(file_names)):
    tmp = math.inf    
    for j in range(len(N_range)):
        tmp2 = fourmis.antSystemAlgorithm(t, N_range[j], 7, 7, 100, 0.3, 
                                   file_names[i], "Groupe[5iG3]-Challenge1",
                                   file_rings[i])
        if (tmp2<tmp):
            tmp = tmp2
            tmp3 = N_range[j]
    score_best_N.append(tmp)        
    best_N.append(tmp3)
    
for i in range(len(file_names)):
    tmp = math.inf    
    for j in range(len(Q_range)):
        tmp2 = fourmis.antSystemAlgorithm(t, 20, 7, 7, 
                                   Q_range[j], 0.3, file_names[i], 
                                   "Groupe[5iG3]-Challenge1", file_rings[i])
        if (tmp2<tmp):
            tmp = tmp2
            tmp3 = Q_range[j]
    score_best_Q.append(tmp)          
    best_Q.append(tmp3)

for i in range(len(file_names)):
   estimated_optimality.append(fourmis.antSystemAlgorithm(t, 20, 7, 7, 100,  
                               0.3, file_names[i], "Groupe[5iG3]-Challenge1",
                               file_rings[i]))
"""
for i in range(len(file_names)):
   score_combined.append(fourmis.antSystemAlgorithm(t, score_best_N[i], 7, 7, 
                               score_best_Q[i], 0.3, file_names[i],
                               "Groupe[5iG3]-Challenge1",file_rings[i]))
"""   
#Au final rien d'exploitable en terme de corrélation            

fig, ax = plt.subplots()
ax.plot(best_N, file_rings)
plt.title("Évolution de N optimal en fonction du ring optimal")
plt.xlabel("N optimal")
plt.ylabel("Ring optimal")

fig, ax = plt.subplots()
ax.plot(best_N, file_sizes)
plt.title("Évolution de N optimal en fonction de la taille du fichier")
plt.xlabel("N optimal")
plt.ylabel("Taille du fichier")

fig, ax = plt.subplots()
ax.plot(best_N, estimated_optimality)
plt.title("Évolution de N optimal en fonction de l'optimalité estimée")
plt.xlabel("N optimal")
plt.ylabel("Optimalité estimée")

fig, ax = plt.subplots()
ax.plot(best_Q, file_rings)
plt.title("Évolution de Q optimal en fonction du ring optimal")
plt.xlabel("Q optimal")
plt.ylabel("Ring optimal")

fig, ax = plt.subplots()
ax.plot(best_Q, file_sizes)
plt.title("Évolution de Q optimal en fonction de la taille du fichier")
plt.xlabel("Q optimal")
plt.ylabel("Taille du fichier")

fig, ax = plt.subplots()
ax.plot(best_Q, estimated_optimality)
plt.title("Évolution de Q optimal en fonction de l'optimalité estimée")
plt.xlabel("Q optimal")
plt.ylabel("Optimalité estimée")

print(f"Best values of N : {best_N}")
print(f"Best values of Q : {best_Q}")
print(f"Best score of N : {score_best_N}")
print(f"Best score of Q : {score_best_Q}")
print(f"Best score combined : {score_combined}")