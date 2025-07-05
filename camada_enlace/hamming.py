def hamming_encode(data):
    """Codifica o dado usando código Hamming."""

    # Calcular quantos bits de paridade (r) são necessários 
    # n é o número de bits de dados que queremos enviar.
    n = len(data)
    # r é o número de bits de paridade que vamos adicionar.
    r = 1
    # A fórmula de Hamming diz que 2^r deve ser maior ou igual ao número total de bits 
    # na mensagem final (dados + paridade) mais 1. Ou seja, 2^r >= n + r + 1.
    # Este loop encontra o menor 'r' que satisfaz essa condição.
    while (2 ** r) < (n + r + 1):
        r += 1

   # A mensagem final terá tamanho n + r.
    encoded = [0] * (n + r)
    j = 0

    # As posições que são potências de 2 (1, 2, 4, 8, ...) são reservadas para os bits de paridade.
    for i in range(1, len(encoded) + 1):
    # Se for uma potência de 2, pulamos a posição, pois ela é para um bit de paridade.
    # o & é o operador lógico AND, compara bits
        if i & (i - 1) == 0:
            continue
        encoded[i - 1] = int(data[j])
        j += 1

    # calcular se vai ser 0 ou 1 para cada bit de paridade
    for i in range(r):
        parity_pos = 2 ** i
        parity = 0

        # Um bit de paridade na posição 'parity_pos' verifica todos os bits nas posições 'j'
        # onde a operação 'j & parity_pos' (bitwise AND) for diferente de zero.
        for j in range(1, len(encoded) + 1):
            if j & parity_pos:
                # O XOR ( ^ ) acumula a paridade. Se o número de '1's for par, o resultado é 0. Se for ímpar, é 1.
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
        error_detected = "houve um bit alterado e corrigido durante a transmissão"
    
    else:
        print("Nenhum erro encontrado na mensagem.")
        error_detected = "nada"
    
    # Retorna a mensagem corrigida (sem bits de paridade)
    corrected_message = []
    for i in range(1, len(data) + 1):
        if i & (i - 1) != 0:  # Ignora as posições de paridade
            corrected_message.append(data[i - 1])

    return ''.join(map(str, corrected_message)), error_detected 
