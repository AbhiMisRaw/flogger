#!/bin/bash

echo "Script is started at : $(date)"
echo "====================================="

while true; do
    echo "================= HEALTH ===================="
    echo "Checking health :"
    echo "Request hit at : $(date +%T)"
    curl -s https://flogger-4kpc.onrender.com/health/
    echo ""
    echo "Response recieved at : $(date +%T)"
    sleep 15
    echo "================= HOMEPAGE ===================="
    echo "Checking HOMPAGE :"
    echo "Request hit at : $(date +%T)"
    curl -I https://flogger-4kpc.onrender.com/flog/homepage/
    echo ""
    echo "Response recieved at : $(date +%T)"
    sleep 15
    
done
