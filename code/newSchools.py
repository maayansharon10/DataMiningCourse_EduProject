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

# -------------------------------- new schools --------------------------------

# create a histogram ( school name and number of appearances in table)
item_code_name = dict()  # once, building a dict of all items' code-names.
df = pd.read_excel(r"C:\Users\ASUS\PycharmProjects\DataProject\code and outputs\EduData\schools_utm.xlsx")
years_count = df["year"].value_counts()
#
# years_count.to_excel("new_schools_by_years.xlsx")

# -------------------------------- new JEWISH schools --------------------------------

# same for jewish schools only :
# create a histogram ( school name and number of appearances in table)
df_jewish = df[df['subgroup']== 'יהודי'] # zakaut without bad schools
years_count_jewish = df_jewish["year"].value_counts()
# years_count.to_excel("new_schools_by_years.xlsx")

# continue analyzing in excel new schools by years.xlsx