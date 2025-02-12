# Tarea 2 Análisis de Algoritmos

## Implementación
En el archivo **Assignment2** se implementan los algoritmos de Push-Relabel y Edmonds-Karp. Estos algoritmos resuelven el problema de flujo máximo en una red de flujo.  Ambos algoritmos se ejecutan sobre un archivo de input con las siguientes características:

- La primera línea debe tener la cantidad de nodos de la red N. Se asume que el primer nodo (el cero) es la fuente y el último (el N-1) el destino.

- Las siguientes líneas tienen tres números que representan la información de ejes de la red. El primero es el id de nodo origen (de 0 a N-2), el segundo es el id de nodo destino (de 1 a N-1). El tercero es la capacidad del eje.

## Ejecución

Una vez que se tiene el archivo de texto con el formato definido, es suficiente con ejecutar el comando:

```bash
python assignment1.py test_file.in output_file.out
```

Donde *test_file.in* es el archivo de texto con el grafo que queremos evaluar y *output_file.out* es el archivo con el resultado de ambos algoritmos. El output cuenta con el flujo máximo por eje, el valor del flujo máximo y el tiempo de ejecución.

## Ejemplo

Input:
```
4
0 1 2
0 2 3
1 3 2
2 3 1
```

Output:
```
Results Edmonds Karp
0 1 2
0 2 1
1 3 2
2 3 1
3
0.0
Results Push Relabel
0 1 2
0 2 1
1 3 2
2 3 1
3
0.0
```