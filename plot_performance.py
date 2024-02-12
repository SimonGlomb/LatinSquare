import re
import numpy as np 
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

x_ticks = [3, 5, 10, 15, 20, 25, 30, 35]
minizinc_performance = "result_from_cluster_for_comparison.txt"

with open(minizinc_performance, "r") as f:
    input_str = f.read()

numbers_minizinc = re.findall(r'\d+\.\d{2}', input_str)


# convert them to integers
numbers_minizinc = [float(number) for number in numbers_minizinc]


plt.xlabel('Size of Latin Square')
plt.ylabel('Computation Time [s]')
plt.title('Performance Comparison')
plt.legend()
plt.show()


plt.plot(numbers_minizinc, 'ko', label='Minizinc Computation Times')
plt.plot(numbers_minizinc, label="Minizinc")
plt.xticks(np.arange(len(x_ticks)), x_ticks)
plt.xlabel('Size of Latin Square')
plt.ylabel('Computation Time [s]')
plt.title('Performance Comparison')
plt.legend()

plt.show()
