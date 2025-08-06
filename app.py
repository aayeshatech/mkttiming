import streamlit as st
import pandas as pd
from datetime import datetime
import random

# Page configuration
st.set_page_config(
    page_title="🌟 Astrological Trading System",
    page_icon="🌟",
    layout="wide"
)

# Simple CSS
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
        padding: 2rem;
        border-radius: 10px;
        text-align: center;
        color: white;
        margin-bottom: 2rem;
    }
</style>
""", unsafe_allow_html=True)

# Planetary data - Corrected Vedic positions
@st.cache_data
def get_planetary_data():
    return [
        {
            "planet": "Sun", "zodiac": "Cancer", "nakshatra": "Aslesha", "pada": 4,
            "position": "20°15'00\"", "motion": "D", "declination": 16.8,
            "themes": "Soul power, mysticism, healing"
        },
        {
            "planet": "Moon", "zodiac": "Sagittarius", "nakshatra": "Mula", "pada": 1,
            "position": "11°41'00\"", "motion": "D", "declination": -26.2,
            "themes": "Root work, transformation, Ketu energy"
        },
        {
            "planet": "Mercury", "zodiac": "Cancer", "nakshatra": "Pushya", "pada": 3,
            "position": "10°48'00\"", "motion": "R", "declination": 18.5,
            "themes": "Retrograde: Communication blocks, reevaluation"
        },
        {
            "planet": "Venus", "zodiac": "Gemini", "nakshatra": "Mrigashira", "pada": 1,
            "position": "1°10'00\"", "motion": "D", "declination": 23.1,
            "themes": "New relationships, curiosity, flexibility"
        },
        {
            "planet": "Mars", "zodiac": "Taurus", "nakshatra": "Rohini", "pada": 2,
            "position": "17°22'00\"", "motion": "D", "declination": 25.4,
            "themes": "Exalted: Steady power, creativity, material success"
        },
        {
            "planet": "Jupiter", "zodiac": "Gemini", "nakshatra": "Ardra", "pada": 4,
            "position": "14°53'00\"", "motion": "D", "declination": 22.8,
            "themes": "Intellectual growth, stormy insights"
        },
        {
            "planet": "Saturn", "zodiac": "Aquarius", "nakshatra": "Dhanishta", "pada": 1,
            "position": "1°35'00\"", "motion": "D", "declination": -20.1,
            "themes": "Discipline in innovation, social duty"
        }
    ]

def generate_signal(planet_data, symbol, time_slot):
    """Generate trading signal based on planetary positions"""
    signal_strength = 0
    
    # Mars exalted in Taurus - very bullish
    mars_data = next((p for p in planet_data if p["planet"] == "Mars"), None)
    if mars_data and mars_data["zodiac"] == "Taurus":
        signal_strength += 3
    
    # Mercury retrograde - bearish
    mercury_data = next((p for p in planet_data if p["planet"] == "Mercury"), None)
    if mercury_data and mercury_data["motion"] == "R":
        signal_strength -= 2
    
    # Jupiter aspects - bullish
    jupiter_data = next((p for p in planet_data if p["planet"] == "Jupiter"), None)
    if jupiter_data and jupiter_data["motion"] == "D":
        signal_strength += 1
    
    # Add some randomness for demonstration
    signal_strength += random.uniform(-1, 1)
    
    # Convert to signal
    if signal_strength >= 2:
        return "STRONG BUY"
    elif signal_strength >= 0.5:
        return "BUY"
    elif signal_strength <= -2:
        return "STRONG SELL"
    elif signal_strength <= -0.5:
        return "SELL"
    else:
        return "HOLD"

def main():
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🌟 Astrological Trading System</h1>
        <p>Vedic Market Timing with BUY/SELL/HOLD Signals</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar
    st.sidebar.header("📊 Control Panel")
    trading_date = st.sidebar.date_input("📅 Trading Date", value=datetime(2025, 8, 6))
    
    # Get planetary data
    planet_data = get_planetary_data()
    
    # Main tabs
    tab1, tab2, tab3 = st.tabs(["📈 Market Signals", "🪐 Planetary Data", "📊 Statistics"])
    
    with tab1:
        st.header("📈 Market Timing Signals")
        
        # Indian market symbols and times
        symbols = ["NIFTY", "BANKNIFTY", "FINNIFTY", "MIDCPNIFTY", "SENSEX"]
        time_slots = ["09:15", "09:45", "10:15", "10:45", "11:15", "11:45", "12:15", "12:45", "13:15", "13:45", "14:15", "14:45", "15:15"]
        
        # Generate and display signals
        st.subheader("🇮🇳 Indian Markets (9:15 AM - 3:30 PM IST)")
        
        # Create a simple table
        signal_data = []
        for symbol in symbols:
            row = {"Symbol": symbol}
            for time_slot in time_slots:
                signal = generate_signal(planet_data, symbol, time_slot)
                row[time_slot] = signal
            signal_data.append(row)
        
        # Display as DataFrame
        df = pd.DataFrame(signal_data)
        st.dataframe(df)
        
        # Signal legend
        st.markdown("### 📋 Signal Legend")
        col1, col2, col3, col4, col5 = st.columns(5)
        col1.success("🚀 STRONG BUY")
        col2.success("📈 BUY") 
        col3.info("⏸️ HOLD")
        col4.error("📉 SELL")
        col5.error("🔻 STRONG SELL")
    
    with tab2:
        st.header("🪐 Corrected Vedic Planetary Transits")
        st.caption("Sidereal Zodiac / Lahiri Ayanamsa = 23°55' in 2025")
        
        # Display planetary data
        for planet in planet_data:
            with st.expander(f"🪐 {planet['planet']} in {planet['zodiac']}", expanded=False):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write(f"**Position:** {planet['position']}")
                    st.write(f"**Motion:** {'🟢 Direct' if planet['motion'] == 'D' else '🔴 Retrograde'}")
                    st.write(f"**Declination:** {planet['declination']}°")
                
                with col2:
                    st.write(f"**Nakshatra:** {planet['nakshatra']} (Pada {planet['pada']})")
                    st.write(f"**Themes:** {planet['themes']}")
        
        # Summary
        st.subheader("📊 Summary")
        retrograde_count = sum(1 for p in planet_data if p['motion'] == 'R')
        direct_count = len(planet_data) - retrograde_count
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Planets", len(planet_data))
        col2.metric("Direct Motion", direct_count)
        col3.metric("Retrograde", retrograde_count)
    
    with tab3:
        st.header("📊 Market Statistics")
        
        # Calculate signal distribution
        all_signals = []
        for symbol in symbols:
            for time_slot in time_slots:
                signal = generate_signal(planet_data, symbol, time_slot)
                all_signals.append(signal)
        
        # Count signals
        signal_counts = {
            'STRONG BUY': all_signals.count('STRONG BUY'),
            'BUY': all_signals.count('BUY'),
            'HOLD': all_signals.count('HOLD'),
            'SELL': all_signals.count('SELL'),
            'STRONG SELL': all_signals.count('STRONG SELL')
        }
        
        # Display metrics
        col1, col2, col3, col4, col5 = st.columns(5)
        col1.metric("🚀 STRONG BUY", signal_counts['STRONG BUY'])
        col2.metric("📈 BUY", signal_counts['BUY'])
        col3.metric("⏸️ HOLD", signal_counts['HOLD'])
        col4.metric("📉 SELL", signal_counts['SELL'])
        col5.metric("🔻 STRONG SELL", signal_counts['STRONG SELL'])
        
        # Market bias
        total_bullish = signal_counts['STRONG BUY'] + signal_counts['BUY']
        total_bearish = signal_counts['STRONG SELL'] + signal_counts['SELL']
        
        if total_bullish > total_bearish:
            st.success(f"🟢 Market Bias: BULLISH ({total_bullish} vs {total_bearish})")
        elif total_bearish > total_bullish:
            st.error(f"🔴 Market Bias: BEARISH ({total_bearish} vs {total_bullish})")
        else:
            st.info(f"🟡 Market Bias: NEUTRAL ({total_bullish} vs {total_bearish})")
        
        # Chart
        chart_data = pd.DataFrame({
            'Signal': list(signal_counts.keys()),
            'Count': list(signal_counts.values())
        })
        st.bar_chart(chart_data.set_index('Signal'))
    
    # Footer
    st.markdown("---")
    st.caption("⚠️ For educational purposes only. Not financial advice. Always consult qualified financial advisors before making trading decisions.")

if __name__ == "__main__":
    main()
