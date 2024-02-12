import re
import numpy as np 
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

x_ticks = [3, 5, 10, 15, 20, 25, 30, 35, 40, 45]
minizinc_performance = "result_from_cluster_for_comparison.txt"
my_search_performance = "results_from_cluster_comparison_fixpoint.txt"

with open(minizinc_performance, "r") as f:
    input_str = f.read()

numbers_minizinc = re.findall(r'\d+\.\d{2}', input_str)

with open(my_search_performance, "r") as f:
    input_str = f.read()
numbers_my_search = re.findall(r'\d+\.\d{2}', input_str)

# convert them to integers
numbers_minizinc = [float(number) for number in numbers_minizinc]
numbers_my_search = [float(number) for number in numbers_my_search]


def func(x, a, b, c):
    return np.exp(b * np.array(x))

popt, pcov = curve_fit(func,  x_ticks,  numbers_minizinc, maxfev=50000)

x_ticks_for_function = [i for i in range(0,100)]
plt.plot(func(x_ticks_for_function, *popt), label="Fitted Curve Minizinc")
plt.xlabel('Size of Latin Square')
plt.ylabel('Computation Time [s]')
plt.title('Performance Comparison')
popt, pcov = curve_fit(func,  x_ticks,  numbers_my_search, maxfev=50000)
plt.plot(func(x_ticks_for_function, *popt), label="Fitted Curve MySearch")
plt.legend()
plt.yscale('log')
plt.show()


plt.plot(numbers_minizinc, 'ko', label='Minizinc Computation Times')
plt.plot(numbers_my_search, 'bs', label='My Search Computation Times')
plt.plot(numbers_minizinc, label="Minizinc")
plt.plot(numbers_my_search, label="MySearch")
plt.xticks(np.arange(len(x_ticks)), x_ticks)
plt.xlabel('Size of Latin Square')
plt.ylabel('Computation Time [s]')
plt.title('Performance Comparison')
plt.legend()

plt.show()

