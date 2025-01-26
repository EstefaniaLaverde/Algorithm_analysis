# Tarea 1 Analisis de algoritmos

## Ejercicio 1

### Modelacion

Modelamos la situacion usando un grafo, donde los vertices representan a las personas y hay una eje entre dos vertices si y solo si las 2 personas respectivas se conocen directamente entre si, no permitimos multiples ejes ni self loops, ademas los ejes son no dirigidos.

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

### Testeo

para propositos de testeo pusimos varios archivos txt con descripciones de grafos en la carpeta tests_eje1, varios de estos fueron escritos a mano con el proposito de evaluar grafos con estructuras particuales, por ejemplo caminos, ciclos, grafos no conexos, etc.

Adicionalmente en Assignment1\generate_test1.py, tenemos un script para generar grafos de forma aleatoria para poder testear aun mas el algoritmo, podemos generar un archivo txt con un grafo aleatorio ejecutando el commando:

```bash
python Assignment1\generate_test1.py path_to_my_test_file.txt n m
```

donde path_to_my_test_file.txt es el path donde queremos que quede guardado el grafo recien generado, n la cantidad de nodos del grafo a generar y m la cantidad de ejes.

### Visualizacion

Para asistir en el testo hemos agregado un script de vizualizacion, para asi poder graficar y verificar correctitud de los resultados manualmente de forma facil, para hacer esto es suficiente con ejecutar el comando

```python .\Assignment1\plot_graph.py path_to_my_test_file.txt
```

donde path_to_my_test_file.txt es el path un archivo txt con el grafo que queremos visualizar
