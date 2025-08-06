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
    .bullish-transit { background-color: rgba(0, 255, 136, 0.1); padding: 0.5rem; border-left: 4px solid #00ff88; margin: 0.5rem 0; }
    .bearish-transit { background-color: rgba(255, 71, 87, 0.1); padding: 0.5rem; border-left: 4px solid #ff4757; margin: 0.5rem 0; }
    .neutral-transit { background-color: rgba(255, 165, 2, 0.1); padding: 0.5rem; border-left: 4px solid #ffa502; margin: 0.5rem 0; }
    .turning-point { background: linear-gradient(90deg, #ff6b6b, #4ecdc4); color: white; padding: 0.5rem; border-radius: 5px; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

# Base Planetary Data for August 6, 2025
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

# Base Transit Aspects for August 6, 2025
@st.cache_data
def get_base_transit_aspects():
    return [
        {
            "time": "02:06", "aspect": "Moon Quintile Node", "planets": "Moon ⚹ ☊",
            "positions": "Moon 6° Capricorn 48', Node 18° Pisces 48'",
            "market_impact": "bullish", "strength": 2, "duration_hours": 4,
            "sectors": ["Banking", "Real Estate", "Traditional Assets"],
            "description": "Karmic opportunity in emotional/security sectors"
        },
        {
            "time": "02:34", "aspect": "Moon Bi Quintile Uranus", "planets": "♃ bQ ♅",
            "positions": "Moon 7° Capricorn 3', Uranus 1° Gemini 3'",
            "market_impact": "neutral", "strength": 1, "duration_hours": 2,
            "sectors": ["Technology", "Innovation", "Cryptocurrency"],
            "description": "Creative breakthrough in tech sectors"
        },
        {
            "time": "02:38", "aspect": "Moon Opposition Venus", "planets": "♃ ☍ ♀",
            "positions": "Moon 7° Capricorn 5', Venus 7° Cancer 5'",
            "market_impact": "bearish", "strength": 3, "duration_hours": 6,
            "sectors": ["Luxury", "Beauty", "Entertainment", "Retail"],
            "description": "Emotional vs material value conflicts"
        },
        {
            "time": "04:38", "aspect": "Sun Bi Quintile Moon", "planets": "☉ bQ ♃",
            "positions": "Sun 14° Leo 9', Moon 8° Capricorn 9'",
            "market_impact": "bullish", "strength": 2, "duration_hours": 8,
            "sectors": ["Leadership", "Government", "Gold", "Energy"],
            "description": "Creative authority and emotional stability"
        },
        {
            "time": "10:25", "aspect": "Mars Semi Square Lilith", "planets": "♂ ∠ ⚸",
            "positions": "Mars 29° Virgo 46', Lilith 14° Scorpio 46'",
            "market_impact": "bearish", "strength": 4, "duration_hours": 3,
            "sectors": ["Defense", "Mining", "Steel", "Energy"],
            "description": "Aggressive energy meets shadow resistance"
        },
        {
            "time": "13:39", "aspect": "Moon Opposition Jupiter", "planets": "♃ ☍ ♃",
            "positions": "Moon 12° Capricorn 55', Jupiter 12° Cancer 55'",
            "market_impact": "bearish", "strength": 5, "duration_hours": 4,
            "sectors": ["Banking", "Finance", "Education", "International Trade"],
            "description": "Overexpansion vs conservative approach - Major turning point"
        },
        {
            "time": "16:53", "aspect": "Sun Quincunx Moon", "planets": "☉ ⚻ ♃",
            "positions": "Sun 14° Leo 38', Moon 14° Capricorn 38'",
            "market_impact": "neutral", "strength": 3, "duration_hours": 6,
            "sectors": ["Healthcare", "Public Services", "Utilities"],
            "description": "Adjustment needed between leadership and public needs"
        },
        {
            "time": "17:10", "aspect": "Moon Sextile Lilith", "planets": "♃ ⚹ ⚸",
            "positions": "Moon 14° Capricorn 47', Lilith 14° Scorpio 47'",
            "market_impact": "bullish", "strength": 2, "duration_hours": 3,
            "sectors": ["Alternative Energy", "Biotech", "Pharmaceuticals"],
            "description": "Productive integration of shadow elements"
        },
        {
            "time": "19:35", "aspect": "Moon Sesquiquadrate Uranus", "planets": "♃ ⚼ ♅",
            "positions": "Moon 16° Capricorn 4', Uranus 1° Gemini 4'",
            "market_impact": "bearish", "strength": 3, "duration_hours": 2,
            "sectors": ["Technology", "Cryptocurrency", "Startups"],
            "description": "Sudden disruption in emotional/security patterns"
        },
        {
            "time": "21:18", "aspect": "Sun Square Lilith", "planets": "☉ □ ⚸",
            "positions": "Sun 14° Leo 49', Lilith 14° Scorpio 49'",
            "market_impact": "bearish", "strength": 4, "duration_hours": 5,
            "sectors": ["Leadership", "Government", "Power", "Authority"],
            "description": "Authority confronts shadow - Evening volatility peak"
        }
    ]

def calculate_planetary_positions_for_date(base_date, target_date):
    """Calculate planetary positions for any date based on daily motion"""
    base_planets = get_base_planetary_data()
    
    daily_motions = {
        "Sun": 1.0, "Moon": 13.2, "Mercury": 1.4, "Venus": 1.2, "Mars": 0.5,
        "Jupiter": 0.083, "Saturn": 0.033, "Uranus": 0.0167, "Neptune": 0.006, "Pluto": 0.003
    }
    
    days_diff = (target_date - base_date).days
    updated_planets = []
    
    for planet_data in base_planets:
        planet_name = planet_data["planet"]
        current_degree = float(planet_data["degree"].split('°')[0]) + float(planet_data["degree"].split('°')[1].replace("'", "")) / 60
        
        motion_direction = -1 if planet_data["motion"] == "R" else 1
        daily_motion = daily_motions.get(planet_name, 0.1) * motion_direction
        
        new_degree = current_degree + (daily_motion * days_diff)
        
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

def calculate_daily_transits(base_date, target_date):
    """Calculate transit aspects for any date"""
    base_transits = get_base_transit_aspects()
    days_diff = (target_date - base_date).days
    
    # For simplicity, we'll cycle through transits with some variation
    # In real implementation, you'd calculate exact planetary aspects
    updated_transits = []
    
    for i, transit in enumerate(base_transits):
        # Simulate daily progression of aspects
        base_hour = int(transit["time"].split(':')[0])
        base_min = int(transit["time"].split(':')[1])
        
        # Add some daily variation (±2 hours)
        hour_variation = (days_diff * 0.5 + i * 0.3) % 4 - 2
        new_hour = max(0, min(23, base_hour + int(hour_variation)))
        new_min = max(0, min(59, base_min + int((hour_variation % 1) * 60)))
        
        updated_transit = transit.copy()
        updated_transit["time"] = f"{new_hour:02d}:{new_min:02d}"
        
        # Vary strength slightly based on date
        strength_variation = (days_diff % 3) * 0.5 - 0.5
        updated_transit["strength"] = max(1, min(5, transit["strength"] + strength_variation))
        
        updated_transits.append(updated_transit)
    
    return updated_transits

def get_sector_impact(transits, sector):
    """Calculate overall impact for a specific sector"""
    sector_impacts = []
    
    for transit in transits:
        if sector in transit["sectors"]:
            impact_value = transit["strength"]
            if transit["market_impact"] == "bearish":
                impact_value *= -1
            elif transit["market_impact"] == "neutral":
                impact_value *= 0.5
                
            sector_impacts.append({
                "time": transit["time"],
                "impact": impact_value,
                "aspect": transit["aspect"],
                "description": transit["description"]
            })
    
    return sector_impacts

def get_turning_points(transits):
    """Identify major market turning points"""
    turning_points = []
    
    for transit in transits:
        if transit["strength"] >= 4:  # High impact transits
            turning_points.append({
                "time": transit["time"],
                "type": "Major Turning Point",
                "direction": transit["market_impact"].upper(),
                "aspect": transit["aspect"],
                "sectors": transit["sectors"],
                "strength": transit["strength"]
            })
    
    return sorted(turning_points, key=lambda x: x["time"])

def advanced_signal_generation(planet_data, transits, symbol, time_slot, date):
    """Enhanced signal generation including transit aspects"""
    signal_strength = 0
    hour = int(time_slot.split(':')[0])
    minute = int(time_slot.split(':')[1])
    current_minutes = hour * 60 + minute
    
    # Original planetary influences
    mars_data = next((p for p in planet_data if p["planet"] == "Mars"), None)
    if mars_data and mars_data["sign"] == "Taurus":
        signal_strength += 3
        if mars_data["nakshatra"] == "Rohini":
            signal_strength += 1
    
    mercury_data = next((p for p in planet_data if p["planet"] == "Mercury"), None)
    if mercury_data and mercury_data["motion"] == "R":
        if symbol in ["BTC", "NASDAQ"]:
            signal_strength -= 3
        else:
            signal_strength -= 2
    
    # Transit aspect influences
    for transit in transits:
        transit_hour = int(transit["time"].split(':')[0])
        transit_minute = int(transit["time"].split(':')[1])
        transit_minutes = transit_hour * 60 + transit_minute
        
        # Check if current time is within transit influence window
        time_diff = abs(current_minutes - transit_minutes)
        duration_minutes = transit["duration_hours"] * 60
        
        if time_diff <= duration_minutes // 2:
            # Apply transit influence
            influence = transit["strength"] * (1 - time_diff / (duration_minutes // 2))
            
            # Check if symbol/sector is affected
            symbol_sectors = {
                "NIFTY": ["Banking", "Finance"], "BANKNIFTY": ["Banking", "Finance"],
                "BTC": ["Technology", "Cryptocurrency"], "GOLD": ["Traditional Assets"],
                "CRUDE": ["Energy"], "NASDAQ": ["Technology"], "USD/INR": ["International Trade"]
            }
            
            affected_sectors = symbol_sectors.get(symbol, [])
            sector_match = any(sector in transit["sectors"] for sector in affected_sectors)
            
            if sector_match or len(affected_sectors) == 0:  # Apply to all if no specific sectors
                if transit["market_impact"] == "bullish":
                    signal_strength += influence
                elif transit["market_impact"] == "bearish":
                    signal_strength -= influence
                else:  # neutral
                    signal_strength += influence * 0.3
    
    # Add time-based and randomness
    if 9 <= hour <= 10:
        signal_strength += 0.5
    elif 14 <= hour <= 15:
        signal_strength -= 0.5
    elif 17 <= hour <= 20:
        signal_strength += 0.3
    
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
        <h1>🌟 Enhanced Astrological Trading System</h1>
        <p>Daily Transit Calculations with Market Timing & Sector Analysis</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar
    st.sidebar.header("📊 Control Panel")
    
    # Date selection
    trading_date = st.sidebar.date_input(
        "📅 Trading Date", 
        value=datetime(2025, 8, 6),
        help="Select any date for automatic planetary & transit calculation"
    )
    
    # Market selection
    market_type = st.sidebar.selectbox(
        "🌍 Market Type",
        ["Indian Markets", "Global Markets", "Both Markets"]
    )
    
    # Sector selection for focused analysis
    sector_focus = st.sidebar.selectbox(
        "🎯 Sector Focus",
        ["All Sectors", "Banking & Finance", "Technology", "Energy", "Healthcare", 
         "Real Estate", "Cryptocurrency", "Commodities", "International Trade"]
    )
    
    # Symbol management (keeping original functionality)
    st.sidebar.subheader("🎯 Symbol Management")
    
    default_indian = ["NIFTY", "BANKNIFTY", "FINNIFTY", "MIDCPNIFTY", "SENSEX"]
    default_global = ["GOLD", "SILVER", "CRUDE", "BTC", "DOWJONES", "NASDAQ", "SPX", "USD/INR"]
    
    if 'indian_symbols' not in st.session_state:
        st.session_state.indian_symbols = default_indian.copy()
    if 'global_symbols' not in st.session_state:
        st.session_state.global_symbols = default_global.copy()
    
    # Calculate planetary positions and transits
    base_date = datetime(2025, 8, 6).date()
    planet_data = calculate_planetary_positions_for_date(base_date, trading_date)
    daily_transits = calculate_daily_transits(base_date, trading_date)
    
    # Main tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["📈 Market Signals", "🪐 Planetary Transits", "⏰ Daily Transit Aspects", "📊 Sector Analysis", "🔄 Turning Points"])
    
    with tab1:
        st.header("📈 Enhanced Market Timing Signals")
        st.info(f"🔮 Signals calculated with planetary positions + transit aspects for {trading_date.strftime('%B %d, %Y')}")
        
        if market_type in ["Indian Markets", "Both Markets"]:
            st.subheader("🇮🇳 Indian Markets (9:15 AM - 3:30 PM IST)")
            
            indian_times = generate_time_slots(9, 15, 15, 30, 30)
            indian_data = []
            
            for symbol in st.session_state.indian_symbols:
                row = {"Symbol": symbol}
                for time_slot in indian_times:
                    signal = advanced_signal_generation(planet_data, daily_transits, symbol, time_slot, trading_date)
                    row[time_slot] = signal
                indian_data.append(row)
            
            df_indian = pd.DataFrame(indian_data)
            st.dataframe(df_indian, height=300)
        
        if market_type in ["Global Markets", "Both Markets"]:
            st.subheader("🌍 Global Markets (5:00 AM - 11:35 PM IST)")
            
            global_times = generate_time_slots(5, 0, 23, 35, 60)
            global_data = []
            
            for symbol in st.session_state.global_symbols:
                row = {"Symbol": symbol}
                for time_slot in global_times:
                    signal = advanced_signal_generation(planet_data, daily_transits, symbol, time_slot, trading_date)
                    row[time_slot] = signal
                global_data.append(row)
            
            df_global = pd.DataFrame(global_data)
            st.dataframe(df_global, height=300)
    
    with tab2:
        st.header(f"🪐 Planetary Transits for {trading_date.strftime('%B %d, %Y')}")
        st.caption("(Sidereal Zodiac / Lahiri Ayanamsa = 23°55' in 2025)")
        
        if trading_date != base_date:
            st.warning(f"⚡ Positions auto-calculated from base date {base_date.strftime('%B %d, %Y')}")
        
        planet_df = pd.DataFrame(planet_data)
        planet_df['Market Influence'] = planet_df.apply(lambda row: 
            "🟢 Very Bullish" if (row['planet'] == 'Mars' and row['sign'] == 'Taurus') else
            "🔴 Very Bearish" if (row['planet'] == 'Mercury' and row['motion'] == 'R') else
            "🟢 Bullish" if row['motion'] == 'D' and row['planet'] in ['Jupiter', 'Venus'] else
            "🔴 Bearish" if row['motion'] == 'R' else
            "🟡 Neutral", axis=1
        )
        
        st.dataframe(planet_df[['planet', 'sign', 'degree', 'nakshatra', 'pada', 'motion', 'Market Influence', 'themes']], height=400)
    
    with tab3:
        st.header(f"⏰ Daily Transit Aspects - {trading_date.strftime('%B %d, %Y')}")
        st.info("🎯 Precise timing of planetary aspects affecting market sentiment throughout the day")
        
        # Display transit aspects in chronological order
        for transit in sorted(daily_transits, key=lambda x: x["time"]):
            impact_class = f"{transit['market_impact']}-transit"
            
            impact_emoji = "🟢" if transit["market_impact"] == "bullish" else "🔴" if transit["market_impact"] == "bearish" else "🟡"
            strength_stars = "⭐" * int(transit["strength"])
            
            st.markdown(f"""
            <div class="{impact_class}">
                <strong>{transit['time']} - {transit['aspect']}</strong> {impact_emoji} {strength_stars}<br>
                <small>{transit['planets']} | {transit['positions']}</small><br>
                📝 {transit['description']}<br>
                🎯 <strong>Sectors:</strong> {', '.join(transit['sectors'])}<br>
                ⏱️ <strong>Duration:</strong> {transit['duration_hours']} hours
            </div>
            """, unsafe_allow_html=True)
    
    with tab4:
        st.header("📊 Sector-Specific Analysis")
        
        # Sector selection for detailed analysis
        if sector_focus != "All Sectors":
            sector_name = sector_focus.replace("& ", "").replace(" ", "")
            sector_impacts = get_sector_impact(daily_transits, sector_focus.split(" & ")[0])
            
            if sector_impacts:
                st.subheader(f"🎯 {sector_focus} Impact Timeline")
                
                # Create timeline chart data
                impact_df = pd.DataFrame(sector_impacts)
                impact_df['time_numeric'] = impact_df['time'].apply(lambda x: int(x.split(':')[0]) + int(x.split(':')[1])/60)
                
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    st.line_chart(impact_df.set_index('time_numeric')['impact'])
                
                with col2:
                    total_impact = sum([abs(i['impact']) for i in sector_impacts])
                    bullish_impact = sum([i['impact'] for i in sector_impacts if i['impact'] > 0])
                    bearish_impact = sum([i['impact'] for i in sector_impacts if i['impact'] < 0])
                    
                    st.metric("Total Impact", f"{total_impact:.1f}")
                    st.metric("Bullish Impact", f"{bullish_impact:.1f}")
                    st.metric("Bearish Impact", f"{bearish_impact:.1f}")
                
                # Detailed impact events
                st.subheader("📋 Detailed Impact Events")
                for impact in sector_impacts:
                    impact_color = "🟢" if impact['impact'] > 0 else "🔴" if impact['impact'] < 0 else "🟡"
                    st.write(f"{impact_color} **{impact['time']}** - {impact['aspect']} (Impact: {impact['impact']:.1f})")
                    st.caption(f"📝 {impact['description']}")
            else:
                st.info(f"No specific transits affecting {sector_focus} today.")
        else:
            # Show all sectors overview
            st.subheader("🌐 All Sectors Overview")
            
            sectors = ["Banking", "Technology", "Energy", "Healthcare", "Real Estate", 
                      "Cryptocurrency", "Commodities", "International Trade"]
            
            sector_data = []
            for sector in sectors:
                impacts = get_sector_impact(daily_transits, sector)
                total_impact = sum([i['impact'] for i in impacts])
                num_events = len(impacts)
                
                sector_data.append({
                    "Sector": sector,
                    "Total Impact": round(total_impact, 1),
                    "Events": num_events,
                    "Bias": "Bullish 🟢" if total_impact > 0 else "Bearish 🔴" if total_impact < 0 else "Neutral 🟡"
                })
            
            sector_df = pd.DataFrame(sector_data)
            st.dataframe(sector_df, height=300)
    
    with tab5:
        st.header("🔄 Market Turning Points")
        st.info("🎯 Major planetary aspects that typically mark significant market reversals")
        
        turning_points = get_turning_points(daily_transits)
        
        if turning_points:
            st.subheader(f"⚠️ {len(turning_points)} Major Turning Points Identified")
            
            for tp in turning_points:
                direction_color = "🟢" if tp["direction"] == "BULLISH" else "🔴" if tp["direction"] == "BEARISH" else "🟡"
                
                st.markdown(f"""
                <div class="turning-point">
                    🕐 <strong>{tp['time']}</strong> - {tp['type']} {direction_color}<br>
                    ⚡ <strong>{tp['aspect']}</strong> (Strength: {"⭐" * int(tp['strength'])})<br>
                    🎯 <strong>Affected Sectors:</strong> {', '.join(tp['sectors'])}
                </div>
                """, unsafe_allow_html=True)
                
                st.write("")  # Add spacing
        else:
            st.info("✅ No major turning points identified for this date - expect relatively stable market conditions.")
        
        # Additional turning point guidance
        st.subheader("📋 Turning Point Trading Guidelines")
        st.markdown("""
        **🎯 How to Use Turning Points:**
        - **30 minutes before**: Prepare positions, check stop losses
        - **During the aspect**: Watch for reversal signals, high volatility expected
        - **1-2 hours after**: Confirm new trend direction
        
        **⚠️ Risk Management:**
        - Reduce position sizes during major turning points
        - Use wider stop losses during high volatility periods
        - Wait for confirmation before entering new positions
        """)
    
    # Footer
    st.markdown("---")
    st.caption("⚠️ **Enhanced Disclaimer**: This system combines Vedic planetary positions with daily transit aspects for educational purposes. Transit timing calculations are approximated. Always consult qualified financial advisors and use proper risk management.")
    st.caption(f"🔮 **Data Status**: Planetary positions and transit aspects calculated for {trading_date.strftime('%B %d, %Y')} from base date August 6, 2025.")

if __name__ == "__main__":
    main()
