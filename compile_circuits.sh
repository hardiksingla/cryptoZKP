#!/bin/bash

echo "Compiling circuits..."

# Compile age verification circuit
circom circuits/age_verify.circom --r1cs --wasm --sym --c -o circuits/
circom circuits/membership.circom --r1cs --wasm --sym --c -o circuits/

# Generate trusted setup (using powers of tau - simplified for demo)
echo "Generating trusted setup..."

# Download powers of tau file (or generate small one for demo)
snarkjs powersoftau new bn128 12 keys/pot12_0000.ptau -v
snarkjs powersoftau contribute keys/pot12_0000.ptau keys/pot12_0001.ptau --name="Demo contribution" -v -e="demo entropy"
snarkjs powersoftau prepare phase2 keys/pot12_0001.ptau keys/pot12_final.ptau -v

# Generate circuit-specific setup
snarkjs groth16 setup circuits/age_verify.r1cs keys/pot12_final.ptau keys/age_verify_0000.zkey
snarkjs zkey contribute keys/age_verify_0000.zkey keys/age_verify_final.zkey --name="Age verify contribution" -v -e="more demo entropy"
snarkjs zkey export verificationkey keys/age_verify_final.zkey keys/age_verify_vkey.json

snarkjs groth16 setup circuits/membership.r1cs keys/pot12_final.ptau keys/membership_0000.zkey
snarkjs zkey contribute keys/membership_0000.zkey keys/membership_final.zkey --name="Membership contribution" -v -e="even more entropy"
snarkjs zkey export verificationkey keys/membership_final.zkey keys/membership_vkey.json

echo "Circuit compilation complete!"