""""Main script for hill-climbing optimisation"""
import random

from pathlib import Path

from hc.optim import optimise
from utils.data import load_yaml_config, read_fasta
from utils.plot import plot_loss
from utils.seed import seed_everything
from utils.tree import sample_tree


def run(cfg_path):
    """Run hill-climbing optimisation.

    Parameters
    ----------
    cfg_path : str or path-like
        Path to a .yml config file
    """
    # Load data
    print('Loading config...')
    cfg = load_yaml_config(cfg_path)
    seed_everything(random.randint(0, cfg.max_seed) if cfg.seed is None else cfg.seed)

    # Read data
    print('Loading data...')
    data = read_fasta(Path(cfg.repo_path, 'data', cfg.fasta_path)).replace('-', float('nan'))

    k = data.shape[1] - 1

    taxa_dict = {i: col.replace(' ', '.') for (i, col) in enumerate(data.columns)}

    print(f'Data: {data.shape[0]} sites; {k+1} taxa.')

    # Sample a random tree
    v_init = sample_tree(k)

    print('Start optimisation')
    v_opt, losses = optimise(cfg, v_init, taxa_dict, debug=cfg.debug)

    print(f'Optimal v: {repr(v_opt)}')

    plot_loss(losses)


if __name__ == '__main__':
    run('cfg/hc_config.yml')
