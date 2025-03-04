import pandas as pd

text_file_sizes=[100000,1000000,10000000]
query_file_sizes=[1000,10000,100000,1000000]

#eje 0 varia t_size
#eje1 varia q_size
values=[[0.0215108,0.2509777,2.10677957,19.8825151],
        [0.21934485,1.5303514003,15.1683752536,149.886436223],
        [2.861390590667,20.2630331516,205.0376465,2018.580348491]]

df=pd.DataFrame(values,columns=['query_size'+str(q) for q in query_file_sizes],
                index=['test_file_size'+str(t) for t in text_file_sizes])

print(df.to_markdown())