"""
Inteligencia Artificial - Proyecto 3
El siguiente proyecto es un sistema basado en algoritmos evolutivos
que planea el calendario de una liga de futbol, considerando que todos los equipos
juegan 2 veces contra todos los demás: una de ida y una de vuelta

Las planeaciones se evalúan con base en criterios como la distancia entre
partidos de ida/vuelta, alternancia entre local y visitante, la distancia de
viaje cuando se está de local y que equipos del mismo estadio no jueguen de local

Mutamos las planeaciones "mezclando" e intercambiando jornadas, para modificar los distintos parámetros
"""
import numpy as np
import random

"""
Generación de población inicial
"""

def generador_cromosoma_valido(N=20):
  """
  Genera un cromosoma válido para un problema de asignación de equipos a partidos deportivos.

  Args:
    N (int): número de equipos participantes en el torneo.

  Returns:
    np.ndarray: matriz cuadrada de tamaño NxN que representa la asignación de partidos entre los equipos.
  """
  if N % 2 == 1:
    # Si el número de equipos es impar, se agrega un equipo de descanso
    N = N + 1
  cromo = np.zeros((N,N))
  # Se crean dos conjuntos para cada fila y cada columna de la matriz,
  # que contendrán los valores posibles que pueden ser asignados a cada posición.
  sets_vertical   = {i : set([j for j in range(1,N)]) for i in range(0,N) }
  sets_horizontal = {i : set([j for j in range(1,N)]) for i in range(0,N) }
  for j in range(N):
    for i in range(j+1,N):
      # Se obtienen los valores posibles que están disponibles tanto en la fila i como en la columna j.
      posibles = list(sets_vertical[i] & sets_horizontal[j])
      # Se elige al azar un valor de los posibles y se asigna a la posición (i,j) y a la posición (j,i)
      val = random.choice(posibles)
      sets_vertical[i].remove(val)
      sets_vertical[j].remove(val)
      sets_horizontal[i].remove(val)
      sets_horizontal[j].remove(val)
      cromo[i,j] = val
      cromo[j,i] = val + N - 1
  return cromo

def genera_poblacion(N=8, p=110):
  """
  Genera una población de cromosomas válidos para el problema de asignación de equipos a partidos deportivos.

  Args:
    N (int): número de equipos participantes en el torneo.
    p (int): tamaño de la población.

  Returns:
    list: lista de matrices cuadradas de tamaño NxN, cada una de las cuales representa una asignación de partidos entre los equipos.
  """
  poblacion = []
  error = 0
  i = 0
  while len(poblacion) != p and i < 10**6:
    try:
      # Se genera un cromosoma válido y se agrega a la población
      cromo = generador_cromosoma_valido(N)
      poblacion.append(cromo)
    except:
      # Si ocurre una excepción al generar un cromosoma válido, se cuenta como un error
      error +=1
    i+=1
  if i == 10**6:
    # Si no se pudieron generar suficientes cromosomas válidos después de 10^6 intentos,
    # se rellena el resto de la población con cromosomas duplicados de los generados anteriormente.
    num_pob = len(poblacion)
    for i in range(0,p-num_pob):
      poblacion.append(poblacion[i])
  return poblacion

"""
Evaluación de las planeaciones
"""
#Funciones auxiliares
def alternancia_local(planeacion, equipo, jornadas):
    """
    Para un equipo dado, evalua qué tanto alterna entre local y visitante
    Mientras mayor sea le puntaje que regresa la función, menos alterna y es "peor"

    :param planeacion: la planeación a evaluar
    :param equipo: el equipo a evaluar
    :param jornadas: el número de jornadas (filas/columnas de la matriz)
    :return: score final de alernancia
    """

    # Score de alternancia
    consecutivos = 0

    # Separamos en local y visitante
    locales = planeacion[equipo, :]
    visitantes = planeacion[:, equipo]

    # Para cada jornada, revisamos si brinca de local a visitante o no (dos seguidos de local,
    for i in range(1, jornadas + 1):
        if i in locales and (i + 1) in locales:
            consecutivos += 1
        if i in visitantes and (i + 1) in visitantes:
            consecutivos += 1

    return consecutivos
def evalua_alternancia(planeacion, equipos, jornadas):
    """
    Para todos los equipos de una liga, evalúa su alternancia
    y regresa la suma total para la planeación

    :param planeacion: Matriz de jornadas
    :param equipos: Número de equipos
    :param jornadas: Número de jornadas
    :return: El valor total de la alternancia para esa planeación

    El algoritmo está diseñado tal que a si los equipos alternan mucho
    la función regrese un valor bajo
    """
    score_alternancia = 0
    # Evaluaación de local vs visitante
    for i in range(equipos):
        score_alternancia = score_alternancia + alternancia_local(planeacion, i, jornadas)
    return score_alternancia

def evalua_separacion(planeacion,equipos):
    """
    Evalúa la separación entre los juegos de ida y vuelta de una planeación

    :param planeacion: Matriz de jornadas
    :param equipos: Número de equipos
    :return: Valor de separación
    """
    #Obtenemos todos los posibles partidos (sin distinguir ida/vuelta)
    todos_partidos = [(equipo1,equipo2) for idx, equipo1 in enumerate(list(range(equipos))) for equipo2 in list(range(equipos))[idx+1:] ]
    distance = 0

    #Calculamos y agregamos la distancia entre los partidos de ida y vuelta
    for partido in todos_partidos:
        distance += abs(planeacion[partido[0]][partido[1]] - planeacion[partido[1]][partido[0]])



    return distance

def distancia_equipo(planeacion, distancias, equipo,jornadas):
    """
    Calcula, para un equipo, la distancia que recorren durante la temporada

    :param planeacion: Matriz de jornadas
    :param distancias: Matriz de distancias entre equipos
    :param equipo: Número de equipos
    :param jornadas: Número de jornadas
    :return: La distancia total para ese equipo


    """
    # Separamos en local y visitante
    locales = planeacion[equipo, :]
    visitantes = planeacion[:, equipo]




    distancia_viajada = 0

    for i in range(1,jornadas+1):

        if i in locales and i+1 in locales:
            pass
        elif i in locales and i+1 in visitantes:
            partida = int(np.where(locales == i)[0])
            llegada = int(np.where(visitantes == (i+1))[0])

            distancia = distancias[partida][llegada]

            distancia_viajada += distancia

        elif i in visitantes and i+1 in locales:

            partida = int(np.where(visitantes == i)[0])
            llegada = int(np.where(locales == (i + 1))[0])



            distancia = distancias[partida][llegada]
            distancia_viajada += distancia

        elif i in visitantes and i+1 in visitantes:
            partida = int(np.where(visitantes == i)[0])
            llegada = int(np.where(visitantes == (i + 1))[0])



            distancia = distancias[partida][llegada]
            distancia_viajada += distancia
        else:
            pass

    return distancia_viajada
def evalua_distancia_total(planeacion,distancias,equipos,jornadas):
    """
    Aplica la función individual de distancia a todos los equipos

    """

    distancia_total = 0
    for equipo in range(equipos):
        distancia_total = distancia_total + distancia_equipo(planeacion,distancias,equipo,jornadas)

    return distancia_total

def encuentra_misma_ciudad(distancias):
    """
    Encuentra los equipos que son de la misma ciudad
    :param distancias: Matriz de distancias
    :return: Un conjunto de tuplas (equipo1, equipo2) para todos los equipos que comparten ciudad/estadio
    """

    misma_ciudad = np.argwhere(distancias == 0)
    misma_ciudad = [tuple(item)for item in misma_ciudad if item[0] != item[1]]
    misma_ciudad = set(misma_ciudad)

    return misma_ciudad
def penaliza_locales(planeacion,distancias):
    """
    Penaliza las jornadas en las que dos equipos de la misma ciudad juegan ambos
    como locales

    :param planeacion: Matriz de jornadas
    :param distancias: Matriz de distancias
    :return: Conteo de las penalizaciones
    """
    #Encuentra los equipos que juegan en la misma ciudad
    locales = encuentra_misma_ciudad(distancias)
    penalizacion = 0

    for par in locales:
        partidos_local_1 = set(planeacion[par[0],:])
        partidos_local_2 = set(planeacion[par[1],:])

        comunes = partidos_local_1.intersection(partidos_local_2)

        penalizacion += len(comunes)

    return penalizacion

#Evaluación
def evalua_planeacion(planeacion, distancias, equipos, jornadas, imprime=False):
    """
     Recibe una planeación de partidos y la evalúa con los siguientes criterios:
     1. Alternancia entre local/visitante para cada equipo
     2. Separación entre partidos de 2 equipos (local/visitante)
     3. Dos juegos con equipos locales en la misma jornada
     4. Distancia recorrida (bajo el supuesto que para partidos de visitante sucesivos se mantienen "on the road"

     Esto nos da la siguiente función de evaluación, que buscamos MINIMIZAR:

     APT = Alternancia + 1 / Separacion + Distancia + PenalizacionesLocales
     """
    Alternancia = evalua_alternancia(planeacion, equipos, jornadas)
    Separacion = evalua_separacion(planeacion, equipos)
    Distancia = evalua_distancia_total(planeacion, distancias, equipos, jornadas)
    PenalizacionLocales = penaliza_locales(planeacion, distancias)

    #NORMALIZAMOS PARA QUE LAS VARIABLES ESTÉN ENTRE 0 y 1
    Valor = (0.25 * (180 - Alternancia) / (180 - 70) + 0.25 * (Separacion - 350) / (1000 - 350) + 0.25 * (
                60_000 - Distancia) / (
                      60_000 - 36000) + 0.25 * (60 - PenalizacionLocales) / (60 - 40))

    if (imprime):
        print("ALTERNANCIA: {}".format((180 - Alternancia) / (180 - 70)))

        print("SEPARACION: {}".format((Separacion - 350) / (1000 - 350)))

        print("DISTANCIA: {}".format((60_000 - Distancia) / (
                60_000 - 36000)))
        print("PENALIZACION LOCALES: {}".format((60 - PenalizacionLocales) / (60 - 40)))
        print("\t Score final: {}".format(Valor))

    # print("\n")

    return (planeacion, Valor)
def evaluacion(planeaciones, distancias, equipos, jornadas):
    """
    Recibe múltiples planeaciones, y para cada uno evalúa la planeación

    :param planeaciones: Matriz de matrices de jornadas
    :param distancias: Matriz de distancia
    :param equipos: Numero de equipos
    :param jornadas: Numero de jornadas
    :return: Arreglo de tuplas (Matriz, Valor)
    """
    PLANEACIONES = []

    for planeacion in planeaciones:
        tupla = evalua_planeacion(planeacion, distancias, equipos, jornadas)
        PLANEACIONES.append(tupla)

    PLANEACIONES = sorted(PLANEACIONES, key=lambda t: t[1])

    return PLANEACIONES

"""
Mutación de las planeaciones
"""
#Esta función recorre toda la matriz cambia dos números dados
def swapNumeros(a, b, matriz):
  n,m=matriz.shape
  for i in range(n):
    for j in range(m):
      if matriz[i,j] == a:
        matriz[i,j] = b
      elif matriz[i,j] == b:
        matriz[i,j] = a
  return matriz

#Este es el método principal de este bloque.
def muta_matriz(matriz):
  i=0
  n,m=matriz.shape
  while i<n:
    #Con probabilidad de 0.8 va a entrar en este ciclo
    if random.random() < 0.8:
      #En esta parte se cambian los números de la matriz
      cambio_aleatorio1=random.randint(1,2*n-2) ### TODO: REVISAR JORNADAS
      cambio_aleatorio2=random.randint(1,2*n-2) ### TODO: REVISAR JORNADAS
      #Este while es por si cambio_aleatorio1 es igual a cambio_aleatorio2
      while cambio_aleatorio1==cambio_aleatorio2:
        cambio_aleatorio2=random.randint(1,2*n-2)
      #Aquí se hace el cambio aleatorio
      matriz = swapNumeros(cambio_aleatorio1, cambio_aleatorio2, matriz)
    i+=1
  #Chance hay que eliminar esto de aqui
  #En esta parte se empareja la matriz triangular inferior para que sea simétrica + n/2 más grande
  #matriz=acomodaLocalVisitante(matriz)
  return matriz

#Este método recibe un arreglo de matrices y muta cada una de ellas
def mutaVariasMatrices(cubo):
  for i in range(len(cubo)):
    cubo[i]=muta_matriz(cubo[i])
  return cubo

"""
Algoritmo completo
"""
def mata_muta_evalua(poblacion_plan_eval, num_pob, matriz_distancias_equip, num_equipos, jornadas):
    # Genera una nueva población aleatoria con un tercio del tamaño de la población original
    nueva_pob_plan = genera_poblacion(num_equipos, 3 * (num_pob // 4))
    # Evalúa la población generada y la agrega a la población de evaluaciones
    for i in range(3 * (num_pob // 4)):
        poblacion_plan_eval[i] = evalua_planeacion(nueva_pob_plan[i], matriz_distancias_equip, num_equipos, jornadas)

    # Mutación: crea nuevas planeaciones a partir de la población original con un tercio de mutación
    for i in range(3* (num_pob // 4), num_pob - 1):
        planeacion_mutada = muta_matriz(poblacion_plan_eval[i][0])
        poblacion_plan_eval[i] = evalua_planeacion(planeacion_mutada, matriz_distancias_equip, num_equipos, jornadas)

    # Reordena la población de evaluaciones por orden de aptitud, de menor a mayor
    poblacion_plan_eval = sorted(poblacion_plan_eval, key=lambda t: t[1])
    return poblacion_plan_eval

def algoritmo_generico(num_equipos, jornadas, matriz_distancias_equip, num_pob=90, porce_exce=0.85,generaciones=300):
    # Genera una población aleatoria de planeaciones con tamaño num_pob
    poblacion_planeaciones = genera_poblacion(num_equipos, num_pob)

    # Evalúa la población generada y guarda los resultados en poblacion_plan_eval
    poblacion_plan_eval = evaluacion(poblacion_planeaciones, matriz_distancias_equip, num_equipos, jornadas)

    # Ejecuta el ciclo principal del algoritmo genético mientras la mejor aptitud obtenida en la población
    # no alcance el porceentaje de excepción deseado o no se haya llegado al máximo de iteraciones permitido (1_000_000)
    max_num = 0
    while poblacion_plan_eval[-1][1] < porce_exce and max_num < generaciones:
        poblacion_plan_eval = mata_muta_evalua(poblacion_plan_eval, num_pob, matriz_distancias_equip, num_equipos,
                                               jornadas)

        print("GENERACION {}".format(max_num))
        evalua_planeacion(poblacion_plan_eval[-1][0],matriz_distancias_equip,num_equipos,jornadas,imprime=True)
        max_num += 1

    # Retorna la mejor planeación encontrada
    return poblacion_plan_eval[-1]


"""
Método auxiliar para imprimir las jornadas
"""

def imprime_jornadas(planeacion,equipos,nombres_equipos,jornadas):

    print("IMPRIMIENDO LAS JORNADAS DE LA PLANEACIÓN")

    for jornada in range(jornadas):
        print("")
        print("JORNADA {}".format(jornada))

        for k in range(equipos):
            for j in range(equipos):
                if planeacion[k][j] == jornada and k != j :
                    print("Juegan {} contra {} ".format(nombres_equipos[k],nombres_equipos[j]))






if __name__ == "__main__":

    #Simulamos una liga de 12 equipos, con 22 jornadas
    EQUIPOS = 12
    JORNADAS = 22

    nombres_equipos = {

        0: "Mario",
        1: "Luigi",
        2: "Peach",
        3: "Daisy",
        4: "DK",
        5: "DK Jr",
        6: "Yoshi",
        7: "Waluigi",
        8: "Wario",
        9: "Bowser",
        10: "Bowser JR",
        11: "Pirahnna Plant",

    }
    distance_matrix = np.array([[0, 0, 70, 140, 100, 100, 100, 300, 250, 250, 250, 400],
                                [0, 0, 70, 140, 100, 100, 100, 300, 250, 250, 250, 400],
                                [70, 70, 0, 70, 170, 170, 170, 370, 320, 320, 320, 470],
                                [140, 140, 70, 0, 240, 240, 240, 440, 390, 390, 390, 540],
                                [100, 100, 170, 240, 0, 0, 50, 200, 150, 150, 150, 300],
                                [100, 100, 170, 240, 0, 0, 50, 200, 150, 150, 150, 300],
                                [100, 100, 170, 240, 50, 50, 0, 250, 200, 200, 200, 350],
                                [300, 300, 370, 440, 200, 200, 250, 0, 50, 300, 300, 100],
                                [250, 250, 320, 390, 150, 150, 200, 50, 0, 300, 300, 150],
                                [250, 250, 320, 390, 150, 150, 200, 300, 300, 0, 0, 200],
                                [250, 250, 320, 390, 150, 150, 200, 300, 300, 0, 0, 200],
                                [400, 400, 470, 540, 300, 300, 350, 100, 150, 200, 200, 0]])

    #Corremos el algoritmo
    mejor = algoritmo_generico(EQUIPOS, JORNADAS, distance_matrix,porce_exce=0.85,generaciones = 300)

    #Evaluamos la mejor
    evalua_planeacion(mejor[0], distance_matrix, EQUIPOS, JORNADAS, imprime=True)

    #La imprimimos
    imprime_jornadas(mejor[0], EQUIPOS, nombres_equipos, JORNADAS + 1)