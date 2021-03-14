import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def load(file, small=False):
    c = 1
    dates = []
    d = {
        "year": [],
        "month": [],
        "day": [],
        "value": []
    }
    global unit
    unit = ""

    for L in file.readlines():
        global prev
        prev = 0
        if L[:13] == "# value:units":
            unit = L.split(" ")[-1].replace("\n", "")

        if L[:4] == "TER ":
            line = L.split()
            if float(line[13]) > -50:
                d["year"].append(line[1])
                d["month"].append(line[2])
                d["day"].append(line[3])
                d["value"].append(float(line[13]))
                dates.append(line[2] + "-" + line[3] + "-" + line[1])
                prev = pd.to_datetime(dates[-1])

        c += 1

    return [[pd.to_datetime(date) for date in dates], d["value"], unit, 1 if small else 0, file.name]


gases = os.popen("ls datasets/TER/").read().split("\n")
gases.pop()  # remove empty string
FILES = {}
for gas in gases:
    gas_files = []
    os.chdir("datasets/TER/" + gas + "/txt")

    gas2 = os.popen("ls -d */").read().split("\n")
    gas2.pop()
    _gas2 = gas2[0].replace("/", "")
    os.chdir(os.getcwd() + "/" + _gas2)

    subdir = os.popen("ls -d */").read().split("\n")
    subdir.pop()

    for d in subdir:
        os.chdir(d)
        base = os.getcwd()
        data_files = os.popen("ls").read().split("\n")
        data_files.pop()
        for i in data_files:
            gas_files.append(base + "/" + i)

        os.chdir("..")

    FILES[gas] = gas_files
    os.chdir("../../../../..")


def refine(x, y, avg, std):
    refined = [[], []]
    c = 0
    for val in y:
        break  # disabled
        z = (val-avg)/std
        threshold = 0
        if std > 1.5:
            threshold = 0.3

        else:
            threshold = 2

        if abs(z) < threshold:
            refined[1].append(val)
            refined[0].append(x[c])

        c += 1

    return [x, y]


def parabola(x, a, b, c):
    return a*x**2 + b*x + c


for gas in gases:
    data = []
    files = []
    for filename in FILES[gas]:
        files.append(open(filename, "r"))
        if "hourly" in filename:
            data.append(load(files[-1], small=True))

        elif "event" in filename:
            pass

        else:
            data.append(load(files[-1]))

    plt.figure(figsize=(10, 5))
    plt.ylabel(gas + " concentration / " + data[0][2])  # set y-axis label to "<gasName> concentration / <unit>"
    plt.xlabel("Time / years")
    plt.title("Source: WDCGG (World Data Center for Greenhouse Gases) - https://gaw.kishou.go.jp")
    avg = 0
    std = 0
    TIME = []
    DATA = []

    count = 0
    for p in data:
        avg += np.average(p[1])
        std += np.std(p[1])
        for t in p[0]:
            TIME.append(t)

        for d in p[1]:
            DATA.append(d)
            #
        # fake_values = [i for i in range(len(p[0]))]
        # opt, opt_ = scipy.optimize.curve_fit(parabola, fake_values, p[1])
        # a, b, c = opt
        # plt.plot(p[0], parabola(np.array(fake_values), a, b, c), "red", linewidth=1.2, zorder=5)
        count += 1

    avg = avg / len(data)
    std = std / len(data)

    for p in data:
        x, y = refine(p[0], p[1], avg, std)
        if p[3]:
            size = 0.0001

        else:
            if len(p[0]) < 10000:
                size = 0.1

            else:
                size = 0.5

        plt.scatter(x, y, s=size, color="blue", marker="x")
        plt.plot(x, y, "blue")

    plt.ylim(min(DATA) - std / 3, max(DATA) + std / 3)
    plt.xlim(min(TIME), max(TIME))
    plt.savefig("arcticwatch/static/graphs/TER/large/{0}.png".format(gas))
    # plt.show()
    for f in files:
        f.close()
