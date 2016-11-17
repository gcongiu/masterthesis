#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created on Sun May  4 12:18:00 2014

@author: Federico
"""

"""
Bar chart demo with pairs of bars grouped for easy comparison.
"""
import numpy as np
import matplotlib.pyplot as plt
import pylab
#no sliding window

n_groups = 2



#### DONE, nothing to do here
#### local, GPFS

##### Mogon

# single client, no AM
means_noAM = (241.40, 223.53779196739197)
std_noAM = (9.3955692867559968, 4.4276278614751385)

#############################

# manca mogon local no sliding window

# single client, no sliding window, target config
means_goodconf = (219.64, 195.50043923854827)
std_goodconf = (0.62528002262115479, 2.594206678379936)

#############################


# single client, no sliding window, bad config # to be added
means_badconf = (229.52905536890029, 196.08466672897339)
std_badconf = (2.3307542339326073, 2.8087625328291383)

#############################

# single client, sliding window
means_slw = (202.87780077457427, 223.92213675975799)
std_slw = (2.4681687052376979, 2.9779783645669058)

#############################



fig, ax = plt.subplots()
#ax.set_aspect('0.3')

#index = [0.2, 0.5]
#index = np.arange(n_groups)
index = np.array((0.6,1.40))
print index
#group_labels = ["Local", "Lustre"]
#num_items = len(group_labels)
#bar_width = 0.07
bar_width = 0.08

# This needs to be a numpy range for xdata calculations
# to work.
#ind = np.arange(num_items)
#margin = 0.1
#bar_width = (1.-2.*margin)/2
#opacity = 0.4
error_config = {'ecolor': '0'}

#margin = 0.45
#bar_width = (1.-2.*margin)/2
#plt.figure(figsize=(1.5, 1.5))

rects1 = plt.bar(index- 2*bar_width, means_noAM, bar_width,
                 #alpha=opacity,
                 color='0.2',
                 yerr=std_noAM,
                 error_kw=error_config,
                 label='w/o AM'
                 )

rects2 = plt.bar(index -bar_width, means_slw, bar_width,
                 #alpha=opacity,
                 color='0.4',
                 yerr=std_slw,
                 error_kw=error_config,
                 label='w/ AM, WillNeed all file')#,
                 #hatch='xx')
                 
                 
                 
rects3 = plt.bar(index, means_badconf, bar_width,
#                 #alpha=opacity,
                 color='0.6',
                 yerr=std_badconf,
                 error_kw=error_config,
                 label='w/ AM, non optimal config'
                 )

rects4 = plt.bar(index +bar_width, means_goodconf, bar_width,
                 #alpha=opacity,
                 color='0.9',
                 yerr=std_goodconf,
                 error_kw=error_config,
                 label='w/ AM, Tailored config file'
                 )                 
              
                 
ax.set_xlim([0, 2])
ax.set_ylim([0, 350])                  
#fig.figure(figsize=(1,1))
#plt.grid()
#plt.xlabel('File systems', fontsize=15, verticalalignment='bottom')
#plt.xlabel('File systems')
plt.ylabel('Execution time [sec]', fontsize=15)
plt.yticks(fontsize=12)
#plt.title('Execution time')
start, end = ax.get_ylim()
#ax.yaxis.set_ticks(np.arange(start, end, 10))
ax.yaxis.grid(True)
ax.xaxis.grid(False)
plt.xticks(index, ('ext4', 'GPFS'), fontsize=15)
plt.legend(loc='upper right', fontsize=12)
#plt.legend(loc='lower right')
#plt.tight_layout()
plt.show()