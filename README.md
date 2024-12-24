# DL-SCLeakageEstimation

This project is part of "Advanced Side-Channel Evaluation Using Contextual Deep Learning-Based
Leakage Modeling" paper.

The main objective is to create a refined dataset, then use it to train DL-based side channel leakage estimaiton models. These models were enhanced using contextual embedding and attention layers.

## Table of Contents

1. [Installation](#installation)
2. [Usage](#usage)
3. [Features](#features)
---

## Installation

```bash
# Clone the repository
git clone https://github.com/PLASS-Lab/DL-SCLeakageEstimation.git

# Navigate to the project directory
cd DL-SCLeakageEstimation

# Install dependencies
python setup.py install
```

## Usage

After uploading the assembly logs, collected from GDB, to the selected folder, it can be converted to a structured CSV file using `assembleyToBianry.py`

```bash
python assembleyToBianry.py
```

The generated CSV file can be passed to `switching_signed_Distance.py` for Hamming based power modeling.

```bash
python switching_signed_Distance.py
```

The refined dataset can then be used for the leakage estimaiton models and performing side channel disassembly analysis.

```bash
python GRU_compined.py
```

## Features

The main features.

- **Assembly to CSV Conversion**: Convert raw assembly logs from GDB into structured CSV files, making them easier to manipulate and analyze.
- **Generating Hamming based Power Modeling**: Use `switching_signed_Distance.py` to generate the power consumption using a Hamming based model.
- **Advanced Leakage Estimation for Disassembly Analysis**: Perform side channel leakage estimation using advanced DL models.

