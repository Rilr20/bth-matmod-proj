import csv
from os import name
from posixpath import abspath
import pandas as pd
import math
from datetime import datetime
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import seaborn as sns

def get_data():
    paths = ["data/smhi-karlskrona", "data/smhi-lund", "data/smhi-simrishamn"]
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
    sns.set_theme(style='whitegrid')
    # tips = sns.load_dataset("tips")
    ax = sns.boxplot(x="city", y="temp", hue="time", data=data)
    # ax = sns.lineplot(x="datetime", y="temp", hue="city", data=data)
    # ax = sns.swarmplot(x="city", y="temp", data=data, color=".25")
    plt.show()

def create_data_frame():
    cities = ['karlskrona', 'lund', 'simrishamn']
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

if __name__ == "__main__":
    get_data()
    mean_test = mean([21.3232, 38.3422, 12.7212, 41.6178])
    # print(mean_test)
    std_test = std([21.3232, 38.3422, 12.7212, 41.6178])
    # print(std_test)
    karlskrona_data = get_city("data/smhi-karlskrona_parsed.csv")
    lund_data = get_city("data/smhi-lund_parsed.csv")
    simrishamn_data = get_city("data/smhi-simrishamn_parsed.csv")
    # print(simrishamn_data)
    # print(mean(karlskrona_data))
    # print(mean(lund_data))
    # print(mean(simrishamn_data))
    data = [karlskrona_data, lund_data, simrishamn_data]
    # plt.boxplot([karlskrona_data, lund_data, simrishamn_data])
    # plt.bar(['Karlskrona', "Lund", "Simrishamn"], [-5, 0, 5, 10])
    # plt.xlabel(['Karlskrona', "Lund", "Simrishamn"])
    # plt.boxplot()
    # ax = sns.stripplot(x="Pclass", y="Age",data=df)
    # ax = sns.boxplot(x="day", y="total_bill", data=data)
    # ax = sns.swarmplot(x="day", y="total_bill", data=data, color=".25")
    # plt.show()
    print()
    dataframe = create_data_frame()

    draw_plot(dataframe)
