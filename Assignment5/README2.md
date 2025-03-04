# Tarea 5

## Implementacion

Para hacer la construccion del suffix array, representamos cada sufijo por el indice donde comienzan, teniendo esta representan damos solucion al problema de ordenar dicho arreglo.

Inicialmente ordenamos el arreglo de indices segun la primera letra del respectivo sufijo, note entonces ahora por induccion, si tenemos el arreglo de indices ordenado por las primeras h letras del respectivo sufijo, es facil ordenar por las primeras 2*h letras de los sufijos, pues primero podemos comparar las primeras h letras, si aqui se define la comparacion entonces bien, en caso contrario debemos comparar el siguiente grupo de h letras posterior a los sufijos, para ejemplificar esto suponga estamos comparando los sujifos con indices i,j, para comparar el segundo grupo de h letras posterior a los sufijos hacemos la comparacion de los sufijos i+h, j+h, con los resultados de comparacion para h letras.

Al aplicar esta idea vemos que h puede duplicarse a lo sumo O(ln(n)) veces con n el tamaño del string, si el paso de ordenamiento lo hacemos en tiempo lineal con radix sort, obtenemos un algoritmo O(n*ln(n)) para la creacion del suffix array.

Teniendo el suffix array podemos hacer busquedas de substring usando busqeuda binaria, suponga el substring a buscar tiene tamaño m, por eficiencia al hacer la busqueda binaria en vez de comparar todo el substring con todo el sufijo cantidato, hacemos m rondas de busqueda binaria, en la primera ronda obtenemos un rango donde el prime caracter de los respectivos sufijos corresponde al primer caracter del substring, siguiendo esta idea en la ronda j obtenemos un rango donde los primeros j caracteres de los sufijos en el rango corresponden a los primeros j caracteres del substring, sin en algun punto de esta busqueda no se logra obtener correspondencia del respectivo caracter en evaluacion retornamos que no hay coincidencia, si el algoritmo se ejecuta hasta el final, los sufijos en el rango encontrado corresponden a las instancias del substring dentro de la base de datos.

Una ronda de busqueda binaria tiene costo O(ln(n)) por tanto m rondas tienen costo O(m*ln(n)).

## Modo de uso

Para procesar un archivo de texto que como nuestra base de datos y un archivo de querys con substrings que queremos buscar en la base de datos, podemos producir un archivo con las posiciones donde aparece cada suvbstring dentro de la base de datos, usamos el comando.

´´´shell
python test_searcher.py text_file.txt query_file.txt output_file.txt
´´´

donde text_file.txt es el path a un archivo .txt txt donde queremos buscar substrings, query_file.txt es el path a un archivo archivo .txt donde cada linea tiene un substring que queremos buscar en la base de datos y output_file.txt es el path donde queremos que se guarden los resultados de la busqueda, en cada linea queda el substring de la busqueda y posteriormente separado por tabs los indices con las posiciones donde el substring aparece en la base de datos.

## Experimentos

Como se indica en el enunciado se miden tiempos de ejecucion usando archivo de texto con tamaños de cien mil, un millon y 10 millones de caracteres y con archivos con mil, diez mil, cien mil y un millon de consultas, los archivos se generan aleatoriamente usando caracteres alfabeticos, para los consultas ponemos un tamaño maximo de 12 caracteres por consulta, este valor busca emular la longitud de una palabra larga en lenguaje natural, y tambien nos asegura los tiempos no sea demasiado largos, el algoritmo soporta busqueda de palabras de longitud arbitraria (segun capacidad de la maquina).

|                        |   query_size1000 |   query_size10000 |   query_size100000 |   query_size1000000 |
|:-----------------------|-----------------:|------------------:|-------------------:|--------------------:|
| test_file_size100000   |        0.0215108 |          0.250978 |            2.10678 |             19.8825 |
| test_file_size1000000  |        0.219345  |          1.53035  |           15.1684  |            149.886  |
| test_file_size10000000 |        2.86139   |         20.263    |          205.038   |           2018.58   |
