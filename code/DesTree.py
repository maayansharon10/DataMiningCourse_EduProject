# DataFrame:
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn import tree
# Vis:
import matplotlib.pyplot as plt
import pydotplus  # GraphVis for tree


### ----- Visualization -------------------- #######

def vis_tree(clf, class_names,features):
    """
    function that takes a tree classifier and visualizing it.
    :param clf: a trained model of decision tree.
    :param class_names: a list of all labels of the tree
    :param features: a list of all columns of the dataframe (features for
    the tree)
    :return: visualization as plt.show and as image
    """
    dot_data = tree.export_graphviz(clf, out_file=None,
                         feature_names=features,
                         class_names=class_names,
                         filled=True, rounded=True,
                         special_characters=True)
    graph = pydotplus.graph_from_dot_data(dot_data)
    graph.write_png('Tree.png')
    fig, ax = plt.subplots(figsize=(24, 24))
    ax.imshow(plt.imread('Tree.png'))
    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)
    plt.show()


### ----- Helper functions (input and data preperation) --------- #######

def input_function():
    """
    function that runs the input conversation with the user
    :return: the chosen keys of: label raw data (col key), label
    aggregation (bin_key, label_key), year of choice (year).
    """
    bool = True
    while bool:  # run basic question of year choice until answer is given
        year = input("choose year:\n"
                     "1-'תשעח', 2-'תשעז', 3-'תשעו', 4-'תשעה', 5-'תשעד' "
                     "0-exit\n")
        if year in ["1","2","3","4","5"]:
            bool = False
        elif year =="0":
            print("goodbye :)")
            exit()
        else:
            print("wrong input, try again")
    bool=True
    while bool: # run question of label choice until answer is given
        col_key = input("choose zacaut kind:\n"
              "1 - general\n"
              "2 - english -4 units\n"
              "3 - english -5 units\n"
              "4 - math - 4 units\n"
              "5 - math - 5 units\n"
              "6 - excellency\n"
              "0 - to exit\n")
        if col_key == "0":
            print("goodbye :)")
            exit()
        if col_key in ["1","2","3","4","5","6"]:
            bool = False
        else:
            print("wrong input, try again")
    bool = True
    while bool:  # run basic question of function of choice to adjust the
        # labels until answer is  given
        label_key = input("good! now choose labeling options:\n"
              "for threshold (example: 60>) - choose 1\n"
              "for binning (0-20,21-20, ect.) - choose 2\n"
              "for exit - choose 0\n")
        if label_key =="1":  # if chosen, runs the threshold choice until given
            bin_key = input("good! now choose threshold options (between "
                            "1-99), or insert 0 for exit\n")
            if bin_key.isdigit():
                if int(bin_key) in list(range(1,99)):
                    bool = False
                elif bin_key == "0":
                    print("goodbye :)")
                    exit()
            else:
                print("wrong input, choose threshold again")
        elif label_key == "2":  # if chosen, runs the binning choice until
            # given
            bin_key = input("good! now choose binning options:\n"
                        "50 - for bins of 50s\n"
                        "20 - for bins of 20s\n "
                        "10 - for bins of 10s\n"
                        "0 - to exit\n")
            if bin_key.isdigit():
                if int(bin_key) in [20,10,5]:
                    bool = False
                elif bin_key == "0":
                    print("goodbye :)")
                    exit()
            else:
                print("wrong input, choose  again")
    return col_key, bin_key, label_key,year


def threshold(df,bin,year,col):
    """
    sub function of turning the data of the label to the boolian threshold
    chosen
    :param df: main Dataframe
    :param bin: the key of the threshold cuter
    :param year: year
    :param col: the name of the data column for the label chosen
    :return: out - dataframe as needed , labels - list of label types (0,1),
    col - column name.
    """
    # choosing relevant data for features, and copy to new dataframe.
    rel_data = ['שנה"ל', 'מחוז מפקח', 'שם רשות', 'צבע מסלול בית ספר',
                'חמשון מדד טיפוח/נוער בסיכון', 'מגזר', 'סוג פיקוח']
    out = df.filter(rel_data, axis=1)
    # filter data rows by year and delet column:
    out = out[out['שנה"ל'] == year]  # check for one year
    del out['שנה"ל']  # delete 'שנה"ל' col from df
    rel_data.remove('שנה"ל')  # delete 'שנה"ל' col from list
    # process the tree by making all categorical features dummies and label
    # as boolian 0/1 :
    print("processing tree...")
    out = pd.get_dummies(out, columns=rel_data, drop_first=True) # drop
    # first because of multico-liniarity
    for idx, row in df.iterrows(): # adjust labels by threshold
        if row[col] > int(bin):
            out.at[idx, col] = 1
        else:
            out.at[idx, col] = 0
    labels = ["0", "1"]
    return out, labels, col


def bins(df, year,col,bin):
    """
    sub function of turning the data of the label to the categorical bins
    chosen
    :param df: dataframe
    :param year: year
    :param col: column name for labels
    :param bin: binning key
    :return: out - adjusted dataframe, labels - list of label kinds,
    col - column name, y_lable - the full data of the labels
    """
    # dictionary for turning key to bins list
    bins_dict = {50: [0, 50, 100],
                 20: [0, 20, 40, 60, 80, 100],
                 10: [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]}
    # choosing relevant data for features and adjust data frame by year:
    rel_data = ['שנה"ל', 'מחוז מפקח', 'שם רשות', 'צבע מסלול בית ספר',
                'חמשון מדד טיפוח/נוער בסיכון', 'מגזר', 'סוג פיקוח', col]
    out = df.filter(rel_data, axis=1)
    out = out[out['שנה"ל'] == year]  # check for one year
    del out['שנה"ל']  # delete 'שנה"ל' col from df
    rel_data.remove('שנה"ל')  # delete 'שנה"ל' col from list
    rel_data.remove(col)  # delete col from list of dummies
    # adjusting labels from row data by bining:
    print("processing tree...")
    bins = bins_dict[int(bin)]
    category = pd.cut(out[col], bins)
    category = category.to_frame()
    category.columns = ['range']
    labels = [str(i) for i in category['range'].unique()]
    # concatenate column and its bins column
    out = pd.concat([out, category], axis=1)
    y_lable = out["range"] # the full data of the labels.
    del out[col]
    del out["range"]
    # make output dataframe with dummies (exept first because of
    # multicoliniarity
    out = pd.get_dummies(out, columns=rel_data, drop_first=True)
    return out, labels, col, y_lable


def df_for_tree(df):
    """
    main function to adjust the dataframe for the tree model, using the
    subfunctions of "threshold or binning as needed.
    :param df: row data
    :return: out - adjusted dataframe, labels - label lis for tree,
    col -column name for tree usage,
    label_kind - key to chose relevant tree creation for threshold/binnig
    labels
    y_lable - label dat (relevant only for binning tree).
    """
    # dictionaries to change given keys to needed values:
    zacaut_cols = {1:'אחוז זכאים לבגרות   ',
                   2: 'אחוז זכאות 4 יחידות אנגלית   ',
                   3:'אחוז זכאות 5 יחידות אנגלית   ',
                   4:'  אחוז זכאות 4 יחידות מתמטיקה    ',
                   5:'אחוז זכאות 5 יחידות מתמטיקה    ',
                   6:'אחוז זכאות לבגרות  מצטיינת    '}
    year_dic = {'1':'תשעח', '2':'תשעז', '3':'תשעו', '4':'תשעה', '5':'תשעד'}

    print("hello! choose Bagrut zacaut feature from the list: ")
    col_key, bin, label_kind,year_code = input_function() # asks the user for
    # column, and labeling options.
    year = year_dic[year_code] # gets the chosen column name
    col = zacaut_cols[int(col_key)] # gets the chosen column name

    # make labels column (threshold / bins):
    if label_kind =="1": # threshold
        out, labels, col = threshold(df, bin, year, col)
        y_lable = []
    else:
        out, labels, col, y_lable = bins(df, year,col,bin)
    return out, labels, col, label_kind,y_lable


### ---------- Main function -----------------------###

def main_tree():
    """
    main function, takes the row bagrut data and runs all fuction to make a
    tree for the user
    :return: tree info and visulaizasion
    """
    full_data = pd.read_excel(r'C:\Users\PC\Documents\all_files\school - bagrut.xlsx')
    # gets the input and prep the dataframe:
    clean_data, labels,col,label_kind,y_lable = df_for_tree(full_data) # cuts the
    # dataframe by the wanted labeling given by the user

    if label_kind == "1":  #tree making if labels created by threshold
        no_labels = clean_data.copy()
        del no_labels[col]
        features = list(no_labels.columns)
        X_train, X_test, y_train, y_test = train_test_split(no_labels,
                                                            clean_data[col],
                                                            test_size=0.25,
                                                            random_state=42)
        # make tree model with max depth of 10 - because more is not
        # relevant for explorative usage and because it's not able to get to
        # singletons.
        clf = tree.DecisionTreeClassifier(max_depth=10)
        X_train = X_train.fillna(0)
        X_test = X_test.fillna(0)
        clf.fit(X_train,y_train)
        # get evaluation of the presition of the tree
        print("Decision Tree Precision:" + str(clf.score(X_test,y_test)))
    else:  # for making tree with binned labels.
        features = list(clean_data.columns)
        y_lable = [str(i) for i in y_lable]
        print(y_lable)
        X_train, X_test, y_train, y_test = train_test_split(clean_data,
                                                            y_lable,
                                                            test_size=0.25,
                                                            random_state=42)
        clf = tree.DecisionTreeClassifier(max_depth=10)
        X_train = X_train.fillna(0)
        X_test = X_test.fillna(0)
        clf.fit(X_train, y_train)
        print("Decision Tree Precision:" + str(clf.score(X_test, y_test)))
    vis_tree(clf,labels,features)
    print("Take a look at the tree! ... (as plt.show and as file:'tree.png'")


#### ----------------- run program ------------------##########
main_tree()