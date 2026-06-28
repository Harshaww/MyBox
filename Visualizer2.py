import matplotlib
matplotlib.use('TkAgg')  # Use TkAgg backend for interactive plotting

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from matplotlib.animation import FuncAnimation

class Visualizer2:
    """
    A class for visualizing movie rating trends and comparisons for actresses.
    """
    def plot_actress_comparison_animated(self, actress_data):
        """
        Plots a professional animated 3D bar chart comparing average ratings of famous actresses,
        with an interactive pause and resume feature.

        Parameters:
        - actress_data: dict with 'actresses' (list of str) and 'average_ratings' (list of floats)
        """
        actresses = actress_data['actresses']
        avg_ratings = actress_data['average_ratings']

        fig = plt.figure(figsize=(14, 10))  # Increased figure size for better layout
        ax = fig.add_subplot(111, projection='3d')

        x_pos = np.arange(len(actresses))
        y_pos = np.zeros(len(actresses))
        z_pos = np.zeros(len(actresses))

        dx = np.ones(len(actresses)) * 0.6
        dy = np.ones(len(actresses)) * 0.6
        dz = avg_ratings

        blue_shades = ['#1f77b4', '#4fa3f7', '#7ba6f7', '#9ec7f7', '#c3d9f7', '#e0ecf7']
        ax.bar3d(x_pos, y_pos, z_pos, dx, dy, dz, color=blue_shades, edgecolor='black', alpha=1.0)

        for x, z in zip(x_pos, avg_ratings):
            ax.text(x, 0, z + 0.1, f'{z:.1f}', ha='center', va='bottom', fontsize=12, fontweight='bold',
                    color='white', backgroundcolor='black')

        ax.set_xticks(x_pos)
        ax.set_xticklabels(actresses, fontsize=12, rotation=45, ha='right', fontweight='medium')
        ax.set_yticks([])

        ax.set_zlabel('Average Rating', fontsize=14, fontweight='bold', labelpad=10)

        # Adjust the title to move it lower
        ax.set_title('Average Ratings of Movies by Actresses', fontsize=18, fontweight='bold', pad=10)

        ax.grid(False)
        ax.xaxis.pane.fill = False
        ax.yaxis.pane.fill = False
        ax.zaxis.pane.fill = False

        def update(frame):
            ax.view_init(elev=20, azim=frame)

        ani = FuncAnimation(fig, update, frames=np.arange(0, 360, 2), interval=50, repeat=True)

        anim_running = [True]

        def on_click(event):
            if anim_running[0]:
                ani.event_source.stop()
                anim_running[0] = False
            else:
                ani.event_source.start()
                anim_running[0] = True

        fig.canvas.mpl_connect('button_press_event', on_click)

        # Adjust margins to avoid title clipping
        plt.subplots_adjust(left=0.05, right=0.95, top=0.9, bottom=0.05)  # Adjust top margin to move the title lower

        plt.show()
