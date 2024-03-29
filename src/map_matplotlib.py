from models import System
import streamlit as st
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def update_markers(
    axis,
    highlight_systems: list[System]
):
    labels = [o.name for o in highlight_systems]
    for i, label in enumerate(labels):
        axis.text(highlight_systems[i].x, highlight_systems[i].y, label)

def update_matplotlib(
    fig,
    axis,
    course: list[System]
    ):
    course_x = [o.x for o in course if o.x is not None ]
    course_y = [o.y for o in course if o.y is not None]
    labels = [o.name for o in course if o.x is not None and o.y is not None]
    for i, label in enumerate(labels):
        axis.text(course_x[i], course_y[i], label)

    plt.plot(course_x, course_y, 'b-', linewidth=0.5)

    margin = 100
    try:
        min_x = min(course_x) - margin
        max_x = max(course_x) + margin
        min_y = min(course_y) - margin
        max_y = max(course_y) + margin
        print(f'min_x: {min_x}, max_x: {max_x}, min_y: {min_y}, max_y: {max_y}')
    except Exception as e:
        print(f'Problem calculating min/max: {e} from course_x: {course_x} and course_y: {course_y}')

    plt.xlim(min_x, max_x)  # Set x-axis limits to zoom in
    plt.ylim(min_y, max_y)  # Set y-axis limits to zoom in

    return (fig, axis)

def map_matplotlib(
        systems: list[System]
    ):

    # Data needs to be separated into a list of x & y values
    all_x = [o.x for o in systems]
    all_y = [o.y for o in systems]
    labels = [o.name for o in systems]

    # Config
    plt.style.use('dark_background')

    # These options do not work
    # plt.grid(True, color="yellow")
    # plt.grid(color='yellow', linestyle='-.', linewidth=0.7)
    # plt.legend(['Data'], loc='best', facecolor='black', edgecolor='yellow', labelcolor='yellow', draggable=True)

    fig, ax = plt.subplots()

    ax.grid(color='white')

    # These have no effect
    # ax.legend(['Data'], loc='best', facecolor='black', edgecolor='yellow', labelcolor='yellow', draggable=True)

    # Create a scatter plot
    # TODO: Support various sizes and colors dependent on system type and importance
    marker_sizes = [3+ 10*o.importance for o in systems]

    # Change color by type
    # marker_colors = ['white' if o.importance > 0.0 else 'blue' if o.type == 'hyperspace' else 'grey' for o in systems]
    marker_colors = ['blue' if o.affiliation == 'Light Side' else "red" if o.affiliation=="Dark Side" else 'grey' for o in systems]

    # marker_labels = [o.name for o in systems if o.importance > 0.0]
    ax.scatter(all_x, all_y, s=marker_sizes, c=marker_colors)

    # Configure scatter plot
    # Set axis labels
    # plt.xlabel('X-axis')
    # plt.ylabel('Y-axis')

    # Set plot title
    # plt.title('Recommended Navigation Plot')

    # Tooltips
    # Define tooltips for points and lines
    # These do not work
    # Set up mplcursors
    # cursor = mplcursors.cursor(hover=True)
    # cursor.connect("add", lambda sel: sel.annotation.set_text(f'({sel.target[0]:.2f}, {sel.target[1]:.2f})'))

    # scatter_tooltip = mplcursors.cursor(scatter_plot, hover=True)
    # line_tooltip = mplcursors.cursor(line_plot, hover=True)

    # Set tooltip formats
    # scatter_tooltip.formatter = '{label}: {x:.2f}, {y:.2f}'.format
    # line_tooltip.formatter = '{label}: {x:.2f}, {y:.2f}'.format

    # Add labels for points
    # for s in filtered_all_systems:
    #     plt.text(s.x, s.y, f'{s.name}', ha='left', va='bottom')
    # return plt

    # Add labels to the scatter plot
    # TODO: Only do this for select systems
    # for i, label in enumerate(labels):
    #     ax.text(all_x[i], all_y[i], label)
    # for i, label in enumerate(marker_labels):
    #     ax.text(all_x[i], all_y[i], label)
    # DOESN'T WORK
    # Configure cursor to display hover info
    # cursors = mplcursors.cursor(scatter_plot, hover=True)

    # # Define the hover info content
    # @cursors.connect("add")
    # def on_add(sel):
    #     ind = sel.target.index
    #     label = labels[ind]
    #     sel.annotation.set(text=label)

    #     # Set the visibility of the annotation based on selection state
    #     sel.annotation.set_visible(sel.index == ind)

    return (fig, ax)


# def display_map_maplotlib(
#         all_systems: list[System],
# ):
#     fig = map_matplotlib(all_systems)
#     fig_html = mpld3.fig_to_html(fig)
#     components.html(fig_html, height=600)