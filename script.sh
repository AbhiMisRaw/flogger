#!/bin/bash

echo "Script is started at : $(date)"
echo "====================================="

while true; do
    echo "Checking health :"
    echo "Request hit at : $(date +%T)"
    curl -s https://flogger-4kpc.onrender.com/health/
    echo ""
    echo "Response recieved at : $(date +%T)"
    sleep 15
done
