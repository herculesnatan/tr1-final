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
            teste = 1

            while True:
                conn, addr = server.accept()
                print(f"Conexão estabelecida com {addr}")

                try:
                    self.update_ui_callback(f"\n---------------------- TESTE: {teste} -----------------------------\n")

                    # Recebe o tamanho dos dados
                    data_size = struct.unpack("!I", conn.recv(4))[0]
                    received_data = b""

                    self.update_ui_callback(f"Tamanho dos dados a receber: {data_size}\n")

                    while len(received_data) < data_size:
                        packet = conn.recv(1024)
                        if not packet:
                            self.update_ui_callback("Dados recebidos incompletos.\n")
                            break
                        received_data += packet

                    if len(received_data) < data_size:
                        self.update_ui_callback("Conexão encerrada prematuramente.\n")
                        continue

                    if not received_data:
                        continue

                    received_json = json.loads(received_data.decode('utf-8'))
                    signal = received_json.get('signal')

                    # Demodulação
                    modulacao = received_json.get("modulacao")
                    if modulacao == "ASK":
                        signal = ask_demodulation(signal[0], signal[1])
                    elif modulacao == "FSK":
                        signal = fsk_demodulation(signal[0], signal[1])
                    elif modulacao == "8QAM":
                        signal = qam_demodulation(signal[0], signal[1])
                    else:
                        raise ValueError("Modulação desconhecida")

                    self.update_ui_callback("====== NOVA MENSAGEM RECEBIDA ======\n")
                    self.update_ui_callback(f"Usuário: {received_json.get('nome')}\n")
                    self.update_ui_callback(f"Sinal demodulado: {' '.join(str(bit) for bit in signal)}\n")

                    # Desenquadramento
                    enquadramento = received_json.get("enquadramento")
                    sinal_str = ''.join(map(str, signal))
                    if enquadramento == "Contagem de caracteres":
                        desenquadrado = remover_contagem_caracteres(sinal_str)
                    elif enquadramento == "Inserção de bytes":
                        desenquadrado = tira_insercao_bytes(sinal_str)
                    else:
                        raise ValueError("Método de enquadramento desconhecido")

                    self.update_ui_callback(f"Sinal desenquadrado: {desenquadrado}\n")

                    # Detecção de erros
                    deteccao = received_json.get("deteccao")
                    if deteccao == "Bit de paridade par":
                        erro_detectado, resultado = bit_paridade_receptor(desenquadrado)
                        self.update_ui_callback(f"{resultado}\n")
                    elif deteccao == "CRC":
                        erro_detectado, resultado, resto = crc_receptor(desenquadrado)
                        self.update_ui_callback(f"{resultado}, resultado do CRC: {resto}\n")
                    else:
                        raise ValueError("Método de detecção de erro desconhecido")

                    self.update_ui_callback(f"Mensagem sem os bits de detecção: {erro_detectado}\n")

                    # Correção de erros com Hamming
                    try:
                        dado_corrigido, erro = hamming_encode_receptor(erro_detectado)
                        self.update_ui_callback(f"Mensagem sem os bits de correção: {dado_corrigido}\n")
                        mensagem = binario_para_texto(dado_corrigido)
                        self.update_ui_callback(f"Mensagem recebida: {mensagem}\n")
                        if erro != "nada":
                            self.update_ui_callback(f"{erro}\n")
                    except Exception as e:
                        self.update_ui_callback(f"Erro ao aplicar Hamming: {e}\n")

                    teste += 1

                except Exception as e:
                    print(f"Erro ao processar dados: {e}")
                    self.update_ui_callback(f"Erro ao processar dados: {e}\n")

                finally:
                    conn.close()
                    print(f"Conexão com {addr} encerrada.")

        except Exception as e:
            print(f"Erro ao iniciar o servidor: {e}")
        finally:
            server.close()
