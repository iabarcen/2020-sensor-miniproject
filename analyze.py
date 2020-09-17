#!/usr/bin/env python3
"""
This example assumes the JSON data is saved one line per timestamp (message from server).

It shows how to read and process a text file line-by-line in Python, converting JSON fragments
to per-sensor dictionaries indexed by time.
These dictionaries are immediately put into Pandas DataFrames for easier processing.

Feel free to save your data in a better format--I was just showing what one might do quickly.
"""
import pandas
from pathlib import Path
import argparse
import json
from datetime import datetime
import typing as T
import matplotlib.pyplot as plt
import numpy as np

import seaborn as sns
from scipy import stats

def load_data(file: Path) -> T.Dict[str, pandas.DataFrame]:

    temperature = {}
    occupancy = {}
    co2 = {}

    with open(file, "r") as f:
        for line in f:
            r = json.loads(line)
            room = list(r.keys())[0]
            time = datetime.fromisoformat(r[room]["time"])

            temperature[time] = {room: r[room]["temperature"][0]}
            occupancy[time] = {room: r[room]["occupancy"][0]}
            co2[time] = {room: r[room]["co2"][0]}

    data = {
        "temperature": pandas.DataFrame.from_dict(temperature, "index").sort_index(),
        "occupancy": pandas.DataFrame.from_dict(occupancy, "index").sort_index(),
        "co2": pandas.DataFrame.from_dict(co2, "index").sort_index(),
    }

    return data


if __name__ == "__main__":

    p = argparse.ArgumentParser(description="load and analyse IoT JSON data")
    p.add_argument("file", help="path to JSON data file")
    P = p.parse_args()
    file = Path(P.file).expanduser()
    data = load_data(file)


    # Calculate medians and variances
    print("\n----------Calculate medians and variances----------\n")

    class1temp = data["temperature"].class1
    class1occu = data["occupancy"].class1
    class1co2 = data["co2"].class1

    timediff = np.diff(data["co2"].index.values).astype(np.int64) / 1000000000 # time diff in sec

    # print(timediff)

    print("Median temperature in class 1: ", end='')
    print('%5.2f' % (class1temp.median()))
    print("Variance in temperature in class 1: ", end='')
    print('%5.2f' % (class1temp.var()))
    print()
    print("Median occupancy in class 1: ", end='')
    print('%5.2f' % (class1occu.median()))
    print("Variance in occupancy in class 1: ", end='')
    print('%5.2f' % (class1occu.var()))
    print()
    print("Median of time intervals: ", end='')
    print('%9.4f' % (np.median(timediff)))
    print("Variance in time intervals: ", end='')
    print('%9.4f' % (np.var(timediff)))

    # Plot PDF for sensor data in Class 1
    class1 = plt.figure("Class 1")
    class1.suptitle('Sensor Data in Class 1\n', fontsize=16)

    ax1 = class1.add_subplot(131)
    ax1.title.set_text('Class 1 Temperature PDF')
    sns.distplot(class1temp, kde=False, fit=stats.gamma, rug=True)

    ax2 = class1.add_subplot(132)
    ax2.title.set_text('Class 1 Occupancy PDF')
    sns.distplot(class1occu, kde=False, fit=stats.gamma, rug=True)

    ax3 = class1.add_subplot(133)
    ax3.title.set_text('Class 1 CO2 PDF')
    sns.distplot(class1co2, kde=False, fit=stats.gamma, rug=True)


    # Plot PDF for time intervals of sensor readings
    timeFig = plt.figure("Time Intervals")
    sns.distplot(timediff, kde=False, fit=stats.gamma, rug=True)
    


    plt.show()

    # for k in data:  # k = temperature, occupancy, and co2
    #     # data[k].plot()
    #     time = data[k].index
    #     data[k].hist()
    #     plt.figure()
        # plt.hist(np.diff(time.values).astype(np.int64) // 1000000000)
        # plt.xlabel("Time (seconds)")

    # plt.show()

    
        #time = data["co2"].index

    # # Load data from client_data.txt
    # file_path = os.getcwd() + "\client_data.txt"
    # data = load_data(file_path)

    # # Room Class1
    # time = data["temperature"].index
    # class1temp = data["temperature"].class1
    # class1occu = data["occupancy"].class1

    # for t in time:
    #     timestr = ('%02d' % t.hour) + ":" + ('%02d' % t.minute)
    #     class1temp = class1temp.rename(index = {t:timestr})
    #     class1occu = class1occu.rename(index = {t:timestr})

    # print(class1temp)

    # plot1 = plt.figure("Class 1 Temperature")
    # class1temp.hist(color='#90EE90')
    # plt.xlabel('temperature') 
    # plt.ylabel('times') 
    # plt.title('Temperature Condition for Class 1\n\n', fontweight ="bold") 

    # plot2 = plt.figure("Class 1 Occupancy")
    # class1occu.hist(color='#A1C7CB')
    # plt.xlabel('occupancy') 
    # plt.ylabel('times') 
    # plt.title('Occupancy Condition for Class 1\n\n', fontweight ="bold") 

    # plt.show()

    #plot1 = plt.figure("Class 1 Temperature")
    #data["temperature"].class1.hist(color='#90EE90')
    
    #print(time.values[1].astype(datetime.datetime))

    # timestr = ('%02d' % time[0].hour) + ":" + ('%02d' % time[0].minute) + ":" + ('%02d' % time[0].second)
    # print(timestr)
    # print ('%02d' % time[0].hour + ":")

    # class1temp = data["temperature"].class1
    # #print(class1temp)
    # #print("--------------------------------")
    # for t in time:
    #     timestr = ('%02d' % t.hour) + ":" + ('%02d' % t.minute) + ":" + ('%02d' % t.second)
    #     # print (timestr)
    #     class1temp = class1temp.rename(index = {t:timestr})
    # #print(class1temp)

    # plot1 = plt.figure("Class 1 Temperature")
    # class1temp.hist(color='#90EE90')
    # plt.xlabel('time') 
    # plt.ylabel('temperature') 
    # plt.title('Temperature Condition for Class1\n\n', fontweight ="bold") 


    # plot2 = plt.figure("Class 1 Occupancy")
    # time = data["occupancy"].index
    # data["occupancy"].class1.hist(color='#90EE90')

    # plt.xlabel('time') 
    # plt.ylabel('occupancy') 
  
    # plt.title('Occupancy Condition for Class1\n\n', fontweight ="bold") 

    # plt.show()

    # Calculate medians and variances
    # print("\n----------Calculate medians and variances----------\n")

    # print("Median temperature in class 1: ", end='')
    # print('%5.2f' % (data["temperature"].class1.median()))
    # print("Variance in temperature in class 1: ", end='')
    # print('%5.2f' % (data["temperature"].class1.var()))
    # print()
    # print("Median occupancy in class 1: ", end='')
    # print('%5.2f' % (data["occupancy"].class1.median()))
    # print("Variance in occupancy in class 1: ", end='')
    # print('%5.2f' % (data["occupancy"].class1.var()))

    
