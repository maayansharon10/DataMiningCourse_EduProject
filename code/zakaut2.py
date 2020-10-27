# =================================important!=================================
# this file was originally few scripts which we ran individually.
# this file is for documentation purposes only.

import pandas as pd

# ====================================================================================
# ------------------------------ zakaut - per nafa -----------------------------------
# ====================================================================================

# this part creates a xlsx file. the final table contains the mean of each nafa according to given year.

# create data frames:
df_main = pd.read_excel(r'C:\Users\ASUS\PycharmProjects\DataProject\files\schools_utm_only_hs.xlsx')
df_bagrut = pd.read_excel(r'C:\Users\ASUS\PycharmProjects\DataProject\files\Makor-Shkifut\school - bagrut.xlsx')

df_main = df_main[['id', 'Nafa']]  # get only id and nafa from main
id_dict = df_main.set_index('id').to_dict()['Nafa']  # dict of instNum and Nafa

# add another col of nafa in df_bagrut :
df_bagrut['Nafa'] = [id_dict[x] if (x in id_dict) else 'False' for x in df_bagrut['instNum']]
df_bagrut = df_bagrut[df_bagrut.Nafa != 'False']  # remove invalid rows
# now bagrut is with nafa, and invalid were removed!

# create new df to save results:
yearsList = df_bagrut.year.unique().tolist()
allNafa = df_bagrut.Nafa.unique().tolist()
nafa_mean_DF = pd.DataFrame(index=allNafa, columns=yearsList)

# fill the nafa_mean_DF with relevant info:
# for each year, create nafa_list according to given year, for each nafa - calc mean and put in table.
for year in yearsList:
    df_bagrut_year = df_bagrut[df_bagrut.year == year]  # create df of a single year
    nafa_yearList = df_bagrut.Nafa.unique()  # list of all nafa's of a given year
    for nafa in nafa_yearList:  # for each nafa - create average and put in new df
        df_nafa_year = df_bagrut_year[df_bagrut_year.Nafa == nafa]  # df of one nafa and one year
        nafa_mean = df_nafa_year['אחוז זכאים לבגרות'].mean()  # get nafa-city mean
        nafa_mean_DF.at[nafa, year] = nafa_mean

# add another col of nafa in school bagrut :
print("outdf \n", nafa_mean_DF)

nafa_mean_DF.to_excel("zacaut_per_nafa_mean.xlsx")  # save

# ====================================================================================
# ------------------------zacaut per city- mean with nafa ----------------------------
# ====================================================================================

# this part creates a xlsx file. the final table contains the mean of each city according to given year
# and another column with the city's matching nafa.

# create data frames:
df_school_zacaut_nafa = pd.read_excel(r'C:\Users\ASUS\PycharmProjects\DataProject\school_zacaut_basic.xlsx')
df_bagrut = pd.read_excel(r'C:\Users\ASUS\PycharmProjects\DataProject\files\Makor-Shkifut\school - bagrut.xlsx')

city_dict = df_bagrut.set_index('instNum').to_dict()['city']  # dict of instNum and city

# create new df to save results:
yearsList = df_bagrut.year.unique().tolist()
allcity = df_bagrut.city.unique().tolist()
city_mean_DF = pd.DataFrame(index=allcity, columns=yearsList)

# fill the city_mean_DF with relevant info:
# for each year, create nafa_list according to given year, for each nafa - calc mean and put in table.
for year in yearsList:
    df_bagrut_year = df_bagrut[df_bagrut.year == year]  # create df of a single year
    city_yearList = df_bagrut.city.unique()  # list of all nafa's of a given year
    for city in city_yearList:  # for each nafa - create average and put in new df
        df_city_year = df_bagrut_year[df_bagrut_year.city == city]  # df of one nafa and one year
        city_mean = df_city_year['אחוז זכאים לבגרות'].mean()  # get nafa-city mean
        city_mean_DF.at[city, year] = city_mean

city_mean_DF['city'] = city_mean_DF.index

df_school_zacaut_nafa = df_school_zacaut_nafa[['שם רשות', 'Nafa']]  # get only id and nafa from main
city_nafa_dict = df_school_zacaut_nafa.set_index('שם רשות').to_dict()['Nafa']  # dict of instNum and Nafa

# add another col of nafa in city_mean_DF :
city_mean_DF['Nafa'] = [city_nafa_dict[x] if (x in city_nafa_dict.keys()) else 'False' for x in city_mean_DF['city']]

# save result as excel file:
city_mean_DF.to_excel("city_mean_zacaut_with_nafa.xlsx")


# ====================================================================================
# ----------------zacaut per city - geo and  nafa ----------------
# ====================================================================================


# create data frames:
df_city_geo = pd.read_excel(r'C:\Users\ASUS\PycharmProjects\DataProject\schools_data_only_hs.xlsx')
df_mean = pd.read_excel(r'C:\Users\ASUS\PycharmProjects\DataProject\city_mean_zacaut_with_nafa.xlsx')
df_mean = df_mean.set_index('idxCol')
print(df_mean.head())

cityList = df_city_geo.city.unique().tolist()

def calcMeanCity(city):
    global df_one_city, city_mean_y, city_mean_x
    df_one_city = df_city_geo[df_city_geo.city == city]  # df of one nafa and one year
    city_mean_y = df_one_city['geo_y'].mean()  # get nafa-city mean
    df_mean.at[city, 'geo_y'] = city_mean_y
    city_mean_x = df_one_city['geo_x'].mean()
    df_mean.at[city, 'geo_x'] = city_mean_x


for city in cityList:
    calcMeanCity(city)

# fix 2 known problems with city names:
city = 'מודיעין-מכבים-רעות'
calcMeanCity(city)
city = 'תל-אביב-יפו'
calcMeanCity(city)

# save result as excel file:
df_mean.to_excel("city_mean_zacaut_geo_with_nafa.xlsx")


# ====================================================================================
# ----------------zacaut per school - all raw data with geo and  nafa ----------------
# ====================================================================================


df_main = pd.read_excel(r'C:\Users\ASUS\PycharmProjects\DataProject\school_zacaut_basic.xlsx')
df_geo = pd.read_excel(r'C:\Users\ASUS\PycharmProjects\DataProject\upload_to_maps\schools_data_only_hs.xlsx')

df_main = df_main[df_main.year == "תשעח"]  # df of one year

df_res = pd.merge(df_main, df_geo, on='instNum',how='right')
print(df_res.head())
df_res.to_excel("zacaut_tsah_full.xlsx")




