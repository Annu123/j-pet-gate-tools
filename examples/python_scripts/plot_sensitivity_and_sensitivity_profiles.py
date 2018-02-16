#!/usr/bin/env python
# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
from numpy import *
from matplotlib import rcParams, rcdefaults, rc
from matplotlib.colors import LogNorm
import matplotlib.image as mpimg
import operator
import pylab
from matplotlib.ticker import FormatStrFormatter
import os

def create_label (template, label_old):

    label_new = ""
    tmp = label_old.split('_')

    flag = 0
    for i in range(len(tmp)):
        if tmp[i]!=template and tmp[i]!="7mm":
            if tmp[i]=="D75":
                label_new += "D=75cm"
            elif tmp[i]=="D85":
                label_new += "D=85cm"
            elif tmp[i]=="D95":
                label_new += "D=95cm"
            elif tmp[i]=="1lay":
                label_new += "1 layer"
            elif tmp[i]=="2lay":
                label_new += "2 layers"
            elif tmp[i]=="L020":
                label_new += "L=20cm"
            elif tmp[i]=="L050":
                label_new += "L=50cm"
            elif tmp[i]=="L100":
                label_new += "L=100cm"
            else:
                label_new += tmp[i]
            if (flag==0):
                label_new += ', '
                flag = 1

    return label_new

if __name__ == "__main__":

  rcParams['font.size'] = 24
  rcParams['legend.fontsize'] = 10
  outputformat = ".png"

  coincidences_directory = "./Results/Sensitivity/"

  workdir = "./Results/Sensitivity/"
  if (not os.path.isdir(workdir)): os.system("mkdir " + workdir)

  files = ["D75_1lay_L020_7mm", "D75_1lay_L050_7mm", "D75_1lay_L100_7mm", "D75_2lay_L020_7mm", "D75_2lay_L050_7mm", "D75_2lay_L100_7mm", "D85_1lay_L020_7mm", "D85_1lay_L050_7mm", "D85_1lay_L100_7mm", "D85_2lay_L020_7mm", "D85_2lay_L050_7mm", "D85_2lay_L100_7mm", "D95_1lay_L020_7mm", "D95_1lay_L050_7mm", "D95_1lay_L100_7mm", "D95_2lay_L020_7mm", "D95_2lay_L050_7mm", "D95_2lay_L100_7mm"]

  data = {}

  for coincidences_file in files:

    sensitivity = float(loadtxt(coincidences_directory + coincidences_file + "_sensitivity.txt"))
    sensitivityProfile = loadtxt(coincidences_directory + coincidences_file + "_sensitivity_profile.txt")

    data[coincidences_file] = [sensitivity, sensitivityProfile]

  N = 0

  templates = ["D75", "D85", "D95", "L020", "L050", "L100", "1lay", "2lay"]

  titles = ["D = 75 cm", "D = 85 cm", "D = 95 cm", "L = 20 cm", "L = 50 cm", "L = 100 cm", "1 layer", "2 layers"]

  for i in range(len(templates)):

    fig = plt.figure(figsize=(8, 6))
    ax = fig.add_subplot(111)
    plt.subplots_adjust(left=0.15, right=0.99, top=0.91, bottom=0.17)

    t = templates[i]
    data_tmp = {}

    for d in data:

      if t in d:
        data_tmp[d] = data[d]

    data_sorted = sorted(data_tmp.items(), key=operator.itemgetter(0))

    plt.clf()

    for d in data_sorted:

      if "1lay" in d[0]:
        lw = 1
      elif "2lay" in d[0]:
        lw = 3

      if "D75" in d[0]:
          ls = '--'
      elif "D85" in d[0]:
          ls = '-'
      elif "D95" in d[0]:
          ls = '-.'

      if "L020" in d[0]:
          N = 20
          c = 'red'
      elif "L050" in d[0]:
          N = 50
          c = 'black'
      elif "L100" in d[0]:
          N = 100
          c = 'blue'

      arguments = linspace(-N/2.+0.5,N/2-0.5, N)

      # Group specific settings
      if t in ["D75", "D85", "D95"]:
        rcParams['font.size'] = 30
        rcParams['legend.fontsize'] = 18
        plt.ylim([0,12])
        plt.gca().get_yaxis().set_major_formatter(FormatStrFormatter('%d'))
        plt.gca().get_yaxis().set_ticks([0,5,10])
      elif t in ["L020", "L050", "L100"]:
        rcParams['font.size'] = 30
        rcParams['legend.fontsize'] = 18
      elif t in ["1lay", "2lay"]:
        rcParams['font.size'] = 26
        rcParams['legend.fontsize'] = 12

      plt.plot(arguments, d[1][1], label=create_label(t,d[0]), linewidth=lw, linestyle=ls, color=c)

    if t=="L020":
      plt.gca().get_yaxis().set_major_formatter(FormatStrFormatter('%d'))
      plt.gca().get_yaxis().set_ticks([0,1])
    elif t=="L100":
      plt.gca().get_yaxis().set_major_formatter(FormatStrFormatter('%d'))
      plt.gca().get_yaxis().set_ticks([0,5,10])

    plt.title(titles[i] + ", 7 mm")
    plt.xlabel("Position along z axis [cm]")
    plt.ylabel("Sensitivity [cps/kBq]")
    #plt.legend(loc=1)
    plt.xlim(-35,35)
    plt.ylim(ymin=0)
    plt.savefig(workdir + "sensitivityProfile_" + t + outputformat)

    # create a second figure for the legend
    #figlegend = pylab.figure(figsize = (8,6))
    # produce a legend for the objects in the other figure
    #pylab.figlegend(*ax.get_legend_handles_labels(), loc = 'upper left')
    #figlegend.savefig(workdir + "sensitivityProfile_" + t + '_legend' + outputformat)
    #figlegend.clf()

    plt.clf()

  plt.xlabel("Length of scintillator [cm]")
  plt.ylabel("Sensitivity [cps/kBq]")

  L = [20,50,100]
  D75_1lay = [data["D75_1lay_L020_7mm"][0], data["D75_1lay_L050_7mm"][0], data["D75_1lay_L100_7mm"][0]]
  D85_1lay = [data["D85_1lay_L020_7mm"][0], data["D85_1lay_L050_7mm"][0], data["D85_1lay_L100_7mm"][0]]
  D95_1lay = [data["D95_1lay_L020_7mm"][0], data["D95_1lay_L050_7mm"][0], data["D95_1lay_L100_7mm"][0]]
  D75_2lay = [data["D75_2lay_L020_7mm"][0], data["D75_2lay_L050_7mm"][0], data["D75_2lay_L100_7mm"][0]]
  D85_2lay = [data["D85_2lay_L020_7mm"][0], data["D85_2lay_L050_7mm"][0], data["D85_2lay_L100_7mm"][0]]
  D95_2lay = [data["D95_2lay_L020_7mm"][0], data["D95_2lay_L050_7mm"][0], data["D95_2lay_L100_7mm"][0]]

  plt.plot(L, D75_1lay, '*', color='r', label="D=75cm, 1 layer")
  plt.plot(L, D85_1lay, 'o', color='r', label="D=85cm, 1 layer")
  plt.plot(L, D95_1lay, '+', color='r', label="D=95cm, 1 layer")
  plt.plot(L, D75_2lay, '*', color='k', label="D=75cm, 2 layers")
  plt.plot(L, D85_2lay, 'o', color='k', label="D=85cm, 2 layers")
  plt.plot(L, D95_2lay, '+', color='k', label="D=95cm, 2 layers")
  rcParams['font.size'] = 24
  rcParams['legend.fontsize'] = 18
  plt.legend(loc=2)

  plt.savefig(workdir + "Sensitivities" + outputformat, bbox_inches='tight')
  plt.clf()
