"""Optimisation with (discrete) gradient descent"""
import random

import numpy as np

from joblib import delayed, Parallel

from hc.loss import raxml_loss
from utils.tree import change_v, get_equivalent_v


def optimise(cfg, v_current, taxa_dict, debug):
    """Run hill-climbing optimisation.

    Parameters
    ----------
    cfg : collections.namedtuple
        Configuration parameters, loaded from a .yml file
    v_current : numpy.ndarray or list
        v representation of a start tree
    taxa_dict : dict[int, str]
        Current mapping of node label (integer) to taxa
    debug : bool
        If True, print intermediary results to help debugging

    Returns
    -------
    v_current : numpy.ndarray or list
        v representation of the optimal tree
    losses : list
        list of losses updated after each optimisation step
    """
    current_loss = raxml_loss(cfg, v_current, taxa_dict)

    # Number of rounds without improvement
    wait = 0

    losses = [current_loss]

    while wait < cfg.patience:
        # Get v equivalences
        v_equivalences = get_equivalent_v(v_current, rooted=cfg.rooted)

        # Pick a random equivalent
        print('Changing equivalences...')
        v_proposal = v_equivalences[random.randint(0, v_equivalences.shape[0]-1)]

        v_proposal, proposal_loss, taxa_dict = optimise_single(
            cfg,
            v_current.copy(),
            taxa_dict,
            debug=debug
        )

        v_current = v_proposal.copy()

        if round(proposal_loss - current_loss, 3) < 0:
            # Found a better loss so reset the patience counter
            current_loss = proposal_loss

            wait = 0
        else:
            # No drastic increase so increment the patience counter
            wait += 1

            print(f'No significantly better loss found {wait}/{cfg.patience}.')

        losses.append(current_loss)

    print(f'Optimization terminated successfully. Final loss: {current_loss:.3f}')

    return v_current, losses


def optimise_single(cfg, v_current, taxa_dict, rounds=1, debug=False):
    """Run optimisation once through every single v_i

    Parameters
    ----------
    cfg : collections.namedtuple
        Configuration parameters, loaded from a .yml file
    v_current : numpy.ndarray or list
        v representation of a start tree
    taxa_dict : dict[int, str]
        Current mapping of node label (integer) to taxa
    rounds : int, optional
        Number of different tree rootings for which an optimisation will be run, by default 1
    debug : bool
        If True, print intermediary results to help debugging

    Returns
    -------
    v_shuffled : numpy.ndarray or list
        v representation of the best tree after a single pass
    current_best_loss :
        loss of v_shuffled
    """
    # Reorder v
    v_shuffled, taxa_dict = change_v(v_current, taxa_dict)

    # Get current loss
    current_best_loss = raxml_loss(cfg, v_shuffled, taxa_dict, 'output.tree')

    if debug:
        print(f'Start optimise_single: {current_best_loss:.3f}')

    for _ in range(rounds):
        for i in reversed(range(1, len(v_shuffled))):
            # Calculate gradient for changes in row i
            # "gradient" here simply refers to a numerical gradient
            # between loss(v_current) and loss(v_proposal)
            proposal_grads, proposal_losses = grad_single(
                cfg,
                v_shuffled, current_best_loss,
                taxa_dict, i
            )

            # find index of max gradient
            grad_choice = proposal_grads.argmax(0)

            # Is there a positive gradient?
            if proposal_grads[grad_choice] > 0:
                # Discrete gradient step
                v_shuffled[i] = grad_choice + 1 if grad_choice >= v_shuffled[i] else grad_choice

                # Reorder v
                # v_shuffled, taxa_dict = change_v(v_shuffled, taxa_dict)

                if debug:
                    grad_propose = proposal_losses[grad_choice] - current_best_loss
                    print(f'Loss: {proposal_losses[grad_choice]:.3f} (diff: {grad_propose:.3f})')

                # Update best loss
                current_best_loss = proposal_losses[grad_choice] #save loss

    if debug:
        print(f'End optimise_single: {current_best_loss:.3f}')

    return v_shuffled, current_best_loss, taxa_dict


def grad_single(cfg, v_proposal, current_loss, taxa_dict, i):
    """Calculate gradients for

    Parameters
    ----------
    cfg : collections.namedtuple
        Configuration parameters, loaded from a .yml file
    v_proposal : numpy.ndarray or list
        v representation of a new tree proposal
    taxa_dict : dict[int, str]
        Current mapping of node label (integer) to taxa
    i : long
        index of v to change and to calculate a gradient on

    NOTE: # "gradient" here simply refers to a numerical gradient
            between loss(v_current) and loss(v_proposal)

    Returns
    -------
    numpy.ndarray
        Difference between the current loss and the proposal losses
    proposal_losses : numpy.ndarray
        Proposal losses
    """
    v_copy = v_proposal.copy()

    def run(v_other, i, j):
        v_other[i] = j
        return raxml_loss(cfg, v_other, taxa_dict, outfile=f'tree{i}{j}.tree')

    proposal_losses = np.array(
        Parallel(n_jobs=-1)(
            delayed(run)(v_copy, i, j) for j in range(2*i + 1) if j != v_proposal[i]
        )
    )

    return current_loss - proposal_losses, proposal_losses
