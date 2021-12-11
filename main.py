import csv
from os import name
from posixpath import abspath
import numpy as np
import pandas as pd
import math
from datetime import datetime
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import seaborn as sns
from scipy.stats import norm
#TODO: UPPGIFT 2 MAX OCH MIN VÄRDE
#TODO: LINJÄR REGRESSION MED 95% KONFIDENSINTERVALL
#TODO: TRANSFORMERAD DATA LOGARITMISK FUNKTION
#TODO: RESIDUALANALYS
#TODO: SAMMANFATTNING
#TODO: MUNTLIG PRESENTATION
#TODO: OPPONERING
def get_data():
    paths = ["data/smhi-malmo", "data/smhi-lund", "data/smhi-simrishamn"]
    for path in paths:
        header = False
        with open(path + '.csv', 'r') as file:
            with open(path+"_parsed.csv", "w") as parsedfile:
                reader = csv.reader(file, delimiter=';')
                writer = csv.writer(parsedfile, delimiter=';')
                for row in reader:
                    if len(row) > 0 and row[0] == 'Datum':
                        # print(row[0] + " & " +  row[1] + ";" + row[2] + ";" + row[3] + ";" + row[4] + ";" + row[5])
                        writer.writerow(row)
                        header = True
                    elif header:
                        if row[1] == "18:00:00" or row[1] == "06:00:00":
                            writer.writerow(row)
                        # print("arg")

def get_city(path):
    data = pd.read_csv(path, delimiter=';') 
    # data['Datum'] = pd.to_datetime(data['Datum'].astype(str) + ' ' + data['Tid (UTC)'])
    # # data['Lufttemperatur'] = pd.to_numeric(data['Lufttemperatur']).astype(float)
    # data.drop(['Tid (UTC)', 'Unnamed: 4', 'Tidsutsnitt:', 'Kvalitet'], inplace=True, axis=1)
    # data = data.set_index('Datum')
    # print(data)
    # with open(path, "r") as file:
    #         reader = csv.reader(file, delimiter=";")
    #         for row in reader:
    #             if len(row) > 0 and row[0] != 'Datum':
    #                 data.append(float(row[2]))
    #                 # print(row[2])
    data['Datum'] = pd.to_datetime(data['Datum'].astype(str) + ' ' + data['Tid (UTC)'])
    # Remove unused data columns
    data.drop(['Tid (UTC)', 'Unnamed: 4', 'Tidsutsnitt:', 'Kvalitet'], inplace=True, axis=1)
    data = data.set_index('Datum')
    # return df
    return data

def mean(data):
    res = 0
    for item in data:
        res = item + res
    res = res / len(data)
    return res

def std(data):
    res = 0
    meanres = mean(data)
    for item in data:
        res = (item-meanres)**2 + res
    res = res / (len(data)-1)
    res = math.sqrt(res)
    return round(res, 4)

def draw_plot(data):
    # print(data)
    fig = plt.figure(1)
    sns.set_theme(style='whitegrid')
    # tips = sns.load_dataset("tips")
    plt.ylabel("celcius")
    ax = sns.boxplot(x="city", y="temp", hue="time", data=data)
    plt.title('Boxplot of temperature')
    fig.savefig('plot/boxplot.png', bbox_inches='tight', dpi=150) 

    # ax = sns.lineplot(x="datetime", y="temp", hue="city", data=data)
    # ax = sns.swarmplot(x="city", y="temp", data=data, color=".25")

def create_data_frame():
    cities = ['malmo', 'lund', 'simrishamn']
    df = pd.dictionary = {
        'city': [],
        'datetime': [],
        'time': [],
        'temp': []
    }
    for city in cities:
        with open(f'data/smhi-{city}_parsed.csv', 'r') as file:
            reader = csv.reader(file, delimiter=';')
            for row in reader:
                if len(row) > 0 and row[0] != "Datum":  
                    # print(row)
                    df["city"].append(city)
                    df["datetime"].append(row[0] + " " + row[1])
                    df["time"].append(row[1])
                    df["temp"].append(float(row[2]))
    return df



def get_df():
    df_malmo = get_city("data/smhi-malmo_parsed.csv")
    df_malmo = df_malmo.rename(columns={'Lufttemperatur' : 'TempMalmo'})
    df_lund = get_city("data/smhi-lund_parsed.csv")
    df_lund = df_lund.rename(columns={'Lufttemperatur' : 'TempLund'})
    df_simrishamn = get_city("data/smhi-simrishamn_parsed.csv")
    df_simrishamn = df_simrishamn.rename(columns={'Lufttemperatur' : 'TempSimrishamn'})
    return [df_malmo, df_lund, df_simrishamn]


def print_mean_std_max_min():
    """
    Uppgift 2: Medelvärde, Standardavvikelse. 
    """
    res = get_df()
    df_malmo = res[0]
    df_lund = res[1]
    df_simrishamn = res[2]

    print("mean of datas")
    print("City        Mean Temp")
    malmo_mean =  df_malmo.mean().to_string()
    lund_mean = df_lund.mean().to_string()
    simrishamn_mean = df_simrishamn.mean().to_string()
    print(malmo_mean)
    print(lund_mean)
    print(simrishamn_mean)
    
    print("\nstandard deviation of datas")
    print("City        Standard Deviation")
    malmo_std = df_malmo.std().to_string()
    lund_std = df_lund.std().to_string()
    simrishamn_std = df_simrishamn.std().to_string()
    print(malmo_std)
    print(lund_std)
    print(simrishamn_std)

    print("\nMax-value")
    print("City        Max Temp")
    malmo_max =  df_malmo.max().to_string()
    lund_max = df_lund.max().to_string()
    simrishamn_max = df_simrishamn.max().to_string()
    print(malmo_max)
    print(lund_max)
    print(simrishamn_max)

    print("\nMin-value")
    print("City        Min Temp")
    malmo_min =  df_malmo.min().to_string()
    lund_min = df_lund.min().to_string()
    simrishamn_min = df_simrishamn.min().to_string()
    print(malmo_min)
    print(lund_min)
    print(simrishamn_min)


def correlation():
    """
    Uppgift 2: Korrelation
    """
    res = get_df()
    df_malmo = res[0]
    df_lund = res[1]
    df_simrishamn = res[2]

    df = pd.concat([df_lund, df_malmo, df_simrishamn], axis = 1)
    df = df.dropna()
    X = df.index.map(datetime.toordinal).values.reshape(-1, 1) 
    Y = df.iloc[:,1].values.reshape(-1, 1)
    linear_reg = LinearRegression()
    linear_reg.fit(X, Y)
    Y_pred = linear_reg.predict(X)
    fig = plt.figure()
    residual = df['TempMalmo'].values - Y_pred.squeeze()
    df['Residual U'] = residual
    df['Residual U'].plot()
    residual_variance = df['Residual U'].var()
   
    correlation = df[df.columns[[0,1,2]]].corr()

    sns.heatmap(correlation)
    plt.title('Correlation between sites')
    fig.savefig('plot/correlation.png') 

def normaldist():
    res = get_df()
    df_malmo = res[0]
    malmo_mean =  df_malmo.mean()
    malmo_std =  df_malmo.std()
    df_lund = res[1]
    lund_mean = df_lund.mean()
    lund_std = df_lund.std()

    df_simrishamn = res[2]
    simrishamn_mean = df_simrishamn.mean()
    simrishamn_std = df_simrishamn.std()

    fig = plt.figure('normal distribution on malmö, lund & simrishamn')
    x = np.arange(float(malmo_mean)-30, float(malmo_mean)+30, 0.001)
    plt.plot(x, norm.pdf(x, malmo_mean, malmo_std), color='blue', linewidth=4)
    # plt.figure('normal distribution on lund')
    x = np.arange(float(lund_mean)-30, float(lund_mean)+30, 0.001)
    plt.plot(x, norm.pdf(x, lund_mean, lund_std), color='orange', linewidth=3)
    # plt.figure('normal distribution on simrishamn')
    x = np.arange(float(simrishamn_mean)-30, float(simrishamn_mean)+30, 0.001)
    plt.plot(x, norm.pdf(x, simrishamn_mean, simrishamn_std), color='red', linewidth=2)
    plt.legend(["Malmö", "Lund", "Simrishamn"])
    fig.savefig('plot/normal_distribution.png', bbox_inches='tight', dpi=350)
    plt.show()

def linear_regression():
    #med 95% confidensinterval
    res = get_df()
    df_malmo = res[0]
    df_lund = res[1]
    df_simrishamn = res[2]



if __name__ == "__main__":
    get_data()
    mean_test = mean([21.3232, 38.3422, 12.7212, 41.6178])
    # print(mean_test)
    std_test = std([21.3232, 38.3422, 12.7212, 41.6178])
    # print(std_test)
    
    # print(simrishamn_data)
    # print(mean(malmo_data))
    # print(mean(lund_data))
    # print(mean(simrishamn_data))
    # data = [malmo_data, lund_data, simrishamn_data]
    # plt.boxplot([malmo_data, lund_data, simrishamn_data])
    # plt.bar(['malmo', "Lund", "Simrishamn"], [-5, 0, 5, 10])
    # plt.xlabel(['malmo', "Lund", "Simrishamn"])
    # plt.boxplot()
    # ax = sns.stripplot(x="Pclass", y="Age",data=df)
    # ax = sns.boxplot(x="day", y="total_bill", data=data)
    # ax = sns.swarmplot(x="day", y="total_bill", data=data, color=".25")
    # plt.show()


    
    dataframe = create_data_frame()
    # print(dataframe)
    print_mean_std_max_min()
    draw_plot(dataframe)
    correlation()
    # print(type(dataframe))
    # new = pd.DataFrame.from_dict(dataframe)
    # print(new)
    # correlation = dataframe[dataframe.columns[[0,1,2]]].corr()
    # sns.heatmap(correlation)
    # plt.title('Correlation between sites')
    # print(correlation)
    # plt.figure(2)

    normaldist()
    plt.show()