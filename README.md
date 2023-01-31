# Phylo2Vec: a vector representation for binary trees (Anonymous repo)

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

## Environment setup
To reproduce the environment, run:

```conda env create -f env.yml```

## Run hill climbing-based optimisation using Phylo2Vec

To run hill climbing-based optimisation using Phylo2Vec, run:

```
conda activate phylo

python -m hc.main
```

## Accessing data
The following datasets were used:
* ```fluA```: https://github.com/4ment/phylostan/tree/master/examples
* ```h3n2_na_20```, ```zika```: https://github.com/neherlab/treetime_examples
* ```yeast```: https://cran.r-project.org/web/packages/phangorn/index.html (comes with pre-loaded datasets including ```yeast```)

## Future work
As mentioned in the submission, we plan to add more optimiation schemes using Phylo2Vec, e.g., MCTS or gradient descent
