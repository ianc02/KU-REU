import math

from scipy import integrate
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

    f = open("gen_input_tmao", 'r')
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

    f2 = open("tmao_traj.xyz", 'r')
    f2_list = f2.readlines()

    d = {}
    c =0
    g = int(f2_list[1].split()[-1])
    print(len(f2_list))
    a = 0
    for i in f2_list:
        i = i.split()
        if a %1000000 == 0:
            t2 = time.time()
            print(f"{(a/104501045)*100} percent done at {t2 -t1} seconds")
        if len(i) == 3:
            c = int(i[-1]) - g
            if c > 1000:
                break
            d[c] = []

        elif len(i) == 4:
            d[c].append(i)
        a +=1

    atom_to_mol = {}
    atom_to_type = {}
    f3 = open("data_input_tmao", 'r')
    f3_list = f3.readlines()
    last_mol_number = 0
    for i in f3_list:
        i = i.split()
        atom_to_mol[int(i[0])-1] = int(i[1])
        atom_to_type[int(i[0])-1] = int(i[2])
        if int(i[1]) > last_mol_number:
            last_mol_number = int(i[1])
    print(last_mol_number)
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

    # print("START")
    na2 = 0
    na1 = 0
    osmolyte_atoms = {}
    for a in range(0, 1050, 50): #maybe an issue where steps == 1000 in input file but only iterate 20 times?

        step = d[a]
        for i in range(atoms - 1):
            if step[i][0] == r1:
                if a < 1:
                    na1 += 1
                osmolyte_atoms = {}
                for j in range(i + 1, atoms):
                    if atom_to_mol[j] == last_mol_number:
                        osmolyte_atoms[j] = step[j][0]
                        if a < 1 and i < 1 and step[j][0] == r2:
                            na2 += 1
                        if j == atoms-1:


                            # if molecule1 != molecule
                            # Not necessary rn because one molecule only has one O
                            com(step, osmolyte_atoms)
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

                                hist[binn] += 2
                                total += binn
    na2 += 1
    total = total / atoms
    # print(total * vn)
    rho = na1 / vol
    for i in range(bins):
        rlow = (i - 1) * dr
        rhigh = rlow + dr
        vvol = (4.0 / 3.0) * math.pi * (rhigh ** 3 - rlow ** 3)
        g[i] = hist[i] / (vvol * steps * na2 * rho)
        #gij = 4 * math.pi * INTEGRATE((g[i] -1) * i**2 dr)
    # print(vvol)
    # print(steps)
    # print(na2)
    # print(rho)
    #
    # print("g",g)
    o = 0.0
    for i in g:
        o += i
    # print(o)
    #
    # print(o * total * vn)
    #
    # print("***")
    f = open("py_OO_tmao.dat", "w")
    for i in range(bins):

        #print("*" * int(round(g[i]*10)))
        f.write("%s     %s \n" % (i * dr, g[i]))
    f.close()
    print(osmolyte_atoms)
    print(na2)

def com(step, osmolyte_atoms):
    xyz = {}
    h = 1.008
    o = 15.999
    n = 14.002
    c = 12.008
    for i in osmolyte_atoms.keys():
        xyz[i] = [float(step[i][1]), float(step[i][2]), float(step[i][3])]

    


main()
