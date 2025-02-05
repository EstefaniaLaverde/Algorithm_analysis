# Tarea 1 Análisis de Algoritmos

## Ejercicio 1

### Modelación

Modelamos la situación utilizando un grafo (**FacebookNetwork**), donde los vértices representan a los usuarios y hay una arista entre dos vértices si y solo si los dos usuarios respectivos se conocen directamente entre sí. No permitimos múltiples aristas ni self loops, las aristas son no dirigidas y no tienen costos.

Una vez definido el grafo donde vamos a trabajar, podemos empezar a resolver el problema; como nos dice el enunciado debemos verificar que cada usuario conozca a cualquier otro usuario través de una cadena de a lo sumo 6 usuarios, es decir, la distancia entre cualquier par de nodos debe ser menor o igual a 6, en otras palabras debemos verificar que el diámetro del grafo sea menor o igual a 6.

La implementación se basa en la utilización de búsqueda en anchura (**BFS** por sus siglas en inglés), para verificar que la distancia entre cualquier par de nodos no excede los 6 grados de separación. Esto se logra iterando sobre cada nodo del grafo, seleccionándolo como raíz y aplicando BFS para determinar si todos los demás nodos se encuentran a una distancia de 6 o menos del nodo raíz. Si se detecta un nodo que supera este límite de distancia o si, al finalizar las iteraciones, no se han visitado todos los nodos, indicando que el grafo es disconexo, se retorna False. Por otro lado, si el grafo cumple con los 6 grados de separación y es conexo, se retorna True. Dicha implementación se puede encontrar en el método ``check6degrees`` de la clase ``FacebookNetwork``.

### Hipótesis asumidas

El enunciado nos habla de verificar la teoría de los 6 grados de separación en una red social como Facebook, basado en esto asumimos las siguientes hipótesis:

- Dado que el grafo tiene millones de nodos, para poder considerar que el grafo es denso (no sparse) entonces sería necesario que el usuario promedio tuviera cientos de miles de amigos, se sabe en general que la cantidad promedio de amigos es alrededor de los cientos, así una fracción muy pequeña del tamaño del grafo, por tanto vamos a asumir que los grafos son sparse.

- El algoritmo debe funcionar para grafos con millones de nodos, así que al implementar no podemos depender de la matriz de adyacencia para representar el grafo, pues si n es la cantidad de nodos, la matriz de adyacencia tiene n^2 elementos, teniendo en cuenta la hipótesis de que el grafo es sparse, además de ser una cantidad inaccesible de memoria también sería una cantidad considerable de memoria desperdiciada.

### Representación de la entrada

Para representar una base de datos de relaciones de amistad utilizamos un archivo de texto que sigue las siguientes especificaciones:

- En la primera línea hay enteros separados por un espacio representando el nodo (usuario) del grafo.
- En la segunda línea hay un entero indicando la cantidad de aristas en el grafo, digamos m.
- En las m líneas posteriores hay dos enteros que deben coincidir con los nodos del grafo y estos dos enteros indican que hay una arista entre esos dos nodos.

Ejemplo, para un grafo que es un ciclo de 4 elementos, el archivo de texto luciría así:

```text
1 2 3 4
4
1 2
2 3
3 4
4 1
```

### Modo de uso

Una vez que se tiene el archivo de texto con el formato definido, es suficiente con ubicarse en la carpeta donde se encuentra el archivo *ejercicio1_final.py* y ejecutar el comando:

```bash
python ejercicio1_final.py path_to_my_test_file.in path_to_my_output.out
```

Donde ``path_to_my_test_file.in`` es el path al archivo de texto con el grafo que queremos evaluar y ``path_to_my_output.out`` es el path al archivo de texto con el resultado.

Tras ejecutar este comando podremos ver en la consola True o False dependiendo de si el grafo cumple o no con la teoría de los 6 grados de separación.


### Solución alternativa

De acuerdo a una propuesta que surgió en clase, también tenemos una solución alternativa para el ejercicio 1 utilizando multiplicación de matrices (haciendo uso de la librería *numpy*). Para solucionar el ejercicio 1 con esta propuesta debemos usar el comando:

```bash
python ejercicio1_matrix.py path_to_my_test_file.in path_to_my_output.out
```
Donde ``path_to_my_test_file.in`` es el path al archivo de texto con el grafo que queremos evaluar y ``path_to_my_output.out`` es el path al archivo de texto con el resultado.

Saldra en la consola True o False, la solución al problema.

Si bien una de las hipótesis que asumimos en el problema es que el grafo es sparse, la solución alternativa es más eficiente cuando se trata de grafos densos.

La solución con BFS está hecha en Python puro, mientras que la solución con matrices utiliza numpy, que por debajo está en C con paralelización y rutinas muy optimizadas, lo cual hace que la comparación no sea tan directa, sin embargo, tenemos evidencia de que los tiempos de ejecución de ambas soluciones varían enormemente dependiendo de la estructura del grafo y dependiendo de esto es mucho mejor tomar una solución sobre la otra. A continuación se encuentra una comparativa con un grafo denso y un grafo sparse.

- Grafo denso de 10000 nodos, tiempo con BFS 30 minutos, tiempo con matrices 52 segundos.
- Grafo sparse con 10000 nodos, tiempo con BFS 0.2 segundos, tiempo con matrices 52 segundos.

Concluyendo que dependiendo de la cantidad de aristas, a veces es mucho mejor la solución por multiplicación de matrices, mientras que a veces es mucho mejor la solución por BFS, el algoritmo con matrices siempre va a requerir más memoria, pero va a ir mejorando a medida que se inventan nuevas formas de multiplicar matrices.

## Ejercicio 5

### Modelación

Modelamos el problema utilizando un grafo donde los vértices son las intersecciones entre vías y las aristas son las vías, el enunciado nos dice que cada vía tiene un costo asociado para convertirla en doble vía, el cual es el costo de la arista respectiva.

El problema nos pide encontrar un conjunto de vías que, al convertirlas en doble vía, permitan ir de cualquier punto de la ciudad a cualquier otro utilizando únicamente doble vías y que, además, esto tenga el costo mínimo, es decir, seleccionar un conjunto de aristas con costo mínimo que de como resultado un grafo conexo.

Bajo este planteamiento, vamos a implementar el algoritmo de Kruskal para árboles de expansión de costo mínimo (**MST** por sus siglas en inglés).

### Hipótesis asumidas

- Se asume que el grafo tiene miles de nodos y es sparse, pues con una aproximación sencilla, una ciudad en cuadrícula con 100 calles y 100 carreras tendrá 10000 intersecciones (nodos) y, a lo sumo, 4 vías por intersección (aristas) por cada intersección, claro hay ciudades mucho más grandes y con presencia de puentes y/o túneles, pero en general asumimos un grafo sparse con miles de nodos.

- Se asume que doble vía da lugar a aristas bidireccionales o no dirigidas, si bien es posible asumir en un principio que las aristas son dirigidas, construir una solución al problema que preserve direccionalidad (es decir que las doble vías también son dirigidas), se convierte en el problema de Minimum Strong Spanning Subdigraphs (MSSS), el cual es un problema NP-hard (*Digraphs: Theory, algorithms and applications,  Prof. Jørgen Bang-Jensen, Prof. Gregory Z. Gutin (auth.), pag 483, primera frase de la seccion 12.2*) y por tanto no se dispone de algoritmo eficiente para solucionar el problema para grafos con miles de nodos.

- Se asume que el grafo es conexo, pues en una ciudad debe ser posible transitar desde cualquier punto hacia cualquier otro punto, en caso de aplicar Kruskal a un grano no conex, se obtiene el bosque de expansion minimo, util en ciertos problemas, sin embargo asumimos el grafo es conexo.
  
### Representación de la entrada

Para representar el grafo con el que modelamos la ciudad utilizamos un archivo de texto con las siguientes especificaciones:

- En la primera línea hay enteros separados por espacio representando los nodos (intersecciones de la ciudad) del grafo.
- En la segunda línea hay un entero indicando la cantidad de aristas en el grafo, digamos `m`.
- En las `m` líneas posteriores hay 3 enteros que describen las aristas del grafo, donde `a b c` quiere decir que una hay arista entre el nodo `a` y `b` con costo `c`.

Ejemplo, para un grafo que es un ciclo de 4 elementos con costos consecutivos, el archivo de texto luciría así:

```text
1 2 3 4
4
1 2 1
2 3 2
3 4 3
4 1 4
```

<!-- Es posible encontrar más archivos de ejemplo en la carpeta tests_eje5. -->

### Modo de uso
Una vez que se tiene el archivo de texto con el formato definido, es suficiente con ubicarse en la carpeta donde se encuentra el archivo *ejercicio5_final.py* y ejecutar el comando:

```bash
python ejercicio5_final.py path_to_my_test_file.in path_to_my_output.out
```

Donde ``path_to_my_test_file.in`` es el path al archivo de texto con el grafo que queremos evaluar y ``path_to_my_output.out`` es el path al archivo de texto con el resultado.

Tras ejecutar este comando podremos ver en la consola cómo se imprimen las aristas que se deben convertir en doble vía para cumplir con los requisitos del ejercicio, los resultados salen en el siguiente formato.

- En la primera línea un entero `m` dictando la cantidad de aristas.
- En las `m` líneas posteriores 3 enteros `a b c` dictando que debemos usar la arista que conecta a `a` con `b` y que tiene costo `c`.

Ejemplo:

```text
3
0 1 1
0 2 2
2 3 4
```

---
Santiago Martínez, Pablo Ortega, Estefanía Laverde
