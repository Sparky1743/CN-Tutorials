import matplotlib.pyplot as plt

clients = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
single_process = [30.023680569, 60.036497411, 90.0531781, 120.071837535, 150.070197761, 180.100327254, 210.093804523, 240.123100509, 270.166767113, 300.163464709]
multi_process = [3.02739837, 3.05560865, 3.078539424, 3.078337925, 3.121361768, 3.106675833, 3.190847606, 3.16420241, 3.220506968, 3.229689229]
multi_threaded = [3.032717809, 3.044436704, 3.067425206, 3.088481507, 3.106143813, 3.142782118, 3.148112196, 3.212299448, 3.18993193, 3.202744687]

plt.plot(clients, single_process, label='Single-Process')
plt.plot(clients, multi_process, label='Multi-Process')
plt.plot(clients, multi_threaded, label='Multi-Threaded')
plt.xlabel('Number of Concurrent Clients')
plt.ylabel('Execution Time (seconds)')
plt.legend()
plt.show()
