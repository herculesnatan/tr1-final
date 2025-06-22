#!/bin/bash

# Abrir um único terminal com múltiplas abas (se usar GNOME Terminal)
gnome-terminal --tab --title="Servidor" -- bash -c "python3 main_server.py; exec bash" \

sleep 1
gnome-terminal --tab --title="Cliente 1" -- bash -c "python3 main_client.py; exec bash" \

gnome-terminal --tab --title="Cliente 2" -- bash -c "python3 main_client.py; exec bash"

# Mensagem de conclusão
echo "Todos os processos foram iniciados em abas separadas."
