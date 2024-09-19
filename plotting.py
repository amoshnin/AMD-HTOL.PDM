import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import plotly.graph_objects as go

@st.cache_data
def load_data():
    return pd.read_csv('combined_data.csv', index_col='DateTime', parse_dates=True)

df = load_data()

st.title('Socket Data Visualization')

# Sidebar for user input
htr_duty_threshold = st.slider('HTR_DUTY Threshold (%)', 0, 100, 90)

date_format_options = {
    'Year': mdates.YearLocator(),
    'Month': mdates.MonthLocator(),
    'Day': mdates.DayLocator(),
    'Hour': mdates.HourLocator(),
}
selected_date_format = st.selectbox('Select Date Format', list(date_format_options.keys()))


# Plotting
for socket_num in range(8):

    HTR_DUTY_column = f'HTR_DUTY.{socket_num}'
    COOL_DUTY_column = f'COOLDUTY.{socket_num}'

    ES0_TEMP_column = f'ES0_TEMP.{socket_num}'
    SNK_TEMP_column = f'SNK_TEMP.{socket_num}'

    filtered_df = df[df[HTR_DUTY_column] >= htr_duty_threshold]
    filtered_df.loc[:, COOL_DUTY_column] = 100 - filtered_df[COOL_DUTY_column]

    st.subheader(f"Socket {socket_num}")

    min_date = filtered_df.index.min() if not filtered_df.empty else pd.Timestamp.today()
    max_date = filtered_df.index.max() if not filtered_df.empty else pd.Timestamp.today()


    start_date, end_date = st.date_input(
        f"Select Date Range for Socket {socket_num}",
        [min_date, max_date],
    )

    filtered_df = filtered_df[start_date:end_date]

    # Temperature Graph
    fig_temp, ax_temp = plt.subplots(figsize=(10, 5))
    for col in [ES0_TEMP_column, SNK_TEMP_column]:
        filtered_df.plot(y=col, ax=ax_temp, style=".")
    ax_temp.set_ylabel("Temperature (°C)")
    ax_temp.set_title(f"Socket {socket_num} Temperature")

    ax_temp.xaxis.set_major_locator(date_format_options[selected_date_format])
    fig_temp.autofmt_xdate()

    # Enable zooming for the temperature graph
    st.pyplot(fig_temp, use_container_width=True)

    # fig_temp = go.Figure()
    # for col in [ES0_TEMP_column, SNK_TEMP_column]:
    #     fig_temp.add_trace(go.Scatter(x=filtered_df.index, y=filtered_df[col], mode='markers', name=col))

    # fig_temp.update_layout(
    #     title=f"Socket {socket_num} Temperature",
    #     xaxis_title="DateTime",
    #     yaxis_title="Temperature (°C)",
    # )

    # st.plotly_chart(fig_temp, use_container_width=True)

    # Percentage Graph
    fig_pct, ax_pct = plt.subplots(figsize=(10, 5))
    for col in [COOL_DUTY_column, HTR_DUTY_column]:
        filtered_df.plot(y=col, ax=ax_pct, style=".")
    ax_pct.set_ylabel("Percentage (%)")
    ax_pct.set_title(f"Socket {socket_num} Duty Cycle")

    ax_pct.xaxis.set_major_locator(date_format_options[selected_date_format])
    fig_pct.autofmt_xdate()

    # Enable zooming for the percentage graph
    st.pyplot(fig_pct, use_container_width=True)

    # fig_pc = go.Figure()
    # for col in [COOL_DUTY_column, HTR_DUTY_column]:
    #     fig_pc.add_trace(go.Scatter(x=filtered_df.index, y=filtered_df[col], mode='markers', name=col))

    # fig_pc.update_layout(
    #     title=f"Socket {socket_num} Temperature",
    #     xaxis_title="DateTime",
    #     yaxis_title="Temperature (°C)",
    # )

    # st.plotly_chart(fig_pc)