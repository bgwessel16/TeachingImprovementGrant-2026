import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Generate samples
samples = np.random.normal(loc=3, scale=0.3, size=500)
samples = np.concatenate([samples, np.full(20, 10)])   # spike
samples = np.concatenate([samples, np.random.normal(loc=3, scale=0.3, size=30)])

fig, ax = plt.subplots()
window_size = 100
ax.set_ylim(0, 11)
ax.set_xlabel("Time in ms")
ax.set_ylabel("IMU Reading")
ax.set_title("IMU Sensor Reading")

line, = ax.plot([], [], lw=2, color='blue')
spike_points, = ax.plot([], [], 'ro', markersize=4)  # red dots for spikes
annotation = None  # placeholder for text annotation

def update(frame):
    global annotation
    start = max(0, frame - window_size)
    end = frame
    x = np.arange(start, end)
    y = samples[start:end]
    line.set_data(x, y)
    ax.set_xlim(start, end)

    # Highlight spikes (value == 10)
    spike_x = x[y == 10]
    spike_y = y[y == 10]
    spike_points.set_data(spike_x, spike_y)

    # Remove old annotation if it exists
    if annotation:
        annotation.remove()
        annotation = None

    # Add annotation when spike is roughly centered in the window
    if len(spike_x) > 0:
        mid_x = (start + end) // 2
        # Check if spike is near the middle of the window
        if np.any((spike_x > mid_x - 5) & (spike_x < mid_x + 5)):
            annotation = ax.annotate(
                "Emergency Stop",
                xy=(mid_x, 10),
                xytext=(mid_x, 10.5),
                color="red",
                fontsize=12,
                ha="center",
                arrowprops=dict(facecolor='red', shrink=0.05)
            )

    return line, spike_points, annotation if annotation else line

ani = animation.FuncAnimation(fig, update, frames=len(samples), interval=30, blit=False)
ani.save("scrolling_line_with_spike.gif", writer="pillow")
