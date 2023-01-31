#pylint:disable=invalid-name
"""Tests for newick2v."""
import random

import numpy as np

from utils.tree import label_tree, newick2v


if __name__ == '__main__':
    k = 20

    n_tests = 1000
    n_correct = 0

    failed_tests = []

    for i in range(n_tests):
        try:
            v_init = np.array([random.randint(0, 2*i) for i in range(k)])
            v_test = newick2v(label_tree(v_init, ete3_format=9)[-2])[1:]
            if np.all(v_init == v_test):
                n_correct += 1
            else:
                print(f'\033[91mFailed test {i+1}\033[0m')
                print(f'Input: {v_init}')
                print(f'Output: {v_test}')
        except Exception as e: # pylint: disable=broad-except
            print(f'\033[91mFailed test {i+1}\033[0m')
            print(f'Input: {v_init}')
            print(f'Error: {e:}')
    print(f'Tests passed: {n_correct}/{n_tests}.')
