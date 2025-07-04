import numpy as np

def nrz_modulation(data: int):
    """
    Modulação NRZ (Non-Return-to-Zero):
    Transforma bits em níveis de tensão:
    - Bit 0 vira -1
    - Bit 1 vira +1
    """
    return np.array([-1 if bit == 0 else 1 for bit in data])

def manchester_modulation(data: list[int]):
    """
    Modulação Manchester:
    Cada bit vira dois valores:
    - Bit 1 vira [1, 0]
    - Bit 0 vira [0, 1]
    Isso garante transições no meio do tempo do bit.
    """
    sinal = []
    for bit in data:
        if bit == 1:
            sinal.extend([1, 0])  # Transição alta-baixa
        else:
            sinal.extend([0, 1])  # Transição baixa-alta
    return np.array(sinal)

def bipolar_modulation(data: int):
    """
    Modulação Bipolar (AMI - Alternate Mark Inversion):
    - Bit 0 vira 0 (nível neutro)
    - Bit 1 alterna entre +1 e -1 a cada ocorrência
    """
    estado = 1  # Próximo nível para bit 1 (+1 ou -1)
    sinal = []
    for bit in data:
        if bit == 0:
            sinal.append(0)
        else:
            sinal.append(estado)
            estado *= -1  # Alterna sinal
    return np.array(sinal)

def ask_modulation(data: int):
    """
    Modulação ASK (Amplitude Shift Keying):
    - Bit 1 vira uma onda senoidal com amplitude A
    - Bit 0 vira sinal com amplitude zero
    """
    A = 1  # Amplitude para bit 1
    f = 2  # Frequência da portadora
    sinal = []
    time = []

    for i, bit in enumerate(data):
        t = np.linspace(i, i + 1, 100, endpoint=False)  # Intervalo de tempo para esse bit
        if bit == 1:
            sinal.extend(A * np.sin(2 * np.pi * f * t))  # Sinal senoidal para 1
        else:
            sinal.extend(np.zeros_like(t))  # Sinal nulo para 0
        time.extend(t)

    return [time, sinal]

def fsk_modulation(data: int):
    """
    Modulação FSK (Frequency Shift Keying):
    - Bit 1 vira onda com frequência f1
    - Bit 0 vira onda com frequência f2
    """
    A = 1
    f1 = 2
    f2 = 1
    sinal = []
    time = []

    for i, bit in enumerate(data):
        t = np.linspace(i, i + 1, 100, endpoint=False)  # Tempo para esse bit
        if bit == 1:
            sinal.extend(A * np.sin(2 * np.pi * f1 * t))  # Frequência f1 para bit 1
        else:
            sinal.extend(A * np.sin(2 * np.pi * f2 * t))  # Frequência f2 para bit 0
        time.extend(t)

    return [time, sinal]

def modulation_8qam(bit_string):
    """
    Modulação 8-QAM (Quadrature Amplitude Modulation):
    Cada 3 bits formam um símbolo que é representado por uma coordenada (I, Q).
    I = componente em cosseno, Q = componente em seno.
    """
    bit_string = ''.join(map(str, bit_string))  # Junta bits em uma string

    fs = 1000  # Frequência de amostragem
    f_carrier = 10  # Frequência da portadora

    # Constelação com símbolos de 3 bits mapeados para (I, Q)
    constellation = {
        '000': (-1, -1.5),
        '001': (-1, 1.5),
        '010': (1, -1.5),
        '011': (1, 1.5),
        '100': (-2, 0),
        '101': (0, -2),
        '110': (2, 0),
        '111': (0, 2)
    }

    # Adiciona bits extras (padding) se necessário
    if len(bit_string) % 3 != 0:
        padding = 3 - (len(bit_string) % 3)
        bit_string += '0' * padding

    # Divide em símbolos de 3 bits
    data = [bit_string[i:i+3] for i in range(0, len(bit_string), 3)]

    constellation_duration = 0.1  # Duração de cada símbolo
    t = np.arange(0, len(data) * constellation_duration, 1 / fs)

    # Inicializa sinal vazio
    modulated_signal = np.zeros_like(t)

    for i, symbol in enumerate(data):
        if symbol not in constellation:
            raise ValueError(f"Símbolo inválido encontrado: {symbol}")

        I, Q = constellation[symbol]  # Coordenadas I e Q
        start = int(i * constellation_duration * fs)
        end = int((i + 1) * constellation_duration * fs)

        # Gera portadora com modulação em amplitude e fase
        carrier = np.cos(2 * np.pi * f_carrier * t[start:end]) * I + \
                  np.sin(2 * np.pi * f_carrier * t[start:end]) * Q

        modulated_signal[start:end] = carrier

    return [t, modulated_signal]

