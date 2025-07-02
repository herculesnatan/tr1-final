import numpy as np

def ask_demodulation(time: list, sinal: list, bit_duration: float = 1.0, threshold: float = 0.5):
    """
    Demodulação ASK (Amplitude Shift Keying):
    Recupera bits com base na amplitude do sinal.
    - bit 1: se a média da amplitude for maior que o limiar (threshold)
    - bit 0: caso contrário
    """
    bits = []
    sample_rate = len(time) / (time[-1] - time[0])  # Taxa de amostragem
    samples_per_bit = int(sample_rate * bit_duration)

    for i in range(0, len(sinal), samples_per_bit):
        segment = sinal[i:i + samples_per_bit]

        if len(segment) < samples_per_bit:
            break

        avg_amplitude = np.mean(np.abs(segment))

        if avg_amplitude > threshold:
            bits.append(1)
        else:
            bits.append(0)

    return bits

def fsk_demodulation(time: np.ndarray, signal: np.ndarray):
    """
    Demodulação FSK (Frequency Shift Keying):
    Verifica a frequência dominante em cada segmento para recuperar os bits.
    - bit 1: se frequência dominante se aproxima de f1
    - bit 0: se se aproxima de f2
    """
    f1 = 2  # Frequência para bit 1
    f2 = 1  # Frequência para bit 0
    num_amostras_por_bit = 100
    bits = []

    if not np.allclose(np.diff(time), time[1] - time[0]):
        raise ValueError("O vetor de tempo não é uniformemente espaçado!")

    for i in range(0, len(signal), num_amostras_por_bit):
        segmento = signal[i:i + num_amostras_por_bit]
        if len(segmento) < num_amostras_por_bit:
            continue

        fft_resultado = np.fft.fft(segmento)
        frequencias = np.fft.fftfreq(len(segmento), time[1] - time[0])
        idx_positivos = frequencias > 0
        frequencias = frequencias[idx_positivos]
        fft_resultado = np.abs(fft_resultado[idx_positivos])

        idx_max = np.argmax(fft_resultado)
        frequencia_dominante = frequencias[idx_max]

        if abs(frequencia_dominante - f1) < abs(frequencia_dominante - f2):
            bits.append(1)
        else:
            bits.append(0)

    return bits

def qam_demodulation(t, modulated_signal):
    """
    Demodulação 8-QAM (Quadrature Amplitude Modulation):
    Recupera os bits com base na posição I-Q (fase/amplitude) do sinal recebido.
    """
    fs = 1000  # Frequência de amostragem (Hz)
    f_carrier = 10  # Frequência da portadora (Hz)

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

    t = np.array(t)
    modulated_signal = np.array(modulated_signal)

    constellation_duration = 0.1
    num_constellation = int(len(t) / (fs * constellation_duration))

    I_values = []
    Q_values = []

    for i in range(num_constellation):
        start = int(i * constellation_duration * fs)
        end = int((i + 1) * constellation_duration * fs)

        I = np.sum(modulated_signal[start:end] * np.cos(2 * np.pi * f_carrier * t[start:end]))
        Q = np.sum(modulated_signal[start:end] * np.sin(2 * np.pi * f_carrier * t[start:end]))

        I_values.append(I)
        Q_values.append(Q)

    decoded_bits = []
    for I, Q in zip(I_values, Q_values):
        min_distance = float('inf')
        closest_constellation = None
        for symbol, (I_ref, Q_ref) in constellation.items():
            distance = (I - I_ref)**2 + (Q - Q_ref)**2
            if distance < min_distance:
                min_distance = distance
                closest_constellation = symbol
        decoded_bits.append(closest_constellation)

    decoded_bit_string = ''.join(decoded_bits)
    padding = len(decoded_bit_string) % 3
    if padding != 0:
        decoded_bit_string = decoded_bit_string[:-padding]

    return decoded_bit_string
