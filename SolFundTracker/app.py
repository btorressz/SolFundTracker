import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import time
import numpy as np
from jupiter_api import JupiterAPI
from funding_calculator import FundingCalculator
from data_logger import DataLogger
import os

# Page configuration
st.set_page_config(
    page_title="Synthetic Perpetuals Funding Rate Tracker",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for colorful styling
st.markdown("""
<style>
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }
    
    .metric-card {
        background: linear-gradient(135deg, #ff9a9e 0%, #fecfef 50%, #fecfef 100%);
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    .stSidebar {
        background: linear-gradient(180deg, #a8edea 0%, #fed6e3 100%);
    }
    
    .funding-positive {
        color: #00c851 !important;
        font-weight: bold;
    }
    
    .funding-negative {
        color: #ff4444 !important;
        font-weight: bold;
    }
    
    .funding-neutral {
        color: #33b5e5 !important;
        font-weight: bold;
    }
    
    .price-card {
        background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    .header-gradient {
        background: linear-gradient(90deg, #1e3c72 0%, #2a5298 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-size: 2.5rem;
        font-weight: bold;
        text-align: center;
        margin-bottom: 1rem;
    }
    
    .header-emoji {
        font-size: 3rem;
        display: inline-block;
        margin-right: 0.5rem;
        filter: drop-shadow(2px 2px 4px rgba(0,0,0,0.3));
    }
</style>
""", unsafe_allow_html=True)

# Initialize components
@st.cache_resource
def init_components():
    jupiter_api = JupiterAPI()
    funding_calc = FundingCalculator()
    data_logger = DataLogger()
    return jupiter_api, funding_calc, data_logger

jupiter_api, funding_calc, data_logger = init_components()

# Initialize session state
if 'data_history' not in st.session_state:
    st.session_state.data_history = []
    
if 'last_update' not in st.session_state:
    st.session_state.last_update = None
    
if 'auto_refresh' not in st.session_state:
    st.session_state.auto_refresh = False

# Main title with gradient and visible emoji
st.markdown('<h1><span class="header-emoji">🔄</span><span class="header-gradient">Synthetic Perpetuals Funding Rate Tracker</span></h1>', unsafe_allow_html=True)
st.markdown("### 🌟 Real-time SOL funding rate simulation using Jupiter API price data")
st.markdown("---")

# Sidebar configuration
with st.sidebar:
    st.markdown("### ⚙️ Configuration")
    
    # Noise and bias configuration
    st.markdown("#### 🎯 Perp Price Simulation")
    noise_level = st.slider("🔊 Noise Level (%)", 0.0, 5.0, 0.5, 0.1)
    trend_bias = st.slider("📈 Trend Bias (%)", -2.0, 2.0, 0.0, 0.1)
    
    # Funding rate parameters
    st.markdown("#### 💰 Funding Rate Parameters")
    funding_coefficient = st.slider("⚡ Funding Coefficient", 0.1, 2.0, 0.375, 0.025)
    max_funding_rate = st.slider("🚫 Max Funding Rate (%)", 0.1, 2.0, 0.75, 0.05)
    
    # Update interval
    st.markdown("#### ⏱️ Update Settings")
    update_interval = st.selectbox("📡 Update Interval (seconds)", [30, 60, 120, 300], index=1)
    
    # Auto refresh toggle
    auto_refresh = st.checkbox("🔄 Auto Refresh", value=st.session_state.auto_refresh)
    st.session_state.auto_refresh = auto_refresh
    
    # Manual refresh button
    if st.button("🔄 Refresh Now", type="primary"):
        st.session_state.force_update = True
        st.rerun()
    
    # Clear data button
    if st.button("🗑️ Clear Data", type="secondary"):
        st.session_state.data_history = []
        st.success("✅ Data cleared!")

# Auto refresh logic
if st.session_state.auto_refresh:
    current_time = datetime.now()
    if (st.session_state.last_update is None or 
        (current_time - st.session_state.last_update).seconds >= update_interval):
        st.session_state.force_update = True

# Data fetching and processing
def fetch_and_process_data():
    try:
        # Fetch SOL spot price from Jupiter API
        spot_price = jupiter_api.get_sol_price()
        
        if spot_price is None:
            st.error("Failed to fetch SOL price from Jupiter API")
            return None
        
        # Generate synthetic perp price
        perp_price = funding_calc.generate_perp_price(
            spot_price, noise_level, trend_bias
        )
        
        # Calculate funding rate
        funding_rate = funding_calc.calculate_funding_rate(
            spot_price, perp_price, funding_coefficient, max_funding_rate
        )
        
        # Create data point
        timestamp = datetime.now()
        data_point = {
            'timestamp': timestamp,
            'spot_price': spot_price,
            'perp_price': perp_price,
            'funding_rate': funding_rate,
            'price_divergence': ((perp_price - spot_price) / spot_price) * 100
        }
        
        # Add to history
        st.session_state.data_history.append(data_point)
        
        # Keep only last 1000 data points
        if len(st.session_state.data_history) > 1000:
            st.session_state.data_history = st.session_state.data_history[-1000:]
        
        # Log to CSV
        data_logger.log_data(data_point)
        
        st.session_state.last_update = timestamp
        
        return data_point
        
    except Exception as e:
        st.error(f"Error fetching data: {str(e)}")
        return None

# Fetch data if needed
if (hasattr(st.session_state, 'force_update') or 
    len(st.session_state.data_history) == 0):
    with st.spinner("Fetching SOL price data..."):
        latest_data = fetch_and_process_data()
    
    if hasattr(st.session_state, 'force_update'):
        del st.session_state.force_update

# Display current metrics with colorful cards
if st.session_state.data_history:
    latest = st.session_state.data_history[-1]
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="price-card">
            <h4 style="color: #2E8B57; margin: 0;">💰 SOL Spot Price</h4>
            <h2 style="color: #2E8B57; margin: 5px 0;">${:.4f}</h2>
        </div>
        """.format(latest['spot_price']), unsafe_allow_html=True)
    
    with col2:
        divergence_color = "#FF6347" if latest['price_divergence'] > 0 else "#32CD32"
        st.markdown("""
        <div class="price-card">
            <h4 style="color: #4169E1; margin: 0;">🎯 Synthetic Perp Price</h4>
            <h2 style="color: #4169E1; margin: 5px 0;">${:.4f}</h2>
            <p style="color: {}; margin: 0; font-weight: bold;">{:.3f}%</p>
        </div>
        """.format(latest['perp_price'], divergence_color, latest['price_divergence']), unsafe_allow_html=True)
    
    with col3:
        funding_rate = latest['funding_rate']
        if funding_rate > 0.05:
            funding_color = "#FF4444"
            funding_class = "funding-negative"
        elif funding_rate < -0.05:
            funding_color = "#00C851"
            funding_class = "funding-positive"
        else:
            funding_color = "#33B5E5"
            funding_class = "funding-neutral"
            
        st.markdown("""
        <div class="price-card">
            <h4 style="color: #8A2BE2; margin: 0;">⚡ Funding Rate</h4>
            <h2 style="color: {}; margin: 5px 0;">{:.4f}%</h2>
        </div>
        """.format(funding_color, funding_rate), unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="price-card">
            <h4 style="color: #FF8C00; margin: 0;">🕒 Last Update</h4>
            <h2 style="color: #FF8C00; margin: 5px 0;">{}</h2>
        </div>
        """.format(latest['timestamp'].strftime("%H:%M:%S")), unsafe_allow_html=True)

# Create visualizations
if len(st.session_state.data_history) > 1:
    df = pd.DataFrame(st.session_state.data_history)
    
    # Funding Rate Chart
    st.markdown("### 📈 Funding Rate History")
    
    fig_funding = go.Figure()
    
    # Add funding rate line with gradient colors
    fig_funding.add_trace(go.Scatter(
        x=df['timestamp'],
        y=df['funding_rate'],
        mode='lines+markers',
        name='Funding Rate (%)',
        line=dict(color='#FF6B6B', width=3),
        marker=dict(size=6, color='#FF6B6B', line=dict(color='white', width=1)),
        fill='tonexty'
    ))
    
    # Add zero line
    fig_funding.add_hline(y=0, line_dash="dash", line_color="#4ECDC4", opacity=0.7, line_width=2)
    
    fig_funding.update_layout(
        title="💹 Funding Rate Over Time",
        title_font=dict(size=18, color='#2C3E50'),
        xaxis_title="🕒 Time",
        yaxis_title="📊 Funding Rate (%)",
        height=450,
        showlegend=True,
        hovermode='x unified',
        plot_bgcolor='rgba(240,248,255,0.8)',
        paper_bgcolor='rgba(255,255,255,0.9)',
        font=dict(color='#2C3E50')
    )
    
    st.plotly_chart(fig_funding, use_container_width=True)
    
    # Price Comparison Chart
    st.markdown("### 💰 Price Comparison")
    
    fig_prices = go.Figure()
    
    # Add spot price with gradient
    fig_prices.add_trace(go.Scatter(
        x=df['timestamp'],
        y=df['spot_price'],
        mode='lines+markers',
        name='💎 SOL Spot Price',
        line=dict(color='#4ECDC4', width=3),
        marker=dict(size=5, color='#4ECDC4', line=dict(color='white', width=1))
    ))
    
    # Add perp price with gradient
    fig_prices.add_trace(go.Scatter(
        x=df['timestamp'],
        y=df['perp_price'],
        mode='lines+markers',
        name='🎯 Synthetic Perp Price',
        line=dict(color='#FFD93D', width=3),
        marker=dict(size=5, color='#FFD93D', line=dict(color='white', width=1))
    ))
    
    fig_prices.update_layout(
        title="💹 Spot vs Synthetic Perpetual Price",
        title_font=dict(size=18, color='#2C3E50'),
        xaxis_title="🕒 Time",
        yaxis_title="💲 Price (USD)",
        height=450,
        showlegend=True,
        hovermode='x unified',
        plot_bgcolor='rgba(248,249,250,0.8)',
        paper_bgcolor='rgba(255,255,255,0.9)',
        font=dict(color='#2C3E50'),
        legend=dict(
            bgcolor="rgba(255,255,255,0.8)",
            bordercolor="rgba(0,0,0,0.2)",
            borderwidth=1
        )
    )
    
    st.plotly_chart(fig_prices, use_container_width=True)
    
    # Price Divergence Chart
    st.markdown("### 📊 Price Divergence")
    
    fig_divergence = go.Figure()
    
    # Create color gradient based on divergence values
    colors = ['#FF6B6B' if x > 0 else '#4ECDC4' for x in df['price_divergence']]
    
    fig_divergence.add_trace(go.Scatter(
        x=df['timestamp'],
        y=df['price_divergence'],
        mode='lines+markers',
        name='📈 Price Divergence (%)',
        line=dict(color='#BA55D3', width=3),
        marker=dict(size=6, color=colors, line=dict(color='white', width=1)),
        fill='tozeroy',
        fillcolor='rgba(186, 85, 211, 0.3)'
    ))
    
    # Add zero line
    fig_divergence.add_hline(y=0, line_dash="dash", line_color="#34495E", opacity=0.7, line_width=2)
    
    fig_divergence.update_layout(
        title="📊 Price Divergence (Perp vs Spot)",
        title_font=dict(size=18, color='#2C3E50'),
        xaxis_title="🕒 Time",
        yaxis_title="📈 Divergence (%)",
        height=450,
        showlegend=True,
        hovermode='x unified',
        plot_bgcolor='rgba(250,250,250,0.8)',
        paper_bgcolor='rgba(255,255,255,0.9)',
        font=dict(color='#2C3E50')
    )
    
    st.plotly_chart(fig_divergence, use_container_width=True)
    
    # Statistics
    st.markdown("### 📋 Statistics")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="price-card">
            <h4 style="color: #E74C3C; margin: 0;">⚡ Funding Rate Statistics</h4>
        </div>
        """, unsafe_allow_html=True)
        funding_stats = df['funding_rate'].describe()
        st.dataframe(funding_stats, use_container_width=True)
    
    with col2:
        st.markdown("""
        <div class="price-card">
            <h4 style="color: #3498DB; margin: 0;">📊 Price Divergence Statistics</h4>
        </div>
        """, unsafe_allow_html=True)
        divergence_stats = df['price_divergence'].describe()
        st.dataframe(divergence_stats, use_container_width=True)
    
    # Recent data table
    st.markdown("### 📑 Recent Data")
    recent_data = []
    for _, row in df.tail(10).iterrows():
        timestamp_str = row['timestamp'].strftime('%Y-%m-%d %H:%M:%S') if hasattr(row['timestamp'], 'strftime') else str(row['timestamp'])
        recent_data.append({
            '🕒 Timestamp': timestamp_str,
            '💰 Spot Price ($)': f"{row['spot_price']:.4f}",
            '🎯 Perp Price ($)': f"{row['perp_price']:.4f}",
            '⚡ Funding Rate (%)': f"{row['funding_rate']:.4f}",
            '📈 Divergence (%)': f"{row['price_divergence']:.3f}"
        })
    
    recent_df = pd.DataFrame(recent_data)
    st.dataframe(recent_df, use_container_width=True)

else:
    st.info("No data available. Click 'Refresh Now' to start collecting data.")

# Footer
st.markdown("---")
st.markdown(
    "**Note:** This is a synthetic perpetuals funding rate tracker for educational and analysis purposes. "
    "Funding rates are calculated based on simulated price divergence and do not represent actual trading data."
)

# Auto-refresh mechanism
if st.session_state.auto_refresh:
    time.sleep(1)  # Small delay to prevent excessive refreshing
    st.rerun()
