import pandas as pd
import glob
from xlsxwriter.workbook import Workbook

# ---------- functions: -------------------------------------------

def add_new_schools(rawDf,outDf, colname):
    """ func: runs in a given data frame and updates the main output
              data frame with indications about the schools in it
        input: rawDf - data frame made from source files
               outDf - the main aggregated df.
        output: updated outDf
    """
    # take all current שם מוסד in output file
    schoolCoods = outDf["instNum"].to_list()
    # creat column for file (with indicative shorten column name)
    colname = colname[-30:]
    outDf[colname] = pd.Series([0]*len(schoolCoods))

    # check all שם מוסד in file, insert True to the file column, and if it's
    # new insert False to others, and appends the new row.
    for idx, code in enumerate(rawDf["סמל מוסד"].items()):
        if code[1] in schoolCoods:
            outDf.at[outDf[outDf["instNum"] == code[1]].index, colname] = \
                True
        else:
            newdata = [{"instNum": code[1],"instName":rawDf.at[idx,"שם מוסד"],
                                       "city":rawDf.at[idx, "שם רשות"]}]
            for col in outDf.columns[3:].to_list():
                if col == colname:
                    newdata[0].update({col:True})
                else:
                    newdata[0].update({col: False})
            outDf.loc[len(outDf.index)] = list(newdata[0].values())
            schoolCoods.append(code[1])
    return outDf


def get_all_schools():
    """
    func: main function that runs on all raw files and maps all schools
    to an aggregated database
    :return: csv output of all schools file, without full mapping of all
    file-instNum combinations.
    """
    path = "C:/Users/PC/Documents/all_files/*"
    outDf = pd.DataFrame(columns=["instNum","instName","city"])
    for fname in glob.glob(path):
        #csv_from_excel(fname)
        curDf = pd.read_excel(fname)
        print(list(curDf.columns))
        if "סמל מוסד" in list(curDf.columns) and "שם מוסד" in list(
                curDf.columns):
            print("reading file: "+fname)
            #curDf = only_highschools(curDf, fname)  # used for prefixing
            # the files.
            outDf = add_new_schools(curDf,outDf, fname)
        else:  # used for prefixing the files.
            print("do not have סמל מוסד in it: "+ fname)
    outDf.to_csv("all_highschools3.csv")

#get_all_schools()

def cross_checking():
    """
    func: reruns on the output file to check all instNum apperances in all
    files.
    :return: output with full data of instNum appearances in all school files
    """
    path = "C:/Users/PC/Documents/all_files/*"
    outDf = pd.read_csv("all_highschools3.csv")
    for fname in glob.glob(path):
        colname = fname[-30:]
        if colname in outDf.columns.to_list():
            curDf = pd.read_excel(fname)
            for idx, row in outDf.iterrows():
                if row[colname] == "0" or row[colname] == "1.0" or  row[
                    colname] =="1":  # takes all placeholders
                    if row["instNum"] in curDf["שם מוסד"].to_list():
                        outDf.at[idx,colname ] = True
                    else:
                        outDf.at[idx, colname] = False
    outDf.to_csv("all_highschools_final1.csv")
#cross_checking()

def make_address():
    """
    func: for google maps search (for x-y coordinates), make address in the
    format of "school, city, Israel" in hebrew.
    :return:csv file.
    """
    out = pd.read_csv("all_highschools_final1.csv")
    out["Address"] = pd.Series([" "]*len(out))
    for idx, row in out.iterrows():
        try:
            out.at[idx, "Address"] = str(str(row["instName"])+" ,"+row["city"] +", ישראל")
        except TypeError:
            print(row["instName"])
            print(row["city"])
    out.to_csv("highschools_index.csv")
    with pd.ExcelWriter('highschools_index.xlsx') as writer:
        out.to_excel(writer, sheet_name='school index')


make_address()

