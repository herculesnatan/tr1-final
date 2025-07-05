import numpy as np
from camada_fisica.modulacao import nrz_modulation, bipolar_modulation, modulation_8qam, manchester_modulation,ask_modulation, fsk_modulation
import socket
import json
import struct

class Transmitter:
    def __init__(self, modulation_type="NRZ", carrier_modulation_type="ASK"):
        self.modulation_type = modulation_type
        self.carrier_modulation_type = carrier_modulation_type

    def encode_text(self, text: str) -> list[int]:
        """Converte o texto em uma lista de bits."""
        binary_data = ''.join(format(ord(char), '08b') for char in text)
        return [int(bit) for bit in binary_data]

    def modulate(self, data: list[int]) -> np.ndarray:
        """Aplica a modulação digital escolhida nos dados."""
        if self.modulation_type == "NRZ":
            return nrz_modulation(data)
        elif self.modulation_type == "Manchester":
            return manchester_modulation(data)
        elif self.modulation_type == "Bipolar":
            return bipolar_modulation(data)
        else:
            print("Tipo de modulação digital não suportado.")
        
    def carrier_modulate(self, data: np.ndarray) -> np.ndarray:
        """Aplica a modulação da portadora escolhida."""
        if self.carrier_modulation_type == "ASK":
            return ask_modulation(data)
        elif self.carrier_modulation_type == "FSK":
            return fsk_modulation(data)
        elif self.carrier_modulation_type == "8QAM":
            return modulation_8qam(data)
        else:
            print("Tipo de modulação por portadora não suportado.")
    
    def send(self, signal, modulacao, enquadramento, deteccao, nome):
        HOST = '127.0.0.1'
        PORT = 5000
        #print("sinal trammisttre: {} ", signal)

        try:
            tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            dest = (HOST, PORT)
            tcp.connect(dest)

            if modulacao in ["NRZ", "Bipolar", "Manchester"]:
                data_to_send = signal.tolist()  # Conversão para lista se necessário
            else:
                data_to_send = signal  # Mantém como np.ndarray para tipos de modulação por portadora

            data = {
                "signal": data_to_send,
                "modulacao": modulacao,
                "enquadramento": enquadramento,
                "deteccao": deteccao,
                "nome": nome
            }

            serialized_data = json.dumps(data).encode('utf-8')
            data_size = struct.pack("!I", len(serialized_data))
            

            tcp.sendall(data_size)  # Enviar o tamanho dos dados
            tcp.sendall(serialized_data)  # Enviar os dados

            print("Dados enviados com sucesso.")
    

        except Exception as e:
            print(f"Erro ao enviar dados: {e}")
        finally:
            tcp.close()
            print("Conexão encerrada.")
