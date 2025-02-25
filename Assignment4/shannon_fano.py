import math


def print_codification_report(counts,codification):
    #hacer prints con reportes de la codificacion
    #la codificacion
    #numero de bits esperado
    #entropia en el peor de los casos
    #numero total de bits para el texto comprimodo

    print('codification:')
    print(sorted(list(codification.items())))

    text_len=sum(counts.values())


    expected_bit_count=0
    for c,count in counts.items():
        expected_bit_count+=(count/text_len)*len(codification[c])
    print('expected bit count per character:',expected_bit_count)


    print('worst case entropy:',math.log2(len(counts)))


    total_bits_compr=0
    for c,count in counts.items():
        total_bits_compr+=count*len(codification[c])

    print('total bits on compressed file:',total_bits_compr)


#convierte un str de 0 y 1 en el int que representan en binario
def str_bin_to_int(s):
    ans=0
    mul=1
    for c in s[::-1]:
        ans+=(ord(c)-ord('0'))*mul
        mul*=2
    return ans

def int_to_str_bin(val):
    s=[]

    while val:
        if val%2:
            s.append('1')
        else:
            s.append('0')

        val=val//2

    s.reverse()
    s=''.join(s)

    return s

def get_code_shannon_fano(text):
    counts={}

    for c in text:
        if c not in counts:
            counts[c]=0
        counts[c]+=1

    freqs={}
    text_size=len(text)
    for c,count in counts.items():
        freqs[c]=count/text_size

    #obtener listado caracteres segun frecuencia
    cs=list(counts.values())
    cs=sorted(cs,key=lambda x: freqs[x],reverse=True)

    L=[math.ceil(math.log2(1/freqs[c])) for c in cs]

    codification={}
    codification[cs[0]]='0'*L[0]
    for i in range(1,len(cs)):
        last_cod=codification[cs[i-1]]
        current_cod=str_bin_to_int(last_cod)+1
        current_cod=int_to_str_bin(current_cod)
        #rellenar de 0 para quedar con longitud igual al anterior
        current_cod='0'*(L[i-1]-len(current_cod))+current_cod
        #agregar 0 al final segun el algoritmo
        current_cod=current_cod+'0'*(L[i]-L[i-1])

        codification[cs[i]]=current_cod

    print_codification_report(counts,codification)

    return codification