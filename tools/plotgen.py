#!/usr/bin/env python
# Helper to generate standardized plots

from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.pyplot as plt
import math
import numpy as np
import os
import re
import sys

import plt_bandwidth as bw

DIR_PLOTS_OUTPUT    = "experiments/_plots"
DEF_FIG_SIZE        = (12, 6)
SAVE_TO_FILE        = False     # save output to file (default is to show)
SHOW_DEMOS          = False     # show plotting demos
PATTERNS            = ["/", "\\", "-", "|", "+", "x", "o", "O", ".", "*"]
CURVES = {
    '1': {
        'color': 'k',
        'linestyle': '-'
    },
    '2': {
        'color': 'r',
        'linestyle': '--'
    },
    '3': {
        'color': 'b',
        'linestyle': ':'
    },
    '4': {
        'color': 'g',
        'linestyle': '-.'
    },
    '5': {
        'color': 'k',
        'dashes': [3, 12, 3, 12],  # line, space, line, space
    },
    '6': {
        'color': 'r',
        'dashes': [1, 2, 4, 2, 1, 6],
    },
    '7': {
        'color': 'b',
        'dashes': [1, 2, 1, 2, 1, 8],
    },
    '8': {
        'color': 'g',
        'dashes': [1, 1, 1, 8],
    },
    '9': {
        'color': 'k',
        'dashes': [1, 8, 8, 1],
    },
    '10': {
        'color': 'r',
        'dashes': [2, 1, 4, 1, 8, 1],
    },
    '11': {
        'color': 'b',
        'dashes': [3, 8, 1, 1],
    },
    '12': {
        'color': 'g',
        'dashes': [1, 1, 1, 2, 1, 4],
    }
}
HELP_MSG = """

    TrustAS standardized plots generation. Plots can be static (from hardcoded data)
    or dynamic (from reference .csv files). The output is to this directory by default.

    Usage: ./plotgen.py [plot types]

    Plot types:
        file:       output to file
        traffic:    plot TrustAS network traffic (static)
        bandwidth:  calculate and plot bandwidth from TrustAS network traffic logs (dynamic)

    Example:        plotgen.py --traffic --file
"""

def set_config():
    """Set plots default configuration."""

    plt.rc('font',  family='serif')
    plt.rc('xtick', labelsize='small')
    plt.rc('ytick', labelsize='small')
    plt.rc('text',  usetex=False)

    if SHOW_DEMOS:
        plot_line_demo()
        plot_column_demo()


def plot_line_demo():

    fig = plt.figure(figsize=DEF_FIG_SIZE)
    ax = fig.add_subplot(1, 1, 1)

    x = np.linspace(0, 4*math.pi, 5)
    sin_x = 10 * np.sin(x)
    for key, curve in CURVES.items():
        factor = int(key) * 10
        ax.plot(x, factor + sin_x, **curve, label='Curve ' + key)

    ax.set_xlabel('Time [s]')
    ax.set_ylabel('Temperature [K]')
    ax.legend()

    plt.show()


def plot_column_demo():

    opacity         = 0.75
    scenarios_size  = 3
    bar_width       = 1 / (scenarios_size + 1)
    edgecolor      = 'k'

    # data to plot
    scenarios = [{
        'label': "Frank",
        'alpha': opacity,
        'width': bar_width,
        'color': 'b',
        'edgecolor': edgecolor,
        'height': (90, 55, 40, 65)
    }, {
        'label': "Guido",
        'alpha': opacity,
        'width': bar_width,
        'color': 'r',
        'edgecolor': edgecolor,
        'height': (85, 62, 54, 20)
    }, {
        'label': "Fredo",
        'alpha': opacity,
        'width': bar_width,
        'color': 'g',
        'edgecolor': edgecolor,
        'height': (85, 22, 56, 47)
    }]

    # create plot
    fig, ax     = plt.subplots()
    n_groups    = len(scenarios[0]["height"])
    index       = np.arange(n_groups)

    # plot data
    rects = []
    for idx, s in enumerate(scenarios):
        hatch = PATTERNS[ idx % len(PATTERNS) ]     # select a hatch pattern
        hatch = hatch * math.ceil(scenarios_size / 2)          # apadpt hatch density to plot density
        new_x_pos = index + (idx * bar_width)
        rects.append(plt.bar(new_x_pos, hatch=hatch, **s))
        for a, b in zip(new_x_pos, s["height"]):
            plt.text(a, b, str(b), ha='center')

    plt.xlabel('Person')
    plt.ylabel('Scores')
    plt.title('Scores by person')
    tick_positions = index + (bar_width / 2) * (scenarios_size - 1)
    print(tick_positions)
    plt.xticks(tick_positions, ('A', 'B', 'C', 'D'))
    plt.legend()

    plt.tight_layout()
    plt.show()


def plot_bandwidth():

    raw_data = bw.process_files()
    files = {}
    for filename, containers in raw_data.items():
        curves = {}
        for ctn_name, ctn in containers.items():
            # filter containers not ending in ".example.com"
            if ".example.com" not in ctn_name or ctn_name.startswith("dev-"):
                continue

            names = ctn_name.split('.')
            if names[1].startswith("org"):
                items = ("org", "XX")
                match = re.match(r"([a-z]+)([0-9]+)", names[1], re.I)
                if match:
                    items = match.groups()
                ctn_name = "AS " + items[1].zfill(2)
            elif names[0] == "orderer":
                ctn_name = "Orderer"

            curves[ctn_name] = {
                "timestamp": [],
                "bw_ing": [],
                "bw_egr": []
            }
            for idx, data in enumerate(ctn):
                curves[ctn_name]["timestamp"].append( data["timestamp"] )
                curves[ctn_name]["bw_ing"].append( data["bw_ing"] )
                curves[ctn_name]["bw_egr"].append( data["bw_egr"] )

        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1)
        fig.set_figwidth(16 / 2)
        fig.set_figheight(9 / 2)

        idx = 0
        top = -math.inf
        for ctn_name, curve in curves.items():

            overall_bandwidth = [x + y for x, y in zip(curve["bw_ing"], curve["bw_egr"])]
            useful_bandwidth = overall_bandwidth[10:]
            top = round(max(top, max(useful_bandwidth)), 2)

            mxm = round(max(useful_bandwidth), 2)
            avg = round(np.average(useful_bandwidth), 2)
            std = round(np.std(useful_bandwidth), 2)

            print("{}\t{}\t{}\t{}\t{}".format(filename, ctn_name, mxm, avg, std))

            idx = idx % len(CURVES.keys())
            ax.plot(
                curve["timestamp"],
                overall_bandwidth,
                **CURVES[str(idx + 1)],
                label=ctn_name)
            idx += 1

        # hline specs
        hlineratio = 2000
        hlinetop = (math.floor(top / hlineratio) + 1) * hlineratio
        for y in range(0, hlinetop, hlineratio):
            plt.axhline(y, color='0.3', dashes=[1, 8], linewidth=1)

        ax.set_xlabel('Time [s]')
        ax.set_ylabel('Bandwidth [kbit/s]')
        # ax.set_title(filename)
        handles, labels = ax.get_legend_handles_labels()
        labels, handles = zip(*sorted(zip(labels, handles), key=lambda t: t[0]))
        ax.legend( handles, labels, ncol=math.ceil(len(labels)/4) )
        # ax.legend()

        # if SAVE_TO_FILE:
        #     fname = '.'.join(filename.split('.')[:-1]) + ".pdf"
        #     save_to_pdf(os.path.join(DIR_PLOTS_OUTPUT, fname))
        # else:
        #     plt.show()


def plot_traffic_one():
    """Plots the following data:
    ASes    & ingress (peers)   & egress (orderer)
    10      & 15.66             & 13.7
    25      & 38.39             & 35.5
    50      & 79.98             & 75.1
    75      & 122.58            & 115.0
    100     & 159.61            & 150.0
    """

    opacity         = 0.6
    edgecolor       = '0.2'
    scenarios_size  = 4
    bar_width       = 1 / (scenarios_size + 1)

    # data to plot
    fname   = 'exp_net_traffic.pdf'
    # title   = 'TrustAS: cost of relevant network traffic'
    title   = ''
    xlabel  = 'ASes in the network'
    ylabel  = 'Network traffic (log scale) [MB]'
    xticks  = ('10', '25', '50', '75', '100')
    scenarios = [
        {
            'label': "Orderer Ingress",
            'alpha': opacity,
            'width': bar_width,
            'color': 'y',
            'edgecolor': edgecolor,
            'height': (1.23, 1.36, 1.49, 1.55, 1.53)
        },
        {
            'label': "Aggregated AS Egress",
            'alpha': opacity,
            'width': bar_width,
            'color': 'g',
            'edgecolor': edgecolor,
            'height': (1.12, 1.77, 3.26, 4.88, 5.91)
        },
        {
            'label': "Orderer Egress",
            'alpha': opacity,
            'width': bar_width,
            'color': 'r',
            'edgecolor': edgecolor,
            'height': (13.7, 35.5, 75.1, 115, 150)
        },
        {
            'label': "Aggregated AS Ingress",
            'alpha': opacity,
            'width': bar_width,
            'color': 'b',
            'edgecolor': edgecolor,
            'height': (15.66, 38.39, 79.98, 122.58, 159.61)
        },
    ]

    # dynamic settings
    fig, ax         = plt.subplots()
    plt.clf()
    n_groups        = len(scenarios[0]["height"])
    index           = np.arange(n_groups)
    density         = scenarios_size + n_groups
    tick_positions  = index + (bar_width / 2) * (scenarios_size - 1)

    # hline specs
    for idx, y in enumerate([1, 2, 5, 10, 20, 50, 100, 200]):
        hcolor = '0.6'
        plt.axhline(y, color=hcolor, dashes=[1, ((idx % 3) + 1) * 2], linewidth=1)

    # plot data
    rects = []
    for idx, s in enumerate(scenarios):

        hatch = PATTERNS[idx % len(PATTERNS)]   # select a hatch pattern
        hatch = hatch * math.ceil(density / 3)  # adapt hatch density to plot density

        new_x_pos = index + (idx * bar_width)
        rects.append(plt.bar(new_x_pos, hatch=hatch, **s))
        for a, b in zip(new_x_pos, s["height"]):
            plt.text(a, b*1.05, str(round(b,1)), ha='center', fontsize=8)

    fig.set_figwidth(16 / 2)
    fig.set_figheight(9 / 2)
    plt.yscale('log')
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.xticks(tick_positions, xticks)
    plt.legend()
    plt.tight_layout()

    if SAVE_TO_FILE:
        save_to_pdf(os.path.join(DIR_PLOTS_OUTPUT, fname))
    else:
        plt.show()


def plot_traffic_two():
    """Plots the ingress and egress of orderer and 5 ASes
    orderer,    1.01MB / 6.88MB,    1010,   6880
    AS 1,       2.12MB / 1.04MB,    2120,   1040
    AS 2,       1.38MB / 24.6kB,    1380,   24.6
    AS 3,       1.38MB / 25.1kB,    1380,   25.1
    AS 4,       1.38MB / 25.2kB,    1380,   25.2
    AS 5,       1.38MB / 24.8kB,    1380,   24.8
    """

    opacity = 0.6
    edgecolor = 'k'
    scenarios_size = 2
    bar_width = 1 / (scenarios_size + 1)

    # data to plot
    fname = 'exp_net_traffic_by_peer.pdf'
    # title   = 'TrustAS: cost of relevant network traffic'
    title = ''
    xlabel = ''
    ylabel = 'Network traffic [MB]'
    xticks = ('Orderer', 'AS 1', 'AS 2', 'AS 3', 'AS 4', 'AS 5')
    scenarios = [
        {
            'label': "Ingress",
            'alpha': opacity,
            'width': bar_width,
            'color': 'b',
            'edgecolor': edgecolor,
            'height': (1.01, 2.12, 1.38, 1.38, 1.38, 1.38)
        },{
            'label': "Egress",
            'alpha': opacity,
            'width': bar_width,
            'color': 'r',
            'edgecolor': edgecolor,
            'height': (6.88, 1.04, 0.02, 0.03, 0.03, 0.02)
        }
    ]

    # dynamic settings
    fig, ax = plt.subplots()
    plt.clf()
    n_groups = len(scenarios[0]["height"])
    index = np.arange(n_groups)
    density = scenarios_size + n_groups
    tick_positions = index + (bar_width / 2) * (scenarios_size - 1)

    # plot data
    top = -math.inf
    rects = []
    for idx, s in enumerate(scenarios):

        hatch = PATTERNS[idx % len(PATTERNS)]  # select a hatch pattern
        hatch = hatch * math.ceil(
            density / 3)  # adapt hatch density to plot density

        new_x_pos = index + (idx * bar_width)
        rects.append(plt.bar(new_x_pos, hatch=hatch, **s))
        for a, b in zip(new_x_pos, s["height"]):
            plt.text(a, b + 0.03, str(b), ha='center')
            top = max(top, b)

    # hline specs
    hlineratio = 2
    hlinetop = (math.floor(top / hlineratio) + 1) * hlineratio
    for y in range(0, hlinetop, hlineratio):
        plt.axhline(y, color='0.5', dashes=[1, 8], linewidth=1)

    # plt.rcParams["figure.figsize"] = [8, 4]
    fig.set_figwidth(16 / 2)
    fig.set_figheight(9 / 2)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.xticks(tick_positions, xticks)
    plt.legend()
    plt.tight_layout()

    if SAVE_TO_FILE:
        save_to_pdf(os.path.join(DIR_PLOTS_OUTPUT, fname))
    else:
        plt.show()


def save_to_pdf(fpath):
    pp = PdfPages(fpath)
    pp.savefig()
    pp.close()
    print("Saved to {}".format(fpath))


def mkdir_p(mypath):
    '''Creates a directory. Equivalent to using mkdir -p <mypath> on the command line.'''

    from errno import EEXIST
    from os import makedirs, path

    try:
        makedirs(mypath)
    except OSError as exc:
        if exc.errno == EEXIST and path.isdir(mypath):
            pass
        else:
            raise


def main():

    global SAVE_TO_FILE
    global SHOW_DEMOS

    set_config()

    plt_traffic = False
    plt_bandwidth = False

    argv = sys.argv[1:]
    for p in argv:
        if len(p) == 0:
            continue
        elif "--help" in p:
            print(HELP_MSG)
            exit(0)
        elif "--file" in p:
            SAVE_TO_FILE = True
            mkdir_p(DIR_PLOTS_OUTPUT)
        elif "--demos" in p:
            SHOW_DEMOS = True
        elif "--traffic" in p:
            plt_traffic = True
        elif "--bandwidth" in p:
            plt_bandwidth = True
        else:
            print("Unknown plotting type '{}'\n\n{}".format(p, HELP_MSG))
            exit(1)

    if plt_traffic:
        print("Generating traffic plot")
        plot_traffic_one()
        # plot_traffic_two()

    if plt_bandwidth:
        print("Generating bandwidth plot")
        plot_bandwidth()

main()
