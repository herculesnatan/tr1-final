import random as r

err_tax = 0.001

def flip_random_bit(binary_list):
    # Faz uma cópia da lista original
    binary_list_copy = list(binary_list)
    
    # Percorre cada bit individualmente
    for i in range(len(binary_list_copy)):
        if r.random() < err_tax:  # Probabilidade de alteração para cada bit
            binary_list_copy[i] = '1' if binary_list_copy[i] == '0' else '0'
    
    # Retorna a cópia alterada
    return ''.join(binary_list_copy)
