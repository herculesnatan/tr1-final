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
    """Realiza o desenquadramento de dados utilizando a técnica de inserção de bytes.
    
    Parâmetros:
        dado (str): Sequência binária enquadrada contendo os dados
        flag (str): Sequência binária que delimita o quadro (padrão: '01111110')
        escape (str): Sequência binária de escape (padrão: '11111111')
    
    Retorno:
        str: Dados desenquadrados em formato binário
    
    Exceções:
        ValueError: Quando os dados não estão corretamente enquadrados ou contêm sequências inválidas
    """
    # Verificação inicial do enquadramento
    if not (dado.startswith(flag) and dado.endswith(escape)):
        print("Erro de enquadramento: flags inicial/final ausentes")
    
    # Remove flags e pré-calcula comprimentos
    dado_limpo = dado[len(flag):-len(flag)]
    len_flag = len(flag)
    len_escape = len(escape)
    
    # Processamento dos dados
    dados_processados = []
    i = 0
    tamanho_dado = len(dado_limpo)
    
    while i < tamanho_dado:
        # Verifica sequência de escape
        if dado_limpo.startswith(escape, i):
            # Calcula posição do próximo byte após o escape
            prox_pos = i + len_escape
            
            # Verifica se há bytes suficientes após o escape
            if prox_pos + len_flag > tamanho_dado:
                raise ValueError(f"Sequência incompleta após escape na posição {i}")
            
            # Trata os casos especiais
            if dado_limpo.startswith(flag, prox_pos):
                dados_processados.append(flag)
                i += len_escape + len_flag
            elif dado_limpo.startswith(escape, prox_pos):
                dados_processados.append(escape)
                i += len_escape + len_escape
            else:
                raise ValueError(f"Sequência inválida após escape na posição {i}")
        else:
            # Adiciona byte normal ao resultado
            dados_processados.append(dado_limpo[i])
            i += 1
    
    return ''.join(dados_processados)