import math
import sys

def decode_text(encoded_text: str, codification_dict: dict[str,str]) -> str:
    """
    Decodifica el texto codificado utilizando el diccionario de codificación dado.

    Args:
        encoded_text (str): El texto codificado a decodificar.
        codification_dict (dict[str,str]): El diccionario utilizado para codificar el texto.

    Returns:
        str: El texto decodificado.
    """
    code2char = dict(zip(codification_dict.values(), codification_dict.keys()))

    decoded_text = ''
    temp = ''
    for bit in encoded_text:
        temp += bit
        if temp in codification_dict.values():
            decoded_text += code2char[temp]
            temp = ''
    return decoded_text

def decompress_file(file: str) -> str:
    """
    Descomprime el contenido de un archivo binario y devuelve el texto original.

    Esta función lee un archivo binario, recupera el diccionario de codificación y el texto codificado, y devuelve el texto original después de decodificarlo.

    Args:
        file (str): El nombre del archivo binario a descomprimir.

    Returns:
        str: El texto original descomprimido.
    """

    # Nos aseguramos de que el archivo de entrada termine en .bin
    assert file.endswith('.bin'), "El archivo de salida debe terminar en .bin"

    with open(file, 'rb') as f: 
        
        # Leo el primer byte con la información de la longitud del diccionario
        len_dict_codificacion = int.from_bytes(f.read(1))

        # Recupero el diccionario
        recovered_dict_codificacion = {}
        for _ in range(len_dict_codificacion):

            # Primer byte dedicado al caracter
            char = chr(int.from_bytes(f.read(1)))

            # Segundo byte dedicado a la longitud de la codificacion del caracter
            len_codigo = int.from_bytes(f.read(1))

            # Obtengo los bytes del código y tomo únicamente los bits de la longitud original
            num_bytes_used = math.ceil(len_codigo / 8)
            bits = ''
            for _ in range(num_bytes_used):
                bits += format(int.from_bytes(f.read(1)), '08b')
            
            recovered_dict_codificacion[char] = bits[-len_codigo:]

        # Recupero la longitud del texto codificado
        len_texto_codificado =  int.from_bytes(f.read(4))
        num_bytes_used = math.ceil(len_texto_codificado / 8)

        # Leo los bytes correspondientes y tomo únicamente los bits de la longitud del texto codificado
        bits = ''
        for _ in range(num_bytes_used):
            bits += format(int.from_bytes(f.read(1)), '08b')
        bits_texto = bits[-len_texto_codificado:]

        # Aplico la función de decodificación
        recovered_text = decode_text(bits_texto, recovered_dict_codificacion)

        return recovered_text
    
if __name__ == '__main__':
    file = sys.argv[1]
    print(decompress_file(file))