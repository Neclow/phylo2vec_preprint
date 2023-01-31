"""Loss functions. Currently only the RAxML loss is shown."""
#pylint: disable=invalid-name
import os
import re
import subprocess
import sys

from pathlib import PurePosixPath

from utils.tree import label_tree

# Regex for a negative float
NEG_FLOAT_PATTERN = re.compile(r'-\d+.\d+')

# Test if the current platform is Windows or not
IS_WINDOWS = sys.platform.startswith('win')


def exec_raxml_ng(raxml_path, fasta_path, tree_path, substitution_model, no_files=True):
    """Optimize branch lengths and free model parameters on a fixed topology
    using RaxML-NG (https://github.com/amkozlov/raxml-ng)

    Parameters
    ----------
    raxml_path : str
        Path to RAxML-NG binary
    fasta_path : str
        Path to FASTA file (MSA)
    tree_path : str
        Path to tree file (Newick representation of the tree)
    substitution_model : str
        DNA evolution model
    no_files : bool, optional
        If True, add the "nofiles" option to raxml

    Returns
    -------
    float
        Negative log-likelihood after optimization
    """
    commands = [
        'cd',
        raxml_path,
        '&&',
        './raxml-ng',
        '--evaluate',
        '--msa',
        fasta_path,
        '--tree',
        tree_path,
        '--model',
        substitution_model,
        '--brlen',
        'scaled',
        '--log',
        'RESULT',
        '--threads',
        '1'
    ]

    if no_files:
        commands.append('--nofiles')

    if IS_WINDOWS:
        commands.insert(0, 'wsl') # Use Windows Subsystem for Linux
    else:
        commands = ' '.join(commands) # For Linux

    try:
        output = subprocess.run(commands, capture_output=True, check=True, shell=not IS_WINDOWS)
    except subprocess.CalledProcessError as _:
        #pylint: disable=subprocess-run-check
        output = subprocess.run(commands, capture_output=True, shell=not IS_WINDOWS)
        #pylint: enable=subprocess-run-check

        raise RuntimeError(output) from _

    stdout = output.stdout.decode('ascii')

    lik_line = [
        line for line in stdout.split('\n')
        if line.startswith('Final LogLikelihood')
    ][0]

    nll = -1*float(re.findall(NEG_FLOAT_PATTERN, lik_line)[0])

    return nll


def raxml_loss(cfg, v, taxa_dict, outfile='tmp.tree', **kwargs):
    """Compute loss for a given v via RaXML-NG.

    Parameters
    ----------
    cfg : collections.namedtuple
        Configuration parameters, loaded from a .yml file
    v : numpy.ndarray or list
        v representation of a tree
    taxa_dict : dict[int, str]
        Current mapping of node label (integer) to taxa
    outfile : str, optional
        Path to a temporary tree written in Newick format, by default 'tmp.tree'

    Returns
    -------
    float
        Negative log-likelihood computed using RaXML-NG
    """
    _, newick, _ = label_tree(v, ete3_format=5, rooted=cfg.rooted)

    for taxa_key, taxa_name in taxa_dict.items():
        newick = re.sub(rf'([^\d]){taxa_key}(:)', rf'\1{taxa_name}\2', newick)

    with open(os.path.join(cfg.repo_path, 'trees', outfile), "w", encoding='utf-8') as nw_file:
        nw_file.write(newick)

    return exec_raxml_ng(
        cfg.raxml_path,
        str(PurePosixPath(cfg.repo_path.replace('C:', '/mnt/c/'), 'data', cfg.fasta_path)),
        str(PurePosixPath(cfg.repo_path.replace('C:', '/mnt/c/'), 'trees', outfile)),
        cfg.substitution_model,
        **kwargs
    )
