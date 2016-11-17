# -*- coding: utf-8 -*-
"""
Created on Wed May  7 10:48:34 2014

@author: Federico
"""

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

#no sliding window

n_groups = 3


#### local, Lustre, GPFS Number of reads

##### Test cluster

# single client, no AM
means_noAM = (24295, 10882, 4697)
std_noAM = (24, 35, 43)

#############################

# single client, no sliding window, target config
means_goodconf = (12219, 5344, 1089)
std_goodconf = (121, 20, 0)

#############################


# single client, no sliding window, bad config ### to be added
means_badconf = (12380, 5201, 3805)
std_badconf = (136, 30, 45)

#############################

# single client, sliding window
means_slw = (10993, 5114, 4509)
std_slw = (36, 15, 48)

#############################



fig, ax = plt.subplots()

#index = np.arange(n_groups)
index = np.array((0.30,0.50,0.70))
#group_labels = ["Local", "Lustre"]
#num_items = len(group_labels)
bar_width = 0.025
#bar_width = 0.05

# This needs to be a numpy range for xdata calculations
# to work.
#ind = np.arange(num_items)
#margin = 0.1
#bar_width = (1.-2.*margin)/2
#opacity = 0.4
error_config = {'ecolor': '0.3'}


rects1 = plt.bar(index- 2*bar_width, means_noAM, bar_width,
                 #alpha=opacity,
                 color='0.2',
                 yerr=std_noAM,
                 error_kw=error_config,
                 label='w/o AM'
                 )

rects2 = plt.bar(index-bar_width, means_slw, bar_width,
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
                 label='With AM, non optimal config'
                 )

rects4 = plt.bar(index+bar_width, means_goodconf, bar_width,
                 #alpha=opacity,
                 color='0.9',
                 yerr=std_goodconf,
                 error_kw=error_config,
                 label='w/ AM, Tailored config file'
                 )                 
              
                 
                 

#plt.grid()
#plt.xlabel('File systems', fontsize=15, verticalalignment='bottom')
#plt.xlabel('File systems')
plt.ylabel('# reads', fontsize=15)
plt.yticks(fontsize=12)
#plt.title('Execution time')
start, end = ax.get_ylim()
#ax.yaxis.set_ticks(np.arange(start, end, 5))
ax.yaxis.grid(True)
ax.xaxis.grid(False)
plt.xticks(index, ('ext4', 'Lustre', 'GPFS'), fontsize=15)
plt.legend(loc='upper right', fontsize=12)

plt.tight_layout()
plt.show()