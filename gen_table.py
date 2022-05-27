# script to generate user-specified potential tables for gromacs md simulation
import os
import sys
import math

# B in nanometer
B_Na_Na=62.1118
B_Cl_Cl=32.57329
B_Na_Cl=29.7619

# nanometer
delr = 0.0005
rcut = 1.0
rstart = 0.004

nbins = int((rcut + 1)/delr) + 1

def write_bkhm(atom_a, atom_b):
    with open("table_{}_{}.xvg".format(atom_a, atom_b), 'w') as f:
        B = globals()["B_{}_{}".format(atom_a, atom_b)]
        for j in range(0, nbins):
            r = delr * j
            # gromacs will never use the paramters when r is too small, simply because two atoms cannot be so close to each other.
            if r == 0 or r < rstart:
                f.write("%e  %e %e  %e %e  %e %e\n" % (r,1,1,1,1,1,1))
            else:
                f.write("%e  %e %e  %e %e  %e %e\n" % (r, 1/r, 1/(r*r), -1/(r**6), -6/(r**7), math.exp(-B*r), -B*math.exp(-B*r)))
    return

def write_LJ(atom_a, atom_b, name):
    with open("table_{}_{}.xvg".format(atom_a, atom_b), 'w') as f:
        for j in range(0, nbins):
            r = delr * j
            if r == 0 or r < rstart:
                f.write("%e  %e %e  %e %e  %e %e\n" % (r,1,1,1,1,1,1))
            else:
                f.write("%e  %e %e  %e %e  %e %e\n" % (r, 1/r, 1/(r*r), -1/(r**6), -6/(r**7), 1/(r**12), 12/(r**13)))
    return


write_bkhm("Na","Na")
write_bkhm("Cl","Cl")
write_LJ("Na","Cl")
