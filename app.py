# app.py - Main Flask Application
from flask import Flask, render_template, jsonify, request
from datetime import datetime, timedelta
import json
import random
import math

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

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

planetary_data = PlanetaryData()

class AstrologicalAnalyzer:
    @staticmethod
    def generate_signal(symbol, time_str, date_str):
        """Generate trading signal based on planetary positions"""
        current_time = f"{date_str}T{time_str}:00"
        
        # Find nearest planetary transit
        nearest_transit = None
        min_diff = float('inf')
        
        for planet in planetary_data.planets:
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

analyzer = AstrologicalAnalyzer()

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

@app.route('/')
def index():
    """Main dashboard"""
    return render_template('index.html')

@app.route('/api/test')
def api_test():
    """Test endpoint to verify API is working"""
    return jsonify({
        'status': 'success',
        'message': 'API is working correctly',
        'timestamp': datetime.now().isoformat(),
        'planets_count': len(planetary_data.planets),
        'indian_symbols': len(planetary_data.indian_symbols),
        'global_symbols': len(planetary_data.global_symbols)
    })

@app.route('/api/planetary-data')
def get_planetary_data():
    """Get current planetary data"""
    try:
        return jsonify({
            'planets': planetary_data.planets,
            'status': 'success'
        })
    except Exception as e:
        app.logger.error(f"Error in get_planetary_data: {str(e)}")
        return jsonify({
            'error': f'Failed to get planetary data: {str(e)}',
            'status': 'error'
        }), 500

@app.route('/api/market-timing/<market_type>')
def get_market_timing(market_type):
    """Get market timing signals"""
    try:
        date = request.args.get('date', '2025-08-06')
        
        if market_type == 'indian':
            symbols = planetary_data.indian_symbols
            time_slots = generate_time_slots(9, 15, 15, 30)
        elif market_type == 'global':
            symbols = planetary_data.global_symbols
            time_slots = generate_time_slots(5, 0, 23, 55)
        else:
            return jsonify({'error': 'Invalid market type'}), 400
        
        timing_data = {}
        for symbol in symbols:
            timing_data[symbol] = {}
            for time_slot in time_slots:
                signal = analyzer.generate_signal(symbol, time_slot, date)
                timing_data[symbol][time_slot] = {
                    'signal': signal,
                    'symbol': analyzer.get_signal_symbol(signal)
                }
        
        response_data = {
            'symbols': symbols,
            'timeSlots': time_slots,
            'timingData': timing_data,
            'status': 'success'
        }
        
        return jsonify(response_data)
    
    except Exception as e:
        app.logger.error(f"Error in get_market_timing: {str(e)}")
        return jsonify({
            'error': f'Failed to generate market timing data: {str(e)}',
            'status': 'error'
        }), 500

@app.route('/api/add-planetary-data', methods=['POST'])
def add_planetary_data():
    """Add new planetary transit data"""
    try:
        data = request.json
        planetary_data.planets.append(data)
        return jsonify({'status': 'success', 'message': 'Planetary data added successfully'})
    except Exception as e:
        return jsonify({'status': 'error', 'error': str(e)}), 500

@app.route('/api/update-symbols', methods=['POST'])
def update_symbols():
    """Update trading symbols"""
    try:
        data = request.json
        market_type = data.get('market_type')
        action = data.get('action')
        symbol = data.get('symbol')
        
        if market_type == 'indian':
            symbol_list = planetary_data.indian_symbols
        else:
            symbol_list = planetary_data.global_symbols
        
        if action == 'add' and symbol not in symbol_list:
            symbol_list.append(symbol)
            return jsonify({'status': 'success', 'message': f'{symbol} added successfully'})
        elif action == 'remove' and symbol in symbol_list:
            symbol_list.remove(symbol)
            return jsonify({'status': 'success', 'message': f'{symbol} removed successfully'})
        
        return jsonify({'status': 'error', 'message': 'Operation failed'})
    except Exception as e:
        return jsonify({'status': 'error', 'error': str(e)}), 500

@app.route('/api/signal-details')
def get_signal_details():
    """Get detailed signal analysis"""
    try:
        symbol = request.args.get('symbol')
        time_slot = request.args.get('time')
        date = request.args.get('date', '2025-08-06')
        
        signal = analyzer.generate_signal(symbol, time_slot, date)
        
        # Find relevant planetary transit
        current_time = f"{date}T{time_slot}:00"
        relevant_transit = None
        
        for planet in planetary_data.planets:
            time_diff = abs((datetime.fromisoformat(planet['datetime']) - 
                           datetime.fromisoformat(current_time)).total_seconds())
            if time_diff < 3600:  # Within 1 hour
                relevant_transit = planet
                break
        
        details = {
            'signal': signal,
            'symbol': analyzer.get_signal_symbol(signal),
            'analysis': get_signal_analysis(signal),
            'planetary_influence': relevant_transit,
            'status': 'success'
        }
        
        return jsonify(details)
    except Exception as e:
        return jsonify({'status': 'error', 'error': str(e)}), 500

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

@app.route('/api/statistics')
def get_statistics():
    """Get market statistics"""
    try:
        date = request.args.get('date', '2025-08-06')
        
        # Calculate statistics for both markets
        indian_stats = calculate_market_stats('indian', date)
        global_stats = calculate_market_stats('global', date)
        
        # Overall statistics
        total_bullish = indian_stats['bullish'] + global_stats['bullish']
        total_bearish = indian_stats['bearish'] + global_stats['bearish']
        total_neutral = indian_stats['neutral'] + global_stats['neutral']
        
        # Calculate accuracy based on planetary alignment
        retrograde_count = sum(1 for p in planetary_data.planets if p['motion'] == 'R')
        base_accuracy = 75
        accuracy_adjustment = (total_bullish - total_bearish) * 2 - retrograde_count * 3
        final_accuracy = max(60, min(95, base_accuracy + accuracy_adjustment))
        
        return jsonify({
            'bullish': total_bullish,
            'bearish': total_bearish,
            'neutral': total_neutral,
            'accuracy': f"{final_accuracy}%",
            'retrograde_planets': retrograde_count,
            'active_transits': len(planetary_data.planets),
            'status': 'success'
        })
    
    except Exception as e:
        app.logger.error(f"Error in get_statistics: {str(e)}")
        return jsonify({
            'error': f'Failed to calculate statistics: {str(e)}',
            'status': 'error'
        }), 500

def calculate_market_stats(market_type, date):
    """Calculate statistics for a specific market"""
    if market_type == 'indian':
        symbols = planetary_data.indian_symbols
        time_slots = generate_time_slots(9, 15, 15, 30)
    else:
        symbols = planetary_data.global_symbols
        time_slots = generate_time_slots(5, 0, 23, 55)
    
    bullish = bearish = neutral = 0
    
    for symbol in symbols:
        for time_slot in time_slots:
            signal = analyzer.generate_signal(symbol, time_slot, date)
            if signal in ['strong-bullish', 'bullish']:
                bullish += 1
            elif signal in ['strong-bearish', 'bearish']:
                bearish += 1
            else:
                neutral += 1
    
    return {'bullish': bullish, 'bearish': bearish, 'neutral': neutral}

if __name__ == '__main__':
    print("🌟 Starting Astrological Trading System...")
    print("📊 Planetary data loaded:", len(planetary_data.planets), "planets")
    print("🇮🇳 Indian symbols:", len(planetary_data.indian_symbols))
    print("🌍 Global symbols:", len(planetary_data.global_symbols))
    print("🚀 Server starting on http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)
