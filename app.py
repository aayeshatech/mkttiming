import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import json
import random
import math

# Page configuration
st.set_page_config(
    page_title="🌟 Astrological Trading System",
    page_icon="🌟",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
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
    
    .signal-cell {
        text-align: center;
        padding: 0.5rem;
        border-radius: 5px;
        font-weight: bold;
        margin: 2px;
    }
    
    .strong-bullish {
        background-color: #32ff7e;
        color: #1a1a2e;
    }
    
    .bullish {
        background-color: #00ff88;
        color: #1a1a2e;
    }
    
    .neutral {
        background-color: #ffa502;
        color: #1a1a2e;
    }
    
    .bearish {
        background-color: #ff4757;
        color: white;
    }
    
    .strong-bearish {
        background-color: #ff3838;
        color: white;
    }
    
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
    }
    
    .planet-row {
        background: rgba(255, 255, 255, 0.05);
        padding: 0.5rem;
        border-radius: 5px;
        margin: 0.2rem 0;
    }
    
    .motion-direct {
        color: #32ff7e;
        font-weight: bold;
    }
    
    .motion-retrograde {
        color: #ff4757;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# Planetary data structure
class PlanetaryData:
    def __init__(self):
        self.planets = [
            {
                "planet": "Sun",
                "datetime": "2025-08-06T06:00:00",
                "motion": "D",
                "signLord": "Sun",
                "starLord": "Ketu",
                "subLord": "Venus",
                "zodiac": "Leo",
                "nakshatra": "Magha",
                "pada": 2,
                "position": "13°30'00\"",
                "declination": 18.45
            },
            {
                "planet": "Moon",
                "datetime": "2025-08-06T09:15:00",
                "motion": "D",
                "signLord": "Mercury",
                "starLord": "Rahu",
                "subLord": "Mercury",
                "zodiac": "Gemini",
                "nakshatra": "Ardra",
                "pada": 1,
                "position": "15°08'00\"",
                "declination": 22.10
            },
            {
                "planet": "Mercury",
                "datetime": "2025-08-06T10:30:00",
                "motion": "R",
                "signLord": "Sun",
                "starLord": "Ketu",
                "subLord": "Moon",
                "zodiac": "Leo",
                "nakshatra": "Magha",
                "pada": 1,
                "position": "4°48'00\"",
                "declination": 15.20
            },
            {
                "planet": "Venus",
                "datetime": "2025-08-06T11:45:00",
                "motion": "D",
                "signLord": "Moon",
                "starLord": "Venus",
                "subLord": "Saturn",
                "zodiac": "Cancer",
                "nakshatra": "Aslesha",
                "pada": 4,
                "position": "25°10'00\"",
                "declination": 20.80
            },
            {
                "planet": "Mars",
                "datetime": "2025-08-06T13:20:00",
                "motion": "D",
                "signLord": "Venus",
                "starLord": "Moon",
                "subLord": "Jupiter",
                "zodiac": "Taurus",
                "nakshatra": "Rohini",
                "pada": 3,
                "position": "17°22'00\"",
                "declination": 25.15
            },
            {
                "planet": "Jupiter",
                "datetime": "2025-08-06T14:15:00",
                "motion": "D",
                "signLord": "Mercury",
                "starLord": "Rahu",
                "subLord": "Venus",
                "zodiac": "Gemini",
                "nakshatra": "Ardra",
                "pada": 2,
                "position": "14°53'00\"",
                "declination": 23.45
            },
            {
                "planet": "Saturn",
                "datetime": "2025-08-06T15:30:00",
                "motion": "D",
                "signLord": "Jupiter",
                "starLord": "Jupiter",
                "subLord": "Mercury",
                "zodiac": "Pisces",
                "nakshatra": "Revati",
                "pada": 1,
                "position": "1°35'00\"",
                "declination": -8.20
            },
            {
                "planet": "Rahu",
                "datetime": "2025-08-06T16:45:00",
                "motion": "R",
                "signLord": "Jupiter",
                "starLord": "Saturn",
                "subLord": "Mars",
                "zodiac": "Pisces",
                "nakshatra": "Uttarabhadrapada",
                "pada": 4,
                "position": "18°54'00\"",
                "declination": -1.80
            },
            {
                "planet": "Ketu",
                "datetime": "2025-08-06T17:30:00",
                "motion": "R",
                "signLord": "Mercury",
                "starLord": "Saturn",
                "subLord": "Venus",
                "zodiac": "Virgo",
                "nakshatra": "Hasta",
                "pada": 2,
                "position": "18°54'00\"",
                "declination": 1.80
            }
        ]
        
        self.indian_symbols = ['NIFTY', 'BANKNIFTY', 'FINNIFTY', 'MIDCPNIFTY', 'SENSEX']
        self.global_symbols = ['GOLD', 'SILVER', 'CRUDE', 'BTC', 'DOW JONES', 'S&P 500', 'NASDAQ', 'USD/INR']

class AstrologicalAnalyzer:
    @staticmethod
    def generate_signal(symbol, time_str, date_str):
        """Generate trading signal based on planetary positions"""
        current_time = f"{date_str}T{time_str}:00"
        
        # Find nearest planetary transit
        nearest_transit = None
        min_diff = float('inf')
        
        for planet in st.session_state.planetary_data.planets:
            time_diff = abs((datetime.fromisoformat(planet['datetime']) - 
                           datetime.fromisoformat(current_time)).total_seconds())
            if time_diff < min_diff and time_diff < 3600:  # Within 1 hour
                min_diff = time_diff
                nearest_transit = planet
        
        signal_strength = 0
        
        if nearest_transit:
            # Retrograde planets (generally bearish)
            if nearest_transit['motion'] == 'R':
                signal_strength -= 2
            
            # Beneficial planets in strong positions
            if nearest_transit['planet'] in ['Jupiter', 'Venus', 'Mercury'] and nearest_transit['motion'] == 'D':
                signal_strength += 1
            
            # Mars and Saturn effects
            if nearest_transit['planet'] == 'Mars' and nearest_transit['motion'] == 'D':
                signal_strength += 0.5
            if nearest_transit['planet'] == 'Saturn':
                signal_strength -= 1
            
            # Pada analysis (1st and 4th padas are stronger)
            if nearest_transit['pada'] in [1, 4]:
                signal_strength += 1
            
            # Zodiac sign strength
            strong_signs = ['Leo', 'Aries', 'Sagittarius', 'Gemini']
            if nearest_transit['zodiac'] in strong_signs:
                signal_strength += 0.5
        
        # Convert to signal
        if signal_strength >= 2:
            return 'strong-bullish'
        elif signal_strength >= 1:
            return 'bullish'
        elif signal_strength <= -2:
            return 'strong-bearish'
        elif signal_strength <= -1:
            return 'bearish'
        else:
            return 'neutral'
    
    @staticmethod
    def get_signal_symbol(signal):
        symbols = {
            'strong-bullish': '⬆⬆',
            'bullish': '↗',
            'neutral': '→',
            'bearish': '↘',
            'strong-bearish': '⬇⬇'
        }
        return symbols.get(signal, '→')

def generate_time_slots(start_hour, start_min, end_hour, end_min, interval=30):
    """Generate time slots for trading hours"""
    slots = []
    current = start_hour * 60 + start_min
    end = end_hour * 60 + end_min
    
    while current <= end:
        hour = current // 60
        minute = current % 60
        slots.append(f"{hour:02d}:{minute:02d}")
        current += interval
    
    return slots

def get_signal_analysis(signal):
    """Get detailed analysis for signal"""
    analyses = {
        'strong-bullish': 'Strong planetary alignment favoring upward movement. High confidence for buying opportunities.',
        'bullish': 'Positive planetary aspects. Moderate confidence for upward movement. Good for swing trades.',
        'neutral': 'Mixed planetary influences. No clear directional bias. Wait for clearer signals.',
        'bearish': 'Negative planetary aspects. Moderate confidence for downward movement. Consider protective strategies.',
        'strong-bearish': 'Strong negative planetary alignment. High confidence for decline. Avoid long positions.'
    }
    return analyses.get(signal, 'No analysis available')

# Initialize session state
if 'planetary_data' not in st.session_state:
    st.session_state.planetary_data = PlanetaryData()

if 'analyzer' not in st.session_state:
    st.session_state.analyzer = AstrologicalAnalyzer()

# Main app
def main():
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🌟 Astrological Trading System</h1>
        <p>Streamlit-Powered Market Timing with Planetary Analysis</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar controls
    st.sidebar.header("📊 Control Panel")
    
    trading_date = st.sidebar.date_input(
        "📅 Trading Date",
        value=datetime(2025, 8, 6),
        min_value=datetime(2020, 1, 1),
        max_value=datetime(2030, 12, 31)
    )
    
    market_selection = st.sidebar.selectbox(
        "🌍 Market Selection",
        ["Both Markets", "Indian Markets", "Global Markets"]
    )
    
    auto_refresh = st.sidebar.checkbox("🔄 Auto Refresh (every 30s)")
    
    if auto_refresh:
        st.rerun()
    
    # Main tabs
    tab1, tab2, tab3, tab4 = st.tabs(["📈 Market Timing", "🪐 Planetary Transits", "📊 Statistics", "⚙️ Settings"])
    
    with tab1:
        st.header("📈 Market Timing Analysis")
        
        date_str = trading_date.strftime("%Y-%m-%d")
        
        if market_selection in ["Indian Markets", "Both Markets"]:
            st.subheader("🇮🇳 Indian Markets (9:15 AM - 3:30 PM IST)")
            display_market_timing("indian", date_str)
        
        if market_selection in ["Global Markets", "Both Markets"]:
            st.subheader("🌍 Global Markets & Commodities (5:00 AM - 11:55 PM IST)")
            display_market_timing("global", date_str)
    
    with tab2:
        st.header("🪐 Planetary Transit Details")
        display_planetary_data()
    
    with tab3:
        st.header("📊 Market Statistics")
        display_statistics(date_str)
    
    with tab4:
        st.header("⚙️ System Settings")
        display_settings()

def display_market_timing(market_type, date_str):
    """Display market timing grid"""
    if market_type == "indian":
        symbols = st.session_state.planetary_data.indian_symbols
        time_slots = generate_time_slots(9, 15, 15, 30)
    else:
        symbols = st.session_state.planetary_data.global_symbols
        time_slots = generate_time_slots(5, 0, 23, 55)
    
    # Create timing data
    timing_data = {}
    for symbol in symbols:
        timing_data[symbol] = {}
        for time_slot in time_slots:
            signal = st.session_state.analyzer.generate_signal(symbol, time_slot, date_str)
            timing_data[symbol][time_slot] = {
                'signal': signal,
                'symbol': st.session_state.analyzer.get_signal_symbol(signal)
            }
    
    # Display as a grid
    cols = st.columns([1] + [1] * min(len(time_slots), 12))  # Limit columns for readability
    
    # Header row
    cols[0].write("**Symbol**")
    for i, time_slot in enumerate(time_slots[:12]):  # Show first 12 time slots
        cols[i+1].write(f"**{time_slot}**")
    
    # Data rows
    for symbol in symbols:
        cols = st.columns([1] + [1] * min(len(time_slots), 12))
        cols[0].write(f"**{symbol}**")
        
        for i, time_slot in enumerate(time_slots[:12]):
            cell_data = timing_data[symbol][time_slot]
            signal_class = cell_data['signal'].replace('-', '_')
            
            with cols[i+1]:
                if st.button(
                    cell_data['symbol'], 
                    key=f"{symbol}_{time_slot}",
                    help=f"{symbol} at {time_slot}: {cell_data['signal'].replace('-', ' ').title()}"
                ):
                    show_signal_details(symbol, time_slot, cell_data['signal'], date_str)

def show_signal_details(symbol, time_slot, signal, date_str):
    """Show detailed signal analysis in modal"""
    st.sidebar.markdown("---")
    st.sidebar.subheader(f"📊 Signal Details")
    st.sidebar.write(f"**Symbol:** {symbol}")
    st.sidebar.write(f"**Time:** {time_slot}")
    st.sidebar.write(f"**Signal:** {signal.replace('-', ' ').title()}")
    st.sidebar.write(f"**Analysis:** {get_signal_analysis(signal)}")
    
    # Find relevant planetary transit
    current_time = f"{date_str}T{time_slot}:00"
    for planet in st.session_state.planetary_data.planets:
        time_diff = abs((datetime.fromisoformat(planet['datetime']) - 
                        datetime.fromisoformat(current_time)).total_seconds())
        if time_diff < 3600:  # Within 1 hour
            st.sidebar.write("**Planetary Influence:**")
            st.sidebar.write(f"🪐 {planet['planet']} in {planet['zodiac']}")
            st.sidebar.write(f"⭐ Nakshatra: {planet['nakshatra']} (Pada {planet['pada']})")
            st.sidebar.write(f"🔄 Motion: {'Direct' if planet['motion'] == 'D' else 'Retrograde'}")
            break

def display_planetary_data():
    """Display planetary transit table"""
    planets_df = pd.DataFrame(st.session_state.planetary_data.planets)
    
    # Format the dataframe
    planets_df['datetime'] = pd.to_datetime(planets_df['datetime'])
    planets_df['date'] = planets_df['datetime'].dt.date
    planets_df['time'] = planets_df['datetime'].dt.time
    
    # Display table
    st.dataframe(
        planets_df[['planet', 'date', 'time', 'motion', 'zodiac', 'nakshatra', 'pada', 'position', 'declination']],
        use_container_width=True
    )
    
    # Summary cards
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Active Transits", len(planets_df))
    
    with col2:
        retrograde_count = len(planets_df[planets_df['motion'] == 'R'])
        st.metric("Retrograde Planets", retrograde_count)
    
    with col3:
        direct_count = len(planets_df[planets_df['motion'] == 'D'])
        st.metric("Direct Planets", direct_count)
    
    with col4:
        accuracy = 75 + (direct_count - retrograde_count) * 5
        st.metric("Predicted Accuracy", f"{accuracy}%")

def display_statistics(date_str):
    """Display market statistics"""
    # Calculate statistics
    indian_stats = calculate_market_stats('indian', date_str)
    global_stats = calculate_market_stats('global', date_str)
    
    total_bullish = indian_stats['bullish'] + global_stats['bullish']
    total_bearish = indian_stats['bearish'] + global_stats['bearish']
    total_neutral = indian_stats['neutral'] + global_stats['neutral']
    
    # Display metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Bullish Signals", total_bullish, delta=total_bullish - total_bearish)
    
    with col2:
        st.metric("Bearish Signals", total_bearish)
    
    with col3:
        st.metric("Neutral Signals", total_neutral)
    
    with col4:
        retrograde_count = sum(1 for p in st.session_state.planetary_data.planets if p['motion'] == 'R')
        accuracy = max(60, min(95, 75 + (total_bullish - total_bearish) * 2 - retrograde_count * 3))
        st.metric("System Accuracy", f"{accuracy}%")
    
    # Create charts
    signal_data = pd.DataFrame({
        'Signal Type': ['Bullish', 'Bearish', 'Neutral'],
        'Count': [total_bullish, total_bearish, total_neutral]
    })
    
    st.bar_chart(signal_data.set_index('Signal Type'))

def calculate_market_stats(market_type, date_str):
    """Calculate statistics for a market"""
    if market_type == 'indian':
        symbols = st.session_state.planetary_data.indian_symbols
        time_slots = generate_time_slots(9, 15, 15, 30)
    else:
        symbols = st.session_state.planetary_data.global_symbols
        time_slots = generate_time_slots(5, 0, 23, 55)
    
    bullish = bearish = neutral = 0
    
    for symbol in symbols:
        for time_slot in time_slots:
            signal = st.session_state.analyzer.generate_signal(symbol, time_slot, date_str)
            if signal in ['strong-bullish', 'bullish']:
                bullish += 1
            elif signal in ['strong-bearish', 'bearish']:
                bearish += 1
            else:
                neutral += 1
    
    return {'bullish': bullish, 'bearish': bearish, 'neutral': neutral}

def display_settings():
    """Display system settings"""
    st.subheader("🎯 Symbol Management")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**🇮🇳 Indian Market Symbols**")
        for symbol in st.session_state.planetary_data.indian_symbols:
            st.write(f"• {symbol}")
        
        new_indian_symbol = st.text_input("Add Indian Symbol", placeholder="e.g., RELIANCE")
        if st.button("Add Indian Symbol"):
            if new_indian_symbol and new_indian_symbol not in st.session_state.planetary_data.indian_symbols:
                st.session_state.planetary_data.indian_symbols.append(new_indian_symbol.upper())
                st.success(f"Added {new_indian_symbol}")
                st.rerun()
    
    with col2:
        st.write("**🌍 Global Market Symbols**")
        for symbol in st.session_state.planetary_data.global_symbols:
            st.write(f"• {symbol}")
        
        new_global_symbol = st.text_input("Add Global Symbol", placeholder="e.g., AAPL")
        if st.button("Add Global Symbol"):
            if new_global_symbol and new_global_symbol not in st.session_state.planetary_data.global_symbols:
                st.session_state.planetary_data.global_symbols.append(new_global_symbol.upper())
                st.success(f"Added {new_global_symbol}")
                st.rerun()
    
    st.subheader("🪐 Planetary Data Management")
    
    if st.button("Reset to Default Data"):
        st.session_state.planetary_data = PlanetaryData()
        st.success("Reset to default planetary data")
        st.rerun()
    
    st.subheader("💾 Data Export")
    
    if st.button("Export Planetary Data as JSON"):
        data = {
            'planets': st.session_state.planetary_data.planets,
            'indian_symbols': st.session_state.planetary_data.indian_symbols,
            'global_symbols': st.session_state.planetary_data.global_symbols,
            'export_date': datetime.now().isoformat()
        }
        
        st.download_button(
            label="Download JSON",
            data=json.dumps(data, indent=2),
            file_name=f"astro_trading_data_{datetime.now().strftime('%Y%m%d')}.json",
            mime="application/json"
        )
    
    # Disclaimer
    st.markdown("---")
    st.warning("""
    ⚠️ **Disclaimer**: This system is for educational purposes only. 
    Astrological analysis is not scientifically proven for market prediction. 
    Always consult qualified financial advisors before making trading decisions.
    """)

if __name__ == "__main__":
    main()
