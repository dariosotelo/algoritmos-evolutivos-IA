import numpy as np
import random

def generador_cromosoma_valido(N=20):
    if N % 2 == 1:
        N = N + 1 ##Agregar un equipo de descanso
    cromo = np.zeros((N,N))
    sets_vertical   = {i : set([j for j in range(1,N)]) for i in range(0,N) }
    sets_horizontal = {i : set([j for j in range(1,N)]) for i in range(0,N) }
    for j in range(N):
        for i in range(j+1,N):
                posibles = list(sets_vertical[i] & sets_horizontal[j])
                #val = posibles.pop()
                val = random.choice(posibles)
                sets_vertical[i].remove(val)
                sets_vertical[j].remove(val)
                sets_horizontal[i].remove(val)
                sets_horizontal[j].remove(val)
                cromo[i,j] = val
                cromo[j,i] = val + N
    return cromo

print(generador_cromosoma_valido(N=5))
for j in range(2,10):
    error=0
    for i in range(100000):
        try:
            generador_cromosoma_valido(N=j)
        except:
             error+=1
    print("Freq de no salir para n= ",j," con 100000",error/100000)
