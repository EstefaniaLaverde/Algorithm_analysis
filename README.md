# Tarea 1 Analisis de algoritmos

## Ejercicio 1

### Modelacion

Modelamos la situacion usando un grafo, donde los vertices representan a las personas y hay una eje entre dos vertices si y solo si las 2 personas respectivas se conocen directamente entre si, no permitimos multiples ejes ni self loops, los ejes son no dirigidos y no tienen costos.

una vez definido el grafo donde vamos a trabajar, podemos empezar a resolver el problema, como nos dice el enunciado debemos verificar que cada persona conozca a cualquier otra persona atraves de una cadena de a lo sumo 6 personas, es decir la distancia entre cualquier par de nodos debe der menor o igual a 6, en otras palabras debemos verificar que el diametro del grafo sea menor a 6.

La idea general de la implenetacion es usar busqueda en anchura (bsf por su acronimo en ingles), para confirmar que entre cualquier par de nodos la distancia es menor o igual a  6, vamos iterando sobre los nodos del grafo seleccionando uno de ellos como raiz y usamos bsf para verificar que todos los nodos estan a distancia menor o igual a 6 del nodo selecionado como raiz, si alguno supera este umbral de distancia retornamos false, este proceso al iterar por cada nodo raiz, nos permite evaluar todas las distancias entre parejas de nodos.

### Hipotesis asumidas

el enunciado nos habla de verificar la teoria de los 6 grafos de separacion en una red social como Facebook, basado en esto asumimos las siguientes hipotesis

- dado que el grafo tiene millones de nodos, para poder considerar que el grafo es denso (no sparse) entonces seria nesesario que el usuario promedio tubiera cientos de miles de amigos, se sabe en general la cantidad promedio de amigos es alrededor de los cientos, asi una fraccion muy pequeña del tamaño del grafo, por tanto vamos a asumir que los grafos son sparse

- el algoritmo debe funcionar para grafos con millones de nodos, asi que al implementar no podemos depender de la matriz de adyacencia para representar el grafo, pues si n es la cantidad de nodos, la matriz de adyancencia tiene n^2 elementos, teniendo en cuanta la hipotesis de que el grafo es sparse, ademas de ser una cantidad inacesible de memoria tambien seria un cantidad enorme de memoria desperdiciada.

### Representacion de la entrada

para representar una base de datos de relaciones de amistad usamos un archivo de txt que sigo las siguientes especificaciones:

- en la primera linea hay enteros separados por espacio representando los nodos (personas) del grafo.
- en la segunda linea hay un entero indicando la cantidad de ejes en el grafo, digamos m
- en las m lineas posterioes hay dos enteros que deben coincidir con los nodos del grafos y estos dos enteros indican que hay un eje entre esos dos nodos

ejemplo, para un grafo que es un ciclo de 4 elementos el archivo txt luciria asi

```text
1 2 3 4
4
1 2
2 3
3 4
4 1
```

es posible encontrar mas archivos de ejemplo en la carpeta tests_eje1

### Modo de uso

una vez se tiene el archivo txt con el formato definido, es suficiente con ejecutar el comando:

```bash
python .\Assignment1\breadth_first_search.py path_to_my_test_file.txt
```

donde path_to_my_test_file.txt es el path al archivo txt con el grafo que queremos evaluar.

tras ejecutar este comando podremos ver en la consola True o False dependiendo de si el grafo cumple o no con la teoria de los 6 grados de separacion

### Testeo

para propositos de testeo pusimos varios archivos txt con descripciones de grafos en la carpeta tests_eje1, varios de estos fueron escritos a mano con el proposito de evaluar grafos con estructuras particuales, por ejemplo caminos, ciclos, grafos no conexos, etc.

Adicionalmente en Assignment1\generate_test1.py, tenemos un script para generar grafos de forma aleatoria para poder testear aun mas el algoritmo, podemos generar un archivo txt con un grafo aleatorio ejecutando el commando:

```bash
python Assignment1\generate_test1.py path_to_my_test_file.txt n m
```

donde path_to_my_test_file.txt es el path donde queremos que quede guardado el grafo recien generado, n la cantidad de nodos del grafo a generar y m la cantidad de ejes.

### Visualizacion

Para asistir en el testeo hemos agregado un script de vizualizacion, para asi poder graficar y verificar correctitud de los resultados manualmente de forma facil, para hacer esto es suficiente con ejecutar el comando

```bash
python .\Assignment1\plot_graph.py path_to_my_test_file.txt
```

donde path_to_my_test_file.txt es el path un archivo txt con el grafo que queremos visualizar

### Solucion alternativa

Deacuerdo a una propuesta que surgio en clase tambien tenemos una solucion alternativa para el ejercicio 1 usando multiplicacion de matrices, para solucionar el ejercicio 1 con esta solucion debemos usar el comando:

```bash
python Assignment1\ejercicio1_matrix.py path_to_my_test_file.txt
```

saldra en la consola True o False, la solucion al problema.

si bien una de los hipotesis que asumimos en el problema es que el grafo es sparse, la solucion alternativa es mas eficiente cuando se trata de grafos densos.

La solucion con bsf esta hecha en python puro mientras que la solucion con matrices usa numpy, que por debajo esta en c con paralelizacion y rutinas muy optimizadas, lo cual hace que la comparacion no sea tan directa, sin embargo tenemos evidencia de que los tiempos de ejecucion de ambas soluciones varian enormente dependiendo la estructura del grafo y dependiendo de esto es mucho mejor tomar una solucion sobre la otra.

- tests_eje1\test6.txt: es un grafo denso de 10000 nodos, tiempo con bsf 30 minutos, tiempo con matrices 52 segundos.
- tests_eje1\test7.txt: es un grafo sparse con 10000 nodos, tiempo con bsf 0.2 segundos, tiempo con matrices 52 segundos.

Concluyendo que dependiento de la cantidad de ejes aveces es mucho mejor la solucion por multiplicacion de matrices mientras que aveces es mucho mejor la solucion por bsf, el algoritmo con matrices simpre va a requerir mas memoria pero va a ir mejorando a medida que se inventan nuevas formas de multiplicar matrices.

## Ejercicio 5

### Modelacion

Modelamos el problema usando un grafo donde nos vertices son las intersecciones entre vias y los ejes son las vias, el enunciado nos dice que cada via tiene un costo asociado para convertirla en doble via, el cual es el costo del respectivo eje.

El problema nos pide encontrar un conjunto de vias que al convertirlas en doble via permitan ir de cualquier punto de la ciudad a cualquier otro usuando unicamente doble vias y que ademas esto tenga el costo minimo, es decir seleccionar un conjunto de ejes de costo minimo que de como resultado un grafo conexo.

Bajo este planteamiento, vamos a implementar el algoritmo de Kruskal para arboles de expansion de costo minimo (msp minimum spanning tree por sus siglas en ingles).

### Hipotesis asumidas

- Se asume el grafo tiene miles de nodos y es sparse, pues con una aproximacion sencilla una ciudad en cuadricula con 100 calles y 100 carreras tendra tendra 10000 intersecciones(nodos) y a lo sumo 4 vias por interseccion (ejes) por cada interseccion, claro hay ciudades mucho mas grandes y con presencia de puentes y/o tuneles, pero en general asumimos un grafo sparse con miles de nodos.

- Se asume que doble via da lugar a ejes bidireccionales o no dirigidos, si bien es posible asumir en un principio que los ejes son dirigidos, construir una solucion al problema que preserve direccionalidad (es decir que las doble vias tambien son dirigidas), se convierte en el problema de Minimum Strong Spanning Subdigraphs (MSSS), el cual es un problema NP-hard (Digraphs: Theory, algorithms and applications,  Prof. Jørgen Bang-Jensen, Prof. Gregory Z. Gutin (auth.), pag 483, primera frase de la seccion 12.2) y por tanto no se dispone de algoritmo eficiente para solucionar el problema para grafos con miles de nodos.

### Representacion de la entrada

para representar al grafo con el que modelamos la ciudad usamos un archivo txt con las siguientes especificaciones:

- en la primera linea hay enteros separados por espacio representando los nodos (intersecciones de la ciudad) del grafo.
- en la segunda linea hay un entero indicando la cantidad de ejes en el grafo, digamos m
- en las m lineas posteriores hay 3 enteros que describen los ejes del grafo, donde `a b c` quiere decir que un eje entre el nodo `a` y `b` con costo `c`

ejemplo, para un grafo que es un ciclo de 4 elementos  el archivo txt luciria asi

```text
1 2 3 4
4
1 2
2 3
3 4
4 1
```

es posible encontrar archivos de ejemplo en la carpeta tests_eje5

### Modo de uso

una vez se tiene el archivo txt con el formato definido, es suficiente con ejecutar el comando:

```bash
python Assignment1\pruebas_mst.ipynb path_to_my_test_file.txt
```

donde path_to_my_test_file.txt es el path al archivo txt con el grafo que queremos evaluar.

tras ejecutar este comando podremos ver en la consola como se imprimen los ejes que se deben convertir en doble via para cumplir con los requisitos del ejercicio, los resultados salen en el siguiente formato.

- en la primera linea un entero `m` dictando la cantidad de ejes
- en las `m` lineas posteriores 3 enteros `a b c` dictando que debemos usar el eje que conecta a `a` con `b` y que tiene costo `c`.

ejemplo:

```text
3
0 1 1
0 2 2
2 3 4
```

### Testeo

al igual que en el ejercicio anterior hemos escrito archivos txt con grafos de diversas estructuras para probar el algoritmo, se puede generar grafos aleatorios con peso usando el comando:

```bash
python Assignment1\generate_test5.py n m min_cost max_cost path_to_my_test_file.txt
```

donde n es la cantidad de nodos en el grafo a generar, m la cantidad de ejes, min_cost y max_cost los costos minimos y maximos de los ejes y path_to_my_test_file.txt el path al archivo donde queremos guardar el grafo aleatorio generado

### Visualizacion

Al igual que en ejercicio anterior agregamos un script de visualizacion, la diferencia importante es que con este script podemos visualziar grafos con peso

```bash
python .\Assignment1\plot_weighted_graph.py path_to_my_test_file.txt
```

donde path_to_my_test_file.txt es el path un archivo txt con el grafo que queremos visualizar.

