#!/usr/bin/env python3

import pandas
from pathlib import Path
import argparse
import json
from datetime import datetime
import typing as T
import matplotlib.pyplot as plt
import numpy as np

def load_data(file: Path) -> T.Dict[str, pandas.DataFrame]:

    temperature = {}

    with open(file, "r") as f:
        for line in f:
            r = json.loads(line)
            room = list(r.keys())[0]
            time = datetime.fromisoformat(r[room]["time"])

            temperature[time] = {room: r[room]["temperature"][0]}

    data = pandas.DataFrame.from_dict(temperature, "index").sort_index()
    return data

def detect_anomalies(data):
    classdf = data["class1"]
    class_mean = classdf.mean()
    class_median = classdf.median()
    class_var = classdf.var() 
    class_std_dev= classdf.std()
    upper_limit = class_mean + class_std_dev
    lower_limit = class_mean - class_std_dev
    class_size=len(classdf)

    ibad = (classdf<lower_limit)|(classdf>upper_limit)
    classdf = classdf.loc[~ibad]
    new_median=classdf.median()
    new_var=classdf.var()
    anomalies=sum(ibad)

    print("The percent of \"bad\" data points for class 1 is"+str((anomalies/class_size)*100)+"%\n")
    print("The temperature median and variance with these anomalies removed are,")
    print("Median:"+str(new_median)+"\nVariance:"+str(new_var))
    print("In comparison the median and variance with these anomallies are,")
    print("Median:"+str(class_median)+"\nVariance:"+str(class_var))

if __name__ == "__main__":
    p = argparse.ArgumentParser(description="load and analyse IoT JSON data")
    p.add_argument("file", help="path to JSON data file")
    P = p.parse_args()

    file = Path(P.file).expanduser()

    data = load_data(file)
    detect_anomalies(data)
