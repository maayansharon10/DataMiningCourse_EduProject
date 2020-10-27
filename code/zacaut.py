import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix
import pandas as pd
from bidi import algorithm as bidialg


# list of all features to check
zacaut_cols = ['אחוז זכאים לבגרות   ','אחוז זכאות לבגרות  מצטיינת    ','אחוז זכאות 4 יחידות אנגלית   ',
       'אחוז זכאות 4 יחידות אנגלית  -חינוך רגיל   ',
       'אחוז זכאות 5 יחידות אנגלית   ',
       'אחוז זכאות 5 יחידות אנגלית - חינוך רגיל   ',
       '  אחוז זכאות 4 יחידות מתמטיקה    ',
       'אחוז זכאות 4 יחידות מתמטיקה-  חינוך רגיל   ',
       'אחוז זכאות 5 יחידות מתמטיקה    ',
       'אחוז זכאות 5 יחידות מתמטיקה-  חינוך רגיל   ',]


def groups_by_sect_quint(df):
    """
    checks the Bagrut zacaut in all subsets of the data by sector and
    quintile, based on the data of columns: 'מגזר' and 'חמשון מדד טיפוח/נוער בסיכון'
    :param df: the zacaut raw dataframe
    :return: df with the information on all the mean and var of the subsets
    """
    quintiles = list(df["חמשון מדד טיפוח/נוער בסיכון"].unique())
    sectors = list(df['מגזר'].unique())
    output  = pd.DataFrame(columns=["quintile","sector","zacaut kind",
                                    "mean", "var"])
    idx = 0
    for quint in quintiles:
        quint_df = df[df["חמשון מדד טיפוח/נוער בסיכון"]==quint]
        for sect in sectors:
            sect_quint = quint_df[quint_df['מגזר']==sect]
            for col in zacaut_cols:
                #box_plot_col(col, sect,quint, sect_quint,str(idx))
                try:
                    mean = sect_quint.groupby("מגזר")[col].mean()[sect]
                    var = sect_quint.groupby("מגזר")[col].var()[sect]
                    output.loc[idx] = [quint, sect, col, mean, var]
                    idx+=1
                except:
                    print([col,sect,quint])
    return output


def official_group(df):
    """
    checks the Bagrut zacaut in all subsets of the data by official groups,
    based on the data of columns: 'אחוז זכאים לבגרות -קבוצת  דומים  '
    :param df: the zacaut raw dataframe
    :return: df with the information on all the mean and var of the subsets
    """
    groups = list(df['אחוז זכאים לבגרות -קבוצת  דומים  '].unique())
    print(groups)
    output = pd.DataFrame(columns=['group', "zacaut kind","mean", "var"])
    idx = 0
    for i, subset in enumerate(groups):
        for col in zacaut_cols:
            #box_plot_col_official(col, i, df,str(idx))
            try:
                mean = df.groupby('אחוז זכאים לבגרות -קבוצת  דומים  ')[
                    col].mean()[subset]
                var = df.groupby('אחוז זכאים לבגרות -קבוצת  דומים  ')[
                    col].var()[subset]
                output.loc[idx] = [idx, col, mean, var]
                idx += 1
            except:
                print((col,subset))
    return output


def study_case(group):
    """
    takes one given group of "alike schools" that the education system is now
    working by it, and checks the sector + quintile destribusion in it.
    :param group: dataframe of one group of "alike schools"
    :return: consule print of the information.
    """
    studycase = df[df['אחוז זכאים לבגרות -קבוצת  דומים  ']==group]
    quintiles = list(studycase["חמשון מדד טיפוח/נוער בסיכון"].unique())
    sectors = list(studycase['מגזר'].unique())
    for sect in sectors:
        cnt = studycase["מגזר"][sect].count()
        print([sect, cnt])
    for quint in quintiles:
        cnt = studycase["חמשון מדד טיפוח/נוער בסיכון"][quint].count()
        print([quint, cnt])


def vis_cm(cm, labels):
    """
    visualising confusion matrix between to categories of school grouping.
    :param cm: confusion matrix object
    :param labels: list of labels of the groups in the matrix.
    :return: plot of cunfusion matrix.
    """
    fig = plt.figure()
    ax = fig.add_subplot(111)
    cax = ax.matshow(cm)
    plt.title('Confusion matrix - sector+quintile vs clusters')
    fig.colorbar(cax)
    ax.set_xticklabels([''] + labels)
    ax.set_yticklabels([''] + labels)
    plt.xlabel('sectors and quintiles')
    plt.ylabel('cluster')
    plt.show()


def cor_mat_prep(df):
    """
    preperation function that takes a given dataframe and turns it to
    one-year dataframe with only  school, used group, and optional group we
    want to check.
    :param df: raw dataframe, mainly used for "school - bagrut.xls"
    :return: xls file
    """
    out = pd.DataFrame(columns=["school", "old group"])
    df1 = df[df['שנה"ל']=="תשעח"]
    out["school"] = df1["שם מוסד"]
    out["old group"] = df1["אחוז זכאים לבגרות -קבוצת  דומים  "]
    for idx, row in df1.iterrows():
        out.at[idx, "new group"] = str(row["מגזר"]) + str(row["חמשון מדד "
                                                              "טיפוח/נוער בסיכון"])
    out = out.astype('category')
    out.to_excel("2 groups.xls")


def cor_mat_groups():
    """
    takes a pre-prepred file, and makes a condusion matrix from it.
    :return: print the cunfusion matrix and calls the vis function.
    """
    clean = pd.read_excel("clusters vs newgroups.xlsx")
    cm_df = pd.DataFrame(columns=["quint","clusters"])
    labels = list(range(17))
    idx_group = list(clean["new group"].unique())
    idx_group1 = list(clean["clusters"].unique())
    for idx, row in clean.iterrows():
        cm_df["quint"].loc[idx] = int(idx_group.index(row["new group"]))
        cm_df["clusters"].loc[idx] = int(idx_group1.index(row["clusters"]))
    cm = confusion_matrix(cm_df["quint"],cm_df["clusters"],labels)
    print(cm)
    vis_cm(cm, labels)


def box_plot_col(col,sect,quint,box_df,idx):
    """
    function to make boxplots for all column in the dataframe
    :param col: the name of the column
    :param sect: sector for title
    :param quint: quintile for title
    :param box_df: dataframe
    :param idx: used for file name
    :return: boxplot as file
    """
    fig1, ax1 = plt.subplots()
    title = bidialg.get_display(col) + 'group: ' + bidialg.get_display(sect)\
            + quint + ' boxplot'
    ax1.set_title(title)
    ax1.boxplot(box_df[col])
    plt.savefig('fig'+idx)
    print('box plot made')


def box_plot_col_official(col,subset,box_df,idx):
    """
    redesigned function, for specail check on the old groups ("alike
    schools").
    :return: boxplot as filw
    """
    fig1, ax1 = plt.subplots()
    title = bidialg.get_display(col) + 'group: ' + str(subset) + ' boxplot'
    ax1.set_title(title)
    ax1.boxplot(box_df[col])
    plt.savefig('fig'+idx + col)
    print('box plot made')


df = pd.read_excel(r'C:\Users\PC\Documents\all_files\school - bagrut.xlsx')
out = groups_by_sect_quint(df)
out.to_excel("zacaut by sect+quint 1.xls")
out1 = official_group(df)
out1.to_excel("zacaut by official groups1.xls")
cor_mat_groups()
