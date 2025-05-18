<h1 align="center"><strong>DL-SCLeakageEstimation</strong></h1>

<p align="left">
  🪪&nbsp;<a href="#about">About</a>
  | 🪄&nbsp;<a href="#Installation">Installation</a>
  | 🗃️&nbsp;<a href="#Usage">Usage</a>
  | 🏷️&nbsp;<a href="#Features">Features</a>
  | 🔗&nbsp;<a href="#citation">Citation</a>
  | 📝&nbsp;<a href="https://doi.org/10.1145/3734219" target="_blank">Paper</a>
</p>

This repository contains the code and the dataset for the paper:
<a href="https://doi.org/10.1145/3734219" target="_blank">Advanced Side-Channel Evaluation Using Contextual Deep Learning-Based Leakage Modeling</a>

## About
The main objective is to create a refined dataset, then use it to train DL-based side channel leakage estimaiton models. These models were enhanced using contextual embedding and attention layers.

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

## Citation
If you find this code and data useful for your research, please cite the following work.
```bibtex
@article{alabdulwahab2025advSCEval,
  journal = {ACM Trans. Softw. Eng. Methodol.},
  title = {Advanced Side-Channel Evaluation Using Contextual Deep Learning-Based Leakage Modeling},
  doi = {10.1145/3734219},
  author = {Alabdulwahab, Saleh and Kim, JaeCheol and Kim, Young-Tak and Son, Yunsik},
  year = {2025}
}
```

<p align="center">
  <a href="https://plass.dongguk.edu" target="_blank">
    <img src="https://github.com/sucystem/PLASS/blob/main/logo.png" width="400" alt="PLASS Lab, Dongguk University">
  </a>
</p>



