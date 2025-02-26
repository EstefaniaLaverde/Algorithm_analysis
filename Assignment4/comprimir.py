import shannon_fano as sf
import sys

def compress_file(file_input: str, file_output:str) -> None:
    """
    Comprime el contenido de un archivo de texto y lo escribe en un archivo binario.
    
    El contenido del archivo de texto es leído y codificado utilizando el algoritmo de Shannon-Fano. El diccionario de codificación resultante es escrito en un archivo binario, seguido del texto codificado.
    El proceso de escritura incluye la longitud del diccionario, cada caracter y su código correspondiente, y finalmente el el número de bits del texto codificado y el texto codificado con el necesario padding para completar bytes.
    
    Args:
        file_input (str): El nombre del archivo de texto a comprimir.
        file_output (str): El nombre del archivo binario comprimido.
    
    Returns:
        None: El contenido del archivo de texto es comprimido y escrito en un archivo binario.
    """
    # Nos aseguramos de que el archivo de salida termine en .bin
    assert file_output.endswith('.bin'), "El archivo de salida debe terminar en .bin"

    # Lectura del archivo con el texto
    with open(file_input, 'r') as f:
        text = f.read()

    # Obtención de la codificacion del texto y el diccionario con los códigos correspondientes
    codif_text, dict_codification = sf.get_code_shannon_fano(text)

    # Inicializamos la escritura de un archivo binario
    with open(file_output, 'wb') as f:

        # Se guarda la longitud del diccionario en un byte
        f.write(len(dict_codification).to_bytes(1))
        
        for char, cod in dict_codification.items():

            # Se guarda un byte por caracter
            f.write(ord(char).to_bytes(1)) 

            # Calcula el padding para cada código
            len_codigo = len(cod)
            len_padding = (8 - (len_codigo % 8)) % 8
            padded_cod = '0'*len_padding+cod

            # Guardamos la longitud del código
            f.write(len_codigo.to_bytes(1))

            # Se guardan los bytes del código con padding
            for i in range(0,len(padded_cod),8):
                byte = padded_cod[i:i+8]
                f.write(int(byte,2).to_bytes(1))

        # Guardo la longitud del texto codificado
        len_codificacion = len(codif_text)
        f.write(len_codificacion.to_bytes(4)) # aqui asumo que la longitud del texto codificado no va a tener más de 4 bytes ((2³² - 1) bits)

        # Añado padding
        len_padding = (8 - (len_codificacion % 8)) % 8
        padded_codificacion_texto = '0'*len_padding+codif_text

        # Guardo cada byte del texto codificado
        for i in range(0,len(padded_codificacion_texto),8):
                byte = padded_codificacion_texto[i:i+8]
                f.write(int(byte,2).to_bytes(1))

if __name__ == "__main__":
    file_input = sys.argv[1]
    file_output = sys.argv[2]
    compress_file(file_input, file_output)