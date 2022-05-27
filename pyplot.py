# pyplot setting from Yunrui
ax1.set_yscale('log')
plt.xlim(-1.5, 200)
plt.ylim(1e1, 1e4)
# =============================================================================
# plt.xlim(-1.5, 20)
# plt.ylim(1.8, 140)
# =============================================================================
plt.xlabel("lag time(ns)", size=13, weight='normal', family='Arial, Helvetica')
plt.ylabel("Implied Time Scale(ITS)($ns$)", size=13, weight='normal', family='Arial, Helvetica')
plt.tick_params(which='major', width=3, direction='in', labelsize=15, length=10)
plt.tick_params(which='minor', width=1, direction='in', length=7)
plt.minorticks_on()
plt.xticks(fontsize=19)
plt.yticks(fontsize=19)
ax1.spines['bottom'].set_linewidth(2.0)
ax1.spines['left'].set_linewidth(2.0)
ax1.spines['top'].set_linewidth(2.0)
ax1.spines['right'].set_linewidth(2.0)
