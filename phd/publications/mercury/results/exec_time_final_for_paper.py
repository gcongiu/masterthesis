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


#### local, Lustre, GPFS

##### Test cluster

# single client, no AM
means_noAM = (107.0673665046692, 134.14148278236388, 83.37485174999999)
std_noAM = (0.38798420331930866, 1.1754509755077274, 0.8945594034974245)

#############################

# single client, no sliding window, target config
means_goodconf = (102.47633774280548, 73.216443490982059, 72.84632065)
std_goodconf = (0.45904493551013592, 0.55475448770501945, 0.7522566832176272)

#############################


# single client, no sliding window, bad config # to be added
means_badconf = (112.84858430624008, 80.769025635719302, 74.65)
std_badconf = (0.58993962948577161, 0.82997751260967223, 0.80)

#############################

# single client, sliding window
means_slw = (88.484313249588013, 74.536100697517398, 84.211109042167664)
std_slw = (1.4131788579314211, 0.49514813374203193, 0.24152696132659912)

#############################

##### Mogon

# single client, no AM
mogon_means_noAM = (241.40, 0, 223.53779196739197)
mogon_std_noAM = (9.3955692867559968, 0, 4.4276278614751385)

#############################

# manca mogon local no sliding window

# single client, no sliding window, target config
mogon_means_goodconf = (219.64, 0, 195.50043923854827)
mogon_std_goodconf = (0.62528002262115479, 0, 2.594206678379936)

#############################

# single client, sliding window
mogon_means_slw = (202.87780077457427, 0, 223.92213675975799)
mogon_std_slw = (2.4681687052376979, 0, 2.9779783645669058)

#############################


fig, ax = plt.subplots()

index = np.arange(n_groups)
#group_labels = ["Local", "Lustre"]
#num_items = len(group_labels)
bar_width = 0.09


# This needs to be a numpy range for xdata calculations
# to work.
#ind = np.arange(num_items)
#margin = 0.1
#bar_width = (1.-2.*margin)/2
#opacity = 0.4
error_config = {'ecolor': '0'}


#margin = 0.2
#bar_width = (1.-2.*margin)/3



rects1 = plt.bar(index - 3*bar_width, means_noAM, bar_width,
                 #alpha=opacity,
                 color='0',
                 yerr=std_noAM,
                 error_kw=error_config,
                 label='w/o AM - Test'
                 )

rects2 = plt.bar(index - 2*bar_width, means_slw, bar_width,
                 #alpha=opacity,
                 color='0.2',
                 yerr=std_slw,
                 error_kw=error_config,
                 label='w/ AM, WillNeed all file - Test')#,
                 #hatch='xx')
                 
                 
rects3 = plt.bar(index - 1*bar_width, means_goodconf, bar_width,
 #                #alpha=opacity,
                 color='0.4',
                 yerr=std_goodconf,
                 error_kw=error_config,
                 label='w/ AM, Tailored config file - Test'
                 )                 

rects4 = plt.bar(index + 0.1*bar_width, mogon_means_noAM, bar_width,
                 #alpha=opacity,
                 color='0.6',
                 yerr=std_noAM,
                 error_kw=error_config,
                 label='w/o AM - Mogon'
                 )

rects5 = plt.bar(index + 1.1*bar_width, mogon_means_slw, bar_width,
                 #alpha=opacity,
                 color='0.8',
                 yerr=std_slw,
                 error_kw=error_config,
                 label='w/ AM, WillNeed all file - Mogon')#,
                 #hatch='xx')
                 
rects6 = plt.bar(index + 2.1*bar_width, mogon_means_goodconf, bar_width,
 #                #alpha=opacity,
                 color='1',
                 yerr=std_goodconf,
                 error_kw=error_config,
                 label='w/ AM, Tailored config file - Mogon'
                 )                 
              
                 
                 
#ax.set_xlim([0.2, 2.0]) 
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
plt.xticks(index, ('ext4', 'Lustre', 'GPFS'), fontsize=15)
#plt.legend(fontsize=12)

#plt.tight_layout()
plt.show()
