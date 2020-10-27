from collections import Counter
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


def plt_dic_regular(dic, name, num):
    """
    function: making a sorted plot and top appearing words.
    :param dic: unsorted dic of tokens and appearances.
    :param name : what the plot is about
    :param num: total number of objects we plot
    output: a plot
    """
    sorted_dic = {k: v for k, v in sorted(dic.items(), key=lambda item: item[
        1],reverse=True)}
    fig = plt.figure()
    ax1 = fig.add_subplot(111)
    ax1.scatter(sorted_dic.keys(),sorted_dic.values(), s=10, c='b', marker="s")
    #ax1.set_yscale('symlog')
    #ax1.set_xscale('symlog')
    ax1.get_xaxis().set_ticks([])
    plt.xlabel("towns")
    plt.ylabel("number of schools in town")

    plt.title(name + ": Freq of "+str(num)+" Schools\n [from file bagruyot 2013-2016.xlsx, InstitutionList] ")
    plt.show()


def plt_dic_regular_with_names(dic, name, num):
    """
    function: making a sorted plot and top appearing words.
    :param dic: unsorted dic of tokens and appearances.
    :param name : what the plot is about
    :param num: total number of objects we plot
    output: a plot
    """
    # reverse the lables to print well in hebrew :
    keys = dic.keys()
    new_k = []
    for key in keys:
        new_k.append(key[::-1])
    keys = new_k
    values = dic.values()
    dictionary = dict(zip(keys, values))
    dic = dictionary

    sorted_dic = {k: v for k, v in sorted(dic.items(), key=lambda item: item[
        1],reverse=True)}

    fig = plt.figure()
    ax1 = fig.add_subplot(111)
    ax1.scatter(sorted_dic.keys(),sorted_dic.values(), s=10, c='b', marker="s")
    #ax1.set_yscale('symlog')
    #ax1.set_xscale('symlog')
    #ax1.get_xaxis().set_ticks([])
    plt.xlabel("towns")
    plt.ylabel("number of schools in town")
    plt.xticks(rotation='vertical')
    plt.title(name + ": Freq of "+str(num)+" Schools\n [from file bagruyot 2013-2016.xlsx, InstitutionList] ")
    plt.show()



def plt_dic_log(dic, name, num):
    """
    function: making a log sorted plot and top appearing words.
    :param dic: unsorted dic of tokens and appearances.
    :param name : what the plot is about
    :param num: total number of objects we plot
    output: a plot
    """
    sorted_dic = {k: v for k, v in sorted(dic.items(), key=lambda item: item[
        1],reverse=True)}
    fig = plt.figure()
    ax1 = fig.add_subplot(111)
    ax1.scatter(sorted_dic.keys(),sorted_dic.values(), s=10, c='b', marker="s")
    # ax1.set_yscale('symlog')
    ax1.set_xscale('symlog')
    plt.xlabel("school names")
    plt.ylabel("freq of apperacne")
    plt.title(name + "Freq of "+str(num)+" schools\n (form file bagruyot 2013-2016.xlsx, InstitutionList) ")
    plt.show()



#create data frame obj:
df = pd.read_excel(r"C:\Users\ASUS\PycharmProjects\DataProject\files\bagruyot - 2013-2016.xlsx",sheet_name='InstitutionList')

# delete all schools which are not high schools:
# (Get names of indexes for which column שלב בחינוך has value 1 )
indexNames = df[ (df['קוד שלב חינוך'] == 1) | (df['קוד שלב חינוך'] ==3) | (df['קוד שלב חינוך'] ==5) ].index
df.drop(indexNames , inplace=True) # only high schools!!!!

# get city and number of schools in city:
df = df.groupby('יישוב')['סמל מוסד'].nunique()
# convert into dict and plot graph:
df_dict = df.to_dict()
plt_dic_regular(df_dict, "Number of High Schools per Town", 363)

# print(df)  # df with town - number of schools
# print(df_dict)

new_dict = dict()
for key in df_dict:
    if df_dict[key]>20:
        new_dict[key] = df_dict[key]

#indexNames = df[ (df['יישוב'] > 10)].index
#df.drop(indexNames , inplace=True) # only highschools!!!!
plt_dic_regular_with_names(new_dict, "Number of High Schools per Town", len(new_dict))

