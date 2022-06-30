import numpy as np
from scipy.integrate import quad
from scipy.integrate import simps
from math import *
from scipy.constants import k
from scipy.constants import N_A as avn
from os import remove 
def integrand(x, gr):
	return (gr-1) * x**2
       


def free_energy(gr, r):
     t = 298.15
     kb = k
     gr = log(gr) if gr!=0 else -np.inf
     r = log(r) if r!=0 else -np.inf
     pmf = -kb * t * gr
     evf = 2 * kb * t * r
     a =  pmf - evf
     a = (a/4184) * avn # To convert from Joule to Kcal/mol
     return a

def main():

     # RDF Files
     #outfile = "OO_water.out"
     outfile = 'comcomOwCu.out'
     #outfile = 'OwHt.out'
     #outfile = 'comcomOwNt.out'
     

     # Energy Files
     #efile = "dOwNt.out"
     efile = "dOwCu.out"


     # Box Dimensions
     #l = 21.7562   #Water
     #l = 21.6822   #TMAO
     l = 21.8124   #Urea

     # Set up for coordination number integration
     x,y = np.genfromtxt(outfile ,unpack=True,usecols=(0,1))
     length = int(len(x))
     new = x*x*y
     for i in range(length):
          output = open("correct.out","a")
          output.write(f"{x[i]} {y[i]} {new[i]}\n")
          output.close()
     data = np.genfromtxt("correct.out")
     
 
     rho = 343 / (l**3)
 
     # setting up r and gr lists
     gfile = open(outfile,'r')
     glines = gfile.readlines()
     r = []
     gr = []
     rm = 0
     for i in glines:
          r.append(float(i.split()[0]))
          gr.append(float(i.split()[1]))
     keepgoing = False
     spot = 0



     # Getting  U(r)
     energy = open(efile, 'r')
     elines = energy.readlines()
     etotal = []
     Ur = []
     for i in range(len(elines)):
          ghr = float(elines[i].split()[1]) + 0.0037
          #ghr = (ghr * 4184) / avn    # Have to convert from Kcal/mol to Joules
          etotal.append(ghr)
          Ur.append(ghr/gr[i]) if gr[i]!=0 else Ur.append(inf)
          
     print(etotal)
     #print(gr)
     #print(Ur)




     # Find Minimum in RDF graph
     for i in range(len(gr)):
          if i > 7 and i != len(gr)-7:
               if gr[i-7] > gr[i] < gr[i+7]:
                    for j in range(10):
                         if gr[i+j] < gr[i]:
                              keepgoing = True
                    if not keepgoing:
                         rm = r[i]
                         spot = i
                         break
                    else:
                         keepgoing = False
     gij = []
     gijnorm = ((1*(10**24))/(6.022*(10**23)))



     # Integration for Kirkwood-Buff Integral
     for i in range(len(r)):
          # Integration for KBI
          f = lambda x: ((gr[i]-1)*(r[i]**2))
          kbi =-4.0 * gijnorm * pi * quad(f, 0, np.inf)[0]
          gij.append(kbi)
          n = lambda x: ((gr[i] * (r[i]**2)))
         
          # Old Integration for Coord Number
          q = quad(n,0,rm)[0]
          nrr = 4.0 * pi * rho  * q



     # Current Integration for Coord Number
     coord =  simps(data[0:spot,2], data[0:spot:,0])
     print(f'Integrate is {coord}')
     coord = 4 * np.pi * rho * coord
     print(f'Coordination Number is {coord}')
     print(f'Min r value is {rm}')
     print(f'Min g(r) value is {gr[spot]}')
     print(f'Occurs at line {spot}')


     
     # Calculating T dS(r)
     tdSr = []
     dAr = []
     a = open(f'kbi{gfile.name}', 'w')
     b = open(f'helmholtz_{gfile.name}', 'w')
     duhr = open(f'duhr_{gfile.name}','w')
     tdsr = open(f'tdsr_{gfile.name}','w')
     for i in range(len(r)):
         a.write(f"{r[i]} {gij[i]}\n")
         h = free_energy(gr[i],r[i])
         if h!= inf and  h!= -inf:
              dAr.append(h)
              tdSr.append(-1 * (h - Ur[i]))
              print(-1*(h-Ur[i]))
              if 5 > h and h > -5:
                   b.write(f"{r[i]} {h}\n")
              if 5 > Ur[i] and Ur[i] > -5:
                   duhr.write(f"{r[i]} {Ur[i]}\n")
              if 5 > (-1*(h-Ur[i])) and (-1*(h-Ur[i])) > -5:
                   tdsr.write(f"{r[i]} {((h-Ur[i]))}\n")
     a.close()
     b.close()
     gfile.close()
     output.close()
     remove("correct.out")
main()
