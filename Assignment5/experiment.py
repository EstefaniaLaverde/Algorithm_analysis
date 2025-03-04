import time
import pandas as pd
from generate_text import generate_text_file, generate_query_file
from text_searcher import solve_querys
import os


if __name__=='__main__':
    text_file_sizes=[100000,1000000,10000000]
    query_file_sizes=[1000,10000,100000,1000000]


    for t_size in text_file_sizes:
        test_file='tests/text_file_'+str(t_size)+'.txt'
        if not os.path.exists(test_file):
            generate_text_file(test_file,t_size)

    for q_size in query_file_sizes:
        query_file='tests/query_file_'+str(q_size)+'.txt'
        if not os.path.exists(query_file):
            generate_query_file(query_file,q_size)

    execution_times=[[0 for i in range(len(query_file_sizes))] for j in range(len(text_file_sizes))]
    for i,t_size in enumerate(text_file_sizes):
        for j,q_size in enumerate(query_file_sizes):
            print('experimenting values:',t_size,q_size)

            test_file='tests/text_file_'+str(t_size)+'.txt'
            query_file='tests/query_file_'+str(q_size)+'.txt'
            result_file='tests/result_file_'+str(t_size)+'_'+str(q_size)+'.txt'

            time_result=solve_querys(test_file,query_file,result_file)

            print(time_result)

            execution_times[i][j]=time_result
    
    df=pd.Dataframe(execution_times,columns=query_file_sizes,index=text_file_sizes)
    print(df)



