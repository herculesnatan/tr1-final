def remover_contagem_caracteres(signal):
    """
    Desenquadramento por contagem de caracteres.
    Remove o tamanho extraído (2 bytes) e retorna o dado real.
    """
    # Extraímos o tamanho (2 primeiros bytes) do dado
    tamanho_extraido = signal[:16]  # Os primeiros 2 caracteres binários (16 bits)
    # Converter de binário para tamanho inteiro
    tamanho_str = ''.join(str(bit) for bit in tamanho_extraido)
    tamanho_int = int(tamanho_str, 2)
    
    # O dado real vem após o tamanho
    dado = signal[16:16 + tamanho_int * 8]  # Aqui assumimos que cada bit do dado é representado como 8 bits (1 byte)
    
    print(f"Tamanho extraído: {tamanho_int}")
    print(f"Dado desenquadrado_arquivo: {dado}")
    
    return dado




def tira_insercao_bytes(dado, flag="01111110", escape="11111111"):
    """Desenquadramento de dados por inserção de bytes."""
    # Remove as flags de início e fim
    if dado.startswith(flag) and dado.endswith(flag):
        dado = dado[len(flag):-len(flag)]
    else:
        raise ValueError("Dados não estão devidamente enquadrados")

    # Decodificar os dados removendo os escapes
    i = 0
    dados_binarios = []
    while i < len(dado):
        # Se encontrar um escape, verifica o próximo conjunto de bits
        if dado[i:i+len(escape)] == escape:
            # Verifica o próximo conjunto de bits após o escape
            prox = dado[i+len(escape):i+len(escape)+len(flag)]
            if prox == flag:  # escape seguido por flag
                dados_binarios.append(flag)
                i += len(escape) + len(flag)
            elif prox == escape:  # escape seguido por outro escape
                dados_binarios.append(escape)
                i += len(escape) + len(escape)
            else:
                raise ValueError("Sequência de escape inválida")
        else:
            # Se não for escape, adiciona diretamente aos dados
            dados_binarios.append(dado[i])
            i += 1

    # Junta os bits processados e converte para string ASCII
    dados_binarios = ''.join(dados_binarios)
    print(f"tira_insercao_bytes: {dados_binarios}")
    return dados_binarios