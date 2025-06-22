import numpy as np

def nrz_modulation(data: int):
    """Modulação NRZ: 0 -> -1, 1 -> +1"""
    return np.array([-1 if bit == 0 else 1 for bit in data])

def manchester_modulation(data: list[int]):
   
    sinal = []
    for bit in data:
        if bit == 1:
            sinal.extend([1,0])  # Representação Manchester para bit 1
        else:
            sinal.extend([0, 1])  # Representação Manchester para bit 0
    print(f"dado original: {data}")
    print(f"manchester aplicado: {sinal}")

    return np.array(sinal)


def bipolar_modulation(data: int):
    """Modulação Bipolar (AMI): 0 -> 0, 1 -> alterna entre +1 e -1"""
    estado = 1  # Indica se o próximo "1" será positivo ou negativo
    sinal = []
    for bit in data:
        if bit == 0:
            sinal.append(0)  # Nível zero para "0"
        else:
            sinal.append(estado)  # Alterna entre +1 e -1 para "1"
            estado *= -1  # Alterna o estado
    return np.array(sinal)

def ask_modulation(data: int):
    A = 1  # Amplitude para bit 1
    f = 2  # Frequência fixa para ambos os bits
    sinal = []
    time = []

    for i, bit in enumerate(data):
        t = np.linspace(i, i + 1, 100, endpoint=False)  # Tempo para este bit
        if bit == 1:
            sinal.extend(A * np.sin(2 * np.pi * f * t))  # Sinal senoidal para bit 1
        else:
            sinal.extend(np.zeros_like(t))  # Amplitude zero para bit 0
        time.extend(t)

    return [time, sinal]

def fsk_modulation(data: int):
    A = 1  # Amplitude fixa
    f1 = 2  # Frequência para bit 1
    f2 = 1  # Frequência para bit 0
    sinal = []
    time = []

    for i, bit in enumerate(data):
        t = np.linspace(i, i + 1, 100, endpoint=False)  # Tempo para este bit
        if bit == 1:
            sinal.extend(A * np.sin(2 * np.pi * f1 * t))  # Sinal senoidal com f1
        else:
            sinal.extend(A * np.sin(2 * np.pi * f2 * t))  # Sinal senoidal com f2
        time.extend(t)

    return [time, sinal]




def modulation_8qam(bit_string):

    bit_string = ''.join(map(str,bit_string))

    # Definir parâmetros do sinal
    fs = 1000  # Frequência de amostragem (Hz)
    f_carrier = 10  # Frequência da portadora (Hz)
    symbols = {
        '000': (-1, -1.5),
        '001': (-1, 1.5),
        '010': (1, -1.5),
        '011': (1, 1.5),
        '100': (-2, 0),
        '101': (0, -2),
        '110': (2, 0),
        '111': (0, 2)
    }
    # Ajustar o comprimento da string de bits para ser múltiplo de 3
    if len(bit_string) % 3 != 0:
        padding = 3 - (len(bit_string) % 3)
        bit_string += '0' * padding

    # Dividir a string de bits em símbolos de 3 bits
    data = [bit_string[i:i+3] for i in range(0, len(bit_string), 3)]

    symbol_duration = 0.1  # Duração de cada símbolo (s)
    t = np.arange(0, len(data) * symbol_duration, 1 / fs)  # Tempo total do sinal

    # Criar o sinal modulador
    modulated_signal = np.zeros_like(t)

    for i, symbol in enumerate(data):
        if symbol not in symbols:
            raise ValueError(f"Símbolo inválido encontrado: {symbol}")
        I, Q = symbols[symbol]  # Coordenadas I e Q do símbolo
        start = int(i * symbol_duration * fs)  # Início do símbolo
        end = int((i + 1) * symbol_duration * fs)  # Fim do símbolo
        
        # Criar a portadora modulada
        carrier = np.cos(2 * np.pi * f_carrier * t[start:end]) * I + np.sin(2 * np.pi * f_carrier * t[start:end]) * Q
        modulated_signal[start:end] = carrier
    return [t, modulated_signal]


