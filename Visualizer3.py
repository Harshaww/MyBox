import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from matplotlib.animation import FuncAnimation

class Visualizer3:
    """
    A class for visualizing movie rating trends and comparisons.
    """
    def plot_director_comparison_animated(self, director_data):
        """
        Plots a professional animated 3D bar chart comparing average ratings of famous directors,
        with an interactive pause and resume feature.

        Parameters:
        - director_data: dict with 'directors' (list of str) and 'average_ratings' (list of floats)
        """
        directors = director_data['directors']
        avg_ratings = director_data['average_ratings']

        # Setup figure and 3D axes
        fig = plt.figure(figsize=(14, 10))  # Increased figure size for better layout
        ax = fig.add_subplot(111, projection='3d')

        # Create x positions for directors
        x_pos = np.arange(len(directors))
        y_pos = np.zeros(len(directors))
        z_pos = np.zeros(len(directors))

        # Bar dimensions
        dx = np.ones(len(directors)) * 0.6
        dy = np.ones(len(directors)) * 0.6
        dz = avg_ratings

        # Shades of blue (a gradient of blue colors)
        blue_shades = ['#1f77b4', '#4fa3f7', '#7ba6f7', '#9ec7f7', '#c3d9f7', '#e0ecf7']

        # Plot 3D bars with different shades of blue
        ax.bar3d(x_pos, y_pos, z_pos, dx, dy, dz, color=blue_shades, edgecolor='black', alpha=1.0)

        # Annotate bars with values and make the text more clear
        for x, z in zip(x_pos, avg_ratings):
            ax.text(x, 0, z + 0.1, f'{z:.1f}', ha='center', va='bottom', fontsize=12, fontweight='bold',
                    color='white', backgroundcolor='black')

        # Set axis labels
        ax.set_xticks(x_pos)
        ax.set_xticklabels(directors, fontsize=12, rotation=45, ha='right', fontweight='medium')
        ax.set_yticks([])
        ax.set_zlabel('Average Rating', fontsize=14, fontweight='bold', labelpad=10)

        # Title with adjusted position
        ax.set_title('Average Ratings of Movies by Directors', fontsize=18, fontweight='bold', pad=10)

        ax.grid(False)
        ax.xaxis.pane.fill = False
        ax.yaxis.pane.fill = False
        ax.zaxis.pane.fill = False

        # Animation function
        def update(frame):
            ax.view_init(elev=20, azim=frame)

        # Animate rotation
        ani = FuncAnimation(fig, update, frames=np.arange(0, 360, 2), interval=50, repeat=True)

        # Variable to toggle animation state
        anim_running = [True]

        def on_click(event):
            """
            Toggles the animation on mouse click.
            """
            if anim_running[0]:
                ani.event_source.stop()
                anim_running[0] = False
            else:
                ani.event_source.start()
                anim_running[0] = True

        # Connect the click event
        fig.canvas.mpl_connect('button_press_event', on_click)

        # Adjust margins to ensure title and plot fit well
        plt.subplots_adjust(left=0.05, right=0.95, top=0.9, bottom=0.05)

        plt.show()


# # Example Data for Famous Directors
# director_data = {
#     'directors': ['Steven Spielberg', 'Christopher Nolan', 'Quentin Tarantino',
#                   'Martin Scorsese', 'James Cameron', 'Greta Gerwig'],
#     'average_ratings': [8.1, 8.6, 8.3, 8.2, 7.9, 7.8]
# }
#
# # Example Usage
# if __name__ == "__main__":
#     visualizer = Visualizer()
#     visualizer.plot_director_comparison_animated(director_data)
