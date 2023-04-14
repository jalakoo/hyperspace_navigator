# Various mapping options experimented with here
# TODO: Refactor into separate files

import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import networkx as nx
from pyvis.network import Network
from models import System

# Using dataframes and scatter plot
# def display_scatter_map(objects: list[dict]):
#     import pandas as pd
#     import numpy as np
#     import hvplot.pandas  # required for hvplot

#     data = pd.DataFrame(objects)

# TODO: Show just recommended route, don't show hyperspace lanes

def display_map_plotly(
        all_systems: list[System],
        systems: list[System]):
    
    # TODO: Uptimize this to only update the course lines

    import plotly.express as px

    # Filter out anything without coordinates - should have
    # been filtered out before this point
    filtered_all_systems = [o for o in all_systems if o.x is not None and o.y is not None]
    filtered_course_systems = [o for o in systems if o.x is not None and o.y is not None]

    # Data needs to be separated into a list of x & y values
    # all_df = pd.DataFrame([{
    #     'name': s.name,
    #     'x': s.x,
    #     'y': s.y,
    #     'region': s.region,
    #     'color': 'black'
    # } for s in filtered_all_systems])

    # hyperspace_df = pd.DataFrame([{
    #     'name': s.name,
    #     'x': s.x,
    #     'y': s.y,
    #     'region': s.region,
    #     'color': 'grey'
    # } for s in hyperspace_systems])

    # course_df = pd.DataFrame([{
    #     'name': s.name,
    #     'x': s.x,
    #     'y': s.y,
    #     'region': s.region,
    #     'color': 'green'
    # } for s in filtered_course_systems])

    # all_x = [o.x for o in filtered_all_systems]
    # all_y = [o.y for o in filtered_all_systems]
    # hyperspace_x = [o.x for o in hyperspace_systems]
    # hyperspace_y = [o.y for o in hyperspace_systems]
    # course_x = [o.x for o in systems]
    # course_y = [o.y for o in systems]


    try:
        fig = px.scatter(filtered_all_systems,
                    x='x',   # specify x-column from dictionary data
                    y='y',   # specify y-column from dictionary data
                    title='Scatter Plot with Negative Coordinates',
                    #  labels={'x': 'X-axis Label', 'y': 'Y-axis Label'},
                    hover_name='name',  # specify column for hover information
                    hover_data=['region'],  # specify columns for hover information
                    color='type'
                    )
        # fig = px.scatter(
        #     data_frame = all_df,
        #     title='Scatter Plot with Negative Coordinates',
        #     #  labels={'x': 'X-axis Label', 'y': 'Y-axis Label'},
        #     hover_name='name',  # specify column for hover information
        #     hover_data=['x','y','region'],  # specify columns for hover information
        #     )
    except Exception as e:
        print(f'Error: {e}. \n\nAll systems: {len(all_systems)}, \n\n plotted systems: {len(systems)}')
        st.stop()
    
    # Set equal aspect ratio and autosize properties
    fig.update_layout(
        height = 800,
        yaxis_scaleanchor="x",
        dragmode='pan',
    )

    # Show hyperspace lanes
    # fig.add_trace(
    #     px.line(hyperspace_systems, title='Hyperspace', x='x', y='y').data[0]
    # )

    # Show course plots
    fig.add_trace(
        px.line(
        filtered_course_systems,
        x='x',
        y='y',
        title='Course').data[0]
    )

    fig.update_traces(marker=dict(size=12,
                              line=dict(width=2,
                                        color='DarkSlateGrey')),
                  selector=dict(mode='markers'))


    # Show the plot
    st.plotly_chart(fig)

def display_map_matplotlib(
        all_systems: list[System],
        systems: list[System]
    ):
    import matplotlib.pyplot as plt
    import mplcursors

    # # Generate some data
    # x = [-3, -1, 2, 4, 0, -2]
    # y = [2, -1, 3, -4, 0, -2]
    print(f'systsems: {systems}')

    # Dump any course options with missing data
    # Shouldn't happen in final dataset
    filtered_all_systems = [o for o in all_systems if o.x is not None and o.y is not None]
    filtered_course_systems = [o for o in systems if o.x is not None and o.y is not None]

    # Data needs to be separated into a list of x & y values
    all_x = [o.x for o in filtered_all_systems]
    all_y = [o.y for o in filtered_all_systems]

    course_x = [o.x for o in systems]
    course_y = [o.y for o in systems]

    # Config
    # plt.axis('off')
    plt.style.use('dark_background')

    # Create a scatter plot
    scatter_plot = plt.scatter(all_x, all_y)

    # Set axis labels
    # plt.xlabel('X-axis')
    # plt.ylabel('Y-axis')

    # Set plot title
    # plt.title('Recommended Navigation Plot')

    # Show grid
    plt.grid(True)

    # Connect coursse of systems with lines
    # connect_indices = [1, 3, 4]  # Indices of the points to connect
    # x_connect = [x[i] for i in connect_indices]
    # y_connect = [y[i] for i in connect_indices]
    line_plot, = plt.plot(course_x, course_y, 'b--', linewidth=1.5)  # Use blue dashed lines with linewidth of 1.5


    # Tooltips
    # Define tooltips for points and lines
    scatter_tooltip = mplcursors.cursor(scatter_plot, hover=True)
    # line_tooltip = mplcursors.cursor(line_plot, hover=True)

    # Set tooltip formats
    scatter_tooltip.formatter = '{label}: {x:.2f}, {y:.2f}'.format
    # line_tooltip.formatter = '{label}: {x:.2f}, {y:.2f}'.format

    # Add labels for points
    # for s in filtered_all_systems:
    #     plt.text(s.x, s.y, f'{s.name}', ha='left', va='bottom')

    st.pyplot(plt)



# Using PyVis
def display_map(objects: list[System]):

    graph = nx.Graph()

    for idx, obj in enumerate(objects):
        if idx == 0:
            # Start node
            graph.add_node(obj.name, x=obj.x, y=obj.y, region=obj.region, color='green')
        elif idx > 0 and idx < len(objects)-1:
            # Intermediate nodes
            graph.add_node(obj.name, x=obj.x, y=obj.y, region=obj.region)
            graph.add_edge(objects[idx-1].name, obj.name)
        elif idx == len(objects)-1:
            # End node
            graph.add_node(obj.name, x=obj.x, y=obj.y, region=obj.region, color='red')
            graph.add_edge(objects[idx-1].name, obj.name)

    # Initiate PyVis network object
    galaxy_net = Network(
                       height='600px',
                       width='100%',
                       bgcolor='#222222',
                       font_color='white',
                       directed=True
                      )

    # Take Networkx graph and translate it to a PyVis graph format
    galaxy_net.from_nx(graph)

    # Generate network with specific layout settings
    galaxy_net.repulsion(
                        node_distance=420,
                        central_gravity=0.33,
                        spring_length=110,
                        spring_strength=0.10,
                        damping=0.95
                       )

    try:
        path = './tmp'
        galaxy_net.save_graph(f'{path}/pyvis_graph.html')
        HtmlFile = open(f'{path}/pyvis_graph.html','r',encoding='utf-8')
        components.html(HtmlFile.read(), height=600)
    except Exception as e:
        print(f'Error: {e}')
        return None