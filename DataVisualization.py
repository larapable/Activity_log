import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Data Visualization", page_icon=":bar_chart:", layout="wide")
st.markdown('<style>div.block-container{padding-top:10px;}<style>', unsafe_allow_html=True)
st.title("AI Global Index")

df = pd.read_csv(r"C:\Users\Lara\Documents\Data Analytics 1\DATASET\Group1_Pogo_ConsolidatedFile.csv")

# Define a column layout container (col1)
col1 = st.container()

with col1:
    st.markdown(
        """
        <div style="display: flex;">
        </div>
        """,
        unsafe_allow_html=True,
    )
    title = "Number of countries by region, cluster, and income group"
    st.markdown(f"<h2 style='font-size: 24px;'>{title}</h2>", unsafe_allow_html=True)

    # Group and count the data
    group_data = df.groupby(['Value', 'Category']).size().reset_index(name='Count')

    # Sort the data by count within each value group
    group_data['Rank'] = group_data.groupby('Value')['Count'].rank(ascending=False, method='first')

    # Filter to keep only the top 5 categories for each value
    top5_data = group_data[group_data['Rank'] <= 3]

    # Create the Sunburst chart
    fig = px.sunburst(
        top5_data,
        values='Count',
        path=['Value', 'Category'],
        color="Value",
        height=600,
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    st.plotly_chart(fig, use_container_width=True)


import streamlit as st
import plotly.graph_objects as go

# Add a separator or text between the charts
st.markdown("---")
st.markdown("<h3>Gauge Chart</h3>", unsafe_allow_html=True)

# Define a color palette for members
color_palette = {
    'Mier': 'orange',
    'Pable': 'green',
    'Selma': 'blue',
}


# Get unique members in the dataset
members = df['Member'].unique()

# Create a single row layout for the gauge charts
columns = st.columns(len(members))

for i, selected_member in enumerate(members):
    # Filter the data for the selected member and "Entertainment and Leisure" category
    filtered_data = df[(df['Member'] == selected_member) & (df['Category'] == "Entertainment and Leisure")]

    # Calculate the average duration for the selected member
    average_duration = filtered_data['Duration'].mean()

    # Set the bar color based on the member's name
    member_color = color_palette.get(selected_member, 'gray')  # Use 'gray' if member color is not defined

    # Create a gauge chart for the member in the corresponding column
    with columns[i]:
        st.subheader(f"{selected_member}'s Entertainment and Leisure Duration")
        st.write(f"Average Entertainment and Leisure Duration: {average_duration:.2f} hours")
        
        # Adjust chart width and add margin
        chart_width = 350  # Adjust the width as needed
        chart_height = 350  # Adjust the height as needed
        
        def create_gauge_chart(duration, max_duration, title, units, bar_color='darkblue'):
            fig = go.Figure(go.Indicator(
                mode="gauge+number",
                value=duration,
                title={"text": title},
                gauge={
                    "axis": {"range": [0, max_duration]},
                    "bar": {"color": bar_color},
                    "threshold": {
                        "line": {"color": "red", "width": 4},
                        "thickness": 0.75,
                        "value": max_duration/2
                    },
                       "bgcolor": "#59788E"  # Color of the unfilled background
                }
            ))
            # Set the size of the entire figure using layout
            fig.update_layout(width=chart_width, height=chart_height)
            fig.update_traces(number={'suffix': units, 'font': {'size': 24, 'color': 'white'}})
            st.plotly_chart(fig, use_container_width=False, key=f"gauge-{i}")
        
        create_gauge_chart(average_duration, 24, "Entertainment and Leisure", "hours", bar_color=member_color)
