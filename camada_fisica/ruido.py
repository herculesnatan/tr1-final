import random as rand

 #todo - Arrumar - melhorar taxa de erro que sempre tem aparecer
taxa_de_erro = 0.0001
def flip_random_bit(binary_list):
    # Faz uma cópia da lista original
    binary_list_copy = list(binary_list)
    
    # Percorre cada bit individualmente
    for i in range(len(binary_list_copy)):
        if rand.random() < taxa_de_erro:  # Probabilidade de alteração para cada bit
            binary_list_copy[i] = '1' if binary_list_copy[i] == '0' else '0'
    
    # Retorna a cópia alterada
    return ''.join(binary_list_copy)

