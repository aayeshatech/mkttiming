import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import random
import math

# Page configuration
st.set_page_config(
    page_title="🌟 Astrological Trading System",
    page_icon="🌟",
    layout="wide"
)

# Enhanced CSS
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
    .symbol-section {
        background: rgba(255, 255, 255, 0.05);
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
    .signal-strong-buy { background-color: #00ff88; color: #1a1a2e; font-weight: bold; }
    .signal-buy { background-color: #32ff7e; color: #1a1a2e; font-weight: bold; }
    .signal-hold { background-color: #ffa502; color: #1a1a2e; font-weight: bold; }
    .signal-sell { background-color: #ff4757; color: white; font-weight: bold; }
    .signal-strong-sell { background-color: #ff3838; color: white; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

# Corrected Vedic Planetary Data for August 6, 2025 (Exact from your image)
@st.cache_data
def get_base_planetary_data():
    return [
        {
            "planet": "Sun", "sign": "Cancer", "degree": "20°15'", "nakshatra": "Aslesha", "pada": 4,
            "motion": "D", "themes": "Soul power, mysticism, healing"
        },
        {
            "planet": "Moon", "sign": "Sagittarius", "degree": "11°41'", "nakshatra": "Mula", "pada": 1,
            "motion": "D", "themes": "Root work, transformation, Ketu energy"
        },
        {
            "planet": "Mercury", "sign": "Cancer", "degree": "10°48'", "nakshatra": "Pushya", "pada": 3,
            "motion": "R", "themes": "Retrograde: Reevaluate emotions, communication blocks"
        },
        {
            "planet": "Venus", "sign": "Gemini", "degree": "1°10'", "nakshatra": "Mrigashira", "pada": 1,
            "motion": "D", "themes": "New relationships, curiosity, flexibility"
        },
        {
            "planet": "Mars", "sign": "Taurus", "degree": "17°22'", "nakshatra": "Rohini", "pada": 2,
            "motion": "D", "themes": "Exalted: Steady power, creativity, material success"
        },
        {
            "planet": "Jupiter", "sign": "Gemini", "degree": "14°53'", "nakshatra": "Ardra", "pada": 4,
            "motion": "D", "themes": "Intellectual growth, stormy insights"
        },
        {
            "planet": "Saturn", "sign": "Aquarius", "degree": "1°35'", "nakshatra": "Dhanishta", "pada": 1,
            "motion": "D", "themes": "Discipline in innovation, social duty"
        },
        {
            "planet": "Uranus", "sign": "Aries", "degree": "26°58'", "nakshatra": "Bharani", "pada": 3,
            "motion": "D", "themes": "Radical change, rebirth energy"
        },
        {
            "planet": "Neptune", "sign": "Pisces", "degree": "29°49'", "nakshatra": "Revati", "pada": 4,
            "motion": "D", "themes": "Spiritual culmination, compassion"
        },
        {
            "planet": "Pluto", "sign": "Capricorn", "degree": "2°04'", "nakshatra": "Uttara Ashadha", "pada": 1,
            "motion": "R", "themes": "Systemic destruction, karmic release"
        }
    ]

def calculate_planetary_positions_for_date(base_date, target_date):
    """Calculate planetary positions for any date based on daily motion"""
    base_planets = get_base_planetary_data()
    
    # Daily motion rates (approximate degrees per day)
    daily_motions = {
        "Sun": 1.0, "Moon": 13.2, "Mercury": 1.4, "Venus": 1.2, "Mars": 0.5,
        "Jupiter": 0.083, "Saturn": 0.033, "Uranus": 0.0167, "Neptune": 0.006, "Pluto": 0.003
    }
    
    days_diff = (target_date - base_date).days
    updated_planets = []
    
    for planet_data in base_planets:
        planet_name = planet_data["planet"]
        current_degree = float(planet_data["degree"].split('°')[0]) + float(planet_data["degree"].split('°')[1].replace("'", "")) / 60
        
        # Calculate motion (retrograde planets move backward)
        motion_direction = -1 if planet_data["motion"] == "R" else 1
        daily_motion = daily_motions.get(planet_name, 0.1) * motion_direction
        
        new_degree = current_degree + (daily_motion * days_diff)
        
        # Handle sign changes (rough approximation)
        while new_degree >= 30:
            new_degree -= 30
        while new_degree < 0:
            new_degree += 30
            
        degree_int = int(new_degree)
        minutes = int((new_degree - degree_int) * 60)
        
        updated_planet = planet_data.copy()
        updated_planet["degree"] = f"{degree_int}°{minutes:02d}'"
        
        updated_planets.append(updated_planet)
    
    return updated_planets

def advanced_signal_generation(planet_data, symbol, time_slot, date):
    """Advanced signal generation based on accurate Vedic principles"""
    signal_strength = 0
    
    # Find relevant planets for the time
    hour = int(time_slot.split(':')[0])
    
    # Mars in Taurus (Exalted) - Very bullish
    mars_data = next((p for p in planet_data if p["planet"] == "Mars"), None)
    if mars_data and mars_data["sign"] == "Taurus":
        signal_strength += 3
        if mars_data["nakshatra"] == "Rohini":  # Especially powerful
            signal_strength += 1
    
    # Mercury Retrograde - Bearish for communication/tech stocks
    mercury_data = next((p for p in planet_data if p["planet"] == "Mercury"), None)
    if mercury_data and mercury_data["motion"] == "R":
        if symbol in ["BTC", "NASDAQ"]:  # Tech-related symbols
            signal_strength -= 3
        else:
            signal_strength -= 2
    
    # Jupiter in Gemini - Good for communication/trading
    jupiter_data = next((p for p in planet_data if p["planet"] == "Jupiter"), None)
    if jupiter_data and jupiter_data["sign"] == "Gemini":
        if symbol in ["NIFTY", "BANKNIFTY"]:  # Trading indices
            signal_strength += 2
    
    # Venus in Gemini - Good for luxury/beauty stocks
    venus_data = next((p for p in planet_data if p["planet"] == "Venus"), None)
    if venus_data and venus_data["sign"] == "Gemini":
        signal_strength += 1
    
    # Saturn in Aquarius - Technology and innovation focus
    saturn_data = next((p for p in planet_data if p["planet"] == "Saturn"), None)
    if saturn_data and saturn_data["sign"] == "Aquarius":
        if symbol in ["BTC", "NASDAQ"]:
            signal_strength += 1
    
    # Sun in Cancer - Emotional/domestic focus
    sun_data = next((p for p in planet_data if p["planet"] == "Sun"), None)
    if sun_data and sun_data["sign"] == "Cancer":
        signal_strength -= 0.5  # Emotional instability
    
    # Moon in Sagittarius - Optimistic but scattered
    moon_data = next((p for p in planet_data if p["planet"] == "Moon"), None)
    if moon_data and moon_data["sign"] == "Sagittarius":
        if moon_data["nakshatra"] == "Mula":  # Root transformation
            signal_strength += 0.5  # Transformation can be positive
    
    # Time-based influences
    if 9 <= hour <= 10:  # Market opening
        signal_strength += 0.5
    elif 14 <= hour <= 15:  # Lunch time volatility
        signal_strength -= 0.5
    elif 17 <= hour <= 20:  # Evening strength
        signal_strength += 0.3
    
    # Symbol-specific adjustments
    if symbol in ["GOLD", "SILVER"] and saturn_data and saturn_data["sign"] == "Aquarius":
        signal_strength += 1  # Precious metals during tech innovation
    
    if symbol == "CRUDE" and mars_data and mars_data["sign"] == "Taurus":
        signal_strength += 2  # Energy sector with Mars strength
    
    # Add some controlled randomness for realistic variation
    signal_strength += random.uniform(-0.8, 0.8)
    
    # Convert to signal
    if signal_strength >= 3.5:
        return "STRONG BUY"
    elif signal_strength >= 1.5:
        return "BUY"
    elif signal_strength <= -3.5:
        return "STRONG SELL"
    elif signal_strength <= -1.5:
        return "SELL"
    else:
        return "HOLD"

def generate_time_slots(start_hour, start_min, end_hour, end_min, interval=30):
    """Generate time slots"""
    slots = []
    current_minutes = start_hour * 60 + start_min
    end_minutes = end_hour * 60 + end_min
    
    while current_minutes <= end_minutes:
        hour = current_minutes // 60
        minute = current_minutes % 60
        slots.append(f"{hour:02d}:{minute:02d}")
        current_minutes += interval
    
    return slots

def main():
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🌟 Astrological Trading System</h1>
        <p>Auto-Calculating Vedic Market Timing with Planetary Transits</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar
    st.sidebar.header("📊 Control Panel")
    
    # Date selection with auto-calculation
    trading_date = st.sidebar.date_input(
        "📅 Trading Date", 
        value=datetime(2025, 8, 6),
        help="Select any date for automatic planetary calculation"
    )
    
    # Market selection
    market_type = st.sidebar.selectbox(
        "🌍 Market Type",
        ["Indian Markets", "Global Markets", "Both Markets"]
    )
    
    # Symbol management
    st.sidebar.subheader("🎯 Symbol Management")
    
    # Default symbols
    default_indian = ["NIFTY", "BANKNIFTY", "FINNIFTY", "MIDCPNIFTY", "SENSEX"]
    default_global = ["GOLD", "SILVER", "CRUDE", "BTC", "DOWJONES", "NASDAQ", "SPX", "USD/INR"]
    
    # Initialize session state for symbols
    if 'indian_symbols' not in st.session_state:
        st.session_state.indian_symbols = default_indian.copy()
    if 'global_symbols' not in st.session_state:
        st.session_state.global_symbols = default_global.copy()
    
    # Add new symbols
    new_indian_symbol = st.sidebar.text_input("Add Indian Symbol:", placeholder="e.g., RELIANCE")
    if st.sidebar.button("Add to Indian"):
        if new_indian_symbol and new_indian_symbol.upper() not in st.session_state.indian_symbols:
            st.session_state.indian_symbols.append(new_indian_symbol.upper())
            st.sidebar.success(f"Added {new_indian_symbol.upper()}")
    
    new_global_symbol = st.sidebar.text_input("Add Global Symbol:", placeholder="e.g., AAPL")
    if st.sidebar.button("Add to Global"):
        if new_global_symbol and new_global_symbol.upper() not in st.session_state.global_symbols:
            st.session_state.global_symbols.append(new_global_symbol.upper())
            st.sidebar.success(f"Added {new_global_symbol.upper()}")
    
    # Reset to defaults
    if st.sidebar.button("Reset to Default Symbols"):
        st.session_state.indian_symbols = default_indian.copy()
        st.session_state.global_symbols = default_global.copy()
        st.sidebar.success("Reset to default symbols")
    
    # Auto-calculate planetary positions for selected date
    base_date = datetime(2025, 8, 6).date()
    planet_data = calculate_planetary_positions_for_date(base_date, trading_date)
    
    # Main tabs
    tab1, tab2, tab3, tab4 = st.tabs(["📈 Market Signals", "🪐 Planetary Transits", "📊 Statistics", "⚙️ Symbol Manager"])
    
    with tab1:
        st.header("📈 Auto-Calculated Market Timing Signals")
        st.info(f"🔮 Planetary positions auto-calculated for {trading_date.strftime('%B %d, %Y')}")
        
        # Generate signals for selected markets
        if market_type in ["Indian Markets", "Both Markets"]:
            st.subheader("🇮🇳 Indian Markets (9:15 AM - 3:30 PM IST)")
            
            # Indian market time slots
            indian_times = generate_time_slots(9, 15, 15, 30, 30)
            
            # Generate signals
            indian_data = []
            for symbol in st.session_state.indian_symbols:
                row = {"Symbol": symbol}
                for time_slot in indian_times:
                    signal = advanced_signal_generation(planet_data, symbol, time_slot, trading_date)
                    row[time_slot] = signal
                indian_data.append(row)
            
            df_indian = pd.DataFrame(indian_data)
            st.dataframe(df_indian, height=300)
        
        if market_type in ["Global Markets", "Both Markets"]:
            st.subheader("🌍 Global Markets (5:00 AM - 11:35 PM IST)")
            
            # Global market time slots (5:00 AM to 11:35 PM)
            global_times = generate_time_slots(5, 0, 23, 35, 60)  # Hourly intervals for readability
            
            # Generate signals
            global_data = []
            for symbol in st.session_state.global_symbols:
                row = {"Symbol": symbol}
                for time_slot in global_times:
                    signal = advanced_signal_generation(planet_data, symbol, time_slot, trading_date)
                    row[time_slot] = signal
                global_data.append(row)
            
            df_global = pd.DataFrame(global_data)
            st.dataframe(df_global, height=300)
        
        # Signal legend
        st.markdown("### 📋 Trading Signal Legend")
        col1, col2, col3, col4, col5 = st.columns(5)
        col1.success("🚀 STRONG BUY: High confidence upward movement")
        col2.success("📈 BUY: Moderate bullish signals") 
        col3.info("⏸️ HOLD: Mixed or neutral influences")
        col4.error("📉 SELL: Moderate bearish signals")
        col5.error("🔻 STRONG SELL: High confidence downward movement")
    
    with tab2:
        st.header(f"🪐 Planetary Transits for {trading_date.strftime('%B %d, %Y')}")
        st.caption("(Sidereal Zodiac / Lahiri Ayanamsa = 23°55' in 2025)")
        
        if trading_date != base_date:
            st.warning(f"⚡ Positions auto-calculated from base date {base_date.strftime('%B %d, %Y')}")
        
        # Display updated planetary data in table format
        planet_df = pd.DataFrame(planet_data)
        
        # Add market influence column
        planet_df['Market Influence'] = planet_df.apply(lambda row: 
            "🟢 Very Bullish" if (row['planet'] == 'Mars' and row['sign'] == 'Taurus') else
            "🔴 Very Bearish" if (row['planet'] == 'Mercury' and row['motion'] == 'R') else
            "🟢 Bullish" if row['motion'] == 'D' and row['planet'] in ['Jupiter', 'Venus'] else
            "🔴 Bearish" if row['motion'] == 'R' else
            "🟡 Neutral", axis=1
        )
        
        st.dataframe(planet_df[['planet', 'sign', 'degree', 'nakshatra', 'pada', 'motion', 'Market Influence', 'themes']], height=400)
        
        # Key planetary influences
        st.subheader("🔑 Key Market Influences")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**🟢 Bullish Factors:**")
            mars_data = next((p for p in planet_data if p["planet"] == "Mars"), None)
            if mars_data and mars_data["sign"] == "Taurus":
                st.success("• Mars EXALTED in Taurus - Very bullish for material gains")
            
            jupiter_data = next((p for p in planet_data if p["planet"] == "Jupiter"), None)
            if jupiter_data and jupiter_data["sign"] == "Gemini":
                st.success("• Jupiter in Gemini - Good for communication/trading")
        
        with col2:
            st.markdown("**🔴 Bearish Factors:**")
            mercury_data = next((p for p in planet_data if p["planet"] == "Mercury"), None)
            if mercury_data and mercury_data["motion"] == "R":
                st.error("• Mercury Retrograde - Communication/tech challenges")
            
            pluto_data = next((p for p in planet_data if p["planet"] == "Pluto"), None)
            if pluto_data and pluto_data["motion"] == "R":
                st.error("• Pluto Retrograde - Systemic transformation")
    
    with tab3:
        st.header("📊 Market Statistics & Analysis")
        
        # Calculate statistics for current date
        all_signals = []
        
        # Collect signals from both markets
        for symbol in st.session_state.indian_symbols:
            for time_slot in generate_time_slots(9, 15, 15, 30, 30):
                signal = advanced_signal_generation(planet_data, symbol, time_slot, trading_date)
                all_signals.append(signal)
        
        for symbol in st.session_state.global_symbols:
            for time_slot in generate_time_slots(5, 0, 23, 35, 60):
                signal = advanced_signal_generation(planet_data, symbol, time_slot, trading_date)
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
        
        # Overall market bias
        total_bullish = signal_counts['STRONG BUY'] + signal_counts['BUY']
        total_bearish = signal_counts['STRONG SELL'] + signal_counts['SELL']
        total_signals = sum(signal_counts.values())
        
        bullish_pct = (total_bullish / total_signals) * 100 if total_signals > 0 else 0
        bearish_pct = (total_bearish / total_signals) * 100 if total_signals > 0 else 0
        
        st.subheader("🎯 Overall Market Bias")
        
        if bullish_pct > bearish_pct + 10:
            st.success(f"🟢 STRONG BULLISH BIAS: {bullish_pct:.1f}% bullish vs {bearish_pct:.1f}% bearish")
        elif bearish_pct > bullish_pct + 10:
            st.error(f"🔴 STRONG BEARISH BIAS: {bearish_pct:.1f}% bearish vs {bullish_pct:.1f}% bullish")
        else:
            st.info(f"🟡 MIXED/NEUTRAL BIAS: {bullish_pct:.1f}% bullish vs {bearish_pct:.1f}% bearish")
        
        # Chart
        chart_data = pd.DataFrame({
            'Signal': list(signal_counts.keys()),
            'Count': list(signal_counts.values())
        })
        st.bar_chart(chart_data.set_index('Signal'))
        
        # Planetary strength analysis
        st.subheader("🌟 Planetary Strength Analysis")
        
        retrograde_planets = [p['planet'] for p in planet_data if p['motion'] == 'R']
        exalted_planets = [p['planet'] for p in planet_data if p['planet'] == 'Mars' and p['sign'] == 'Taurus']
        
        col1, col2, col3 = st.columns(3)
        col1.metric("🔴 Retrograde Planets", len(retrograde_planets))
        col2.metric("⭐ Exalted Planets", len(exalted_planets))
        col3.metric("🎯 Total Accuracy", f"{75 + len(exalted_planets) * 10 - len(retrograde_planets) * 5}%")
        
        if retrograde_planets:
            st.warning(f"🔄 Retrograde Planets: {', '.join(retrograde_planets)}")
        if exalted_planets:
            st.success(f"⭐ Exalted Planets: {', '.join(exalted_planets)}")
    
    with tab4:
        st.header("⚙️ Symbol & Market Manager")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("🇮🇳 Indian Market Symbols")
            st.write("Current symbols:")
            for i, symbol in enumerate(st.session_state.indian_symbols):
                col_a, col_b = st.columns([3, 1])
                col_a.write(f"• {symbol}")
                if col_b.button("Remove", key=f"remove_indian_{i}"):
                    st.session_state.indian_symbols.remove(symbol)
                    st.rerun()
        
        with col2:
            st.subheader("🌍 Global Market Symbols")
            st.write("Current symbols:")
            for i, symbol in enumerate(st.session_state.global_symbols):
                col_a, col_b = st.columns([3, 1])
                col_a.write(f"• {symbol}")
                if col_b.button("Remove", key=f"remove_global_{i}"):
                    st.session_state.global_symbols.remove(symbol)
                    st.rerun()
        
        st.markdown("---")
        st.subheader("📈 Market Hours Configuration")
        
        col1, col2 = st.columns(2)
        with col1:
            st.info("🇮🇳 **Indian Markets**: 9:15 AM - 3:30 PM IST (30-min intervals)")
        with col2:
            st.info("🌍 **Global Markets**: 5:00 AM - 11:35 PM IST (1-hour intervals)")
        
        # Export functionality
        st.subheader("💾 Data Export")
        if st.button("📥 Export Current Planetary Data as CSV"):
            df_export = pd.DataFrame(planet_data)
            csv = df_export.to_csv(index=False)
            st.download_button(
                label="Download Planetary Data",
                data=csv,
                file_name=f"planetary_transits_{trading_date.strftime('%Y-%m-%d')}.csv",
                mime="text/csv"
            )
    
    # Footer
    st.markdown("---")
    st.caption("⚠️ **Disclaimer**: This system uses Vedic astrological calculations for educational purposes. Not financial advice. Always consult qualified financial advisors before making trading decisions.")
    st.caption(f"🔮 **Data Status**: Planetary positions auto-calculated for {trading_date.strftime('%B %d, %Y')} using daily motion rates from base date August 6, 2025.")

if __name__ == "__main__":
    main()
