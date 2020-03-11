import numpy as np
import pandas as pd
from bisect import bisect_left
import time

def BinarySearch(a, x):
    i = bisect_left(a, x)
    if i != len(a) and a[i] == x:
        return i
    else:
        return -1

def vehicle_times(veh_times):
    value_max = max(veh_times.values())
    count = 0
    while value_max > 0:
        count = count + 1
        value_max = value_max // 10
    print '      Car   :    Times'
    for keys, values in veh_times.items():
        print '|', ' ', keys, ' :', '    ', values, '  ' * count, '|'

# -----------------------------------------------------------------------------------------------------------------------------------
# 1.Load And PreProcess The Data (park_data):   [Generalized]

park_data = np.array(pd.read_excel(r'/Users/nikhil/Desktop/Project/PUS/Utilities/Parking_Usage_Survey.xlsx'))
park_data = np.sort(park_data, axis=0)
period = float(input('Enter The Period Interval (hrs) :  '))
for i in range(park_data.shape[0]):
    for j in range(park_data.shape[1]):
        if np.isnan(park_data[i][j]):
            park_data[i][j] = 0
# -----------------------------------------------------------------------------------------------------------------------------------
# 2.Obtaining Different Vehicles Present (veh_list):    [Generalized]

start_time = time.time()
veh = np.reshape(park_data, (1, -1))[0]   # All The Vehicle's (A Single Vehicle Can Be More Than Once)
veh_list = []
[veh_list.append(veh) for veh in veh if veh not in veh_list]    # Appends Different Vehicle's Which Had Come Into The Parking Lot
# -----------------------------------------------------------------------------------------------------------------------------------
# 3.Obtaining In How Many Different Period's Of Time A Single Particular Vehicle Is Present (veh_times): [Generalized]

veh_times = {}
for vehicle in veh_list:  # Searching For This Particular Vehicle In Various Time-Slots
    seen_times = 0
    for i in range(park_data.shape[1]):
        veh_slot =[]
        [veh_slot.append(val) for val in park_data[:, i] if val != 0]
        if BinarySearch(veh_slot, vehicle) != -1:
            seen_times += 1
    veh_times[str(vehicle)] = seen_times
del veh_times['0.0']
#vehicle_times(veh_times)
# -----------------------------------------------------------------------------------------------------------------------------------
# 4. Obtaining The Parking Load (DataFrame:df):
veh_count = []
val_car = veh_times.values()
val_max = max(val_car)
times = [x for x in range(1, val_max + 1, 1)]
dur = [x * period for x in range(1, len(times) + 1)]
for val_times in times:
    count = 0
    for val_ in val_car:
        if val_times == val_:
            count += 1
    veh_count.append(count)
park_load = [float(a)*b for a,b in zip(veh_count, dur)]
df = {'Times Seen' : times, 'Duration (Hrs)' : dur, 'No. Of Vehicles' : veh_count, 'Parking Load' : park_load}
df = pd.DataFrame(df)
cols = df.columns.tolist()
cols = cols[-1:] + cols[:-1]
df = df[cols]
print df
print '                                                       ---------'
print '                                                         ', sum(df.iloc[:, 3])
print '                                                       ---------'
# -----------------------------------------------------------------------------------------------------------------------------------
# 5.Printing Results:

print 'Parking Load = ', sum(df.iloc[:, 3])

print 'Time Taken = ', time.time() - start_time