import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import os

# Set page config
st.set_page_config(page_title="Beijing Air Quality Analysis", layout="wide", page_icon="🌬️")

# Custom CSS to enhance the look
st.markdown("""
<style>
.big-font {
    font-size:20px !important;
    font-weight: bold;
}
.medium-font {
    font-size:16px !important;
}
.small-font {
    font-size:14px !important;
}
.conclusion {
    background-color: #f0f2f6;
    padding: 20px;
    border-radius: 10px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}
</style>
""", unsafe_allow_html=True)

# Load data
base_dir = os.path.dirname(os.path.abspath(__file__))
@st.cache_data
def load_data():
    data = pd.read_csv(os.path.join(base_dir, 'main_data.csv'))
    data['datetime'] = pd.to_datetime('2013-03-01') + pd.to_timedelta(data['No'] - 1, unit='H')
    return data

data = load_data()

# Sidebar
st.sidebar.image(os.path.join(base_dir, 'air-quality.jpg'), use_column_width=True)
st.sidebar.title("Navigation")
page = st.sidebar.radio("", ["🏠 Home", "📊 Pollutant Analysis", "🌡️ Weather Impact", "📈 Long-term Trends"])

# Main content
if page == "🏠 Home":
    st.title("🌆 Beijing Air Quality Analysis")
    st.markdown("<p class='big-font'>Explore the air quality data of Beijing through interactive visualizations and in-depth analysis.</p>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Records", f"{len(data):,}")
    with col2:
        st.metric("Date Range", f"{data['datetime'].min().date()} to {data['datetime'].max().date()}")
    with col3:
        st.metric("Monitoring Stations", data['station'].nunique())
    
    st.markdown("---")
    st.markdown("<p class='medium-font'>This dashboard provides insights into:</p>", unsafe_allow_html=True)
    st.markdown("- 📊 Pollutant concentrations across monitoring sites")
    st.markdown("- 🌡️ Impact of weather conditions on air quality")
    st.markdown("- 📈 Long-term trends in air quality")
    
    st.markdown("---")
    st.markdown("<p class='small-font'>Use the sidebar to navigate between different analyses.</p>", unsafe_allow_html=True)

elif page == "📊 Pollutant Analysis":
    st.title("📊 Pollutant Concentration Analysis")
    
    pollutants = ['PM2.5', 'PM10', 'SO2', 'NO2', 'CO', 'O3']
    avg_concentrations = data[pollutants].mean().sort_values(ascending=False)
    
    fig = px.bar(x=avg_concentrations.index, y=avg_concentrations.values,
                 labels={'x': 'Pollutants', 'y': 'Average Concentration (μg/m³)'},
                 title='Average Pollutant Concentrations Across All Sites')
    st.plotly_chart(fig, use_container_width=True)
    
    highest_pollutant = avg_concentrations.index[0]
    st.info(f"The pollutant with the highest average concentration is **{highest_pollutant}** at **{avg_concentrations[highest_pollutant]:.2f} μg/m³**.")
    
    st.markdown("---")
    st.markdown("<div class='conclusion'>", unsafe_allow_html=True)
    st.markdown("### 🔍 Conclusion: Pollutant Analysis")
    st.markdown(f"""
    - The analysis reveals that **{highest_pollutant}** is the most prevalent pollutant in Beijing's air, with an average concentration of **{avg_concentrations[highest_pollutant]:.2f} μg/m³**.
    - This is followed by {avg_concentrations.index[1]} and {avg_concentrations.index[2]}, indicating a significant presence of particulate matter and gases in the air.
    - The high levels of these pollutants suggest potential risks to public health and the need for targeted air quality management strategies.
    - Further investigation into the sources of these pollutants and their spatial distribution across Beijing could provide valuable insights for policymakers and environmental agencies.
    """)
    st.markdown("</div>", unsafe_allow_html=True)

elif page == "🌡️ Weather Impact":
    st.title("🌡️ Weather Impact on Air Quality")
    
    weather_conditions = ['TEMP', 'PRES', 'DEWP', 'RAIN', 'WSPM']
    pollutants = ['PM2.5', 'PM10', 'SO2', 'NO2', 'CO', 'O3']
    
    corr = data[pollutants + weather_conditions].corr()
    
    fig = px.imshow(corr.loc[weather_conditions, pollutants],
                    labels=dict(x="Pollutants", y="Weather Conditions", color="Correlation"),
                    x=pollutants, y=weather_conditions,
                    color_continuous_scale="RdBu_r", aspect="auto")
    fig.update_layout(title='Correlation between Weather Conditions and Pollutants')
    st.plotly_chart(fig, use_container_width=True)
    
    strongest_correlation = corr.loc[weather_conditions, pollutants].abs().max().idxmax()
    weather_factor = corr.loc[weather_conditions, strongest_correlation].abs().idxmax()
    correlation_value = corr.loc[weather_factor, strongest_correlation]
    
    st.info(f"The weather condition with the strongest influence on air quality is **{weather_factor}**. "
            f"It has a correlation of **{correlation_value:.2f}** with **{strongest_correlation}**.")
    
    st.markdown("---")
    st.markdown("<div class='conclusion'>", unsafe_allow_html=True)
    st.markdown("### 🔍 Conclusion: Weather Impact on Air Quality")
    st.markdown(f"""
    - The analysis shows that **{weather_factor}** has the strongest influence on air quality, particularly on **{strongest_correlation}** levels.
    - This {weather_factor}-{strongest_correlation} relationship (correlation: {correlation_value:.2f}) suggests that changes in {weather_factor} significantly affect the concentration of {strongest_correlation} in the air.
    - Other notable weather-pollutant relationships include:
        - Temperature shows a strong positive correlation with O3, indicating higher ozone levels during warmer periods.
        - Wind speed generally has a negative correlation with most pollutants, suggesting its role in dispersing air pollutants.
    - These findings highlight the complex interplay between weather conditions and air quality, emphasizing the need to consider meteorological factors in air quality forecasting and management strategies.
    """)
    st.markdown("</div>", unsafe_allow_html=True)

elif page == "📈 Long-term Trends":
    st.title("📈 Long-term Air Quality Trends")
    
    pollutants = ['PM2.5', 'PM10', 'SO2', 'NO2', 'CO', 'O3']
    daily_data = data.groupby('datetime')[pollutants].mean().reset_index()
    
    trends = {}
    for pollutant in pollutants:
        st.subheader(f"{pollutant} Trend")
        fig = px.line(daily_data, x='datetime', y=pollutant, 
                      title=f'Long-term Trend in {pollutant} Levels')
        fig.update_layout(xaxis_title='Date', yaxis_title=f'{pollutant} Concentration (μg/m³)')
        
        # Add trend line
        x = np.arange(len(daily_data))
        y = daily_data[pollutant]
        z = np.polyfit(x, y, 1)
        p = np.poly1d(z)
        fig.add_trace(go.Scatter(x=daily_data['datetime'], y=p(x), 
                                 mode='lines', name='Trend', line=dict(color='red', dash='dash')))
        
        st.plotly_chart(fig, use_container_width=True)
        
        trend = z[0]
        trends[pollutant] = trend
        if trend < 0:
            st.success(f"The trend for {pollutant} is improving (decreasing) over time.")
        elif trend > 0:
            st.warning(f"The trend for {pollutant} is worsening (increasing) over time.")
        else:
            st.info(f"There is no clear trend for {pollutant} over time.")
        
        st.markdown("---")
    
    st.markdown("<div class='conclusion'>", unsafe_allow_html=True)
    st.markdown("### 🔍 Conclusion: Long-term Air Quality Trends")
    improving = [p for p, t in trends.items() if t < 0]
    worsening = [p for p, t in trends.items() if t > 0]
    stable = [p for p, t in trends.items() if t == 0]
    
    st.markdown(f"""
    The long-term trend analysis of air pollutants in Beijing reveals a mixed picture:
    
    - **Improving Trends**: {', '.join(improving) if improving else 'No pollutants show clear improvement'}
    - **Worsening Trends**: {', '.join(worsening) if worsening else 'No pollutants show clear worsening'}
    - **Stable Trends**: {', '.join(stable) if stable else 'No pollutants show stable trends'}
    
    These trends suggest that:
    - Air quality management efforts have been {
        'partially successful' if improving else 'facing challenges'} in reducing certain pollutants.
    - {
        'However, there are still concerns with increasing levels of some pollutants.' if worsening else 
        'The stability in some pollutant levels indicates a need for more aggressive measures to achieve significant improvements.'
    }
    - Factors such as changes in industrial activities, transportation patterns, and environmental policies may have contributed to these trends.
    - Continued monitoring and targeted interventions are crucial for improving overall air quality in Beijing.
    """)
    st.markdown("</div>", unsafe_allow_html=True)

# Footer
st.sidebar.markdown("---")
st.sidebar.info("Created by Made Pranajaya Dibyacita")
st.sidebar.markdown("Data Source: [Air Quality Dataset](https://drive.google.com/file/d/1RhU3gJlkteaAQfyn9XOVAz7a5o1-etgr/view)")
st.sidebar.subheader("About the Author")
st.sidebar.markdown("**Name**: Made Pranajaya Dibyacita")
st.sidebar.markdown("**Email**: mdpranajaya@gmail.com")
st.sidebar.markdown("**Dicoding ID**: [mdprana](https://www.dicoding.com/users/mdprana/academies)")