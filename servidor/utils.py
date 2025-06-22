# TESTEEEEESS

import socket

def send_message_to_server():
    message = input("Digite a mensagem para enviar ao servidor: ")
    
    # Criar o socket para o cliente
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect(('localhost', 12345))  # Conectar ao servidor
        client_socket.send(message.encode('utf-8'))  # Enviar a mensagem

if __name__ == "__main__":
    send_message_to_server()
