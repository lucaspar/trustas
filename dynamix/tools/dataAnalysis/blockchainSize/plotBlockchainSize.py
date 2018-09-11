#!/usr/bin/python
import sys
import os
import matplotlib.pyplot as plt
import pylab
import numpy as np

def plot(path):

    plt.figure()
    plt.yscale('log')

    linestyles = ['-', '--', '-.', ':']
    markers = ['*']
    i = 0
    f = []
    files = os.listdir(path)
    for file in sorted(files):
        if ".log" in file:
            f.append(int(file.split(".log")[0]))

    for file in sorted(f):
            size = open(path+str(file)+".log", "r")
            x = []
            y = []

            for line in size:
                t = line.split(" ")[0]
                s = line.split(" ")[1]

                y.append(float(s)/(1024*1024))

                x.append(int(t))

            size.close()

            print len(x), len(y)

            #pylab.title("Blockchain size x cumulative number of transactions", fontsize=18)
            if i>0 and i < 5:
                plt.plot(x, y, linestyle=linestyles[i%4], linewidth=2, label=str(file)+"-TPB")
            elif i == 5:
                plt.plot(x, y, linestyle=linestyles[i%4], linewidth=2, marker="o", markevery=1000, label=str(file)+"-TPB")
            else:
                plt.plot(x, y, linestyle=linestyles[i%4], linewidth=2, marker="x", markevery=1000, label=str(file)+"-TPB")

            i = i+1

    plt.ylabel("Blockchain size (MB)", fontsize=18)
    plt.xlabel("Cumulative number of transactions", fontsize=18)
    plt.grid(True)
#    pylab.tight_layout()
    #pylab.tick_params(labelsize=13)
    plt.xlim(0, 10000)
    plt.ylim(0, )
    pylab.legend(loc="best", fontsize=14)
    plt.legend(loc="best", ncol=2)
    plt.savefig('blockchainSize.pdf', dpi=600)
    plt.savefig('blockchainSize.png', dpi=600)
    os.system("pdfcrop %s %s" % ("blockchainSize.pdf", "blockchainSize.pdf"))
    plt.show() #uncomment to show plots during execution
    plt.clf()

#Main function
if __name__ == "__main__":
    path = sys.argv[1]
    plot(path)