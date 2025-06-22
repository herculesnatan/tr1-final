def bit_paridade(dado):
    """Adiciona bit de paridade par ao final do dado."""
    paridade = sum(int(bit) for bit in dado) % 2
    return f"{dado}{paridade}"

def crc(mensagem_bits: str):

    # Polinômio padrão do CRC-32 (IEEE 802.3)
    CRC32_POLYNOMIAL = 0x04C11DB7
    CRC32_XOR_OUT = 0xFFFFFFFF  # XOR final
    
    # Converte a string de bits em um número inteiro
    mensagem = int(mensagem_bits, 2)

    # Adiciona 32 zeros à direita (equivalente a multiplicar por 2^32)
    mensagem <<= 32

    # Obtém o tamanho da mensagem (em bits)
    tamanho = len(mensagem_bits)

    # Aplica a divisão binária módulo 2
    for i in range(tamanho):
        if mensagem & (1 << (tamanho + 31 - i)):  # Verifica se o bit mais à esquerda é 1
            mensagem ^= CRC32_POLYNOMIAL << (tamanho - 1 - i)  # Aplica o XOR com o polinômio deslocado

    # O CRC final são os 32 bits menos significativos
    crc = mensagem & 0xFFFFFFFF

    # Aplica a inversão final (XOR com 0xFFFFFFFF)
    crc ^= CRC32_XOR_OUT

    # Converte o CRC para string binária de 32 bits
    crc_bin = f"{crc:032b}"

    # Retorna a mensagem original + CRC calculado
    return mensagem_bits + crc_bin


def bit_paridade_receptor(dado):
    """Verifica se o bit de paridade par no final do dado está correto."""
    # Divide os dados entre o conteúdo e o bit de paridade
    dado_sem_paridade = dado[:-1]  # Todos os bits, exceto o último
    bit_paridade_recebido = int(dado[-1])  # Último bit é o bit de paridade
    
    # Calcula a paridade do dado recebido
    paridade_calculada = sum(int(bit) for bit in dado_sem_paridade) % 2
    
    # Compara a paridade calculada com o bit de paridade recebido
    if paridade_calculada == bit_paridade_recebido:
        resultado = "Não há erro: o bit de paridade é válido."
    else:
        resultado = "Há erro: o bit de paridade não é válido."
    
    return dado_sem_paridade, resultado



def crc_receptor(mensagem_com_crc: str):
    CRC32_POLYNOMIAL = 0x04C11DB7
    CRC32_XOR_OUT = 0xFFFFFFFF  # XOR final
    # Separar a mensagem original e o CRC recebido
    mensagem_bits = mensagem_com_crc[:-32]  # Mensagem original
    crc_recebido = mensagem_com_crc[-32:]   # Últimos 32 bits são o CRC

    # Converte para inteiro
    mensagem = int(mensagem_bits, 2)
    crc_recebido_int = int(crc_recebido, 2)

    # Adiciona 32 zeros para realizar a divisão
    mensagem <<= 32

    # Obtém o tamanho da mensagem original (sem CRC)
    tamanho = len(mensagem_bits)

    # Aplica a divisão binária módulo 2
    for i in range(tamanho):
        if mensagem & (1 << (tamanho + 31 - i)):  # Se o bit mais à esquerda for 1
            mensagem ^= CRC32_POLYNOMIAL << (tamanho - 1 - i)  # XOR com polinômio deslocado

    # O CRC calculado são os últimos 32 bits
    crc_calculado = mensagem & 0xFFFFFFFF

    # Aplica XOR final (padrão CRC-32)
    crc_calculado ^= CRC32_XOR_OUT

    # Verifica se o CRC recebido é igual ao CRC calculado
    crc_valido = (crc_calculado == crc_recebido_int)

    if crc_valido:
        print("CRC válido: mensagem recebida corretamente.")
    else:
        print("Erro: CRC inválido, dados corrompidos.")

    return mensagem_bits