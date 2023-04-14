import streamlit as st
from neo4j_driver import execute_query
from utils import list_from_csv
from models import System
from map_matplotlib import map_matplotlib, update_matplotlib

@st.cache_data
def get_system_names():
    # Returns a list of famous system names
    return list_from_csv('https://gist.githubusercontent.com/jalakoo/7d2495dbea7040979dc37b8958666a55/raw', 'name')

# If wanting from database instead
# def get_system_names():
#     query = """
#     MATCH (n:System)
#     RETURN DISTINCT n.name
#     """
#     return execute_query(query)

@st.cache_data
def get_all_systems():
    query = """
    MATCH (n:System)
    WHERE n.name IS NOT NULL AND n.X IS NOT NULL AND n.Y IS NOT NULL AND n.Region IS NOT NULL
    RETURN n
    """
    try:
        records = execute_query(query)
        # Maybe good time to start using that OGM
        result = []
        for r in records:
            s = System(name=r['n'].get('name', None), x=r['n'].get('X', None), y=r['n'].get('Y', None), region=r['n'].get('Region', None))
            # print(f'\n System: {s}')
            result.append(s)
        return result
    except Exception as e:
        print(f'Error: {e}')
        return []

@st.cache_data
def get_hyperspace_systems():
    # Probably more efficient if we add a flag to the systems which would be grabbed in the earlier query
    query = """
    MATCH (n:System)-[:CONNECTED_TO]->(m:System)
    WITH DISTINCT n
    WHERE n.name IS NOT NULL AND n.X IS NOT NULL AND n.Y IS NOT NULL AND n.Region IS NOT NULL
    RETURN n
    """
    try:
        records = execute_query(query)
        # Maybe good time to start using that OGM
        result = []
        for r in records:
            s = System(name=r['n'].get('name', None), x=r['n'].get('X', None), y=r['n'].get('Y', None), region=r['n'].get('Region', None, type='HyperSpace Connected System'))
            # print(f'\n System: {s}')
            result.append(s)
        return result
    except Exception as e:
        print(f'Error: {e}')
        return []

@st.cache_data
def get_course(
    start_system, 
    end_system,
    exclude_systems: list[str] = []
    )->list[System]:
    # Returns a list of System objects

    query = """
        MATCH (start:System {name: $start_system})
        MATCH (end:System {name: $end_system}),
        path = shortestPath((start)-[:CONNECTED_TO|NEAR*1..100]-(end))
        WHERE ALL(y IN nodes(path) WHERE NOT y.name IN $exclude_systems)
        RETURN path
    """

    path = execute_query(query, params={
        'start_system': start_system, 
        'end_system': end_system,
        'exclude_systems': exclude_systems
        })
    try:
        nodes = path[0]['path'].nodes
        result = []
        for node in nodes:
            # print(f'Node: {node}')
            result.append(System(name=node['name'], x=node['X'], y=node['Y'], region=node['Region'], type='Plotted System'))
    except Exception as e:
        print(f'\nError: {e} from query response: {path}')
        result = []
    return result


# UI
st.set_page_config(
    page_title="Star Wars Hyperspace Navigator",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://www.extremelycoolapp.com/help',
        'Report a bug': "https://www.extremelycoolapp.com/bug",
        'About': "# This is a header. This is an *extremely* cool app!"
    }
)

# Convulted way to center image
# col1, col2, col3 = st.columns([2,1,2])
# with col1:
#     st.write('')
# with col2:
#     st.image('./media/benjamin-cottrell-astralanalyzer.png', width=100)
# with col3:
#     st.write('')
# st.title("Hyperspace Navigator")
# st.markdown("<h1 style='text-align: center; color: white;'>Hyperspace Navigator</h1>", unsafe_allow_html=True)

col1, col2 = st.columns([4,1])
with col1:
    st.title("Hyperspace Navigator")
with col2:
    st.image('./media/benjamin-cottrell-astralanalyzer.png', width=80)

systems = get_system_names()
course = []

# System Search
c1, c2, c3, c4 = st.columns([1,1,3,1])
with c1:
    # Coruscant is the default
    start_system = st.selectbox("Start System", systems, index=377)
with c2:
    # Alderaan is the default
    end_system = st.selectbox("End System", systems, index=36)
with c3:
    # Cheap spacer
    st.markdown("")
    st.markdown("")
    with st.expander("Advanced Options"):
        # include = st.multiselect("Intermediary Stops", [x for x in systems if x != start_system])
        exclude = st.multiselect("Avoid", [x for x in systems if x != start_system])

with c4:
    # Cheap spacer
    st.markdown("")
    st.markdown("")
    if st.button('Plot course'):
        # st.write(f'Plotting course from {start_system} to {end_system}...')

        # Check to see if course already ran
        if st.session_state.get(f'{start_system}_{end_system}_{exclude}'):
            print(f'Course already plotted from {start_system} to {end_system}. Retrieving from session state.')
            course = st.session_state[f'{start_system}_{end_system}_{exclude}']
        else:
            course = get_course(start_system, end_system, exclude)
            st.session_state[f'{start_system}_{end_system}_{exclude}'] = course
        if len(course) == 0:
            st.error(f'No course found from {start_system} to {end_system}.')


# Pull down all systems
if st.session_state.get('all_systems') is None:
    all = get_all_systems()
    if all is None or len(all) == 0:
        st.error('No systems found. Please check your Neo4j database.')
        st.stop()
    hyperspace = get_hyperspace_systems()

#  Display master galaxy map
fig, ax = map_matplotlib(all)

# Update map
if len(course) > 0:
    update_matplotlib(fig, ax, course)

st.pyplot(fig)

# Plotted course
if len(course) > 0:
    st.write(f'Recommended Course:')
    st.write(course)