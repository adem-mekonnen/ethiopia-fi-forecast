import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os

# --- Page Config ---
st.set_page_config(page_title="Ethiopia FI Forecast 2027", layout="wide")

# --- Data Loading Helper ---
@st.cache_data
def load_data():
    # Use the processed data from previous tasks
    data_path = 'data/processed/ethiopia_fi_enriched.csv'
    forecast_path = 'data/processed/final_forecasts_2027.csv'
    matrix_path = 'data/processed/event_indicator_matrix.csv'
    
    # Check if files exist
    if not all(os.path.exists(p) for p in [data_path, forecast_path, matrix_path]):
        return None, None, None

    # 1. Load the main enriched dataset
    df = pd.read_csv(data_path)
    
    # CRITICAL FIX: Generate 'year' column from 'observation_date'
    if 'year' not in df.columns:
        df['observation_date'] = pd.to_datetime(df['observation_date'], errors='coerce')
        df['year'] = df['observation_date'].dt.year
    
    # Data Cleaning: remove rows with missing core data
    df = df.dropna(subset=['year', 'value_numeric'])
    df['year'] = df['year'].astype(int)

    # 2. Load the Forecast dataset (from Task 4)
    df_forecast = pd.read_csv(forecast_path)

    # 3. Load the Association Matrix (from Task 3)
    df_matrix = pd.read_csv(matrix_path, index_col=0)
    
    return df, df_forecast, df_matrix

# Execute Data Loading
df, df_forecast, df_matrix = load_data()

# Handle missing files error
if df is None:
    st.error("⚠️ Missing data files in 'data/processed/'.")
    st.info("Please run your Task 1, 3, and 4 scripts in the terminal first to generate the necessary CSV files.")
    st.stop()

# --- Sidebar Navigation ---
st.sidebar.title("Navigation")
st.sidebar.image("https://img.icons8.com/color/96/ethiopia.png", width=100)
page = st.sidebar.radio("Go to", ["Overview", "Historical Trends", "Event Impacts", "2027 Projections"])

# --- Page 1: Overview ---
if page == "Overview":
    st.title("🇪🇹 Ethiopia Financial Inclusion Overview")
    
    # Calculation of latest metrics
    try:
        latest_acc = df[(df['indicator_code'] == 'ACC_OWNERSHIP') & (df['year'] == 2024)]['value_numeric'].iloc[-1]
        latest_usg = df[(df['indicator_code'] == 'ACC_MM_ACCOUNT') & (df['year'] == 2024)]['value_numeric'].iloc[-1]
    except IndexError:
        latest_acc, latest_usg = 0, 0

    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Account Ownership (2024)", f"{latest_acc}%", "+3pp vs 2021")
    with col2:
        st.metric("Mobile Money Adoption (2024)", f"{latest_usg}%", "Leading Growth")
    with col3:
        # P2P/ATM Crossover Indicator
        crossover_data = df[df['indicator_code'] == 'USG_CROSSOVER']
        crossover_val = crossover_data['value_numeric'].max() if not crossover_data.empty else "N/A"
        st.metric("P2P/ATM Ratio", f"{crossover_val}x", "Crossover Achieved")

    st.divider()
    
    st.subheader("Executive Summary")
    st.write("""
    The Ethiopian financial landscape is undergoing a non-linear transformation. 
    While the **Usage** of digital payments (P2P transfers) has exploded following the launch of Telebirr and M-Pesa, 
    **Access** (formal account ownership) remains stuck near 49%. 
    
    **The Goal:** Reach **60% Financial Inclusion** by the end of 2027 through the 
    National Financial Inclusion Strategy (NFIS-II) and the Fayda Digital ID rollout.
    """)

# --- Page 2: Historical Trends ---
elif page == "Historical Trends":
    st.title("📈 Historical Inclusion Trends")
    
    # Filter for observations only
    obs_only = df[df['record_type'] == 'observation']
    
    available_indicators = sorted(obs_only['indicator_code'].unique())
    selected_indicators = st.multiselect("Select Indicators to View", 
                                        options=available_indicators, 
                                        default=['ACC_OWNERSHIP', 'ACC_MM_ACCOUNT'])
    
    if selected_indicators:
        mask = obs_only[obs_only['indicator_code'].isin(selected_indicators)]
        fig = px.line(mask, x="year", y="value_numeric", color="indicator_code",
                      markers=True, title="Historical Trajectory (2011-2024)",
                      labels={"value_numeric": "Percentage (%)", "year": "Year"})
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("Please select at least one indicator.")

# --- Page 3: Event Impacts ---
elif page == "Event Impacts":
    st.title("⚡ Event Impact Analysis")
    st.write("This matrix quantifies the expected 'shock' or magnitude each event has on various indicators.")
    
    # Matrix Heatmap
    fig_heat = px.imshow(df_matrix, 
                         labels=dict(x="Indicator", y="Event", color="Impact Magnitude"),
                         x=df_matrix.columns,
                         y=df_matrix.index,
                         color_continuous_scale='YlGnBu',
                         text_auto=True)
    st.plotly_chart(fig_heat, use_container_width=True)
    
    st.divider()
    
    st.subheader("Key National Milestones")
    events = df[df['record_type'] == 'event'].sort_values('year', ascending=False)
    st.dataframe(events[['year', 'indicator', 'category', 'notes']], use_container_width=True, hide_index=True)

# --- Page 4: 2027 Projections ---
elif page == "2027 Projections":
    st.title("🚀 2027 Inclusion Roadmap")
    
    col_a, col_b = st.columns([1, 3])
    
    with col_a:
        scenario = st.radio("Select Forecast Scenario", ["Base", "Optimistic", "Pessimistic"])
        st.info(f"The **{scenario}** scenario assumes different levels of success for the Fayda ID rollout and M-Pesa adoption.")

    # Filtering forecast data
    sub_forecast = df_forecast[df_forecast['Scenario'] == scenario]
    
    # Target Gauge
    target_goal = 60.0
    val_2027 = sub_forecast[sub_forecast['Year'] == 2027]['Access_Rate'].values[0]
    
    with col_b:
        fig_gauge = go.Figure(go.Indicator(
            mode = "gauge+number+delta",
            value = val_2027,
            domain = {'x': [0, 1], 'y': [0, 1]},
            title = {'text': f"Projected 2027 Account Ownership ({scenario})"},
            delta = {'reference': target_goal},
            gauge = {'axis': {'range': [None, 100]},
                     'bar': {'color': "#006837"},
                     'steps' : [
                         {'range': [0, 49], 'color': "#eeeeee"},
                         {'range': [49, 60], 'color': "#bbbbbb"}],
                     'threshold' : {'line': {'color': "red", 'width': 4}, 'thickness': 0.75, 'value': target_goal}}))
        st.plotly_chart(fig_gauge, use_container_width=True)

    st.divider()
    
    # Multi-scenario Comparison
    st.subheader("Scenario Comparison: Access Rate (%)")
    fig_multi = px.line(df_forecast, x="Year", y="Access_Rate", color="Scenario",
                       title="Forecast Paths to 2027", markers=True,
                       line_dash="Scenario", color_discrete_map={"Optimistic": "green", "Base": "blue", "Pessimistic": "red"})
    st.plotly_chart(fig_multi, use_container_width=True)

    st.download_button("📩 Download Forecast Results (CSV)", 
                       df_forecast.to_csv(index=False), 
                       "ethiopia_fi_projections_2027.csv", "text/csv")

# --- Footer ---
st.sidebar.markdown("---")
st.sidebar.caption("📊 Developed for the Financial Inclusion Consortium by Selam Analytics.")