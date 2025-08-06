# 🌟 Astrological Trading System

A Python Flask web application that provides market timing analysis based on planetary transits and astrological calculations.

## 📁 Project Structure

```
mkttiming/
├── app.py                 # Main Flask application
├── templates/
│   └── index.html        # Main HTML template
├── requirements.txt      # Python dependencies
├── README.md            # This file
└── static/              # Static files (optional)
```

## 🚀 Installation & Setup

### 1. Create Project Directory
```bash
mkdir mkttiming
cd mkttiming
```

### 2. Create Virtual Environment
```bash
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Create Templates Directory
```bash
mkdir templates
```

### 5. Add Files
- Copy `app.py` to the root directory
- Copy `index.html` to the `templates/` directory
- Ensure `requirements.txt` is in the root directory

### 6. Run the Application
```bash
python app.py
```

The application will start on `http://localhost:5000`

## 🌟 Features

### 📈 Market Timing Analysis
- **Indian Markets**: 9:15 AM - 3:30 PM IST (30-minute intervals)
- **Global Markets**: 5:00 AM - 11:55 PM IST (30-minute intervals)
- Real-time signal generation based on planetary positions

### 🪐 Planetary Transit System
- Current planetary positions with accurate astronomical data
- Motion tracking (Direct/Retrograde)
- Nakshatra and Pada analysis
- Sign Lords and Sub Lords

### 📊 Signal Generation Algorithm
The system uses sophisticated astrological calculations:

```python
# Signal Strength Calculation
if planet_motion == 'R':
    signal_strength -= 2  # Retrograde penalty

if planet in ['Jupiter', 'Venus', 'Mercury'] and motion == 'D':
    signal_strength += 1  # Beneficial planets boost

if pada in [1, 4]:
    signal_strength += 1  # Strong pada positions

if zodiac in ['Leo', 'Aries', 'Sagittarius', 'Gemini']:
    signal_strength += 0.5  # Fire/Air sign boost
```

### 🎯 Signal Types
- **Strong Bullish** ⬆⬆: High confidence upward movement
- **Bullish** ↗: Moderate confidence upward movement  
- **Neutral** →: Mixed influences, no clear direction
- **Bearish** ↘: Moderate confidence downward movement
- **Strong Bearish** ⬇⬇: High confidence downward movement

## 🔧 API Endpoints

### Market Data
- `GET /api/market-timing/indian?date=YYYY-MM-DD`
- `GET /api/market-timing/global?date=YYYY-MM-DD`

### Planetary Data
- `GET /api/planetary-data`
- `POST /api/add-planetary-data`

### Statistics
- `GET /api/statistics?date=YYYY-MM-DD`

### Signal Analysis
- `GET /api/signal-details?symbol=NIFTY&time=10:00&date=YYYY-MM-DD`

## 🌍 Supported Markets

### Indian Markets
- NIFTY, BANKNIFTY, FINNIFTY, MIDCPNIFTY, SENSEX
- Trading hours: 9:15 AM - 3:30 PM IST

### Global Markets  
- GOLD, SILVER, CRUDE, BTC
- DOW JONES, S&P 500, NASDAQ, USD/INR
- Extended hours: 5:00 AM - 11:55 PM IST

## 📱 Usage Instructions

1. **Select Date**: Choose trading date in the control panel
2. **Choose Market**: Select Indian, Global, or Both markets
3. **View Signals**: Click on any timing cell for detailed analysis
4. **Auto-Update**: Enable automatic refresh (30s or 1min intervals)
5. **Planetary Data**: Switch to Planetary tab for transit details
6. **Statistics**: View overall market statistics and accuracy

## ⚠️ Important Disclaimers

1. **Educational Purpose**: This system is for educational and research purposes only
2. **Not Financial Advice**: Do not use as sole basis for trading decisions
3. **Risk Warning**: All trading involves risk of financial loss
4. **Consult Experts**: Always consult qualified financial advisors
5. **Accuracy**: Astrological analysis is not scientifically proven for market prediction

## 🔧 Customization

### Adding New Symbols
```python
# In app.py, modify the symbol lists:
planetary_data.indian_symbols.append('RELIANCE')
planetary_data.global_symbols.append('AAPL')
```

### Adjusting Signal Algorithm
Modify the `generate_signal()` method in the `AstrologicalAnalyzer` class to customize signal generation logic.

### Adding New Planetary Data
Use the API endpoint or modify the initial data in the `PlanetaryData` class.

## 🐛 Troubleshooting

### Common Issues
1. **Port 5000 in use**: Change port in `app.run(port=5001)`
2. **Template not found**: Ensure `templates/index.html` exists
3. **CSS not loading**: Check file paths and Flask static configuration
4. **API errors**: Check browser console for detailed error messages

### Debug Mode
The application runs in debug mode by default. For production:
```python
app.run(debug=False, host='0.0.0.0', port=5000)
```

## 📈 Future Enhancements

- [ ] Database integration for persistent data storage
- [ ] Real-time market data feeds
- [ ] Advanced planetary aspect calculations
- [ ] Email/SMS alert system
- [ ] Portfolio integration
- [ ] Historical accuracy tracking
- [ ] Mobile responsive design improvements

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📞 Support

For technical issues or questions about the astrological system, please refer to:
- Vedic astrology texts for planetary calculations
- Ephemeris data sources for accurate positions
- Financial market documentation for trading hours

---

**Remember**: This is an experimental system combining astrology with market analysis. Always do your own research and never risk more than you can afford to lose in any trading activity.
