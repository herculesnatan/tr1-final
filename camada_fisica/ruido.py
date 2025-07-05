import random as r


err_tax = 0.3


def flip_random_bit(binary_list):
    # Faz uma cópia da lista original
    binary_list_copy = list(binary_list)

    # simulando um possíel erro
    if r.random() < err_tax:
        #limitando a 1 bit de erro no máx
        i = r.randint(0, len(binary_list_copy) - 1)
        binary_list_copy[i] = '1' if binary_list_copy[i] == '0' else '0'
    
    # Retorna a cópia alterada
    return ''.join(binary_list_copy)

