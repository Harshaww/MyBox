import matplotlib
matplotlib.use('TkAgg')  # Use TkAgg backend for interactive plotting

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from matplotlib.animation import FuncAnimation

class Visualizer1:
    def plot_actor_comparison_animated(self, actor_data):
        actors = actor_data['actors']
        avg_ratings = actor_data['average_ratings']

        fig = plt.figure(figsize=(12, 8))
        ax = fig.add_subplot(111, projection='3d')

        x_pos = np.arange(len(actors))
        y_pos = np.zeros(len(actors))
        z_pos = np.zeros(len(actors))

        dx = dy = 0.6
        dz = avg_ratings

        blue_shades = ['#1f77b4', '#4fa3f7', '#7ba6f7', '#9ec7f7', '#c3d9f7', '#e0ecf7']
        ax.bar3d(x_pos, y_pos, z_pos, dx, dy, dz, color=blue_shades, edgecolor='black', alpha=1.0)

        for x, z in zip(x_pos, avg_ratings):
            ax.text(x, 0, z + 0.1, f'{z:.1f}', ha='center', va='bottom', fontsize=12, fontweight='bold',
                    color='white', backgroundcolor='black')

        ax.set_xticks(x_pos)
        ax.set_xticklabels(actors, fontsize=12, rotation=45, ha='right', fontweight='medium')
        ax.set_yticks([])
        ax.set_zlabel('Average Rating', fontsize=14, fontweight='bold', labelpad=10)
        ax.set_title('Average Ratings of Movies by Actors', fontsize=18, fontweight='bold', pad=20)

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

        plt.show()