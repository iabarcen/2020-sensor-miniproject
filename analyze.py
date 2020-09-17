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

    print("Median temperature in class 1: ", end='')
    print('%5.4f' % (class1temp.median()))
    print("Variance in temperature in class 1: ", end='')
    print('%5.4f' % (class1temp.var()))
    print()
    print("Median occupancy in class 1: ", end='')
    print('%5.4f' % (class1occu.median()))
    print("Variance in occupancy in class 1: ", end='')
    print('%5.4f' % (class1occu.var()))
    print()

    print("Median of time intervals: ", end='')
    print('%5.4f' % (np.median(timediff)))
    print("Variance in time intervals: ", end='')
    print('%5.4f' % (np.var(timediff)))
    print()


    # Plot PDF for sensor data in Class 1
    class1 = plt.figure("Class 1 Sensor Data", figsize=(18, 6))
    class1.suptitle('Sensor Data in Class 1\n', fontsize=16)

    ax1 = class1.add_subplot(131)
    ax1.title.set_text('Class 1 Temperature PDF')
    ax1.set_ylabel('Probability Density')
    sns.distplot(class1temp, kde=False, fit=stats.gamma, rug=True)

    ax2 = class1.add_subplot(132)
    ax2.title.set_text('Class 1 Occupancy PDF')
    ax2.set_ylabel('Probability Density')
    sns.distplot(class1occu, kde=False, fit=stats.gamma, rug=True)

    ax3 = class1.add_subplot(133)
    ax3.title.set_text('Class 1 CO2 PDF')
    ax3.set_ylabel('Probability Density')
    sns.distplot(class1co2, kde=False, fit=stats.gamma, rug=True)

    ax1.set_xlabel('temperature(Celcius)')
    ax2.set_xlabel('occupancy')
    ax3.set_xlabel('CO2')


    # Plot PDF for time intervals of sensor readings
    timeFig = plt.figure("Time Intervals", figsize=(8, 6))
    sns.distplot(timediff, kde=False, fit=stats.gamma, rug=True)
    timeFig.suptitle('PDF for Time Intervals', fontsize=16)
    plt.xlabel('time(sec)')
    plt.ylabel('Probablity Density')
    

    plt.show()

    
