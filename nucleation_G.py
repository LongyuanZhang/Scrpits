import csv
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import os
import sys
import numpy as np
import paramiko
import getpass

# paramiko server connect ####################

pswd = getpass.getpass('CHTC password:')
trans = paramiko.Transport(('submit-1.chtc.wisc.edu', 22))
trans.connect(username='lzhang657', password=pswd)
ssh = paramiko.SSHClient()
ssh._transport = trans
sftp = paramiko.SFTPClient.from_transport(trans)

# GCMC part ##################################

M = 4 # number of intermediate states + 1
UpperLimit = 8 # maximum number of atom (pairs)
LowerLimit = 1 # minimum number of atom (pairs)
Temperature = 298.15
kT = 2.478957 * Temperature / 298.15
N = 4

folders = list(range(1,N+1)) # 1, 2, 3, 4

data = [] # list of data of N gcmc tries
data_split = [] # list of data split of N gcmc tries [[['-0', '0'], ...], ...]
G_gcmc = [] # list of free energy data in kT of N gcmc tries float numbers [[-0, ...], ...]
G_gcmc_means = [] # list of mean free energy in kT [-0, ...]
G_gcmc_stderr = [] # list of free energy standard deviation in kT [0, ...]

for i in folders:
    with open("%s/results" % i) as f:
        lines = f.readlines()
    data_tmp = lines[(M * (LowerLimit - UpperLimit) - 2):-1:M]
    data.append(data_tmp)
    data_split.append([state.split() for state in data_tmp])
    G_gcmc.append([float(state.split()[0])/(kT * 1000) for state in data_tmp])

for i in range(LowerLimit-1, UpperLimit):
    G_i = [gcmc[i] for gcmc in G_gcmc]
    G_gcmc_means.append(np.mean(G_i))
    G_gcmc_stderr.append(np.std(G_i))

plt.scatter(list(range(LowerLimit, UpperLimit+1)), np.array(G_gcmc_means), label='GCMC NonInteracting Red-Blue')

# Graph-based approach part ####################

Mu = 50 # chemical potential
Temperature = 298.15
kT = 2.478957 * Temperature / 298.15

start = int(sys.argv[1]) # i of folder N$i
end  = int(sys.argv[2])

dG_means = []
dG_stderrs = []

for i in range(start, end+1):
    with sftp.open('/home/lzhang657/Nucleation_send/results/N%s/dG.txt' % i) as f:
        lines = f.readlines()
    dG_array = np.loadtxt(lines)
    dG_mean = -1 * np.log(np.mean(np.exp(-1 * dG_array[~np.isnan(dG_array)]))) + Mu/kT
    dG_means.append(dG_mean)
    samples = []
    for j in range(5000):
        dG_sample = np.random.choice(dG_array, size = 1000, replace = True)
        dG_sample_mean = -1 * np.log(np.mean(np.exp(-1 * dG_sample[~np.isnan(dG_sample)]))) + Mu/kT
        samples.append(dG_sample_mean)
    dG_stderrs.append(np.std(samples))

G_gb_means = np.cumsum(np.array(dG_means))
G_gb_means = np.insert(G_gb_means, 0, 0)
dG_vars = np.square(np.array(dG_stderrs))
G_gb_vars = np.cumsum(dG_vars)
G_gb_vars = np.insert(G_gb_vars, 0, 0)
G_gb_stderrs = np.sqrt(G_gb_vars)
#print(G_stderrs)
#err_test = np.linspace(0.05, 0.2, 12)

plt.plot(list(range(start, end+2)), G_gb_means, label='Graph-based approach NI Red-Blue')
plt.fill_between(list(range(start, end+2)), G_gb_means-G_gb_stderrs, G_gb_means+G_gb_stderrs, color='r', alpha=0.2)
#plt.fill_between(list(range(start, end+2)), G_means-err_test, G_means+err_test, color='r', alpha=0.2)

################################################

plt.xlabel('N (pairs)')
plt.ylabel('G (kT)')
#plt.fill_between(list(range(LowerLimit, UpperLimit+1)), np.array(G_means)-np.array(G_stderr), np.array(G_means)+np.array(G_stderr), color='r', alpha=0.2)
plt.legend()
plt.savefig('NI_RB.pdf')
