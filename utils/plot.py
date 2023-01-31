""""Plotting utilities."""
#pylint: disable=invalid-name
import matplotlib.pyplot as plt
import seaborn as sns


def clear_axes(
    ax=None,
    top=True, right=True, left=False, bottom=False,
    minorticks_off=True
):
    """A more forcing version of sns.despine.

    Parameters
    ----------
    ax : matplotlib axes, optional
        Specific axes object to despine.
    top, right, left, bottom : boolean, optional
        If True, remove that spine.
    minorticks_off: boolean, optional
        If True, remove all minor ticks
    """
    if ax is None:
        axes = plt.gcf().axes
    else:
        axes = [ax]

    for ax_i in axes:
        sns.despine(ax=ax_i, top=top, right=right, left=left, bottom=bottom)
        if minorticks_off:
            ax_i.minorticks_off()


def set_size(width, layout='h', fraction=1):
    """Set figure dimensions to avoid scaling in LaTeX.

    Adapted from: https://jwalton.info/Embed-Publication-Matplotlib-Latex/

    Parameters
    ----------
    width: float
        Document textwidth or columnwidth in pts
        Report: 390 pt
    layout: string
        h: horizontal layout
        v: vertical layout
        s: square layout
    fraction: float, optional
        Fraction of the width which you wish the figure to occupy

    Returns
    -------
    fig_dim: tuple
            Dimensions of figure in inches
    """
    # Width of figure (in pts)
    fig_width_pt = width * fraction

    # Convert from pt to inches
    inches_per_pt = 1 / 72.27

    # Golden ratio for aesthetic figures
    # https://disq.us/p/2940ij3
    golden_ratio = (5**.5 - 1) / 2

    # Figure width in inches
    fig_width_in = fig_width_pt * inches_per_pt
    # Figure height in inches
    if layout == 'h':
        fig_height_in = fig_width_in * golden_ratio
    elif layout == 'v':
        fig_height_in = fig_width_in / golden_ratio
    elif layout == 's':
        fig_height_in = fig_width_in

    fig_dim = (fig_width_in, fig_height_in)

    return fig_dim


def plot_loss(losses, xlabel='Epoch', ylabel='NLL Felsenstein loss', ax=None, **kwargs):
    """Plot the loss/cost function value over training epochs.

    Parameters
    ----------
    losses : array-like
        List of losses at each epoch
    xlabel : str, optional
        Name of the x axis, by default 'Epoch' (training epoch)
    ylabel : str, optional
        Name of the loss function, by default 'NLL Felsenstein loss'
    ax : matplotlib.AxesSubplot, optional
        Current axis to plot on, by default None
    kwargs
        All other keywords argument are passed to sns.lineplot

    Returns
    -------
    ax: matplotlib.axes.Axes
        The matplotlib axes containing the plot.
    """
    sns.lineplot(data=losses, color='k', ax=ax, **kwargs)

    if ax is None:
        ax = plt.gca()

    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    clear_axes(ax=ax)

    return ax
