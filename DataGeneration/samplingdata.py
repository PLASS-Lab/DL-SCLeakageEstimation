import pandas as pd

# Load the data
data = pd.read_csv('.csv')
data = data[['Instr', 'Imm', 'signedD', 'Context', 'AssemblyLine']]

# Function to take a deterministic sample of 30% from each group without sorting
def deterministic_sample(group):
    n_samples = int(len(group) * 0.7)  
    return group.iloc[:n_samples] 

# Apply the function to each group
data = data.groupby('Context').apply(deterministic_sample).reset_index(drop=True)

def group_instructions(instr):
    # Mapping of instructions to categories if needed for future studies
    categories = {
        'Arithmetic': ['add', 'sub', 'subs', 'subhi', 'addne', 'subne', 'rsb', 'smull', 'asr'],
        'Load': ['ldr', 'ldrb', 'ldrh', 'ldm'],
        'Store': ['str', 'strb', 'strh', 'stmia', 'stm'],
        'Branching': ['bx', 'bl', 'bne', 'b', 'ble', 'bcc', 'bcs', 'blt', 'bgt', 'bge', 'beq', 'bhi', 'bls', 'bichi', 'movls', 'lsrhi'],
        'Logical': ['and', 'eor', 'orr', 'ands', 'bic', 'eors', 'tst'],
        'Comparison': ['cmp'],
        'Shift': ['lsl', 'lsr', 'lsls'],
        'System': ['nop', 'pop', 'push', 'movhi', 'moveq', 'movne', 'movcs', 'movcc', 'mov', 'mvn'],
    }
    for category, ops in categories.items():
        if instr in ops:
            return category
    return 'Other'

# Group instructions and calculate frequency encoding
data['Instr_group'] = data['Instr'].apply(group_instructions)
data['Instr_length'] = data['Instr'].apply(len)
data['Instr_freq'] = data['Instr'].map(data['Instr'].value_counts(normalize=True))

# Filter out instructions with less than 1000 samples
counts = data['Instr'].value_counts()
data = data[data['Instr'].isin(counts[counts >= 5000].index)]

# Save the modified dataset
#data.to_csv('.csv', index=False)

# Print unique instructions and their counts after filtering
unique_instr = data['Instr'].unique()
unique_instr_count = data['AssemblyLine'].value_counts()

print("Unique Instructions:", unique_instr)
print("Count of each unique line:")
print(unique_instr_count)
