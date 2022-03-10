# Script from Soonho Kwon
import linecache
import os

Angs2Bohr = 1.889726126
#--------------------------------------------------------------------------
# get lattice info
a1 = linecache.getline("./CONTCAR", 3).split()
a2 = linecache.getline("./CONTCAR", 4).split()
a3 = linecache.getline("./CONTCAR", 5).split()

a11 = str(float(a1[0])*Angs2Bohr)
a12 = str(float(a1[1])*Angs2Bohr)
a13 = str(float(a1[2])*Angs2Bohr)
a21 = str(float(a2[0])*Angs2Bohr)
a22 = str(float(a2[1])*Angs2Bohr)
a23 = str(float(a2[2])*Angs2Bohr)
a31 = str(float(a3[0])*Angs2Bohr)
a32 = str(float(a3[1])*Angs2Bohr)
a33 = str(float(a3[2])*Angs2Bohr)
#--------------------------------------------------------------------------
#get element info
type = linecache.getline("./CONTCAR", 6).split()
num = linecache.getline("./CONTCAR", 7).split()
element_list = []
for i in range(len(num)):
	for j in range(int(num[i])):
		element_list.append(type[i])
#--------------------------------------------------------------------------
f = open("geo.in", 'w')

f.write("lattice  \\\n")
f.write(a11.rjust(20)+ a21.rjust(20)+ a31.rjust(20)+"  \\\n")
f.write(a12.rjust(20)+ a22.rjust(20)+ a32.rjust(20)+"  \\\n")
f.write(a13.rjust(20)+ a23.rjust(20)+ a33.rjust(20)+"\n\n")
f.write("coords-type Lattice\n")

dump = 0
with open("./CONTCAR", 'r') as r:
	for num, line in enumerate(r, 1):
		if num > 9 and line != " \n":
			content = line.split()
			#print(content)
			f.write("ion "+element_list[dump].ljust(4)+content[0]+"    "+content[1]+"    "+content[2]+ "   0\n")
			dump += 1
		elif line == " \n":
			break
f.close()

