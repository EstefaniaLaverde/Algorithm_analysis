### Instrucciones de uso

Se implementa la construcción del Suffix Array y el buscador en text_searcher.py, para hacer el arreglo de un archivo y hacer busquedas sobre el mismo se debe ejecutar el siguiente comando. 

```bash
python text_searcher.py text_file.txt query_file.txt output_file.txt
```

Al ejecutar se creará el arreglo de sufijos usando el text_file.txt, se hacen las consultas en query_file.txt y se escriben los resultados en output_file.txt.



### Resultados experimentos

| Text Size  | SA Construction Time (s) | Query Time (1000 queries) (s) | Query Time (10000 queries) (s) | Query Time (100000 queries) (s) | Query Time (1000000 queries) (s) |
|------------|--------------------------:|------------------------------:|-------------------------------:|--------------------------------:|---------------------------------:|
| 100000     |             4.53004074097 |                    0.02151084 |                     0.25097775 |                     2.10677958 |                    19.88251519  |
| 1000000    |            86.66922235489 |                    0.21934485 |                     1.53035140 |                    15.16837525 |                   149.88643622  |
| 10000000   |          1106.87513041496 |                    2.86139059 |                    20.26303315 |                   205.03764653 |                  2018.58034849   |


![alt text](image.png)


