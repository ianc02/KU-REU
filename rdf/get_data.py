

def main():

	f = open("data.new",'r')
	fl = f.readlines()
	f2 = open("data_input_tmao", 'w')
	get = False
	n = 0
	d = {}
	for i in fl:
		if "atoms" in i:
			n = int(i.split()[0])
		if "Atoms" in i:
			get = True
		elif "Bonds" in i or "Vel" in i:
			get = False
		elif get:
			if len(i)>1:
				d[int(i.split()[0])] = i
				#f2.write(i)
	for i in range(n):
		f2.write(d[i+1])
	
	f2.close()
	f.close()

main()
