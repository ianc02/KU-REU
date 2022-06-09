import math

#import numpy as np
import time


def main():
    t1 = time.time()
    r1 = ''
    r2 = ''
    steps = 0
    atoms = 0
    l1 = 0
    l2 = 0
    l3 = 0
    bins = 0

    print("Hello, Ian!")

    f = open("gen_input", 'r')
    file_list = f.readlines()
    for i in range(len(file_list)):

        if i == 0:
            r1 = file_list[i].split()[-1]
        if i == 1:
            r2 = file_list[i].split()[-1]
        if i == 2:
            steps = int(file_list[i].split()[-1])
        if i == 3:
            atoms = int(file_list[i].split()[-1])
        if i == 4:
            l1 = float(file_list[i].split()[-1])
        if i == 5:
            l2 = float(file_list[i].split()[-1])
        if i == 6:
            l3 = float(file_list[i].split()[-1])
        if i == 7:
            bins = int(file_list[i].split()[-1])

    f2 = open("traj.xyz", 'r')
    f2_list = f2.readlines()

    d = {}
    c = 0
    for i in f2_list:
        i = i.split()
        if len(i) == 3:
            c = int(i[-1]) - 1000000
            if c > 1000:
                break
            d[c] = []

        elif len(i) == 4:
            d[c].append(i)

    vol = l1 * l2 * l3
    dr = l1 / (2 * bins)
    vn = vol / (atoms ** 2)
    rmax = l1 / 2.0

    hist = []
    g = []
    for i in range(bins):
        hist.append(0)
        g.append(0)

    total = 0
    na2 = 0
    na1 = 0
    print("START")
    q = 0
    s = 0
    for a in range(0, 1050, 50):

        step = d[a]

        for i in range(atoms - 1):
            if step[i][0] == r1:
                na1 += 1
                for j in range(i + 1, atoms):
                    if step[j][0] == r2:
                        # if molecule1 != molecule2
                        na2 += 1

                        r1x = float(step[i][1])
                        r1y = float(step[i][2])
                        r1z = float(step[i][3])
                        r2x = float(step[j][1])
                        r2y = float(step[j][2])
                        r2z = float(step[j][3])

                        r1x = r1x - l1 * round((r1x - r2x) / l1)
                        r1y = r1y - l2 * round((r1y - r2y) / l2)
                        r1z = r1z - l3 * round((r1z - r2z) / l3)


                        r = math.sqrt(((r1x - r2x) ** 2) + ((r1y - r2y) ** 2) + ((r1z - r2z) ** 2))
                        # r = math.sqrt((((float(step[j][1]) - float(step[i][1])) ** 2) + ((float(step[j][2]) -
                        # float(step[i][2])) ** 2) + ( (float(step[j][3]) - float(step[i][3])) ** 2)))

                        if r <= rmax:
                            binn = (int)(r // dr)

                            hist[binn] += 1
                            total += binn

    total = total / atoms
    print(total * vn)
    rho = na1 / vol
    for i in range(bins):
        rlow = (i - 1) * dr
        rhigh = rlow + dr
        vvol = (4.0 / 3.0) * math.pi * (rhigh ** 3 - rlow ** 3)
        g[i] = hist[i] / (vvol * steps * na2 * rho)

    print(g)
    o = 0.0
    for i in g:
        o += i
    print(o)

    print(o * total * vn)

    print("***")
    for i in range(bins):
        print("*" * int(1 + hist[i] / 10))
    print(hist[100])
    print(hist[200])
    print(hist[300])
    print(hist[-1])
    t2 = time.time()

    print(t2 - t1)


main()