'''
this script reads the assembly files in the directory and extracts the assembly 
instructions, immediate values, binary code, hamming weight and hamming distance 
between consecutive instructions then writes the results to a CSV file.
'''

import subprocess
import re
import os
import csv

def extract_immediate(instruction):
    matches = re.findall(r'\#(-?\d+|\w+)|=(\w+)', instruction)
    values = [m[0] if m[0] else m[1] for m in matches]
    return ', '.join(values)

def extract_mnemonic(instruction):
    return instruction.split()[0]

def hamming_weight(binary_string):
    return binary_string.count('1')

def hamming_distance(bin1, bin2):
    return sum(c1 != c2 for c1, c2 in zip(bin1, bin2))

def assemble_instructions_to_binary(assembly_code):
    with open("temp.s", "w") as f:
        f.write(".section .text\n.global main\nmain:\n")
        for code in assembly_code:
            f.write(code + "\n")

    try:
        subprocess.run(["arm-linux-gnueabi-as", "-o", "temp.o", "temp.s"], check=True)
        result = subprocess.run(["arm-linux-gnueabi-objdump", "-d", "temp.o"], capture_output=True, text=True)
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        return []

    binary_instructions = []
    for line in result.stdout.split('\n'):
        match = re.search(r'^\s*[0-9a-f]+:\s*([0-9a-f ]+)\s', line)
        if match:
            binary_str = ''.join(f"{int(x, 16):08b}" for x in match.group(1).split())
            binary_instructions.append(binary_str)

    os.remove("temp.s")
    os.remove("temp.o")
    return binary_instructions

def process_files(directory):
    all_data = []
    for filename in os.listdir(directory):
        if filename.endswith('.txt'):
            filepath = os.path.join(directory, filename)
            with open(filepath, 'r') as file:
                content = file.read()
            lines = content.split("\n")
            assembly_instructions = []
            for line in lines:
                if ">:" in line and not line.startswith("(gdb)"):
                    instruction = line.split(":")[1].strip()
                    instruction = instruction.split(";")[0].strip()
                    instruction = instruction.split("<")[0].strip()
                    instruction = instruction.replace("\t", " ").replace('")', '').replace('"', '')
                    excluded_instructions = ('')
                    if instruction and all(excluded not in instruction for excluded in excluded_instructions):
                        assembly_instructions.append(instruction)
            binary_instructions = assemble_instructions_to_binary(assembly_instructions)
            previous_binary = None
            for assembly, binary in zip(assembly_instructions, binary_instructions):
                immediate_values = extract_immediate(assembly)
                mnemonic = extract_mnemonic(assembly)
                weight = hamming_weight(binary)
                distance = hamming_distance(previous_binary, binary) if previous_binary else None
                previous_binary = binary
                # Remove any words after the underscore in the filename
                simplified_filename = filename.split('_')[0]
                all_data.append([simplified_filename, mnemonic, assembly, immediate_values, binary, weight, distance])
    
    # Write aggregated results to a single CSV file
    with open(r'/home/sal/HDModel/assemblyfiles/output.csv', 'w', newline='') as csvfile:
        fieldnames = ['Context', 'Instr', 'AssemblyLine', 'Imm', 'BinaryCode', 'HW', 'HD']
        writer = csv.writer(csvfile)
        writer.writerow(fieldnames)
        for row in all_data:
            writer.writerow(row)

def main():
    directory = '/home/sal/HDModel/assemblyfiles/'
    process_files(directory)

main()
