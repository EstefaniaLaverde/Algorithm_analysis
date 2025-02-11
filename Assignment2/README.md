# Tarea 2 Análisis de Algoritmos

## Edmonds-Karp

Se realiza la implementación del algoritmo Edmonds-Karp en el archivo `edmonds_karp.py`, en el cual se implementa la técnica de búsqueda en anchura con el algoritmo *Ford-Fulkerson* para hallar flujo maximal en una red de flujos. 

El input a la implementación debe ser un archivo con las siguientes características:
- La primera linea debe tener la cantidad de nodos de la red N. Se asume que el primer nodo (el cero) es la fuente y el último (el N-1) el destino.

- Las siguientes lineas tienen tres números que representan la información de ejes de la red. El primero es el id de nodo origen (de 0 a N-2), el segundo es el id de nodo destino (de 1 a N-1). El tercero es la capacidad del eje.

Para ejecutar el archivo, se debe usar el siguiente comando:

```bash
python edmonds_karp.py my_test_file.in my_output.out
```

Donde `my_test_file.in` es el  archivo de texto con el grafo que queremos evaluar que cuente con las características del archivo de entrada y `my_output.out` es el archivo de texto con el resultado.

El output cuenta con el flujo máximo por eje, el valor del flujo máximo y el tiempo de ejecución.

### Ejemplos

Input

```
4
0 1 2
0 2 3
1 3 2
2 3 1
```

Ouput
```
0 1 3
0 2 9
1 2 3
2 4 12
12
0.0
```

## Push-Relabel
Se realiza la implementación del algoritmo Push-Relabel en el archivo `push_relabel.py`, en el cual se implementa la técnica de preflujo y reetiquetado para hallar flujo maximal en una red de flujos. 

El input a la implementación es un archivo con las mismas características que el descrito para [Edmonds-Karp](#edmonds-karp)

Para ejecutar el archivo, se debe usar el siguiente comando:



Para ejecutar el archivo, se debe usar el siguiente comando:

```bash
python edmonds_karp.py my_test_file.in my_output.out
```

Donde `my_test_file.in` es el  archivo de texto con el grafo que queremos evaluar que cuente con las características del archivo de entrada y `my_output.out` es el archivo de texto con el resultado.

El output cuenta con el flujo máximo por eje, el valor del flujo máximo y el tiempo de ejecución.

### Ejemplos

Input

```
5
0 1 4
0 2 9
1 2 3
2 4 13
```

Output
```
0 1 3
0 2 9
1 2 3
2 4 12
12
0.0
```