


def main():
   

     outfile = open("output.log",'r')
     energyfile = open("energy",'w')
     outlines = outfile.readlines()
     check = False
     check2 = False
     p = 0
     for i in outlines:
          p +=1
          if p % 600000 == 0:
               print(f"{p/6000000} percent done")
          if check:
               if i != "" and i != "\n":
                    if i.split()[0].isnumeric():
                         i = i.split()
                         t = int(i[0])
                         i = f"{i[3]} {i[5]} {i[6]} {i[7]} {i[10]}\n"
                         if t == 1000850:
                              print(i)
                         energyfile.write(i)
                    else:
                         break
          else:
               if i != "" and i != "\n":
                    if i.split()[0] == "Step":
                         if check2:
                              check = True
                              energyfile.write(i)
                         
                         else:
                              check2 = True

main()                    
