def binario_para_texto(binario):
    """Converte uma string binária para texto usando a tabela ASCII."""
    texto = ""
    
    # Verificar se a string binária é múltipla de 8 bits
    #if len(binario) % 8 != 0:
        #raise ValueError("A string binária deve ter um comprimento múltiplo de 8 bits.")

    # Iterar sobre a string binária em blocos de 8 bits
    for i in range(0, len(binario), 8):
        byte = binario[i:i+8]  # Pega cada bloco de 8 bits
        char = chr(int(byte, 2))  # Converte o byte para caractere usando a tabela ASCII
        texto += char
    
    return texto