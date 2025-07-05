#!/bin/bash

konsole --new-tab -e bash -c "python3 main_server.py; exec bash" &
sleep 1
konsole --new-tab -e bash -c "python3 main_client.py; exec bash" &
