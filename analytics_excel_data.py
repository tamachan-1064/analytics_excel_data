# -*- coding: utf-8 -*-
"""
Created on Mon May 28 20:36:09 2018

@author: tamac
"""
import xlrd
from collections import OrderedDict
# グラフ化に必要なものの準備
import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import datetime as dt

from collections import Counter
import seaborn as sns
import sys
from pprint import pprint

from scipy import stats
#この2行はfont変更させてしまう
#sns.set_style('whitegrid')
#plt.style.use('ggplot') 

#font = {"family":"ipaexg"}
#matplotlib.rc('font', **font)


# Excel ファイル(ブック)を読み込み
book = xlrd.open_workbook('結果.xlsx')

'''Excelデータ読み込み関数'''
def load_data(sheet_id, num_sample, num_ew):
    sheet = book.sheet_by_index(sheet_id)
    dic = OrderedDict()
    
    for i in range(num_sample):
        sample = sheet.cell_value(i*num_ew + 1, 0)    
        dic.setdefault(sample, OrderedDict())
        
        for rowno in range(i*num_ew + 1, i*num_ew + num_ew + 1):
            ew = sheet.cell_value(rowno, 2)
            dic[sample].setdefault(ew)
        
#        score = []
#        for j in range(20):
#            cell = sheet.cell_value(rowno,j+3)
#            score.append(cell)
            dic[sample][ew] = [sheet.cell_value(rowno,j+3) for j in range(20)]


    return dic

"""Calculates Kullback–Leibler divergence"""
def kl(w1,w2):
    return stats.entropy(w1, w2, 2)
"""Calculates JS divergence"""
def js(w1, w2):
    r = (w1 + w2) / 2
    return 0.5 * (stats.entropy(w1, r, 2) + stats.entropy(w2, r, 2))





shape = load_data(1, 25, 17)
#motion = load_data(0, 24, 19)


for sample in shape.keys():
    for ew in shape[sample].keys():
        selected_score = shape[sample][ew]
     

ew_list = list(shape[sample].keys())
sample_list = list(shape.keys())


for ew in ew_list:
    fig,ax = plt.subplots(4,6,figsize=(45,15))
    plt.subplots_adjust(wspace=0.4, hspace=0.6)
    plt.suptitle(str(ew))
    for i, sample in enumerate(sample_list[1:]):
        ax[int(i/6)][i%6].set_title(sample[:-4])
        plotted_still = sns.distplot(shape['still.jpg'][ew], rug=True, label="still", ax=ax[int(i/6)][i%6])
        plotted_sample = sns.distplot(shape[sample][ew], rug=True, label=sample[:-4], ax=ax[int(i/6)][i%6])
#    break
#    sns.plt.ylim(0, max(shape[sample][ew].key())
#"""Plot Saving as Png"""
#    plt.savefig("seaborntest_{}.png".format(ew))

#for r in range(8):
#    data_dict = [[data_x, data_y] = shape[sample][ew].lines[r].get_data()]
#    r += 1


#data_plotted_sample = [[]]
list_sample_data = OrderedDict()
still_data_x, still_data_y = plotted_still.lines[0].get_data()

for r in range(24):
    sample_data_x, sample_data_y = plotted_sample.lines[0].get_data()
    list_sample_data[r].append(sample_data_y)


#testsum=0 
#test = [h.get_height() for h in plotted_still.patches]
#for x in range(6):
#    testsum += test[x]  







hist_still = OrderedDict()
hist_sample = OrderedDict()
dict_hist_sample = OrderedDict()

for i in range(17):
    hist_data1 = np.histogram(shape['still.jpg'][ew_list[i]], bins=7, range=(1, 7),)
    hist_still.setdefault(ew_list[i], hist_data1[0])
    
    for j in range(1, 17):
        hist_data2 = np.histogram(shape[sample_list[j]][ew_list[i]], bins=7, range=(1, 7),)
        hist_sample.setdefault(ew_list[i], hist_data2[0])
        
        for k in range(1, 24):
            dict_hist_sample.setdefault(sample_list[k], hist_sample)


"""Strages Calclated JS Score"""
def calc_js(num_sample, num_ew):
    dic_js = OrderedDict()
    for i in range(1, num_sample): 
        dic_js.setdefault(sample_list[i], OrderedDict())
        for rowno in range(num_ew):
            dic_js[sample_list[i]].setdefault(ew_list[rowno], None)
            dic_js[sample_list[i]][ew_list[rowno]] = js(hist_still[ew_list[rowno]], dict_hist_sample[sample_list[i]][ew_list[rowno]])
    return dic_js


#test = calc_js(24, 17)


