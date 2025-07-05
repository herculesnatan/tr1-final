from camada_fisica.ruido import  flip_random_bit
def contagem_caracteres(dado, tamanho):
    """Enquadramento por contagem de caracteres."""
    # Converter o tamanho original para string
    tamanho_str = f"{tamanho:02d}"
    
    # Transformar cada caractere (dígito) para binário ASCII
    tamanho_binario_ascii = ''.join(format(ord(char), '08b') for char in tamanho_str)
    dado_ruido = flip_random_bit(dado)
    print(f"Dado original    : {dado}")
    print(f"Dado após o ruido: {dado_ruido}")

    return f"{tamanho_binario_ascii}{dado_ruido}"

def insercao_bytes(dado, flag="01111110", escape="11111111"):

    # Inicializar dados enquadrados
    dados_enquadrados = ""
    
    # Percorrer cada byte (8 bits) nos dados binários
    for i in range(0, len(dado), 8):
        byte = dado[i:i+8]  # Obter um byte
        
        # Adicionar o escape antes de qualquer ocorrência da flag ou do escape
        if byte == flag or byte == escape:
            dados_enquadrados += escape
        
        # Adicionar o byte atual
        dados_enquadrados += byte


    dado_ruido = flip_random_bit(dados_enquadrados)

    print(f"Dado original    : {dados_enquadrados}")
    print(f"Dado após o ruido: {dado_ruido}")
    # Retornar os dados com a flag no início e no final
    return f"{flag}{dado_ruido}{flag}"


