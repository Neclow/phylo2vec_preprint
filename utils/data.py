#pylint: disable=invalid-name, line-too-long
"""Other general utility functions."""
from collections import namedtuple
from pathlib import Path
from pprint import pprint

import pandas as pd
import yaml


def read_fasta(file_path):
    """Read a FASTA file into DataFrame.

    Parameters
    ----------
    file_path : str, path object, file-like object
        String, path object (implementing os.PathLike[str]), or file-like object implementing a write() function

    Returns
    -------
    pandas.DataFrame
        Two-dimensional data structure where:
        Columns = Species/Taxa.
        1 row = 1 nucleotide/aa site.
    """
    sequences = {}

    with open(file_path, 'r', encoding='utf-8') as f:
        current_seq_name = None
        current_seq_values = ''
        for line in f:
            line = line.strip()
            if line[0] == ">":
                if current_seq_name:
                    sequences[current_seq_name] = current_seq_values.lower()
                current_seq_name = line[1:]
                current_seq_values = ''
            else:
                current_seq_values += line

        # Add the final species to the dictionary
        sequences[current_seq_name] = current_seq_values.lower()

    return pd.DataFrame({key: list(val) for key, val in sequences.items()})


def to_fasta(file_path, df):
    """Write object to a FASTA file.

    Parameters
    ----------
    file_path : str, path object, file-like object
        String, path object (implementing os.PathLike[str]), or file-like object implementing a write() function
    df : pandas.DataFrame
        Object to write
    """
    with open(file_path, 'w', encoding='utf-8') as f:
        for column in df.columns:
            f.write(f">{column}\n{''.join(df[column])}\n")


def load_yaml_config(file_path):
    """Read a yml file into namedtuple

    Parameters
    ----------
    file_path : str, path object, file-like object
        String, path object (implementing os.PathLike[str]), or file-like object implementing a write() function

    Returns
    -------
    collections.namedtuple
        namedtuple version of the dict constructed by yaml.safe_load
    """
    cfg = yaml.safe_load(Path(file_path).read_text(encoding='utf-8'))
    pprint(cfg)
    Args = namedtuple('Args', cfg)
    return Args(**cfg)
