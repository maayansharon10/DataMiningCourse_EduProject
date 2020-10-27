import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math


def per_student(raw):
    """
    func: takes a data frame that contains information on badget and number
    of students and returns an dataframe with aggregated values of badget
    per student
    :param raw: dataframe
    :return: output dataframe.
    """
    output = pd.DataFrame(columns=["school", "city","average badget", "per "
                                                    "student"])
    schools = list(set(raw["סמל מוסד"].to_list()))
    schools = schools[1:]
    schools = [int(i) for i in schools]
    for idx, school in enumerate(schools):
        badget = raw.groupby("סמל מוסד")["תקציב שכר ותשלומים"].sum()[school]
        ave = raw.groupby("סמל מוסד")["תקציב שכר ותשלומים"].mean()[school]
        studets = raw.groupby("סמל מוסד")["מספר תלמידים בפועל חינוך מיוחד"].sum()[
            school] + raw.groupby("סמל מוסד")["מספר תלמידים בפועל חינוך רגיל"].sum()[
            school]
        output.at[idx, "school"] = school
        output.at[idx, "city"] = raw[raw["סמל מוסד"]==school]["שם " \
                                                              "רשות"].to_list()[0]
        output.at[idx, "per student"] = badget/studets
        output.at[idx,"average badget"] = ave
    return output


def per_student_for_map(raw):
    """
    func: takes a data frame that contains information on badget and number
    of students and returns an dataframe with aggregated values of badget
    per student and other features for the map.
    :param raw: dataframe
    :return: output dataframe.
    """
    geo = pd.read_excel("maayan_2020.xlsx")
    output = pd.DataFrame(columns=["school", "school code", "city",
                                   "sector", "kind", "edu_hours",
                                   "edu_hours_cost","edu_hours_personal",
                                   "badget", "per student", "geo_x","geo_y"])
    raw = raw[raw["שלבי חינוך במוסד"].isin(["יסודי ועליונה","עליונה בלבד",
                                          'חט"ב ועליונה','יסודי חט"ב '
                                                         'ועליונה'])]
    raw = raw[raw["שנת לימודים"]=="תשעח"]
    raw = raw[raw["סוג חינוך מוסד"]=="רגיל"]
    for idx, row in raw.iterrows():
        school_code = row["סמל מוסד"]
        school = row["שם מוסד"]
        city = row["שם רשות"]
        sector = row["מגזר"]
        kind = row["סוג פיקוח"]
        edu_hours = row[" שעות הוראה"]
        edu_hours_cost = row["עלות  שעות הוראה"]
        edu_hours_personal = row["שעות פרטניות"]
        badget = row["תקציב שכר ותשלומים"]
        students = row["מספר תלמידים בפועל חינוך מיוחד"]+\
                  row["מספר תלמידים בפועל חינוך רגיל"]
        try:
            per_student = badget / students
        except:
            print([school_code, badget, students])
        try:
            geo_x = geo[geo["id"]==school_code]["geo_x"].tolist()[0]
        except:
            print(school_code)
        try:
            geo_y = geo[geo["id"]==school_code]["geo_y"].tolist()[0]
        except:
            print(school_code)
        output.loc[idx] = [school, school_code, city,sector, kind, edu_hours,
                                   edu_hours_cost,edu_hours_personal,
                                   badget, per_student, geo_x,geo_y]
    return output

def plot_per_student(sorted_schools):
    """
    function
    :param sorted_schools:
    :return:
    """
    fig = plt.figure()
    ax1 = fig.add_subplot(111)
    ax1.scatter(sorted_schools["school"], sorted_schools["per student"], s=10,
                c='r',
                marker="s", label="badget per student")
    ax1.scatter(sorted_schools["school"], sorted_schools["average badget"],
                s=10,
                c='b', marker="s", label="average badget")
    ax1.set_yscale('symlog')
    sorted_schools.plot.scatter("school", "per student")
    plt.show()


def ishighschool(check):
    """
    checks if the schools in the dataframe are all highschools
    :param check: dataframe of schools with "סמל מוסד" column
    :return: the dataframe with only highschools in it
    """
    hsDf = pd.read_csv("all_highschools_final1.csv")
    highschools = hsDf["instNum"].to_list()
    check_schools = check["סמל מוסד"].to_list()
    droplst = list(set(check_schools) - set(highschools))
    for num in droplst:
        check.drop(check[check["סמל מוסד"]==num].index, inplace=True)
    return check


def equality_in_city(df):
    """
    func: checks the variance of badget per student in
    :param df:
    :return:
    """
    cities = list(df["city"].unique())
    cities = [i for i in cities if not pd.isna(i)]
    city_var = pd.DataFrame(columns=["city","var"])
    print(cities)
    for idx, city in enumerate(cities):
        var = df.groupby("city")["per student"].var()[city]
        norm = df.groupby("city")["per student"].sum()[city]
        city_var.loc[idx] = [city, math.sqrt(var/norm)]
    return city_var


### --------- function running:  ----------------###
# these functions ar all used for checking and adjusting the data for the
# later function. it was built with stopping points to save the data-frames
# as file, because it's an product as is.
# Also, some of the code re-arrainging and visualization where made
# by-hand on the files.

df = pd.read_excel("school - money.xlsx")
df = ishighschool(df)
schools = per_student(df)
schools.to_csv("school_bad_p_stud_with_badget.csv")
schools = pd.read_csv("school_bad_p_stud.csv")
cities = equality_in_city(schools)
cities.to_csv("cities_equality.csv")
# the file was sorted by hand in excel for comfortability.
sorted_cities = pd.read_csv("cities_equality_sorted.csv")
sorted_schools = pd.read_csv("school_bad_p_stud_with_badget.csv")
sorted_cities.plot.scatter("city","normalized SD", title="Normalized SD of "
                                                          "Badget per student by cities")

out = per_student_for_map(pd.read_excel("school - money.xlsx"))
out.to_excel("per_stud_data_for_map_1.xls")