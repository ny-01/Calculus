# aim of project: calculus calculator
from matplotlib.patches import Circle
import matplotlib.pyplot as plt
start=0
step=.1
x = [i*step for i in range(start,10)]
derivative_sequence=[]

class DraggablePoint:
    def __init__(self, point, callback=None):
        self.point = point
        self.press = None
        self.callback = callback
        self.connect()

    def connect(self):
        self.cid_press = self.point.figure.canvas.mpl_connect(
            'button_press_event', self.on_press)
        self.cid_release = self.point.figure.canvas.mpl_connect(
            'button_release_event', self.on_release)
        self.cid_motion = self.point.figure.canvas.mpl_connect(
            'motion_notify_event', self.on_motion)

    def on_press(self, event):
        if event.inaxes != self.point.axes: return
        contains, _ = self.point.contains(event)
        if not contains: return
        self.press = (self.point.center, event.xdata, event.ydata)

    def on_motion(self, event):
        if self.press is None or event.inaxes != self.point.axes: return
        (cx, cy), xpress, ypress = self.press
        dx = event.xdata - xpress
        dy = event.ydata - ypress
        self.point.center = (cx + dx, cy + dy)
        if self.callback:
            self.callback(self.point.center)
        self.point.figure.canvas.draw()

    def on_release(self, event):
        self.press = None
        self.point.figure.canvas.draw()

# [x_0,x_1,x_2]
# [y_0]
# now to generate next element, we take current derivative, which is a function of for instance y_2 and x_2 and we generate y_3
# therefore the list is a function of the old list
# [x_0,x_1,x_2]
# [y_0,y_1]
# etc.

# we can see that [y_0,y_1] is determined because it is a function of [y_0] and x, where we used x_0 and y_0 for the derivative which yielded y_1

def derivative(fn, start, step):
    # (start+((len(fn)-1)*step)) = current x value
    x=(start+((len(fn)-1)*step))
    y=fn[-1]
    # (fn[-1]) = current y value
    # return -(1/(((start+len(fn)-1)*step)**2))
    derivative_sequence.append(x**2+y**2)
    return (x**2+y**2)

def create_fn(current_fn, domain, start, step):
    while len(current_fn) < len(domain):
        next_val = current_fn[-1] + (step * derivative(current_fn, start, step))
        current_fn.append(next_val)
    else:
        # print(start+((len(current_fn)-1)*step)) # prints the final x-value (for the last point of the sequence)
        derivative_sequence.append(current_fn[-1])
    return current_fn

# Callback to use the coordinates elsewhere
def update_coords(new_coords):
    derivative_sequence.clear()
    x, y = new_coords
    # print(f"Point moved to: ({x:.2f}, {y:.2f})")
    start=x
    # print(f"start: {start}")
    step=.1
    domain = [start+i*step for i in range(0,10)]
    function = create_fn([y], domain, start, step)
    # print(function)
    line.set_ydata(function)
    line.set_xdata(domain)
    print(function)
    line2.set_ydata(derivative_sequence)
    print(derivative_sequence)
    print(domain)
    line2.set_xdata(domain)

# Set up plot
plt.ion()
fig, ax = plt.subplots()
ax.set_xlim(-10, 10)
ax.set_ylim(-10, 10)
ax.set_aspect('equal')

# Create a draggable point
point = Circle((5, 5), 0.5, fc='red', alpha=0.5)
ax.add_patch(point)
initial_function=create_fn([0],x,start,step)
print(initial_function)
print(derivative_sequence)
line, = ax.plot(x, initial_function, marker='o', linestyle='--', label="Function")
line2, = ax.plot(x, derivative_sequence, marker='o', linestyle='--', label="Derivative")
plt.subplots_adjust(left=.4)
axbox=plt.axes([0.1,.8,.2,.05])
axbox.set_xticks([])
axbox.set_yticks([])
dragger = DraggablePoint(point, callback=update_coords)