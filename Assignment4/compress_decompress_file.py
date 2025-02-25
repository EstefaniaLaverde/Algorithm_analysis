import shannon_fano as sf

text = 'test_text/test_file.txt'


def char_to_bin(char):
    return format(ord(char), '08b')

def bin_to_char(binary):
    return chr(int(binary, 2))

def compress_text(file):
    with open(file, 'r') as f:
        text = f.read()
    codif_text, dict_codification = sf.get_code_shannon_fano(text)
    with open('compressed_file.txt', 'w') as file:
        file.write(bin(len(dict_codification))[2:] + '\n')
        for key, value in dict_codification.items():
            file.write(char_to_bin(key) + ' ' + value + '\n')
        file.write(codif_text)

def decode_text(encoded_text, codification_dict):
    code2char = dict(zip(codification_dict.values(), codification_dict.keys()))

    decoded_text = ''
    temp = ''
    for bit in encoded_text:
        temp += bit
        if temp in codification_dict.values():
            decoded_text += code2char[temp]
            temp = ''
    return decoded_text


def decompress(file):
    with open(file, 'r') as f:
        lines = f.readlines()
        num_chars = int(lines[0].strip(),2)
        dict_codification = {}
        for i in range(1,num_chars+1):
            char, code = lines[i].strip().split()
            dict_codification[bin_to_char(char)] = code
        codif_text = lines[-1].strip()

        return decode_text(codif_text, dict_codification)
    

def compress_text_gpt(file):
    with open(file, 'r') as f:
        text = f.read()
    codif_text, dict_codification = sf.get_code_shannon_fano(text)
    
    # Convert the binary string to actual bytes
    # Pad the encoded text to ensure it's a multiple of 8
    padding_length = (8 - len(codif_text) % 8) % 8
    codif_text += '0' * padding_length
    
    # Convert binary string to bytes
    encoded_bytes = bytes(int(codif_text[i:i+8], 2) for i in range(0, len(codif_text), 8))
    
    with open('compressed_file.bin', 'wb') as file:
        # Write dictionary length as 4 bytes
        file.write(len(dict_codification).to_bytes(4, byteorder='big'))
        # Write padding length as 1 byte
        file.write(padding_length.to_bytes(1, byteorder='big'))
        
        # Write each character and its code
        for char, code in dict_codification.items():
            # Write character as 1 byte
            file.write(ord(char).to_bytes(1, byteorder='big'))
            # Write code length as 1 byte
            file.write(len(code).to_bytes(1, byteorder='big'))
            # Write code as bytes
            code_padded = code + '0' * ((8 - len(code) % 8) % 8)
            code_bytes = bytes(int(code_padded[i:i+8], 2) for i in range(0, len(code_padded), 8))
            file.write(code_bytes)
        
        # Write encoded text
        file.write(encoded_bytes)

def decompress_gpt(file):
    with open(file, 'rb') as f:
        # Read dictionary length
        dict_size = int.from_bytes(f.read(4), byteorder='big')
        # Read padding length
        padding_length = int.from_bytes(f.read(1), byteorder='big')
        
        # Read dictionary
        dict_codification = {}
        for _ in range(dict_size):
            # Read character
            char = chr(int.from_bytes(f.read(1), byteorder='big'))
            # Read code length
            code_length = int.from_bytes(f.read(1), byteorder='big')
            # Read code bytes and convert to binary string
            code_bytes_length = (code_length + 7) // 8
            code_bytes = f.read(code_bytes_length)
            code_bin = ''.join(format(byte, '08b') for byte in code_bytes)
            # Get actual code by removing padding
            code = code_bin[:code_length]
            dict_codification[char] = code
        
        # Read encoded text
        encoded_bytes = f.read()
        encoded_text = ''.join(format(byte, '08b') for byte in encoded_bytes)
        # Remove padding from encoded text
        encoded_text = encoded_text[:-padding_length] if padding_length else encoded_text
        
        return decode_text(encoded_text, dict_codification)

compress_text_gpt('test_text/test_file.txt')

print(decompress_gpt('compressed_file.bin'))