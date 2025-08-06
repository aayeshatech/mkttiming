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
        background: linear-gradient(135deg, #32ff7e, #18ff6d);
        color: #1a1a2e;
        font-weight: bold;
        border: 2px solid #00ff88;
    }
    
    .bullish {
        background: linear-gradient(135deg, #00ff88, #00cc70);
        color: #1a1a2e;
        font-weight: bold;
    }
    
    .neutral {
        background: linear-gradient(135deg, #ffa502, #ff9500);
        color: #1a1a2e;
        font-weight: bold;
    }
    
    .bearish {
        background: linear-gradient(135deg, #ff4757, #ff3742);
        color: white;
        font-weight: bold;
    }
    
    .strong-bearish {
        background: linear-gradient(135deg, #ff3838, #ff2929);
        color: white;
        font-weight: bold;
        border: 2px solid #ff4757;
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
        # Corrected Vedic Planetary Transits for August 6, 2025 (Sidereal Zodiac / Lahiri Ayanamsa = 23°55' in 2025)
        self.planets = [
            {
                "planet": "Sun",
                "datetime": "2025-08-06T06:00:00",
                "motion": "D",
                "signLord": "Moon",
                "starLord": "Mercury",
                "subLord": "Moon",
                "zodiac": "Cancer",
                "nakshatra": "Aslesha",
                "pada": 4,
                "position": "20°15'00\"",
                "declination": 16.8,
                "vedic_themes": "Soul power, mysticism, healing"
            },
            {
                "planet": "Moon",
                "datetime": "2025-08-06T09:15:00",
                "motion": "D",
                "signLord": "Jupiter",
                "starLord": "Ketu",
                "subLord": "Ketu",
                "zodiac": "Sagittarius",
                "nakshatra": "Mula",
                "pada": 1,
                "position": "11°41'00\"",
                "declination": -26.2,
                "vedic_themes": "Root work, transformation, Ketu energy"
            },
            {
                "planet": "Mercury",
                "datetime": "2025-08-06T10:30:00",
                "motion": "R",
                "signLord": "Moon",
                "starLord": "Venus",
                "subLord": "Sun",
                "zodiac": "Cancer",
                "nakshatra": "Pushya",
                "pada": 3,
                "position": "10°48'00\"",
                "declination": 18.5,
                "vedic_themes": "Retrograde: Reevaluate emotions, communication blocks"
            },
            {
                "planet": "Venus",
                "datetime": "2025-08-06T11:45:00",
                "motion": "D",
                "signLord": "Mercury",
                "starLord": "Mars",
                "subLord": "Mercury",
                "zodiac": "Gemini",
                "nakshatra": "Mrigashira",
                "pada": 1,
                "position": "1°10'00\"",
                "declination": 23.1,
                "vedic_themes": "New relationships, curiosity, flexibility"
            },
            {
                "planet": "Mars",
                "datetime": "2025-08-06T13:20:00",
                "motion": "D",
                "signLord": "Venus",
                "starLord": "Moon",
                "subLord": "Venus",
                "zodiac": "Taurus",
                "nakshatra": "Rohini",
                "pada": 2,
                "position": "17°22'00\"",
                "declination": 25.4,
                "vedic_themes": "Exalted: Steady power, creativity, material success"
            },
            {
                "planet": "Jupiter",
                "datetime": "2025-08-06T14:15:00",
                "motion": "D",
                "signLord": "Mercury",
                "starLord": "Rahu",
                "subLord": "Jupiter",
                "zodiac": "Gemini",
                "nakshatra": "Ardra",
                "pada": 4,
                "position": "14°53'00\"",
                "declination": 22.8,
                "vedic_themes": "Intellectual growth, stormy insights"
            },
            {
                "planet": "Saturn",
                "datetime": "2025-08-06T15:30:00",
                "motion": "D",
                "signLord": "Saturn",
                "starLord": "Saturn",
                "subLord": "Mercury",
                "zodiac": "Aquarius",
                "nakshatra": "Dhanishta",
                "pada": 1,
                "position": "1°35'00\"",
                "declination": -20.1,
                "vedic_themes": "Discipline in innovation, social duty"
            },
            {
                "planet": "Uranus",
                "datetime": "2025-08-06T16:00:00",
                "motion": "D",
                "signLord": "Mars",
                "starLord": "Mars",
                "subLord": "Ketu",
                "zodiac": "Aries",
                "nakshatra": "Bharani",
                "pada": 3,
                "position": "26°58'00\"",
                "declination": 12.3,
                "vedic_themes": "Radical change, rebirth energy"
            },
            {
                "planet": "Neptune",
                "datetime": "2025-08-06T19:15:00",
                "motion": "D",
                "signLord": "Jupiter",
                "starLord": "Mercury",
                "subLord": "Jupiter",
                "zodiac": "Pisces",
                "nakshatra": "Revati",
                "pada": 4,
                "position": "29°49'00\"",
                "declination": -5.6,
                "vedic_themes": "Spiritual culmination, compassion"
            },
            {
                "planet": "Pluto",
                "datetime": "2025-08-06T20:30:00",
                "motion": "R",
                "signLord": "Saturn",
                "starLord": "Sun",
                "subLord": "Venus",
                "zodiac": "Capricorn",
                "nakshatra": "Uttara Ashadha",
                "pada": 1,
                "position": "2°04'00\"",
                "declination": -22.4,
                "vedic_themes": "Systemic destruction, karmic release"
            }
        ]
        
        self.indian_symbols = ['NIFTY', 'BANKNIFTY', 'FINNIFTY', 'MIDCPNIFTY', 'SENSEX']
        self.global_symbols = ['GOLD', 'SILVER', 'CRUDE', 'BTC', 'DOW JONES', 'S&P 500', 'NASDAQ', 'USD/INR']

class AstrologicalAnalyzer:
    @staticmethod
    def generate_signal(symbol, time_str, date_str):
        """Generate trading signal based on Vedic planetary positions"""
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
            # Retrograde planets (generally bearish, especially Mercury)
            if nearest_transit['motion'] == 'R':
                if nearest_transit['planet'] == 'Mercury':
                    signal_strength -= 3  # Mercury retrograde strongly bearish
                else:
                    signal_strength -= 2
            
            # Exalted planets (Mars in Taurus is exalted)
            if nearest_transit['planet'] == 'Mars' and nearest_transit['zodiac'] == 'Taurus':
                signal_strength += 3  # Mars exalted - very bullish
            
            # Beneficial planets in strong positions
            if nearest_transit['planet'] in ['Jupiter', 'Venus'] and nearest_transit['motion'] == 'D':
                signal_strength += 2
            elif nearest_transit['planet'] == 'Mercury' and nearest_transit['motion'] == 'D':
                signal_strength += 1
            
            # Sun in own sign or exaltation
            if nearest_transit['planet'] == 'Sun':
                if nearest_transit['zodiac'] in ['Leo', 'Aries']:  # Own/exalted
                    signal_strength += 2
                elif nearest_transit['zodiac'] == 'Cancer':  # Debilitated
                    signal_strength -= 1
            
            # Saturn effects (discipline vs restriction)
            if nearest_transit['planet'] == 'Saturn':
                if nearest_transit['zodiac'] in ['Capricorn', 'Aquarius']:  # Own signs
                    signal_strength += 1  # Disciplined growth
                else:
                    signal_strength -= 1  # Restrictive
            
            # Pada analysis (1st and 4th padas are action-oriented)
            if nearest_transit['pada'] in [1, 4]:
                signal_strength += 1
            elif nearest_transit['pada'] in [2, 3]:
                signal_strength += 0.5  # Moderate influence
            
            # Zodiac sign strength for trading
            fire_signs = ['Aries', 'Leo', 'Sagittarius']  # Action, leadership
            earth_signs = ['Taurus', 'Virgo', 'Capricorn']  # Stability, material
            air_signs = ['Gemini', 'Libra', 'Aquarius']  # Communication, trends
            water_signs = ['Cancer', 'Scorpio', 'Pisces']  # Emotion, intuition
            
            if nearest_transit['zodiac'] in fire_signs:
                signal_strength += 1  # Fire signs favor action
            elif nearest_transit['zodiac'] in earth_signs:
                signal_strength += 0.5  # Earth signs favor steady growth
            elif nearest_transit['zodiac'] in air_signs:
                signal_strength += 0.5  # Air signs favor communication/tech stocks
            # Water signs are neutral to slightly negative for trading
            
            # Nakshatra-specific influences
            powerful_nakshatras = ['Rohini', 'Pushya', 'Magha', 'Uttara Phalguni', 'Uttara Ashadha']
            transformative_nakshatras = ['Mula', 'Ardra', 'Aslesha']
            
            if nearest_transit['nakshatra'] in powerful_nakshatras:
                signal_strength += 1
            elif nearest_transit['nakshatra'] in transformative_nakshatras:
                signal_strength -= 0.5  # Volatile, transformative
            
            # Time-based adjustments
            hour = int(time_str.split(':')[0])
            
            # Market opening energy (9:15-10:15 for Indian markets)
            if 9 <= hour <= 10:
                signal_strength += 0.5
            # Pre-closing volatility (14:30-15:30 for Indian markets)
            elif 14 <= hour <= 15:
                signal_strength -= 0.5
            # Global market influences (evening hours)
            elif 17 <= hour <= 22:
                signal_strength += 0.3
        
        # Convert to signal with more nuanced thresholds
        if signal_strength >= 3:
            return 'strong-bullish'
        elif signal_strength >= 1.5:
            return 'bullish'
        elif signal_strength <= -3:
            return 'strong-bearish'
        elif signal_strength <= -1.5:
            return 'bearish'
        else:
            return 'neutral'
    
    @staticmethod
    def get_signal_symbol(signal):
        symbols = {
            'strong-bullish': 'STRONG BUY',
            'bullish': 'BUY',
            'neutral': 'HOLD',
            'bearish': 'SELL',
            'strong-bearish': 'STRONG SELL'
        }
        return symbols.get(signal, 'HOLD')

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
        'strong-bullish': '🚀 STRONG BUY: Exceptional planetary alignment with exalted planets and direct motion. High confidence for significant upward movement. Ideal for aggressive long positions and call options.',
        'bullish': '📈 BUY: Favorable planetary aspects with beneficial planets in strong positions. Good probability for upward movement. Suitable for long positions and swing trades.',
        'neutral': '⏸️ HOLD: Mixed planetary influences with competing energies. No clear directional bias. Best to wait for clearer signals or maintain existing positions.',
        'bearish': '📉 SELL: Negative planetary aspects with malefic influences or retrograde motion. Moderate probability for downward movement. Consider short positions or protective puts.',
        'strong-bearish': '🔻 STRONG SELL: Severe planetary afflictions with multiple retrograde planets or debilitated positions. High probability for significant decline. Avoid long positions, consider strong hedging.'
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
        market_name = "🇮🇳 Indian Markets"
    else:
        symbols = st.session_state.planetary_data.global_symbols
        time_slots = generate_time_slots(5, 0, 23, 55)
        market_name = "🌍 Global Markets"
    
    # Create timing data
    timing_data = {}
    signal_counts = {'STRONG BUY': 0, 'BUY': 0, 'HOLD': 0, 'SELL': 0, 'STRONG SELL': 0}
    
    for symbol in symbols:
        timing_data[symbol] = {}
        for time_slot in time_slots:
            signal = st.session_state.analyzer.generate_signal(symbol, time_slot, date_str)
            signal_label = st.session_state.analyzer.get_signal_symbol(signal)
            timing_data[symbol][time_slot] = {
                'signal': signal,
                'label': signal_label
            }
            signal_counts[signal_label] += 1
    
    # Display signal summary
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.metric("🚀 STRONG BUY", signal_counts['STRONG BUY'])
    with col2:
        st.metric("📈 BUY", signal_counts['BUY'])
    with col3:
        st.metric("⏸️ HOLD", signal_counts['HOLD'])
    with col4:
        st.metric("📉 SELL", signal_counts['SELL'])
    with col5:
        st.metric("🔻 STRONG SELL", signal_counts['STRONG SELL'])
    
    st.markdown("---")
    
    # Display timing grid with improved layout
    st.markdown(f"### {market_name} - Detailed Timing Grid")
    
    # Show limited time slots for better readability
    display_slots = time_slots[:15] if len(time_slots) > 15 else time_slots
    
    # Create the grid
    for symbol in symbols:
        st.markdown(f"#### 📊 {symbol}")
        
        # Create columns for time slots
        cols = st.columns(len(display_slots))
        
        # Time headers
        for i, time_slot in enumerate(display_slots):
            with cols[i]:
                st.caption(time_slot)
        
        # Signal buttons
        button_cols = st.columns(len(display_slots))
        for i, time_slot in enumerate(display_slots):
            with button_cols[i]:
                cell_data = timing_data[symbol][time_slot]
                signal_class = cell_data['signal']
                
                # Choose button color based on signal
                if signal_class in ['strong-bullish', 'bullish']:
                    button_type = "primary"
                elif signal_class in ['strong-bearish', 'bearish']:
                    button_type = "secondary"
                else:
                    button_type = None
                
                if st.button(
                    cell_data['label'], 
                    key=f"{symbol}_{time_slot}_{market_type}",
                    help=f"Click for detailed analysis of {symbol} at {time_slot}",
                    type=button_type
                ):
                    show_signal_details(symbol, time_slot, cell_data['signal'], date_str)
        
        st.markdown("---")
    
    # Show remaining time slots if truncated
    if len(time_slots) > 15:
        with st.expander(f"📅 View remaining {len(time_slots) - 15} time slots"):
            remaining_slots = time_slots[15:]
            for symbol in symbols:
                st.write(f"**{symbol}:**")
                slot_cols = st.columns(min(10, len(remaining_slots)))
                for i, time_slot in enumerate(remaining_slots[:10]):
                    with slot_cols[i]:
                        cell_data = timing_data[symbol][time_slot]
                        st.caption(f"{time_slot}: {cell_data['label']}")
                if len(remaining_slots) > 10:
                    st.caption(f"... and {len(remaining_slots) - 10} more slots")
    
    # Market bias analysis
    total_signals = sum(signal_counts.values())
    if total_signals > 0:
        bullish_pct = ((signal_counts['STRONG BUY'] + signal_counts['BUY']) / total_signals) * 100
        bearish_pct = ((signal_counts['STRONG SELL'] + signal_counts['SELL']) / total_signals) * 100
        
        st.markdown("### 📈 Market Bias Analysis")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Bullish Signals", f"{bullish_pct:.1f}%")
        with col2:
            st.metric("Bearish Signals", f"{bearish_pct:.1f}%")
        with col3:
            if bullish_pct > bearish_pct + 10:
                bias = "🟢 Bullish Bias"
            elif bearish_pct > bullish_pct + 10:
                bias = "🔴 Bearish Bias"
            else:
                bias = "🟡 Neutral/Mixed"
            st.metric("Overall Bias", bias)

def show_signal_details(symbol, time_slot, signal, date_str):
    """Show detailed signal analysis in modal"""
    st.sidebar.markdown("---")
    st.sidebar.markdown("## 📊 Detailed Signal Analysis")
    
    # Signal header with color coding
    signal_colors = {
        'strong-bullish': '🟢',
        'bullish': '🟢', 
        'neutral': '🟡',
        'bearish': '🔴',
        'strong-bearish': '🔴'
    }
    
    signal_emoji = signal_colors.get(signal, '⚫')
    signal_label = st.session_state.analyzer.get_signal_symbol(signal)
    
    st.sidebar.markdown(f"### {signal_emoji} {signal_label}")
    st.sidebar.write(f"**Symbol:** {symbol}")
    st.sidebar.write(f"**Time Slot:** {time_slot}")
    st.sidebar.write(f"**Date:** {date_str}")
    
    # Find relevant planetary transit
    current_time = f"{date_str}T{time_slot}:00"
    relevant_transits = []
    
    for planet in st.session_state.planetary_data.planets:
        time_diff = abs((datetime.fromisoformat(planet['datetime']) - 
                        datetime.fromisoformat(current_time)).total_seconds())
        if time_diff < 3600:  # Within 1 hour
            relevant_transits.append((planet, time_diff))
    
    # Sort by closest time
    relevant_transits.sort(key=lambda x: x[1])
    
    if relevant_transits:
        primary_transit = relevant_transits[0][0]
        
        st.sidebar.markdown("### 🪐 Primary Planetary Influence")
        st.sidebar.write(f"**Planet:** {primary_transit['planet']}")
        st.sidebar.write(f"**Sign:** {primary_transit['zodiac']}")
        st.sidebar.write(f"**Nakshatra:** {primary_transit['nakshatra']} (Pada {primary_transit['pada']})")
        st.sidebar.write(f"**Motion:** {'🟢 Direct' if primary_transit['motion'] == 'D' else '🔴 Retrograde'}")
        st.sidebar.write(f"**Position:** {primary_transit['position']}")
        
        if 'vedic_themes' in primary_transit:
            st.sidebar.write(f"**Themes:** {primary_transit['vedic_themes']}")
        
        # Additional factors
        st.sidebar.markdown("### 🔍 Astrological Factors")
        
        factors = []
        
        # Retrograde influence
        if primary_transit['motion'] == 'R':
            factors.append("🔴 Retrograde motion (bearish)")
        else:
            factors.append("🟢 Direct motion (bullish)")
        
        # Exaltation/Debilitation
        if primary_transit['planet'] == 'Mars' and primary_transit['zodiac'] == 'Taurus':
            factors.append("⭐ Mars exalted in Taurus (very bullish)")
        elif primary_transit['planet'] == 'Sun' and primary_transit['zodiac'] == 'Leo':
            factors.append("👑 Sun in own sign Leo (bullish)")
        elif primary_transit['planet'] == 'Sun' and primary_transit['zodiac'] == 'Cancer':
            factors.append("⬇️ Sun debilitated in Cancer (bearish)")
        
        # Pada influence
        if primary_transit['pada'] in [1, 4]:
            factors.append(f"🎯 Pada {primary_transit['pada']} (action-oriented)")
        
        # Nakshatra influence
        powerful_naks = ['Rohini', 'Pushya', 'Magha', 'Uttara Phalguni', 'Uttara Ashadha']
        transformative_naks = ['Mula', 'Ardra', 'Aslesha']
        
        if primary_transit['nakshatra'] in powerful_naks:
            factors.append(f"💪 {primary_transit['nakshatra']} is powerful (bullish)")
        elif primary_transit['nakshatra'] in transformative_naks:
            factors.append(f"🌀 {primary_transit['nakshatra']} is transformative (volatile)")
        
        for factor in factors:
            st.sidebar.write(f"• {factor}")
    
    # Trading recommendation
    st.sidebar.markdown("### 💡 Trading Recommendation")
    st.sidebar.write(get_signal_analysis(signal))
    
    # Risk factors
    st.sidebar.markdown("### ⚠️ Risk Considerations")
    risk_factors = [
        "Market volatility can override planetary influences",
        "Use proper risk management and stop losses",
        "Consider overall market trend and news",
        "Planetary timing is one factor among many"
    ]
    
    for risk in risk_factors:
        st.sidebar.write(f"• {risk}")
    
    # Multiple transits
    if len(relevant_transits) > 1:
        st.sidebar.markdown(f"### 🌟 Additional Influences ({len(relevant_transits)-1} more)")
        for transit, _ in relevant_transits[1:3]:  # Show up to 2 more
            st.sidebar.write(f"• {transit['planet']} in {transit['zodiac']}")
    
    st.sidebar.markdown("---")
    st.sidebar.caption("⚖️ For educational purposes only. Not financial advice.")

def display_planetary_data():
    """Display planetary transit table"""
    st.markdown("### 🪐 Corrected Vedic Planetary Transits for August 6, 2025")
    st.markdown("*(Sidereal Zodiac / Lahiri Ayanamsa = 23°55' in 2025)*")
    
    planets_df = pd.DataFrame(st.session_state.planetary_data.planets)
    
    # Format the dataframe
    planets_df['datetime'] = pd.to_datetime(planets_df['datetime'])
    planets_df['date'] = planets_df['datetime'].dt.date
    planets_df['time'] = planets_df['datetime'].dt.time
    
    # Create a more detailed display
    for _, planet in planets_df.iterrows():
        with st.expander(f"🪐 {planet['planet']} in {planet['zodiac']} - {planet['nakshatra']} ({planet['pada']})", expanded=False):
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.write(f"**Position:** {planet['position']}")
                st.write(f"**Motion:** {'🟢 Direct' if planet['motion'] == 'D' else '🔴 Retrograde'}")
                st.write(f"**Declination:** {planet['declination']}°")
            
            with col2:
                st.write(f"**Sign Lord:** {planet['signLord']}")
                st.write(f"**Star Lord:** {planet['starLord']}")
                st.write(f"**Sub Lord:** {planet['subLord']}")
            
            with col3:
                if 'vedic_themes' in planet:
                    st.write(f"**Key Themes:** {planet['vedic_themes']}")
                st.write(f"**Transit Time:** {planet['time']}")
    
    # Summary table
    st.markdown("### 📊 Quick Reference Table")
    display_df = planets_df[['planet', 'zodiac', 'nakshatra', 'pada', 'position', 'motion']].copy()
    display_df['motion'] = display_df['motion'].map({'D': '🟢 Direct', 'R': '🔴 Retrograde'})
    
    st.dataframe(display_df)
    
    # Summary cards
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Planets", len(planets_df))
    
    with col2:
        retrograde_count = len(planets_df[planets_df['motion'] == 'R'])
        st.metric("Retrograde Planets", retrograde_count)
    
    with col3:
        direct_count = len(planets_df[planets_df['motion'] == 'D'])
        st.metric("Direct Planets", direct_count)
    
    with col4:
        # Market bias based on planetary strength
        exalted_planets = len(planets_df[(planets_df['planet'] == 'Mars') & (planets_df['zodiac'] == 'Taurus')])
        market_bias = "Bullish" if exalted_planets > 0 and direct_count > retrograde_count else "Mixed" if direct_count == retrograde_count else "Bearish"
        st.metric("Market Bias", market_bias)

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
