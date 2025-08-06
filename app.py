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
    .timeline-bullish { background-color: rgba(0, 255, 136, 0.15); padding: 1rem; border-left: 5px solid #00ff88; border-radius: 8px; margin: 0.5rem 0; }
    .timeline-bearish { background-color: rgba(255, 71, 87, 0.15); padding: 1rem; border-left: 5px solid #ff4757; border-radius: 8px; margin: 0.5rem 0; }
    .timeline-neutral { background-color: rgba(255, 165, 2, 0.15); padding: 1rem; border-left: 5px solid #ffa502; border-radius: 8px; margin: 0.5rem 0; }
    .symbol-timeline { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 1rem; border-radius: 10px; margin: 0.5rem 0; }
    .market-status-open { color: #00ff88; font-weight: bold; }
    .market-status-closed { color: #ff4757; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

# Base Planetary Data for August 6, 2025
@st.cache_data
def get_base_planetary_data():
    return [
        {
            "planet": "Sun", "sign": "Cancer", "degree": "20°15'", "nakshatra": "Aslesha", "pada": 4,
            "motion": "D", "themes": "🔥 BEARISH: Healthcare, Pharma, Real Estate | NEUTRAL: Government, PSUs, Banking",
            "market_effect": "bearish", "sectors": ["Healthcare", "Pharma", "Real Estate", "FMCG"]
        },
        {
            "planet": "Moon", "sign": "Sagittarius", "degree": "11°41'", "nakshatra": "Mula", "pada": 1,
            "motion": "D", "themes": "🟡 NEUTRAL: International Trade, Travel, Education | TRANSFORMATION: Tech disruption",
            "market_effect": "neutral", "sectors": ["International Trade", "Travel", "Education", "Philosophy"]
        },
        {
            "planet": "Mercury", "sign": "Cancer", "degree": "10°48'", "nakshatra": "Pushya", "pada": 3,
            "motion": "R", "themes": "🔴 VERY BEARISH: IT, Telecom, Media | AVOID: NIFTY IT, Communication stocks",
            "market_effect": "very_bearish", "sectors": ["IT", "Telecom", "Media", "Communication", "E-commerce"]
        },
        {
            "planet": "Venus", "sign": "Gemini", "degree": "1°10'", "nakshatra": "Mrigashira", "pada": 1,
            "motion": "D", "themes": "🟢 BULLISH: Luxury, FMCG, Retail, Entertainment | GOOD: Consumer stocks",
            "market_effect": "bullish", "sectors": ["Luxury", "FMCG", "Retail", "Entertainment", "Beauty", "Textiles"]
        },
        {
            "planet": "Mars", "sign": "Taurus", "degree": "17°22'", "nakshatra": "Rohini", "pada": 2,
            "motion": "D", "themes": "🚀 VERY BULLISH: Banking, Realty, Steel, Auto | STRONG: NIFTY, BANKNIFTY, Infrastructure",
            "market_effect": "very_bullish", "sectors": ["Banking", "Realty", "Steel", "Auto", "Infrastructure", "Construction"]
        },
        {
            "planet": "Jupiter", "sign": "Gemini", "degree": "14°53'", "nakshatra": "Ardra", "pada": 4,
            "motion": "D", "themes": "🟢 BULLISH: Education, Publishing, Airlines | MODERATE: Financial services, NBFCs",
            "market_effect": "bullish", "sectors": ["Education", "Publishing", "Airlines", "Financial Services", "NBFCs"]
        },
        {
            "planet": "Saturn", "sign": "Aquarius", "degree": "1°35'", "nakshatra": "Dhanishta", "pada": 1,
            "motion": "D", "themes": "🟡 NEUTRAL: Tech innovation, Utilities | DISCIPLINED: Long-term investments",
            "market_effect": "neutral", "sectors": ["Technology", "Utilities", "Renewable Energy", "Innovation"]
        },
        {
            "planet": "Uranus", "sign": "Aries", "degree": "26°58'", "nakshatra": "Bharani", "pada": 3,
            "motion": "D", "themes": "🔥 VOLATILE: Defense, Chemicals, Metals | DISRUPTION: Traditional industries",
            "market_effect": "volatile", "sectors": ["Defense", "Chemicals", "Metals", "Mining", "Explosives"]
        },
        {
            "planet": "Neptune", "sign": "Pisces", "degree": "29°49'", "nakshatra": "Revati", "pada": 4,
            "motion": "D", "themes": "🟡 NEUTRAL: Pharma, Chemicals, Oil | SPIRITUAL: Alternative medicine",
            "market_effect": "neutral", "sectors": ["Pharmaceuticals", "Chemicals", "Oil", "Shipping", "Fisheries"]
        },
        {
            "planet": "Pluto", "sign": "Capricorn", "degree": "2°04'", "nakshatra": "Uttara Ashadha", "pada": 1,
            "motion": "R", "themes": "🔴 BEARISH: Government, Traditional banks | TRANSFORMATION: Systemic changes",
            "market_effect": "bearish", "sectors": ["Government", "PSU Banks", "Traditional Systems", "Bureaucracy"]
        }
    ]

# Base Planetary Aspects Timeline for August 6, 2025
@st.cache_data
def get_base_planetary_aspects_timeline():
    return [
        {
            "time": "02:06", "aspect": "Moon Quintile Node (☽ ⬠ ☊)", "planets": "☽ ⬠ ☊",
            "astrological_meaning": "Unusual opportunities, karmic shifts",
            "indian_market": "Neutral", "commodities": "Neutral", "forex_btc": "Sudden trend change", "global_market": "Neutral",
            "market_status": "⚫ Closed", "overall_impact": "neutral",
            "detailed_impact": {
                "NIFTY": "Neutral", "BANKNIFTY": "Neutral", "GOLD": "Neutral", "SILVER": "Neutral", 
                "CRUDE": "Neutral", "BTC": "Sudden trend change", "DOWJONES": "Neutral"
            }
        },
        {
            "time": "02:34", "aspect": "Moon BiQuintile Uranus (☽ bQ ♅)", "planets": "☽ bQ ♅",
            "astrological_meaning": "Innovative but erratic energy",
            "indian_market": "Tech stocks volatile", "commodities": "Neutral", "forex_btc": "Bullish", "global_market": "Neutral",
            "market_status": "⚫ Closed", "overall_impact": "bullish",
            "detailed_impact": {
                "NIFTY": "Tech stocks volatile", "BANKNIFTY": "Neutral", "GOLD": "Neutral", "SILVER": "Neutral", 
                "CRUDE": "Neutral", "BTC": "Bullish", "DOWJONES": "Neutral"
            }
        },
        {
            "time": "02:38", "aspect": "Moon Opposition Venus (☽ ☍ ♀)", "planets": "☽ ☍ ♀",
            "astrological_meaning": "Emotional vs. financial balance",
            "indian_market": "Neutral", "commodities": "Short-term dip", "forex_btc": "Neutral", "global_market": "Neutral",
            "market_status": "⚫ Closed", "overall_impact": "bearish",
            "detailed_impact": {
                "NIFTY": "Neutral", "BANKNIFTY": "Neutral", "GOLD": "Short-term dip", "SILVER": "Short-term dip", 
                "CRUDE": "Short-term dip", "BTC": "Neutral", "DOWJONES": "Neutral"
            }
        },
        {
            "time": "04:38", "aspect": "Sun BiQuintile Moon (☉ bQ ☽)", "planets": "☉ bQ ☽",
            "astrological_meaning": "Creative problem-solving",
            "indian_market": "BankNifty recovery", "commodities": "Neutral", "forex_btc": "Neutral", "global_market": "Neutral",
            "market_status": "🌍 Global Market Open", "overall_impact": "bullish",
            "detailed_impact": {
                "NIFTY": "Neutral", "BANKNIFTY": "Recovery", "GOLD": "Neutral", "SILVER": "Neutral", 
                "CRUDE": "Neutral", "BTC": "Neutral", "DOWJONES": "Neutral"
            }
        },
        {
            "time": "10:25", "aspect": "Mars SemiSquare Lilith (♂ ∠ ⚸)", "planets": "♂ ∠ ⚸",
            "astrological_meaning": "Aggressive speculation",
            "indian_market": "Midcaps/Smallcaps risks", "commodities": "Neutral", "forex_btc": "Neutral", "global_market": "Neutral",
            "market_status": "🇮🇳 Indian Market Open", "overall_impact": "bearish",
            "detailed_impact": {
                "NIFTY": "Midcap risks", "BANKNIFTY": "Smallcap risks", "GOLD": "Neutral", "SILVER": "Neutral", 
                "CRUDE": "Neutral", "BTC": "Neutral", "DOWJONES": "Neutral"
            }
        },
        {
            "time": "13:39", "aspect": "Moon Opposition Jupiter (☽ ☍ ♃)", "planets": "☽ ☍ ♃",
            "astrological_meaning": "Overconfidence vs. reality check",
            "indian_market": "Rally then profit-booking", "commodities": "Neutral", "forex_btc": "Neutral", "global_market": "Temporary rally then profit-booking",
            "market_status": "🇮🇳 Indian Market Open", "overall_impact": "mixed",
            "detailed_impact": {
                "NIFTY": "Rally then profit-booking", "BANKNIFTY": "Rally then profit-booking", "GOLD": "Neutral", "SILVER": "Neutral", 
                "CRUDE": "Neutral", "BTC": "Neutral", "DOWJONES": "Temporary rally then profit-booking"
            }
        },
        {
            "time": "16:53", "aspect": "Sun Quincunx Moon (☉ ⚻ ☽)", "planets": "☉ ⚻ ☽",
            "astrological_meaning": "Adjustments needed",
            "indian_market": "Neutral", "commodities": "Bearish pressure", "forex_btc": "Neutral", "global_market": "Neutral",
            "market_status": "🌍 Global Market Open", "overall_impact": "bearish",
            "detailed_impact": {
                "NIFTY": "Neutral", "BANKNIFTY": "Neutral", "GOLD": "Bearish pressure", "SILVER": "Bearish pressure", 
                "CRUDE": "Bearish pressure", "BTC": "Neutral", "DOWJONES": "Neutral"
            }
        },
        {
            "time": "17:10", "aspect": "Moon Sextile Lilith (☽ ⚹ ⚸)", "planets": "☽ ⚹ ⚸",
            "astrological_meaning": "Hidden opportunities",
            "indian_market": "Neutral", "commodities": "Neutral", "forex_btc": "Altcoins rally", "global_market": "Neutral",
            "market_status": "🌍 Global Market Open", "overall_impact": "bullish",
            "detailed_impact": {
                "NIFTY": "Neutral", "BANKNIFTY": "Neutral", "GOLD": "Neutral", "SILVER": "Neutral", 
                "CRUDE": "Neutral", "BTC": "Altcoins rally", "DOWJONES": "Neutral"
            }
        },
        {
            "time": "19:35", "aspect": "Moon Sesquiquadrate Uranus (☽ ⚼ ♅)", "planets": "☽ ⚼ ♅",
            "astrological_meaning": "Sudden disruptions",
            "indian_market": "Neutral", "commodities": "Neutral", "forex_btc": "Neutral", "global_market": "After-hours volatility",
            "market_status": "🌍 Global Market Open", "overall_impact": "volatile",
            "detailed_impact": {
                "NIFTY": "Neutral", "BANKNIFTY": "Neutral", "GOLD": "Neutral", "SILVER": "Neutral", 
                "CRUDE": "Neutral", "BTC": "Neutral", "DOWJONES": "After-hours volatility"
            }
        },
        {
            "time": "21:18", "aspect": "Sun Square Lilith (☉ ☐ ⚸)", "planets": "☉ ☐ ⚸",
            "astrological_meaning": "Power struggles, manipulation",
            "indian_market": "Neutral", "commodities": "Institutional manipulation", "forex_btc": "Neutral", "global_market": "Neutral",
            "market_status": "🌍 Global Market Open", "overall_impact": "bearish",
            "detailed_impact": {
                "NIFTY": "Neutral", "BANKNIFTY": "Neutral", "GOLD": "Institutional manipulation", "SILVER": "Institutional manipulation", 
                "CRUDE": "Institutional manipulation", "BTC": "Neutral", "DOWJONES": "Neutral"
            }
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

def calculate_planetary_aspects_for_date(base_date, target_date):
    """Calculate planetary aspects timeline for any date"""
    base_aspects = get_base_planetary_aspects_timeline()
    days_diff = (target_date - base_date).days
    
    updated_aspects = []
    
    for aspect_data in base_aspects:
        # Calculate time variations based on lunar and planetary cycles
        base_hour = int(aspect_data["time"].split(':')[0])
        base_min = int(aspect_data["time"].split(':')[1])
        
        # Add cyclical variations (Moon cycle = 29.5 days)
        time_variation_hours = (days_diff * 0.87) % 24  # Slightly less than 1 hour per day
        time_variation_minutes = (days_diff * 13.2) % 60  # Moon's daily motion influence
        
        new_hour = int((base_hour + time_variation_hours) % 24)
        new_min = int((base_min + time_variation_minutes) % 60)
        
        # Determine market status based on time and date
        market_status = get_market_status(new_hour, new_min)
        
        # Adjust impact based on planetary cycles
        impact_modifier = 1 + (days_diff % 7 - 3) * 0.1  # Weekly cycle variation
        
        updated_aspect = aspect_data.copy()
        updated_aspect["time"] = f"{new_hour:02d}:{new_min:02d}"
        updated_aspect["market_status"] = market_status
        
        # Modify impacts based on date variation
        for symbol in updated_aspect["detailed_impact"]:
            current_impact = updated_aspect["detailed_impact"][symbol]
            if current_impact not in ["Neutral", "neutral"]:
                # Add some variation while keeping the core meaning
                if days_diff % 3 == 1:
                    if "Bullish" in current_impact or "rally" in current_impact:
                        updated_aspect["detailed_impact"][symbol] = current_impact.replace("rally", "strong rally").replace("Bullish", "Strong Bullish")
                elif days_diff % 3 == 2:
                    if "Bearish" in current_impact or "dip" in current_impact:
                        updated_aspect["detailed_impact"][symbol] = current_impact.replace("dip", "sharp dip").replace("Bearish", "Strong Bearish")
        
        updated_aspects.append(updated_aspect)
    
    return sorted(updated_aspects, key=lambda x: x["time"])

def get_market_status(hour, minute):
    """Determine market status based on time"""
    current_minutes = hour * 60 + minute
    
    # Indian market: 9:15 AM to 3:30 PM (555 to 930 minutes from midnight)
    if 555 <= current_minutes <= 930:
        return "🇮🇳 Indian Market Open"
    # Global market: 5:00 AM to 11:55 PM (300 to 1435 minutes from midnight)
    elif 300 <= current_minutes <= 1435:
        return "🌍 Global Market Open"
    else:
        return "⚫ Closed"

def search_symbol_timeline(aspects_data, symbol):
    """Search timeline for specific symbol impacts"""
    symbol_timeline = []
    
    for aspect in aspects_data:
        if symbol in aspect["detailed_impact"]:
            impact = aspect["detailed_impact"][symbol]
            if impact not in ["Neutral", "neutral"]:
                symbol_timeline.append({
                    "time": aspect["time"],
                    "aspect": aspect["aspect"],
                    "impact": impact,
                    "meaning": aspect["astrological_meaning"],
                    "market_status": aspect["market_status"],
                    "overall_impact": aspect["overall_impact"]
                })
    
    return symbol_timeline

def get_timeline_market_bias(impact_text):
    """Determine bullish/bearish bias from impact text"""
    bullish_keywords = ["rally", "recovery", "bullish", "strong", "opportunity", "positive"]
    bearish_keywords = ["dip", "bearish", "risks", "pressure", "manipulation", "volatile", "disruption"]
    
    impact_lower = impact_text.lower()
    
    if any(keyword in impact_lower for keyword in bullish_keywords):
        return "🟢 Bullish"
    elif any(keyword in impact_lower for keyword in bearish_keywords):
        return "🔴 Bearish"
    else:
        return "🟡 Neutral"

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

def get_daily_market_effects(planet_data, transits, target_date):
    """Generate specific timing effects for major markets"""
    
    # Asset-specific planetary rulerships and sensitivities
    asset_rules = {
        "NIFTY": {
            "primary": ["Mars", "Jupiter"], "secondary": ["Sun", "Mercury"], 
            "bearish": ["Saturn", "Rahu"], "sectors": ["Banking", "IT", "Auto"]
        },
        "BANKNIFTY": {
            "primary": ["Mars", "Jupiter"], "secondary": ["Venus", "Mercury"],
            "bearish": ["Saturn"], "sectors": ["Banking", "Financial Services"]
        },
        "GOLD": {
            "primary": ["Sun", "Jupiter"], "secondary": ["Venus"],
            "bearish": ["Mars", "Saturn"], "sectors": ["Precious Metals", "Traditional Assets"]
        },
        "BTC": {
            "primary": ["Uranus", "Mercury"], "secondary": ["Saturn"],
            "bearish": ["Mercury Retrograde"], "sectors": ["Cryptocurrency", "Technology"]
        },
        "CRUDE": {
            "primary": ["Mars", "Sun"], "secondary": ["Jupiter"],
            "bearish": ["Venus", "Moon"], "sectors": ["Energy", "Chemicals"]
        }
    }
    
    market_effects = {}
    
    for asset, rules in asset_rules.items():
        daily_timeline = []
        
        # Morning session (9:15 - 11:30)
        morning_strength = 0
        for planet_info in planet_data:
            planet = planet_info["planet"]
            if planet in rules["primary"]:
                if planet_info["market_effect"] == "very_bullish":
                    morning_strength += 3
                elif planet_info["market_effect"] == "bullish":
                    morning_strength += 2
                elif planet_info["market_effect"] == "bearish":
                    morning_strength -= 2
                elif planet_info["market_effect"] == "very_bearish":
                    morning_strength -= 3
            elif planet in rules["secondary"]:
                if planet_info["market_effect"] == "very_bullish":
                    morning_strength += 1.5
                elif planet_info["market_effect"] == "bullish":
                    morning_strength += 1
                elif planet_info["market_effect"] == "bearish":
                    morning_strength -= 1
                elif planet_info["market_effect"] == "very_bearish":
                    morning_strength -= 1.5
        
        # Add transit influences for morning
        for transit in transits:
            transit_hour = int(transit["time"].split(':')[0])
            if 9 <= transit_hour <= 11:
                if any(sector in rules["sectors"] for sector in transit["sectors"]):
                    if transit["market_impact"] == "bullish":
                        morning_strength += transit["strength"] * 0.5
                    elif transit["market_impact"] == "bearish":
                        morning_strength -= transit["strength"] * 0.5
        
        morning_bias = "STRONG BULLISH" if morning_strength >= 3 else "BULLISH" if morning_strength >= 1 else "STRONG BEARISH" if morning_strength <= -3 else "BEARISH" if morning_strength <= -1 else "NEUTRAL"
        daily_timeline.append({"time": "09:15-11:30", "session": "Morning", "bias": morning_bias, "strength": morning_strength})
        
        # Afternoon session (11:30 - 15:30)
        afternoon_strength = morning_strength * 0.7  # Carry forward with dampening
        
        for transit in transits:
            transit_hour = int(transit["time"].split(':')[0])
            if 11 <= transit_hour <= 15:
                if any(sector in rules["sectors"] for sector in transit["sectors"]):
                    if transit["market_impact"] == "bullish":
                        afternoon_strength += transit["strength"] * 0.8
                    elif transit["market_impact"] == "bearish":
                        afternoon_strength -= transit["strength"] * 0.8
        
        afternoon_bias = "STRONG BULLISH" if afternoon_strength >= 3 else "BULLISH" if afternoon_strength >= 1 else "STRONG BEARISH" if afternoon_strength <= -3 else "BEARISH" if afternoon_strength <= -1 else "NEUTRAL"
        daily_timeline.append({"time": "11:30-15:30", "session": "Afternoon", "bias": afternoon_bias, "strength": afternoon_strength})
        
        # Evening/Global session (for 24h markets)
        if asset in ["GOLD", "BTC", "CRUDE"]:
            evening_strength = afternoon_strength * 0.5
            
            for transit in transits:
                transit_hour = int(transit["time"].split(':')[0])
                if 16 <= transit_hour <= 23:
                    if any(sector in rules["sectors"] for sector in transit["sectors"]):
                        if transit["market_impact"] == "bullish":
                            evening_strength += transit["strength"] * 0.6
                        elif transit["market_impact"] == "bearish":
                            evening_strength -= transit["strength"] * 0.6
            
            evening_bias = "STRONG BULLISH" if evening_strength >= 3 else "BULLISH" if evening_strength >= 1 else "STRONG BEARISH" if evening_strength <= -3 else "BEARISH" if evening_strength <= -1 else "NEUTRAL"
            daily_timeline.append({"time": "16:00-23:00", "session": "Evening", "bias": evening_bias, "strength": evening_strength})
        
        market_effects[asset] = daily_timeline
    
    return market_effects

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
    
    # Calculate planetary positions, transits, daily market effects, and planetary aspects
    base_date = datetime(2025, 8, 6).date()
    planet_data = calculate_planetary_positions_for_date(base_date, trading_date)
    daily_transits = calculate_daily_transits(base_date, trading_date)
    daily_market_effects = get_daily_market_effects(planet_data, daily_transits, trading_date)
    planetary_aspects = calculate_planetary_aspects_for_date(base_date, trading_date)
    
    # Main tabs
    tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs(["📈 Market Signals", "🪐 Planetary Transits", "⏰ Daily Transit Aspects", "📊 Sector Analysis", "🎯 Daily Market Effects", "🔄 Turning Points", "⏰ Timeline"])
    
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
            "🚀 Very Bullish" if row['market_effect'] == 'very_bullish' else
            "🟢 Bullish" if row['market_effect'] == 'bullish' else
            "🔴 Very Bearish" if row['market_effect'] == 'very_bearish' else
            "🔴 Bearish" if row['market_effect'] == 'bearish' else
            "⚡ Volatile" if row['market_effect'] == 'volatile' else
            "🟡 Neutral", axis=1
        )
        
        st.dataframe(planet_df[['planet', 'sign', 'degree', 'nakshatra', 'pada', 'motion', 'Market Influence', 'themes']], height=400)
        
        # Today's Major Planetary Effects Summary
        st.subheader("🎯 Today's Major Market Effects by Planet")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 🚀 Strongest Bullish Influences")
            bullish_planets = [p for p in planet_data if p['market_effect'] in ['very_bullish', 'bullish']]
            for planet in sorted(bullish_planets, key=lambda x: 2 if x['market_effect'] == 'very_bullish' else 1, reverse=True):
                strength_emoji = "🚀" if planet['market_effect'] == 'very_bullish' else "🟢"
                st.success(f"{strength_emoji} **{planet['planet']} in {planet['sign']}** - {planet['themes'].split('|')[0].strip()}")
        
        with col2:
            st.markdown("### 🔴 Strongest Bearish Influences")
            bearish_planets = [p for p in planet_data if p['market_effect'] in ['very_bearish', 'bearish']]
            for planet in sorted(bearish_planets, key=lambda x: 2 if x['market_effect'] == 'very_bearish' else 1, reverse=True):
                strength_emoji = "🔴" if planet['market_effect'] == 'very_bearish' else "🟡"
                st.error(f"{strength_emoji} **{planet['planet']} in {planet['sign']}** - {planet['themes'].split('|')[0].strip()}")
    
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
        st.header("🎯 Daily Market Effects - Major Assets")
        st.info(f"📊 Precise bullish/bearish timing for NIFTY, BANKNIFTY, GOLD, BTC, CRUDE on {trading_date.strftime('%B %d, %Y')}")
        
        # Display market effects for each major asset
        for asset, timeline in daily_market_effects.items():
            st.subheader(f"📈 {asset} - Session-wise Analysis")
            
            cols = st.columns(len(timeline))
            
            for i, session_data in enumerate(timeline):
                with cols[i]:
                    # Color coding based on bias
                    if "STRONG BULLISH" in session_data["bias"]:
                        st.success(f"🚀 **{session_data['session']}**\n\n**{session_data['time']}**\n\n**{session_data['bias']}**\n\nStrength: {session_data['strength']:.1f}")
                    elif "BULLISH" in session_data["bias"]:
                        st.success(f"🟢 **{session_data['session']}**\n\n**{session_data['time']}**\n\n**{session_data['bias']}**\n\nStrength: {session_data['strength']:.1f}")
                    elif "STRONG BEARISH" in session_data["bias"]:
                        st.error(f"🔴 **{session_data['session']}**\n\n**{session_data['time']}**\n\n**{session_data['bias']}**\n\nStrength: {session_data['strength']:.1f}")
                    elif "BEARISH" in session_data["bias"]:
                        st.warning(f"🟡 **{session_data['session']}**\n\n**{session_data['time']}**\n\n**{session_data['bias']}**\n\nStrength: {session_data['strength']:.1f}")
                    else:
                        st.info(f"⚖️ **{session_data['session']}**\n\n**{session_data['time']}**\n\n**{session_data['bias']}**\n\nStrength: {session_data['strength']:.1f}")
            
            st.markdown("---")
        
        # Overall market summary
        st.subheader("📋 Overall Market Bias Summary")
        
        summary_data = []
        for asset, timeline in daily_market_effects.items():
            overall_strength = sum([session["strength"] for session in timeline]) / len(timeline)
            dominant_bias = max(timeline, key=lambda x: abs(x["strength"]))["bias"]
            
            summary_data.append({
                "Asset": asset,
                "Overall Bias": dominant_bias,
                "Avg Strength": f"{overall_strength:.1f}",
                "Best Session": max(timeline, key=lambda x: x["strength"])["session"],
                "Best Time": max(timeline, key=lambda x: x["strength"])["time"]
            })
        
        summary_df = pd.DataFrame(summary_data)
        st.dataframe(summary_df, height=200)
        
        # Trading recommendations
        st.subheader("💡 Trading Recommendations")
        
        strongest_bullish = max(daily_market_effects.items(), 
                               key=lambda x: max([session["strength"] for session in x[1] if "BULLISH" in session["bias"]], default=0))
        
        strongest_bearish = max(daily_market_effects.items(), 
                               key=lambda x: min([session["strength"] for session in x[1] if "BEARISH" in session["bias"]], default=0))
        
        col1, col2 = st.columns(2)
        
        with col1:
            if strongest_bullish[0]:
                best_session = max(strongest_bullish[1], key=lambda x: x["strength"])
                st.success(f"""
                **🚀 STRONGEST BULLISH OPPORTUNITY**
                
                **Asset:** {strongest_bullish[0]}
                **Time:** {best_session['time']}
                **Session:** {best_session['session']}
                **Bias:** {best_session['bias']}
                **Strength:** {best_session['strength']:.1f}
                """)
        
        with col2:
            if strongest_bearish[0]:
                worst_session = min(strongest_bearish[1], key=lambda x: x["strength"])
                st.error(f"""
                **🔴 STRONGEST BEARISH PRESSURE**
                
                **Asset:** {strongest_bearish[0]}
                **Time:** {worst_session['time']}
                **Session:** {worst_session['session']}
                **Bias:** {worst_session['bias']}
                **Strength:** {worst_session['strength']:.1f}
                """)
    
    with tab6:
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
    
    with tab7:
        st.header("⏰ Planetary Aspects & Market Impact Timeline")
        st.info(f"📊 Precise planetary aspects timing with market impacts for {trading_date.strftime('%B %d, %Y')}")
        
        # Calculate planetary aspects for the selected date
        planetary_aspects = calculate_planetary_aspects_for_date(base_date, trading_date)
        
        # Symbol search section
        st.subheader("🔍 Symbol-Specific Timeline Search")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            available_symbols = ["NIFTY", "BANKNIFTY", "GOLD", "SILVER", "CRUDE", "BTC", "DOWJONES"]
            selected_symbol = st.selectbox(
                "Select Symbol for Timeline Analysis",
                available_symbols,
                help="Search for specific timing and transit impacts for your chosen symbol"
            )
        
        with col2:
            if st.button("🔍 Search Timeline", type="primary"):
                symbol_timeline = search_symbol_timeline(planetary_aspects, selected_symbol)
                
                if symbol_timeline:
                    st.success(f"Found {len(symbol_timeline)} relevant aspects for {selected_symbol}")
                    
                    # Display symbol-specific timeline
                    st.subheader(f"📈 {selected_symbol} - Specific Timeline")
                    
                    for event in symbol_timeline:
                        bias = get_timeline_market_bias(event["impact"])
                        
                        # Create colored containers based on bias
                        if "🟢" in bias:
                            st.success(f"""
                            **🕐 {event['time']}** - {event['aspect']} {bias}
                            
                            **Impact:** {event['impact']}
                            **Meaning:** {event['meaning']}
                            **Market Status:** {event['market_status']}
                            """)
                        elif "🔴" in bias:
                            st.error(f"""
                            **🕐 {event['time']}** - {event['aspect']} {bias}
                            
                            **Impact:** {event['impact']}
                            **Meaning:** {event['meaning']}
                            **Market Status:** {event['market_status']}
                            """)
                        else:
                            st.warning(f"""
                            **🕐 {event['time']}** - {event['aspect']} {bias}
                            
                            **Impact:** {event['impact']}
                            **Meaning:** {event['meaning']}
                            **Market Status:** {event['market_status']}
                            """)
                else:
                    st.info(f"No specific transit impacts found for {selected_symbol} on this date.")
        
        st.markdown("---")
        
        # Complete timeline table
        st.subheader("📋 Complete Planetary Aspects Timeline")
        
        # Market timing info
        col1, col2, col3 = st.columns(3)
        with col1:
            st.info("🇮🇳 **Indian Markets**\n\n9:15 AM - 3:30 PM IST")
        with col2:
            st.info("🌍 **Global/Commodity Markets**\n\n5:00 AM - 11:55 PM IST")
        with col3:
            st.info("📊 **Market Categories**\n\nIndian: NIFTY, BANKNIFTY\nCommodities: GOLD, SILVER, CRUDE\nForex: BTC\nGlobal: DOWJONES")
        
        # Timeline table
        timeline_data = []
        for aspect in planetary_aspects:
            timeline_data.append({
                "Time": aspect["time"],
                "Aspect": aspect["aspect"],
                "Astrological Meaning": aspect["astrological_meaning"],
                "Indian Market": aspect["indian_market"],
                "Commodities": aspect["commodities"],
                "Forex (BTC)": aspect["forex_btc"],
                "Global Market": aspect["global_market"],
                "Market Status": aspect["market_status"]
            })
        
        timeline_df = pd.DataFrame(timeline_data)
        st.dataframe(timeline_df, height=500)
        
        # Summary statistics
        st.subheader("📊 Timeline Summary")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            total_aspects = len(planetary_aspects)
            st.metric("Total Aspects", total_aspects)
        
        with col2:
            indian_market_active = len([a for a in planetary_aspects if "🇮🇳" in a["market_status"]])
            st.metric("During Indian Market", indian_market_active)
        
        with col3:
            global_market_active = len([a for a in planetary_aspects if "🌍" in a["market_status"]])
            st.metric("During Global Market", global_market_active)
        
        with col4:
            market_closed = len([a for a in planetary_aspects if "⚫" in a["market_status"]])
            st.metric("Market Closed", market_closed)
        
        # Detailed timing analysis
        st.subheader("⏰ Session-wise Impact Analysis")
        
        # Indian market session (9:15 AM - 3:30 PM)
        indian_session_aspects = [a for a in planetary_aspects if "🇮🇳" in a["market_status"]]
        if indian_session_aspects:
            st.markdown("### 🇮🇳 Indian Market Session (9:15 AM - 3:30 PM)")
            
            for aspect in indian_session_aspects:
                impact_summary = []
                
                # Collect non-neutral impacts
                if aspect["indian_market"] != "Neutral":
                    bias = get_timeline_market_bias(aspect["indian_market"])
                    impact_summary.append(f"Indian Market: {aspect['indian_market']} {bias}")
                
                if aspect["commodities"] != "Neutral":
                    bias = get_timeline_market_bias(aspect["commodities"])
                    impact_summary.append(f"Commodities: {aspect['commodities']} {bias}")
                
                if aspect["forex_btc"] != "Neutral":
                    bias = get_timeline_market_bias(aspect["forex_btc"])
                    impact_summary.append(f"BTC: {aspect['forex_btc']} {bias}")
                
                if impact_summary:
                    impact_text = " | ".join(impact_summary)
                    
                    # Color code based on dominant bias
                    if "🟢" in impact_text and "🔴" not in impact_text:
                        st.success(f"**{aspect['time']}** - {aspect['aspect']}\n\n{impact_text}")
                    elif "🔴" in impact_text and "🟢" not in impact_text:
                        st.error(f"**{aspect['time']}** - {aspect['aspect']}\n\n{impact_text}")
                    else:
                        st.warning(f"**{aspect['time']}** - {aspect['aspect']}\n\n{impact_text}")
        else:
            st.info("No major planetary aspects during Indian market hours.")
        
        # Global market session impacts
        global_session_aspects = [a for a in planetary_aspects if "🌍" in a["market_status"]]
        if global_session_aspects:
            st.markdown("### 🌍 Global Market Session (5:00 AM - 11:55 PM)")
            
            # Show only major impacts to avoid clutter
            major_global_aspects = [a for a in global_session_aspects 
                                  if any(impact != "Neutral" for impact in 
                                        [a["indian_market"], a["commodities"], a["forex_btc"], a["global_market"]])]
            
            for aspect in major_global_aspects[:5]:  # Limit to top 5 to avoid clutter
                st.info(f"**{aspect['time']}** - {aspect['aspect']} - {aspect['astrological_meaning']}")
        
        # Trading recommendations based on timeline
        st.subheader("💡 Timeline-Based Trading Recommendations")
        
        # Find best bullish and bearish opportunities
        bullish_opportunities = []
        bearish_warnings = []
        
        for aspect in planetary_aspects:
            # Check for bullish signals
            bullish_signals = [
                aspect["indian_market"], aspect["commodities"], 
                aspect["forex_btc"], aspect["global_market"]
            ]
            
            for signal in bullish_signals:
                if any(keyword in signal.lower() for keyword in ["rally", "recovery", "bullish", "opportunity"]):
                    bullish_opportunities.append({
                        "time": aspect["time"],
                        "aspect": aspect["aspect"],
                        "signal": signal,
                        "market_status": aspect["market_status"]
                    })
            
            # Check for bearish warnings
            for signal in bullish_signals:
                if any(keyword in signal.lower() for keyword in ["dip", "risks", "pressure", "bearish", "manipulation"]):
                    bearish_warnings.append({
                        "time": aspect["time"],
                        "aspect": aspect["aspect"],
                        "signal": signal,
                        "market_status": aspect["market_status"]
                    })
        
        col1, col2 = st.columns(2)
        
        with col1:
            if bullish_opportunities:
                st.success("**🚀 Best Bullish Opportunities**")
                for opp in bullish_opportunities[:3]:  # Show top 3
                    st.write(f"🕐 **{opp['time']}** - {opp['signal']} ({opp['market_status']})")
            else:
                st.info("No major bullish opportunities identified in timeline.")
        
        with col2:
            if bearish_warnings:
                st.error("**⚠️ Key Bearish Warnings**")
                for warn in bearish_warnings[:3]:  # Show top 3
                    st.write(f"🕐 **{warn['time']}** - {warn['signal']} ({warn['market_status']})")
            else:
                st.info("No major bearish warnings in timeline.")
        
        # Auto-calculation note
        st.markdown("---")
        st.info(f"""
        📊 **Auto-Calculation Status**: 
        - Planetary aspects automatically calculated for {trading_date.strftime('%B %d, %Y')}
        - Base calculations from August 6, 2025 reference date
        - Transit timings adjusted for {abs((trading_date - base_date).days)} days difference
        - Market timing: Indian (9:15 AM-3:30 PM) | Global/Commodity (5:00 AM-11:55 PM)
        """)

    # Footer
    st.markdown("---")
    st.caption("⚠️ **Enhanced Disclaimer**: This system combines Vedic planetary positions with daily transit aspects and planetary timeline calculations for educational purposes. Transit timing and aspect calculations are approximated. Always consult qualified financial advisors and use proper risk management.")
    st.caption(f"🔮 **Data Status**: Planetary positions, transit aspects, and timeline calculations computed for {trading_date.strftime('%B %d, %Y')} from base date August 6, 2025. Symbol-specific timeline search available for precise timing analysis.")

if __name__ == "__main__":
    main()
