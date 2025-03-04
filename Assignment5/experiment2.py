import time
import pandas as pd
from generate_text import generate_text_file, generate_query_file
from text_searcher import solve_querys, suffix_array, get_positions
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
        test_file='tests/text_file_'+str(t_size)+'.txt'

        with open(test_file) as f:
            text=f.read()

        start=time.time()
        suff_arr=suffix_array(text)
        end=time.time()

        print('t_size suffix array construction',t_size,end-start)

        for j,q_size in enumerate(query_file_sizes):
            print('experimenting values:',t_size,q_size)

            query_file='tests/query_file_'+str(q_size)+'.txt'

            with open(query_file) as f:
                querys=f.read()
            querys=querys.split('\n')


            start=time.time()
            result_file='tests2/result_file_'+str(t_size)+'_'+str(q_size)+'.txt'
            """with open(result_file,'w') as f:
                for q in querys:
                    pos=get_positions(text,suff_arr,q)
                    f.write(q)
                    for p in pos:
                        f.write('\t'+str(p))
                    f.write('\n')
            end=time.time()"""

            start=time.time()
            for q in querys:
                pos=get_positions(text,suff_arr,q)
            end=time.time()


            print('query time',q_size,end-start)

            execution_times[i][j]=end-start

    
    df=pd.Dataframe(execution_times,columns=query_file_sizes,index=text_file_sizes)
    print(df)

    df.to_excel('results_experiment2.xlsx')


