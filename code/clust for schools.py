import pandas as pd
import matplotlib.pyplot as plt
from bidi import algorithm as bidialg
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

def SSE_check(df):
    """
    checks on the data without responses,whats the best number of clusters (by
    sse checking and elbow finding.
    """
    kmeans_kwargs = {
         "init": "random",
         "max_iter": 300,
         "random_state": 42}
    sse = []
    for k in range(1, 25):
        kmeans = KMeans(n_clusters=k, **kmeans_kwargs)
        kmeans.fit(df)
        sse.append(kmeans.inertia_)

    plt.style.use("fivethirtyeight")
    plt.plot(range(1, 25), sse)
    plt.xticks(range(1, 25))
    plt.xlabel("Number of Clusters")
    plt.ylabel("SSE")
    plt.show()
    # A list holds the silhouette coefficients for each k
    silhouette_coefficients = []
    for k in range(2, 25):
        kmeans = KMeans(n_clusters=k, **kmeans_kwargs)
        kmeans.fit(df)
        score = silhouette_score(df, kmeans.labels_)
        silhouette_coefficients.append(score)
    plt.style.use("fivethirtyeight")
    plt.plot(range(2, 25), silhouette_coefficients)
    plt.xticks(range(2, 25))
    plt.xlabel("Number of Clusters")
    plt.ylabel("Silhouette Coefficient")
    plt.show()

def data_prep():
    """
    data preperation function, takes the wanted file for clustering and
    returns with all the needed columns, and calls the SSE function to check
     best k parameter for k-means clustering
    :return: the fixed data fill and the old one for next function
    """
    df = pd.read_excel("city_mean_zacaut_geo_with_nafa_clean.xlsx")
    out = pd.DataFrame(columns=["idxCol","תשעה",	"תשעז"	,"תשעח",	"תשעד",
    "תשעו","average",	"city",	"Nafa",	"geo_y",	"geo_x"])
    for idx, row in df.iterrows():
        out.loc[idx] = row.fillna(row["average"])
    df = pd.read_excel(r'C:\Users\PC\Documents\all_files\school - bagrut.xlsx')
    df = df[df['שנה"ל']=="תשעח"]
    df = df[df["חמשון מדד טיפוח/נוער בסיכון"]!="לא מחושב"]
    out = df.drop(columns=['שנה"ל','שם רשות.1',	'מחוז מפקח',	'סמל רשות',
                          'שם רשות',
                          'סמל מוסד','שם מוסד',	'צבע מסלול בית ספר','חמשון מדד טיפוח/נוער בסיכון',	'מגזר',	'שם רשות','סוג פיקוח'])
    SSE_check(out)
    return out, df

def k_means(df,out):
    """
    function to make the clusters with the needed 'k',and to append it as a
    column to the output dataframe
    :param df: dataframe for clustering info
    :param out: raw dataframe to append it the clustering information
    :return: "out" dataframe
    """
    kmeans_kwargs = {
        "init": "random",
        "max_iter": 300,
        "random_state": 42}
    kmeans = KMeans(n_clusters=17, **kmeans_kwargs)
    kmeans.fit(df)
    labels = kmeans.labels_
    out["clusters"] = pd.Series(labels).to_list()
    out.to_excel("zacaut clusters17new.xls")


def descriptive(filelst):
    """
    function that runs several descriptive methods: describe function on
    each column and histogarms on wanted files.
    :param filelst: list of file names
    :return: prints descriptive statistics; histograms as files
    """
    idx = 0 # index for file names
    for file in filelst:
        df = pd.read_excel(file)
        clusters = list(df["clusters"].unique()) # for checking each cluster
        for clust in clusters:
            check = df[df["clusters"]==clust] # run only on the data of the
            # cluster
            for col in check.columns: #checks each column
                print(file + " cluster:"+str(clust) + "column: "+col)
                print(check[col].describe()) # print once for each column
                # for full descriptive data
                # columns1 and columns2 are to groups of columns for
                # different hostoframe making (1 - zacaut presentage;
                # 2 - demographic info)
                columns1 =["אחוז זכאים לבגרות   ",
                           "אחוז זכאות לבגרות  מצטיינת    ",
                           'אחוז זכאות 4 יחידות אנגלית   ',
                           'אחוז זכאות 5 יחידות אנגלית   ',
                           '  אחוז זכאות 4 יחידות מתמטיקה    ',
                           'אחוז זכאות 5 יחידות מתמטיקה    ']
                columns2 = ['חמשון מדד טיפוח/נוער בסיכון','מגזר','סוג פיקוח']
                if col in columns2:
                    check[col].plot(kind='hist', title="cluster:"+str(clust)
                                                       + "column: "+bidialg.get_display(col))
                    plt.savefig(str(idx)+".png")
                    idx+=1
                    plt.close()

out, full = data_prep()
k_means(out,full)
descriptive(["zacaut clusters17.xls","zacaut clusters20.xls","zacaut "
                                                             "clusters6.xls"])
descriptive(["zacaut clusters17new.xls"])
