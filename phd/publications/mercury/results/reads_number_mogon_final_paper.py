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


#### local, Lustre, GPFS number of reads

##### Test cluster

# single client, no AM
means_noAM = (107.0673665046692, 134.14148278236388, 33)
std_noAM = (0.38798420331930866, 1.1754509755077274, 1)

#############################

# single client, no sliding window, target config
means_goodconf = (102.47633774280548, 73.216443490982059, 33)
std_goodconf = (0.45904493551013592, 0.55475448770501945, 1)

#############################


# single client, no sliding window, bad config
means_badconf = (102.41522600650788, 73.299172472953799, 33)
std_badconf = (0.74934338758966634, 0.58922943036197994, 1)

#############################

# single client, sliding window
means_slw = (88.484313249588013, 74.536100697517398, 33)
std_slw = (1.4131788579314211, 0.49514813374203193, 1)

#############################



fig, ax = plt.subplots()

index = np.arange(n_groups)
#group_labels = ["Local", "Lustre"]
#num_items = len(group_labels)
bar_width = 0.09
#bar_width = 0.05

# This needs to be a numpy range for xdata calculations
# to work.
#ind = np.arange(num_items)
margin = 0.1
#bar_width = (1.-2.*margin)/2
#opacity = 0.4
error_config = {'ecolor': '0.3'}


rects1 = plt.bar(index+margin, means_noAM, bar_width,
                 #alpha=opacity,
                 color='r',
                 yerr=std_noAM,
                 error_kw=error_config,
                 label='NO AM'
                 )

rects2 = plt.bar(index+margin+bar_width, means_slw, bar_width,
                 #alpha=opacity,
                 color='w',
                 yerr=std_slw,
                 error_kw=error_config,
                 label='With AM,sliding window',
                 hatch='xx')
                 
                 
                 
rects3 = plt.bar(index+margin+ 2*bar_width, means_badconf, bar_width,
                 #alpha=opacity,
                 color='b',
                 yerr=std_badconf,
                 error_kw=error_config,
                 label='With AM, target config'
                 )

rects4 = plt.bar(index + margin + 3*bar_width, means_goodconf, bar_width,
                 #alpha=opacity,
                 color='y',
                 yerr=std_goodconf,
                 error_kw=error_config,
                 label='With AM, general config'
                 )                 
              
                 
                 

#plt.grid()
#plt.xlabel('File systems', fontsize=15, verticalalignment='bottom')
#plt.xlabel('File systems')
plt.ylabel('Execution time [sec]', fontsize=15)
plt.title('Execution time')
start, end = ax.get_ylim()
ax.yaxis.set_ticks(np.arange(start, end, 5))
ax.yaxis.grid(True)
ax.xaxis.grid(False)
plt.xticks(index + 3*bar_width, ('Local FS', 'Lustre', 'GPFS'), fontsize=15)
plt.legend()

plt.tight_layout()
plt.show()