#!/bin/bash

konsole --new-tab -e bash -c "python3 main_server.py; exec bash" &
sleep 1
konsole --new-tab -e bash -c "python3 main_client.py; exec bash" &

echo "Todos os processos foram iniciados em abas separadas."


"""
usar esse comandos para conseguir compilar os códigos
sudo apt install konsole
chmod +x script.sh
./script.sh

"""