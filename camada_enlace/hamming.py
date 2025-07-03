def hamming_encode(data):
    """Codifica o dado usando código Hamming."""

    # Etapa 1: Calcular quantos bits de paridade (r) são necessários 
    # n é o número de bits de dados que queremos enviar.
    n = len(data)
    # r é o número de bits de paridade que vamos adicionar.
    r = 1
    # A fórmula de Hamming diz que 2^r deve ser maior ou igual ao número total de bits 
    # na mensagem final (dados + paridade) mais 1. Ou seja, 2^r >= n + r + 1.
    # Este loop encontra o menor 'r' que satisfaz essa condição.
    while (2 ** r) < (n + r + 1):
        r += 1

    # Etapa 2: Preparar a lista para a mensagem codificada e inserir os bits de dados
    # A mensagem final terá tamanho n + r.
    # Inicializamos uma lista de zeros com o tamanho total da mensagem.
    encoded = [0] * (n + r)
    # 'j' será o índice para percorrer os bits de dados originais.
    j = 0
    # Percorremos as posições da futura mensagem codificada (de 1 a n+r).
    # As posições que são potências de 2 (1, 2, 4, 8, ...) são reservadas para os bits de paridade.
    for i in range(1, len(encoded) + 1):
        # A expressão 'i & (i - 1) == 0' é uma forma rápida de verificar se 'i' é uma potência de 2.
        # Se for uma potência de 2, pulamos a posição, pois ela é para um bit de paridade.
        # o & é o operador lógico AND, compara bits
        if i & (i - 1) == 0:
            continue
        # Se não for uma potência de 2, é uma posição de dado.
        # Colocamos o bit de dado original na posição correspondente.
        encoded[i - 1] = int(data[j])
        j += 1

    # Etapa 3: Calcular o valor de cada bit de paridade
    # Agora, vamos calcular o valor (0 ou 1) para cada bit de paridade.
    for i in range(r):
        # A posição do bit de paridade atual (P1, P2, P4, ...). Ex: 2**0=1, 2**1=2, 2**2=4.
        parity_pos = 2 ** i
        # Usaremos o operador XOR (^) para calcular a paridade.
        parity = 0
        # Percorremos todas as posições da mensagem para ver quais delas este bit de paridade verifica.
        for j in range(1, len(encoded) + 1):
            # Um bit de paridade na posição 'parity_pos' verifica todos os bits nas posições 'j'
            # onde a operação 'j & parity_pos' (bitwise AND) for diferente de zero.
            if j & parity_pos:
                # O XOR ( ^ ) acumula a paridade. Se o número de '1's for par, o resultado é 0. Se for ímpar, é 1.
                parity ^= encoded[j - 1]
        
        # Inserimos o valor de paridade calculado na sua posição reservada.
        encoded[parity_pos - 1] = parity

    # --- Etapa 4: Retornar a mensagem codificada como uma string ---
    return ''.join(map(str, encoded))


def hamming_encode_receptor(received_data):
    """
    Verifica e corrige erros em uma mensagem codificada com Hamming.
    """
    
    # --- Etapa 1: Preparar os dados recebidos ---
    # Converte a string de bits recebida para uma lista de inteiros para facilitar os cálculos.
    data = [int(bit) for bit in received_data]
    
    # --- Etapa 2: Calcular o número de bits de paridade (r) na mensagem recebida ---
    r = 0
    # Com base no tamanho total da mensagem recebida, descobrimos quantos bits de paridade ela contém.
    while (2 ** r) < len(data):
        r += 1

    # --- Etapa 3: Recalcular a paridade para encontrar a posição do erro ---
    # 'error_pos' guardará a posição do bit com erro. Se for 0 no final, não há erro.
    error_pos = 0
    # Para cada bit de paridade que deveria existir na mensagem...
    for i in range(r):
        # Pega a posição do bit de paridade (1, 2, 4, 8, ...).
        parity_pos = 2 ** i
        # Recalcula a paridade para o grupo de bits que este bit de paridade verifica.
        parity = 0
        # O loop percorre todas as posições da mensagem recebida.
        for j in range(1, len(data) + 1):
            # A verificação é a mesma da codificação: P_k verifica a posição j se (j & k != 0).
            if j & parity_pos:
                # O XOR agora inclui o bit de paridade que foi recebido.
                # Se não houver erro neste grupo, o resultado do XOR de todos os bits (dados + paridade) será 0.
                parity ^= data[j - 1]
        
        # Se a paridade calculada for 1 (diferente de 0), significa que este grupo tem um erro.
        if parity != 0:
            # Adicionamos a posição do bit de paridade com falha à variável 'error_pos'.
            # A soma das posições dos bits de paridade que falham aponta exatamente para a posição do erro.
            # Isso é chamado de "síndrome do erro".
            error_pos += parity_pos

    # --- Etapa 4: Corrigir o erro, se houver ---
    # Se 'error_pos' for maior que 0, encontramos um erro de um único bit.
    if error_pos > 0:
        print(f"Erro encontrado na posição: {error_pos}")
        # Usamos XOR com 1 para inverter o bit na posição do erro (0 vira 1, 1 vira 0).
        data[error_pos - 1] ^= 1
    else:
        print("Nenhum erro encontrado na mensagem.")
    
    # --- Etapa 5: Extrair a mensagem original (sem os bits de paridade) ---
    # Agora que a mensagem está (potencialmente) corrigida, removemos os bits de paridade.
    corrected_message = []
    # Percorremos as posições da mensagem.
    for i in range(1, len(data) + 1):
        # 'i & (i - 1) != 0' verifica se a posição 'i' NÃO é uma potência de 2.
        # Ou seja, selecionamos apenas as posições que contêm bits de dados.
        if i & (i - 1) != 0:
            corrected_message.append(data[i - 1])
    
    # Retornamos a mensagem original e corrigida como uma string.
    return ''.join(map(str, corrected_message))
