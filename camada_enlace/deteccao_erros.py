def bit_paridade(dado):
    """Adiciona um bit de paridade par ao final da string binária.
    
    Args:
        dado: String contendo apenas caracteres '0' ou '1'
    
    Returns:
        String original com um bit de paridade anexado
    
    Raises:
        ValueError: Se a string contiver caracteres inválidos
    """
    bits_ativos = sum(int(bit) for bit in dado)
    bit_paridade = bits_ativos % 2
    return dado + str(bit_paridade)

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

def crc_receptor(mensagem_com_crc: str) -> str:
    """Verifica a integridade de uma mensagem com CRC-32.
    
    Args:
        mensagem_com_crc: String binária contendo a mensagem + CRC de 32 bits
        
    Returns:
        A mensagem original (sem o CRC) se a verificação for bem-sucedida
        
    Raises:
        ValueError: Se a mensagem for menor que 32 bits ou contiver caracteres inválidos
    """
    # Constantes CRC-32 (padrão Ethernet, ZIP, etc.)
    CRC32_POLYNOMIAL = 0x04C11DB7
    CRC32_XOR_OUT = 0xFFFFFFFF

    
    # Separa mensagem e CRC
    mensagem_bits = mensagem_com_crc[:-32]
    crc_recebido = mensagem_com_crc[-32:]
    
    # Converte para inteiros
    #try:
    mensagem_int = int(mensagem_bits, 2)
    crc_recebido_int = int(crc_recebido, 2)
    #except ValueError:
    #    raise ValueError("Formato binário inválido na mensagem ou CRC")

    
    # Prepara mensagem para cálculo (adiciona 32 zeros)
    mensagem_int <<= 32
    
    # Cálculo do CRC
    for i in range(len(mensagem_bits)):
        if mensagem_int & (1 << (len(mensagem_bits) + 31 - i)):
            shift_amount = len(mensagem_bits) - 1 - i
            mensagem_int ^= CRC32_POLYNOMIAL << shift_amount
    
    # Extrai e ajusta o CRC calculado
    crc_calculado = mensagem_int & 0xFFFFFFFF
    crc_calculado ^= CRC32_XOR_OUT
    
    # Verificação do CRC
    crc_valido = crc_calculado == crc_recebido_int
    
    if crc_valido:
        resultado = "CRC válido: mensagem recebida corretamente."
    else:
        resultado = "Erro: CRC inválido, dados corrompidos."
    print(f"mensagem_bits: {mensagem_bits}")
    return mensagem_bits, resultado, mensagem_bits 