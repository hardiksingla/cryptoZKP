#!/bin/bash

echo "Setting up zk-creds demo..."

# Make compile script executable
chmod +x compile_circuits.sh

# Create necessary directories
mkdir -p keys proofs circuits/age_verify_js circuits/membership_js

# Compile circuits (this may take a while)
echo "Compiling circuits and generating trusted setup..."
./compile_circuits.sh

# Start the backend server
echo "Starting demo server..."
cd backend
python main.py