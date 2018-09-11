#!/usr/bin/python
import sys
import os
import matplotlib
import pylab
import numpy as np

def plot(times):

    file = open (times, "r")

    x = []
    qt = []
    et = []
    tt = []
    for line in file:
        x.append(int(line.split()[0]))
        qt.append(float(line.split()[1]))
        et.append(float(line.split()[2]))
        tt.append(float(line.split()[3]))

    file.close()

    markers_on = [50, 100, 150, 200]

    pylab.plot(x, qt, label='Query time', linestyle="solid", linewidth=2, marker='s')
    pylab.plot(x, et, label='Establish time', linestyle="dashed", linewidth=2, marker='o')
    pylab.ylabel("Time (s)", fontsize=18)
    pylab.xlabel("Number of ASes", fontsize=18)
    pylab.grid(True)
    pylab.xticks(np.arange(50, 201, 50))
    pylab.xlim(30, 220)
    pylab.ylim(0, )
    pylab.legend(loc="best", fontsize=14)
    pylab.savefig("time.pdf", dpi=600)
    pylab.savefig("time.png", dpi=600)
    pylab.clf()

#Main function
if __name__ == "__main__":

    print sys.argv[1]
    plot(sys.argv[1])