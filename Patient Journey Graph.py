import networkx as nx
import matplotlib.pyplot as plt
import streamlit as st
import json
import os

# Function to load care plan data from JSON file
def load_care_plan():
    if os.path.exists('care_plan.json'):
        with open('care_plan.json', 'r') as f:
            return json.load(f)
    else:
        return {
            "Patient 1": [
                {"day": 1, "event": "Admission to hospital"},
                {"day": 3, "event": "Surgery"},
                {"day": 5, "event": "Rehabilitation starts"},
                {"day": 7, "event": "Discharge from hospital"},
                {"day": 10, "event": "Follow-up appointment"}
            ],
            "Patient 2": [
                {"day": 1, "event": "Admission to hospital"},
                {"day": 2, "event": "Diagnostic tests"},
                {"day": 4, "event": "Treatment starts"},
                {"day": 6, "event": "Discharge from hospital"},
                {"day": 9, "event": "Follow-up appointment"}
            ],
            "Patient 3": [
                {"day": 1, "event": "Admission to hospital"},
                {"day": 2, "event": "Surgery"},
                {"day": 4, "event": "Rehabilitation starts"},
                {"day": 6, "event": "Discharge from hospital"},
                {"day": 10, "event": "Follow-up appointment"}
            ]
        }

# Load the care plan data
care_plan = load_care_plan()

# App title and header
st.title("Patient Journey Mapping Tool")
st.header("Care Management UI Application")

# Sidebar for patient selection
st.sidebar.title("Navigation")
st.sidebar.write("Select a patient:")
patient_list = ["Patient 1", "Patient 2", "Patient 3"]
patient = st.sidebar.selectbox("", patient_list)

# Initialize session state if not already present
if "updated_care_plan" not in st.session_state:
    st.session_state.updated_care_plan = {key: value.copy() for key, value in care_plan.items()}

# Display the care transition plan for the selected patient
if patient:
    st.header(f"Care Transition Plan for {patient}")
    
    # Show the care plan data and allow editing
    updated_care_plan = []
    for i, data in enumerate(st.session_state.updated_care_plan[patient]):
        day = data["day"]
        event = data["event"]
        new_event = st.sidebar.text_input(f"Edit Event for Day {day}:", value=event)
        updated_care_plan.append({"day": day, "event": new_event})

    # Check if the care plan has been updated and update the session state
    if updated_care_plan != st.session_state.updated_care_plan[patient]:
        st.session_state.updated_care_plan[patient] = updated_care_plan

        # Save the updated care plan back to a file
        with open('care_plan.json', 'w') as f:
            json.dump(st.session_state.updated_care_plan, f, indent=4)

    # Create a directed graph
    G = nx.DiGraph()

    # Add nodes for days (Level 1) and events (Level 2)
    pos = {}
    day_nodes = []  # To store only the day nodes for dotted lines
    event_nodes = []  # Store event nodes separately

    # Add nodes and edges to the graph
    for i, data in enumerate(updated_care_plan):
        day_node = f"Day {data['day']}"
        event_node = data["event"]
        
        # Add nodes for days and events
        G.add_node(day_node, level=1)  # Level 1: Days
        G.add_node(event_node, level=2)  # Level 2: Events
        
        # Add edges between days and events
        G.add_edge(day_node, event_node)
        
        # Position the nodes
        pos[day_node] = (i * 3, 1)  # Days on top (y=1)
        pos[event_node] = (i * 3, 0)  # Events below (y=0)
        
        day_nodes.append(day_node)  # Append the day node
        event_nodes.append(event_node)  # Append the event node

    # Draw the graph
    plt.figure(figsize=(16, 6))  # Wider figure for better spacing
    
    # Draw day nodes with circles
    nx.draw_networkx_nodes(G, pos, nodelist=day_nodes, node_color="lightblue", node_size=4000)
    nx.draw_networkx_labels(G, pos, labels={node: node for node in day_nodes}, font_size=14, font_color="black")
    
    # Draw dotted edges between consecutive day nodes
    dotted_edges = [(day_nodes[i], day_nodes[i + 1]) for i in range(len(day_nodes) - 1)]
    nx.draw_networkx_edges(
        G, pos, edgelist=dotted_edges, style="dotted", edge_color="gray", width=1.5
    )

    # Draw solid edges between day nodes and event labels
    nx.draw_networkx_edges(
        G, pos, edgelist=G.edges(), edge_color="gray", width=1.5
    )
    
    # Add event node labels (without circles)
    nx.draw_networkx_labels(
        G, pos, labels={node: node for node in event_nodes}, font_size=14, font_color="black"
    )

    # Add vertical lines from the top of the first and last day node
    first_day_pos = pos[day_nodes[0]]
    plt.plot([first_day_pos[0], first_day_pos[0]], [first_day_pos[1] + 0.2, 1.5], linestyle='-', color='blue', linewidth=2)

    last_day_pos = pos[day_nodes[-1]]
    plt.plot([last_day_pos[0], last_day_pos[0]], [last_day_pos[1] + 0.2, 1.5], linestyle='-', color='blue', linewidth=2)

    # Title placement
    mid_x = (first_day_pos[0] + last_day_pos[0]) / 2
    title_y = 1.5  # Adjust y-position for the title (above the vertical lines)
    plt.text(mid_x, title_y, 'Pre-Procedure Prep', fontsize=18, fontweight='bold', ha='center')

    # Add horizontal lines from the title to the vertical lines
    # Left horizontal line
    plt.plot([first_day_pos[0] , first_day_pos[0]+3.5], [title_y, title_y], linestyle='-', color='blue', linewidth=2)
    # Right horizontal line
    plt.plot([last_day_pos[0]-3.5, last_day_pos[0] ], [title_y, title_y], linestyle='-', color='blue', linewidth=2)

    # Remove axis and border
    plt.axis('off')

    # Adjust layout for no overlap
    plt.tight_layout()  # Ensure nothing is cut off

    # Show the graph in Streamlit
    st.pyplot(plt)
