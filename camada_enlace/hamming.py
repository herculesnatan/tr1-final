def hamming_encode(data):
    """Codifica o dado usando código Hamming."""
    n = len(data)
    r = 1
    while (2 ** r) < (n + r + 1):
        r += 1

    encoded = [0] * (n + r)
    j = 0
    for i in range(1, len(encoded) + 1):
        if i & (i - 1) == 0:
            continue
        encoded[i - 1] = int(data[j])
        j += 1

    for i in range(r):
        parity_pos = 2 ** i
        parity = 0
        for j in range(1, len(encoded) + 1):
            if j & parity_pos:
                parity ^= encoded[j - 1]
        encoded[parity_pos - 1] = parity

    return ''.join(map(str, encoded))


def hamming_encode_receptor(received_data):
    """
    Verifica e corrige erros em uma mensagem codificada com Hamming.
    """
    # Converte a mensagem recebida para uma lista de inteiros
    data = [int(bit) for bit in received_data]
    
    # Calcula o número de bits de paridade (r)
    r = 0
    while (2 ** r) < len(data):
        r += 1

    # Verifica os bits de paridade para encontrar o erro
    error_pos = 0
    for i in range(r):
        parity_pos = 2 ** i
        parity = 0
        for j in range(1, len(data) + 1):
            if j & parity_pos:
                parity ^= data[j - 1]
        if parity != 0:
            error_pos += parity_pos

    # Corrige o erro, se encontrado
    if error_pos > 0:
        print(f"Erro encontrado na posição: {error_pos}")
        data[error_pos - 1] ^= 1  # Inverte o bit com erro
    else:
        print("Nenhum erro encontrado na mensagem.")
    
    # Retorna a mensagem corrigida (sem bits de paridade)
    corrected_message = []
    for i in range(1, len(data) + 1):
        if i & (i - 1) != 0:  # Ignora as posições de paridade
            corrected_message.append(data[i - 1])
    
    return ''.join(map(str, corrected_message))