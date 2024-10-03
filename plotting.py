import streamlit as st
import pandas as pd
import plotly.graph_objects as go

@st.cache_data
def load_data():
    return pd.read_csv('combined_data.csv', index_col='DateTime', parse_dates=True)

df = load_data()

st.title('Socket Data Visualization')

# Sidebar for user input
htr_duty_threshold = st.slider('HTR_DUTY Threshold (%)', 0, 100, 90)

# Plotting
for socket_num in range(8):
    HTR_DUTY_column = f'HTR_DUTY.{socket_num}'
    COOL_DUTY_column = f'COOLDUTY.{socket_num}'
    ES0_TEMP_column = f'ES0_TEMP.{socket_num}'
    SNK_TEMP_column = f'SNK_TEMP.{socket_num}'

    @st.cache_data  # Cache filtered DataFrame
    def filter_data(df, threshold, socket_num):
        filtered_df = df[df[f'HTR_DUTY.{socket_num}'] >= threshold]
        filtered_df.loc[:, f'COOLDUTY.{socket_num}'] = 100 - filtered_df[f'COOLDUTY.{socket_num}']
        return filtered_df

    filtered_df = filter_data(df, htr_duty_threshold, socket_num)

    # Temperature Graph
    fig_temp = go.Figure()
    for col in [ES0_TEMP_column, SNK_TEMP_column]:
        fig_temp.add_trace(go.Scatter(x=filtered_df.index, y=filtered_df[col], mode='markers', name=col))

    fig_temp.update_layout(
        title=f"Socket {socket_num} Temperature",
        xaxis_title="DateTime",
        yaxis_title="Temperature (°C)",
    )

    st.plotly_chart(fig_temp, use_container_width=True)

    # Percentage Graph
    fig_pct = go.Figure()
    for col in [COOL_DUTY_column, HTR_DUTY_column]:
        fig_pct.add_trace(go.Scatter(x=filtered_df.index, y=filtered_df[col], mode='markers', name=col))

    fig_pct.update_layout(
        title=f"Socket {socket_num} Duty Cycle",
        xaxis_title="DateTime",
        yaxis_title="Percentage (%)",
    )
    st.plotly_chart(fig_pct, use_container_width=True)