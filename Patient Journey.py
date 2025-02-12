import streamlit as st
import plotly.graph_objects as go

# Define the care transition plan data
care_plan = {
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

# App title and header
st.title("Patient Journey Mapping Tool")
st.header("Care Management UI Application")

# Create a sidebar with navigation links
st.sidebar.title("Navigation")
st.sidebar.write("Select a patient:")
patient_list = ["Patient 1", "Patient 2", "Patient 3"]
patient = st.sidebar.selectbox("", patient_list)

# Display the care transition plan for the selected patient
if patient:
    st.header("Care Transition Plan for " + patient)
    care_plan_data = care_plan[patient]
    fig = go.Figure(data=[go.Scatter(
        x=[day["day"] for day in care_plan_data],
        y=[1]*len(care_plan_data),
        mode="markers",
        marker=dict(size=20, color="blue"),
        text=[day["event"] for day in care_plan_data],
        textposition="top center"
    )])
    fig.update_layout(
        title="Care Transition Plan",
        xaxis_title="Day",
        yaxis_title="",
        showlegend=False,
        height=600,
        width=800
    )
    st.plotly_chart(fig)

# Add a footer with contact information
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Contact Us:</p>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Email: <a href='mailto:support@patientjourneymap.com'>support@patientjourneymap.com</a></p>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Phone: 555-555-5555</p>", unsafe_allow_html=True)
