import streamlit as st
from neo4j_driver import execute_query
from utils import list_from_csv
from models import System
from map_matplotlib import map_matplotlib, update_matplotlib, update_markers

# @st.cache_data
# def get_system_names():
#     # Returns a list of famous system names
#     return list_from_csv('https://gist.githubusercontent.com/jalakoo/7d2495dbea7040979dc37b8958666a55/raw', 'name')

# If wanting from database instead from a csv list
# @st.cache_data
# def get_system_names():
#     query = """
#     MATCH (n:System)
#     WHERE n.importance IS NOT NULL
#     RETURN DISTINCT n
#     """
#     response = execute_query(query)
#     print(f'response: {response}')
#     result = [r['n'].get('name') for r in response]
#     return result


@st.cache_data
def get_important_systems(systems):
    sort = sorted(systems, key=lambda system: system.importance, reverse=True)
    return sort

@st.cache_data
def get_important_system_names(systems):
    # Returns a list of famous system names
    sort = get_important_system_names(systems)
    return [s.name for s in sort]

@st.cache_data
def get_all_system_names(systems):
    return [s.name for s in systems]

@st.cache_data(ttl="60")
def get_all_systems():
    query = """
    MATCH (n:Planet)
    OPTIONAL MATCH (n)-[:HAS_AFFILIATION]-(m:Affiliation)
    WHERE n.name IS NOT NULL AND n.X IS NOT NULL AND n.Y IS NOT NULL
    RETURN n.name as name, n.X as X, n.Y as Y, n.Region as Region, n.type as type, n.pagerank as pagerank, m.name as affiliation
    """
    try:
        records = execute_query(query)
        # Maybe good time to start using that OGM
        result = []
        for r in records:
            name = r.get('name', None)
            x = r.get('X', None)
            y = r.get('Y', None)
            region = r.get('Region', None)
            type = r.get('type', None)
            affiliation = r.get('affiliation', "Neutral")
            if affiliation is None or affiliation == "None":
                affiliation = "Neutral"
            importance = r.get('pagerank', 0.0)
            if x == None or y == None:
                # Invalid coordinate data, skip this record
                continue
            s = System(
                name=name, 
                x=x, 
                y=y, 
                region=region, 
                type=type, 
                affiliation=affiliation,
                importance=importance)
            result.append(s)
        print(f'{len(result)} Planets found')
        return result
    except Exception as e:
        print(f'Error: {e}')
        return []

# @st.cache_data
# def get_hyperspace_systems():
#     # Probably more efficient if we add a flag to the systems which would be grabbed in the earlier query
#     query = """
#     MATCH (n:System)-[:CONNECTED_TO|NEAR]-(m:System)
#     WITH DISTINCT n
#     WHERE n.name IS NOT NULL AND n.X IS NOT NULL AND n.Y IS NOT NULL AND n.Region IS NOT NULL
#     RETURN n
#     """
#     try:
#         records = execute_query(query)
#         # Maybe good time to start using that OGM
#         result = []
#         for r in records:
#             s = System(name=r['n'].get('name', None), x=r['n'].get('X', None), y=r['n'].get('Y', None), region=r['n'].get('Region', None, type='HyperSpace Connected System', importance=r['n'].get('importance', 0.0)))
#             result.append(s)
#         return result
#     except Exception as e:
#         print(f'Error: {e}')
#         return []

# @st.cache_data
def get_course(
    start_system, 
    end_system,
    max_jumps: int = 100,
    include_systems: list[str] = [],
    exclude_systems: list[str] = []
    )->list[System]:
    # Returns a list of System objects

    # TODO: Support intermediate include_systems
    
    query = f"""
        MATCH (start:Planet {{name: $start_system}})
        MATCH (end:Planet {{name: $end_system}}),
        path = shortestPath((start)-[:NEXT_TO|NEAR*0..{max_jumps}]-(end))
        WHERE ALL(y IN nodes(path) WHERE NOT y.name IN $exclude_systems)
        RETURN path
    """
#     query = f"""
# MATCH (n:System)
# WHERE n.name IN $include_systems
# WITH collect(n) as nodes
# UNWIND nodes as n
# UNWIND nodes as m
# WITH * WHERE n.name < m.name
# MATCH path = shortestPath( (n)-[:CONNECTED_TO|NEAR*..{max_jumps}]-(m) )
# WHERE ALL(x IN nodes(path) WHERE NOT x.name IN $exclude_systems)
# RETURN path
#     """
    # include_systems.insert(0, end_system)
    # include_systems.append(start_system)
    # print(f'included systems: {include_systems}')
    path = execute_query(query, params={
        'start_system': start_system, 
        'end_system': end_system,
        'include_systems': include_systems,
        'exclude_systems': exclude_systems
        })
    try:
        nodes = path[0]['path'].nodes
        result = []
        for node in nodes:
            # print(f'Node: {node}')
            result.append(System(name=node['name'], x=node['X'], y=node['Y'], region=node['Region'], type='Plotted System', importance=node.get('pagerank', 0.0)))
    except Exception as e:
        print(f'\nError: {e} from query response: {path}')
        result = []
    return result

def index_for_system(
        systems: list[str], 
        system_name: str
    ):
    try:
        for i, s in enumerate(systems):
            if s == system_name:
                return i
        return None
    except Exception as e:
        print(f'Problem finding system named: {system_name} in list: {systems}. Error: {e}')
        return ["<Problem extracting names>"]

# UI
st.set_page_config(
    page_title="Star Wars Hyperspace Navigator",
    layout="wide",
    initial_sidebar_state="expanded",
    # menu_items={
    #     'Get Help': 'https://www.extremelycoolapp.com/help',
    #     'Report a bug': "https://www.extremelycoolapp.com/bug",
    #     'About': "# This is a header. This is an *extremely* cool app!"
    # }
)

# HEADER
col1, col2 = st.columns([4,1])
with col1:
    st.title("Hyperspace Navigator")
with col2:
    st.image('./media/benjamin-cottrell-astralanalyzer.png', width=80)

# Pull down all systems
if st.session_state.get('all_systems') is None:
    all = get_all_systems()
    if all is None or len(all) == 0:
        st.error('No systems found. Please check your Neo4j database.')
        st.stop()
    ranked_systems = get_important_systems(all)
    ranked_systems = list(set(ranked_systems)) #dedup
    # system_names = get_important_system_names(all)
    all_system_names = get_all_system_names(all)
course = []

# SEARCH
c1, c2, c3, c4 = st.columns([1,1,3,1])
with c1:
    # Coruscant is the default
    start_index = index_for_system(all_system_names, 'Tatooine') 
    start_system = st.selectbox("Start System", all_system_names, index=start_index)
with c2:
    # Alderaan is the default
    end_index = index_for_system(all_system_names, 'Alderaan')
    end_system = st.selectbox("End System", all_system_names, index=end_index)
with c3:
    # Cheap spacer
    st.markdown("")
    st.markdown("")
    with st.expander("Advanced Options"):
        max_jumps = st.slider("Max Jumps", 1, 200, 100)
        include = []
        # include = st.multiselect("Intermediary Systems", [x for x in all_system_names if x != start_system and x != end_system])
        exclude = st.multiselect("Systems to Avoid", [x for x in all_system_names if x != start_system and x != end_system])

with c4:
    # Cheap spacer
    st.markdown("")
    st.markdown("")
    if st.button('Plot course'):
        # Check to see if course already cached
        state_id = f'{start_system}_{end_system}_{max_jumps}_{include}_{exclude}'
        if st.session_state.get(state_id):
            print(f'Course already plotted from {start_system} to {end_system}. Retrieving from session state.')
            course = st.session_state[state_id]
        else:
            course = get_course(start_system, end_system, max_jumps, include, exclude)
            st.session_state[state_id] = course
        if len(course) == 0:
            st.error(f'No course found from {start_system} to {end_system}.')

#  Display master galaxy map
fig, ax = map_matplotlib(all)

# Update map
if len(course) > 0:
    update_matplotlib(fig, ax, course)

# Update markers selected
s_index = index_for_system(all_system_names, start_system)
e_index = index_for_system(all_system_names, end_system)
selected_systems = [get_all_systems()[s_index], get_all_systems()[e_index]]
update_markers(ax,selected_systems)

st.pyplot(fig)

o1, o2, o3 = st.columns(3)
with o1:
    # Cheap spacer
    st.markdown("")
    st.markdown("")
    with st.expander("Most Important Planets"):
        top_10_systems = ranked_systems[:10]
        # print(f'top_10 systems: {top_10_systems}')
        top_10_str = [f"{s.name} : {s.affiliation}" for s in top_10_systems]
        st.write(top_10_str)
with o2:
    # Cheap spacer
    st.markdown("")
    st.markdown("")
    with st.expander("Most Important Rebel Planets"):
        top_rebel = [s for s in ranked_systems if s.affiliation == "Light Side"]
        top_10_rebels = top_rebel[:10]
        # print(f'top_10 rebel: {top_10_rebels}')
        top_10_rebel_str = [f"{s.name} : {s.affiliation}" for s in top_10_rebels]
        st.write(top_10_rebel_str)
with o3:
    # Cheap spacer
    st.markdown("")
    st.markdown("")
    with st.expander("Most Important Imperial Planets"):
        top_imp = [s for s in ranked_systems if s.affiliation == "Dark Side"]
        top_10_imp = top_imp[:10]
        # print(f'top_10 imp systems: {top_10_imp}')
        top_10_imp_str = [f"{s.name} : {s.affiliation}" for s in top_10_imp]
        st.write(top_10_imp_str)


# Plotted course
if len(course) > 0:
    st.write(f'Plotted Jumps: {len(course)-1}')
    st.write(f'Recommended Course:')
    cleaned_course = [{"System": x.name, "Coordinates": f'{x.x}, {x.y}',"Region": x.region} for x in course]
    st.table(cleaned_course)