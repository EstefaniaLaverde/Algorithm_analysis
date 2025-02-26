# Tarea 4 Análisis de Algoritmos
**Autores:** Santiago Martínez - 202510729, Pablo Ortega - 202021700, Estefanía Laverde - 201922512

## Codigos de Shannon-Fano

Se implementan los codigos de Shannon-Fano en shannon_fano.py, para codificar un archivo y obtener el reporte de codificacion sobre un archivo *input_file.txt* y guardar el resultado en *output_file.txt*, debemos ejecutar el comando.

```bash
python shannon_fano.py input_file.txt output_file.txt
```

al ejecutar este comando se hara un print en la terminal con la codificacion, numero de bits esperado, entropia en el peor de los casos y numero total de bits para el texto comprimido, ademas que se guardara la respectiva secuencia de caracteres 0 y 1 en output_file.txt, para obtener compresion efectiva ver seccion el ejercicio bono.

## Ejercicio Bono
Se implementa un sistema de compresión y descompresión de archivos haciendo uso del algoritmo Shannon-Fano. El sistema consta de dos componentes principales: un compresor que convierte archivos de texto en archivos binarios comprimidos, y un descompresor que recupera el texto original.
El proceso de compresión, implementado en *comprimir.py*, toma un archivo de texto y genera un archivo binario (.bin) que contiene tanto el diccionario de codificación como el texto codificado. El diccionario se almacena guardando para cada carácter su representación binaria junto con la longitud de la representación para su recuperación. El texto codificado se almacena con la información de su longitud para asegurar su decodificación.
Por otra parte, el descompresor, implementado en *descomprimir.py*, lee el archivo binario, reconstruye el diccionario de codificación y utiliza esta información para recuperar el texto original.

Para hacer uso de la compresión es necesario ejecutar el comando:

```bash
python comprimir.py test_file.txt output_file.bin
```

Donde *test_file.txt* es un archivo con el texto que se quiere comprimir y *output_file.bin* es el archivo binario comprimido.

Para descomprimir se ejecuta:
```bash
python descomprimir.py output_file.bin
```

donde *output_file.bin* es el binario resultante de la compresión. El texto resultante se imprime en la consola de comandos.