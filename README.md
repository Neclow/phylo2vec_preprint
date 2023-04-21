# Phylo2Vec: a vector representation for binary trees

This repository contains an implementation of Phylo2Vec which includes:
* ```cfg/```: Example configuration files
* ```data/```: Placeholder folder to contain sequence files in FASTA format.
* ```examples/```: Example notebooks for different datasets
* ```hc/```: Phylogenetic tree optimisation via hill-climbing optimisation
    * Branch length and nucleotide subsitution model optimisation relies on [RAxML-NG](https://github.com/amkozlov/raxml-ng)
* ```tests/```: Placeholder folder for unit tests
* ```trees/```: Placeholder folder to contain tree files as Newick strings.
* ```utils/```: Utility functions including definitions of Phylo2Vec and transforms from commonly used tree formats to Phylo2Vec (and *vice versa*).

## Demo
A quick demo detailing hill-climbing optimisation with Phylo2Vec is available on the ```demo.ipynb``` notebook.

A more minimalistic demo with an updated defiition of Phylo2Vec is available on Colab: [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/10ZENm-wgWiRFa4ABY8piGDY_QoJyZ30X?usp=sharing)

## Environment setup
To reproduce the environment, run:

```conda env create -f env.yml```

## Run hill climbing-based optimisation using Phylo2Vec

To run hill climbing-based optimisation using Phylo2Vec, run:

```
conda activate phylo

python -m hc.main
```

## Other third-party software
* Download a binary of RAxML-NG at: https://github.com/amkozlov/raxml-ng. For Windows, consider using the [Windows Subsystem for Linux](https://learn.microsoft.com/en-us/windows/wsl/install).

## Accessing data
The following datasets were used:
* ```primates```: https://evolution.gs.washington.edu/book/datasets.html
* ```fluA```: https://github.com/4ment/phylostan/tree/master/examples
* ```M501```: DS2 dataset in https://github.com/zcrabbit/vbpi-gnn/tree/main/data/hohna_datasets_fasta
* ```h3n2_na_20```, ```zika```: https://github.com/neherlab/treetime_examples
* ```yeast```: https://cran.r-project.org/web/packages/phangorn/index.html (comes with pre-loaded datasets including ```yeast```)

## Future work
As mentioned in the submission, we plan to add more optimiation schemes using Phylo2Vec, e.g., MCTS or gradient descent.

See https://github.com/Neclow/gradme
