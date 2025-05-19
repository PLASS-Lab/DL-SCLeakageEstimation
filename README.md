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
[Advanced Side-Channel Evaluation Using Contextual Deep Learning-Based Leakage Modeling](https://doi.org/10.1145/3734219)

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
If you use this code or data for your research, please cite the following paper.
>Title: Advanced Side-Channel Evaluation Using Contextual Deep Learning-Based Leakage Modeling \
>Journal: ACM Transactions on Software Engineering and Methodology \
>DOI: [10.1145/3734219](https://doi.org/10.1145/3734219)
```bibtex
@article{alabdulwahab2025advSCEval,
  author = {Alabdulwahab, Saleh and Kim, JaeCheol and Kim, Young-Tak and Son, Yunsik},
  title = {Advanced Side-Channel Evaluation Using Contextual Deep Learning-Based Leakage Modeling},
  year = {2025},
  publisher = {Association for Computing Machinery},
  address = {New York, NY, USA},
  issn = {1049-331X},
  url = {https://doi.org/10.1145/3734219},
  doi = {10.1145/3734219},
  journal = {ACM Trans. Softw. Eng. Methodol.},
  keywords = {Side channel attacks, Reverse engineering, Deep learning, Disassemble}
}
```

<p align="center">
  <a href="https://plass.dongguk.edu" target="_blank">
    <img src="https://github.com/sucystem/PLASS/blob/main/logo.png" width="400" alt="PLASS Lab, Dongguk University">
  </a>
</p>



