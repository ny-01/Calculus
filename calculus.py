# aim of project: calculus calculator
import matplotlib.pyplot as plt
import numpy as np
start=1000
step=.001
x = [i*step for i in range(start,10000)]

# [x_0,x_1,x_2]
# [y_0]
# now to generate next element, we take current derivative, which is a function of for instance y_2 and x_2 and we generate y_3
# therefore the list is a function of the old list
# [x_0,x_1,x_2]
# [y_0,y_1]
# etc.

# we can see that [y_0,y_1] is determined because it is a function of [y_0] and x, where we used x_0 and y_0 for the derivative which yielded y_1

def derivative(fn):
    # (start+len(fn)-1)*step = current x value
    # (fn[-1]) = current y value
    return -(1/(((start+len(fn)-1)*step)**2))

def create_fn(current_fn):
    while len(current_fn) < len(x):
        next_val = current_fn[-1] + (step * derivative(current_fn))
        current_fn.append(next_val)
    return current_fn

for i in np.arange(-1,1,.1):
    print(f"current i: {i}")
    y=create_fn([1])
    # Plot
    plt.plot(x, y, marker='o', linestyle='-', color='b')
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.title("Graph")
    plt.grid(True)
    plt.show()
    plt.show()