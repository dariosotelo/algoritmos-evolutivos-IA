import numpy as np

def generador_cromosoma_valido(N=20):
    cromo = np.zeros((N+1,N+1))
    sets_vertical   = {i : set([j for j in range(1,N+1)]) for i in range(0,N+1) }
    sets_horizontal = {i : set([j for j in range(1,N+1)]) for i in range(0,N+1) }
    for j in range(N+1):
        for i in range( N+1):
            if i != j:
                posibles = sets_vertical[i] & sets_horizontal[j]
                val = posibles.pop()
                sets_vertical[i].remove(val)
                sets_horizontal[j].remove(val)
                cromo[i,j] = val
                cromo[j,i] = val + N 
    return cromo
print(generador_cromosoma_valido(N=3))


