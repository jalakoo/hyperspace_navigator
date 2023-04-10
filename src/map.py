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