import pandas as pd

# this file creates a xlsx file. the final table contains the mean of each city according to given year
# and another column with the city's matching nafa.

# create data frames:

df_school_zacaut_nafa = pd.read_excel(r'C:\Users\ASUS\PycharmProjects\DataProject\code and outputs\output excels\school_zacaut_nafa3.xlsx')
df_bagrut = pd.read_excel(r'C:\Users\ASUS\PycharmProjects\DataProject\code and outputs\EduData\ShkifutSource\school_bagrut_EngTitle.xlsx')


city_dict = df_bagrut.set_index('instNum').to_dict()['city']  # dict of instNum and city

# create new df to save results:
yearsList = df_bagrut.year.unique().tolist()
allcity = df_bagrut.city.unique().tolist()
city_gap_zacautDF = pd.DataFrame(index=allcity, columns=yearsList)

# fill the city_gap_zacautDF with relevant info:
# for each year, create nafa_list according to given year, for each nafa - calc mean and put in table.
for year in yearsList:
    df_bagrut_year = df_bagrut[df_bagrut.year == year]  # create df of a single year
    city_yearList = df_bagrut.city.unique()  # list of all nafa's of a given year
    for city in city_yearList:  # for each nafa - create average and put in new df
        df_city_year = df_bagrut_year[df_bagrut_year.city == city]  # df of one nafa and one year
        city_max = df_city_year['אחוז זכאים לבגרות'].max()
        city_min = df_city_year['אחוז זכאים לבגרות'].min()
        if (city_min==city_max or city_min == 0 ):
            city_gap_zacautDF.at[city, year] = 0
        else: city_gap_zacautDF.at[city, year] = city_max - city_min

city_gap_zacautDF['city'] = city_gap_zacautDF.index

df_school_zacaut_nafa = df_school_zacaut_nafa[['שם רשות', 'Nafa']]  # get only id and nafa from main
city_nafa_dict = df_school_zacaut_nafa.set_index('שם רשות').to_dict()['Nafa']  # dict of instNum and Nafa

# add another col of nafa in city_gap_zacautDF :
city_gap_zacautDF['Nafa'] = [city_nafa_dict[x] if (x in city_nafa_dict.keys()) else 'False' for x in city_gap_zacautDF['city']]

# save result as excel file:
#city_gap_zacautDF.to_excel("city_gap_zacaut_with_nafa.xlsx") # currently disabled
