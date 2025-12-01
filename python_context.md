Ejemplo 1 codigo profesor:

import random

def busca_secuencia(vector, desde, secuencia):
  # Retorna Verdadero o False
  if len(secuencia) > len(vector) - desde:
    return False
  i = 0
  while i < len(secuencia):
    if vector[desde+i] == secuencia[i]:
      i = i + 1
    else:
      return False   
  return True

a = []
i = 0
while i < 10000000:
  a.append(random.randint(0,10))
  i = i + 1

secuencia = [3, 1, 4, 1, 6, 4]
i = 0
c = 0
while i < len(a):
  encontrado = busca_secuencia(a, i, secuencia)
  if encontrado:
    c = c + 1
    i = i + len(secuencia)
  else:
    i = i + 1

print(c)

Ejemplo 2:

# Lee un archivo y retorna un vector con el contenido del archivo
def lee_archivo(filename):
    fd = open(filename, "rt")
    vector = []
    numero = fd.readline()
    while numero != "":
        n = int(numero)
        vector.append(n) # vector = vector + [n]
        numero = fd.readline()
    fd.close()
    return vector

def busca_posicion_minimo(vec, desde):
    m = 0 
    p = 0
    i = desde
    while i < len(vec):
        if vec[i] < m or i == desde:
            m = vec[i]
            p = i
        i = i + 1
    return p

def ordenar_por_seleccion(vector):
    i = 0
    while i < len(vector):
        p = busca_posicion_minimo(vector, i)
        # Intercambiar
        tmp = vector[i]
        vector[i] = vector[p]
        vector[p] = tmp
        i = i + 1
    return vector

def escribir_archivo(filename, vector):
    fd = open(filename, "wt")
    i = 0
    while i < len(vector):
        vector[i] = str(vector[i]) + "\n"
        i = i + 1
    fd.writelines(vector)
    fd.close()

vector = lee_archivo("numeros.txt")
vector = ordenar_por_seleccion(vector)
escribir_archivo("numeros.txt", vector)

Ejemplo 3:

def busqueda_binaria_recursiva(vector, objetivo, inicio, final):
  if inicio > final:
    return -1
  
  medio = (inicio + final) // 2
  if vector[medio] == objetivo:
    return medio
  if vector[medio] < objetivo:
    return busqueda_binaria_recursiva(vector, objetivo, medio+1, final)
  else:
    return busqueda_binaria_recursiva(vector, objetivo, inicio, medio-1)

    Ejemplo 5:

    vector = [2,3,1,-1,2,5,7,8,1,0,-4,-10]
vector2 = [-1333,-2,-6,-10,-11,-3,-1, -5]
vector3 = [-1000000001, -1000000002, -1000000003]


def busca_valor(vector, valor):
  i = 0
  while i < len(vector):
    if vector[i] == valor:
      return i
    i = i + 1
  return -1

print(busca_valor(vector, -4))

def valor_maximo(v):
  i = 0
  m = 0
  while i < len(v):
    if v[i] > m or i == 0:
      m = v[i]
    i = i + 1
  return m

def valor_minimo(v):
  i = 0
  m = 0
  while i < len(v):
    if v[i] < m or i == 0:
      m = v[i]
    i = i + 1
  return m

def posicion_minimo(v):
  i = 0
  m = 0
  posicion = 0
  while i < len(v):
    if v[i] < m or i == 0:
      m = v[i]
      posicion = i
    i = i + 1
  return posicion

def posicion_maximo(v):
  i = 0
  m = 0
  posicion = 0
  while i < len(v):
    if v[i] > m or i == 0:
      m = v[i]
      posicion = i
    i = i + 1
  return posicion