from models import System
import streamlit as st
import matplotlib.pyplot as plt
import mplcursors
import mpld3
import streamlit.components.v1 as components

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

    plt.plot(course_x, course_y, 'b--', linewidth=1.5)  # Use blue dashed lines with linewidth of 1.5

    margin = 1000
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
    # plt.axis('off')
    plt.style.use('dark_background')

    fig, ax = plt.subplots()

    ax.grid(color='white')

    # Configure legend with white text color
    ax.legend(['Data'], loc='best', facecolor='black', edgecolor='white', labelcolor='white', draggable=True)

    # Create a scatter plot
    scatter_plot = ax.scatter(all_x, all_y, s=3)

    # Configure scatter plot
    # Set axis labels
    # plt.xlabel('X-axis')
    # plt.ylabel('Y-axis')

    # Set plot title
    # plt.title('Recommended Navigation Plot')

    # Show grid
    plt.grid(True, color="white")

    # Tooltips
    # Define tooltips for points and lines
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

    # DOESN'T WORK
    # Configure cursor to display hover info
    cursors = mplcursors.cursor(scatter_plot, hover=True)

    # Define the hover info content
    @cursors.connect("add")
    def on_add(sel):
        ind = sel.target.index
        label = labels[ind]
        sel.annotation.set(text=label)

        # Set the visibility of the annotation based on selection state
        sel.annotation.set_visible(sel.index == ind)



    return (fig, ax)

def display_map_matplotlib(
        all_systems: list[System],
        systems: list[System]
    ):

    import matplotlib.pyplot as plt
    import mplcursors

    # Data needs to be separated into a list of x & y values
    all_x = [o.x for o in all_systems]
    all_y = [o.y for o in all_systems]

    course_x = [o.x for o in systems]
    course_y = [o.y for o in systems]

    # Config
    # plt.axis('off')
    plt.style.use('dark_background')

    # Create a scatter plot
    scatter_plot = plt.scatter(all_x, all_y)

    # Configure scatter plot
    # Set axis labels
    # plt.xlabel('X-axis')
    # plt.ylabel('Y-axis')

    # Set plot title
    # plt.title('Recommended Navigation Plot')

    # Show grid
    plt.grid(True)

    # Display course plot
    # Connect coursse of systems with lines
    line_plot = plt.plot(course_x, course_y, 'b--', linewidth=1.5)  # Use blue dashed lines with linewidth of 1.5


    # Tooltips
    # Define tooltips for points and lines
    # Set up mplcursors
    cursor = mplcursors.cursor(hover=True)
    cursor.connect("add", lambda sel: sel.annotation.set_text(f'({sel.target[0]:.2f}, {sel.target[1]:.2f})'))

    scatter_tooltip = mplcursors.cursor(scatter_plot, hover=True)
    # line_tooltip = mplcursors.cursor(line_plot, hover=True)

    # Set tooltip formats
    scatter_tooltip.formatter = '{label}: {x:.2f}, {y:.2f}'.format
    # line_tooltip.formatter = '{label}: {x:.2f}, {y:.2f}'.format

    # Add labels for points
    # for s in filtered_all_systems:
    #     plt.text(s.x, s.y, f'{s.name}', ha='left', va='bottom')
    st.pyplot(plt)

def display_map_maplotlib(
        all_systems: list[System],
):
    fig = map_matplotlib(all_systems)
    fig_html = mpld3.fig_to_html(fig)
    components.html(fig_html, height=600)