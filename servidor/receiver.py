import socket
import json
import struct
import threading
from camada_enlace.desenquadramento import remover_contagem_caracteres, tira_insercao_bytes
from camada_enlace.deteccao_erros import bit_paridade_receptor, crc_receptor
from camada_enlace.hamming import hamming_encode_receptor
from servidor.binario_texto import binario_para_texto
from camada_fisica.demodulacao import ask_demodulation, fsk_demodulation, qam_demodulation

class Receiver:
    def __init__(self, update_ui_callback):
        self.update_ui_callback = update_ui_callback

    def start(self):
        thread = threading.Thread(target=self.run_server)
        thread.start()

    def run_server(self):
        HOST = "127.0.0.1"
        PORT = 5000
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            server.bind((HOST, PORT))
            server.listen(5)
            print(f"Servidor ouvindo em {HOST}:{PORT}")

            while True:
                conn, addr = server.accept()
                print(f"Conexão estabelecida com {addr}")
                try:
                    data_size = struct.unpack("!I", conn.recv(4))[0]
                    received_data = b""
                    while len(received_data) < data_size:
                        packet = conn.recv(1024)
                        if not packet:
                            break
                        received_data += packet

                    if received_data:
                        received_json = json.loads(received_data.decode('utf-8'))
                        print(f"Dados recebidos: {received_json}")


                        
                        #pega o sinal do Objeto:
                        signal = received_json.get('signal')

                        #Analisa qual tipo de portadora foi utilizada:
                        if received_json["modulacao"] == "ASK":
                            signal = ask_demodulation(signal[0],signal[1])
                        elif received_json["modulacao"] == "FSK":
                            time = signal[0]
                            sinal_lista = signal[1]
                            signal = fsk_demodulation(time, sinal_lista)
                        elif received_json["modulacao"] == "8QAM":
                            signal = qam_demodulation(signal[0], signal[1])
                        self.update_ui_callback(f"Usuário: {received_json.get('nome')} \n")
                        # self.update_ui_callback(f"sinal: {received_json.get('signal')} \n")
                        self.update_ui_callback(f"Sinal demodulado: {signal} \n")

                        #Analisa o tipo de enquadramento utilizada:
                        if received_json['enquadramento'] == 'Contagem de caracteres':
                            desenquadramento = remover_contagem_caracteres(''.join(map(str, signal)))
                        elif received_json['enquadramento'] == 'Inserção de bytes':
                            desenquadramento = tira_insercao_bytes(''.join(map(str, signal)))
                        else:
                            raise ValueError("Método de enquadramento desconhecido")
                        self.update_ui_callback(f"Sinal desenquadrado: {desenquadramento}")


                        #Analisa o tipo de detecção de erro utilizada:
                        if received_json['deteccao'] == 'Bit de paridade par':
                            erro_detectado, resultado = bit_paridade_receptor(desenquadramento)
                            self.update_ui_callback(f"{resultado} \n")
                        elif received_json['deteccao'] == 'CRC':
                            erro_detectado, resultado, resto = crc_receptor(desenquadramento)
                            self.update_ui_callback(f"{resultado}, resultado do CRC: {resto} \n")
                        else:
                            raise ValueError("Método de detecção desconhecido \n")
                        
                        self.update_ui_callback(f"Mensagem sem os bits de detcção: {erro_detectado} \n")

                        dado_corrigido = hamming_encode_receptor(erro_detectado)
                        self.update_ui_callback(f"Mensagem sem os bits de correção: {dado_corrigido} \n")

                        #try:
                        mensagem = binario_para_texto(dado_corrigido)
                        self.update_ui_callback(f"Mensagem recebida: {mensagem} \n")
                        

                except Exception as e:
                    print(f"Erro ao processar dados: {e}")
                finally:
                    conn.close()
                    print(f"Conexão com {addr} encerrada.")
        except Exception as e:
            print(f"Erro ao iniciar o servidor: {e}")
        finally:
            server.close()
