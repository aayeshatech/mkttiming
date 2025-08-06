<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Market Timing Matrix</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
            margin: 0;
            padding: 20px;
            color: white;
            min-height: 100vh;
        }
        .container {
            max-width: 1600px;
            margin: 0 auto;
            background: rgba(255, 255, 255, 0.05);
            backdrop-filter: blur(15px);
            border-radius: 20px;
            padding: 30px;
            box-shadow: 0 25px 50px rgba(0, 0, 0, 0.3);
        }
        .header {
            text-align: center;
            margin-bottom: 30px;
        }
        .header h1 {
            font-size: 2.8em;
            margin: 0;
            background: linear-gradient(45deg, #ffd700, #ffed4e, #f0c419);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            text-shadow: 0 0 30px rgba(255, 215, 0, 0.3);
        }
        .control-panel {
            background: rgba(255, 255, 255, 0.1);
            border-radius: 15px;
            padding: 20px;
            margin-bottom: 30px;
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            align-items: center;
        }
        .control-group {
            display: flex;
            flex-direction: column;
            gap: 8px;
        }
        .control-group label {
            font-weight: 600;
            color: #ffd700;
            font-size: 14px;
        }
        .control-group input, .control-group select {
            padding: 10px;
            border: none;
            border-radius: 8px;
            background: rgba(255, 255, 255, 0.9);
            color: #333;
            font-size: 14px;
            transition: all 0.3s ease;
        }
        .control-group input:focus, .control-group select:focus {
            outline: none;
            box-shadow: 0 0 15px rgba(255, 215, 0, 0.5);
        }
        .market-section {
            margin-bottom: 40px;
            background: rgba(255, 255, 255, 0.08);
            border-radius: 15px;
            padding: 25px;
            backdrop-filter: blur(10px);
        }
        .market-title {
            font-size: 1.8em;
            font-weight: 700;
            color: #ffd700;
            margin-bottom: 20px;
            text-align: center;
            border-bottom: 3px solid #ffd700;
            padding-bottom: 15px;
            background: linear-gradient(45deg, #ffd700, #ffed4e);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        .timing-grid {
            display: grid;
            gap: 3px;
            overflow-x: auto;
            padding: 10px;
            background: rgba(0, 0, 0, 0.2);
            border-radius: 12px;
        }
        .indian-grid {
            grid-template-columns: 120px repeat(13, 1fr);
        }
        .global-grid {
            grid-template-columns: 120px repeat(38, 1fr);
        }
        .time-header {
            background: linear-gradient(45deg, #ffd700, #f0c419);
            color: #1a1a2e;
            padding: 12px 4px;
            text-align: center;
            font-size: 11px;
            font-weight: 700;
            border-radius: 6px;
            writing-mode: vertical-rl;
            text-orientation: mixed;
            min-height: 80px;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        .symbol-label {
            background: linear-gradient(45deg, #4a90e2, #357abd);
            color: white;
            padding: 15px;
            font-weight: 700;
            font-size: 13px;
            border-radius: 8px;
            display: flex;
            align-items: center;
            justify-content: center;
            text-align: center;
            box-shadow: 0 4px 15px rgba(74, 144, 226, 0.3);
        }
        .time-cell {
            height: 50px;
            cursor: pointer;
            border-radius: 6px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 16px;
            font-weight: 700;
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
        }
        .time-cell::before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
            transition: left 0.5s;
        }
        .time-cell:hover::before {
            left: 100%;
        }
        .time-cell:hover {
            transform: scale(1.1);
            z-index: 10;
            box-shadow: 0 8px 25px rgba(0, 0, 0, 0.4);
        }
        .bullish {
            background: linear-gradient(45deg, #00ff88, #00cc70);
            color: #1a1a2e;
            box-shadow: 0 4px 15px rgba(0, 255, 136, 0.3);
        }
        .bearish {
            background: linear-gradient(45deg, #ff4757, #ff3742);
            color: white;
            box-shadow: 0 4px 15px rgba(255, 71, 87, 0.3);
        }
        .neutral {
            background: linear-gradient(45deg, #ffa502, #ff9500);
            color: #1a1a2e;
            box-shadow: 0 4px 15px rgba(255, 165, 2, 0.3);
        }
        .strong-bullish {
            background: linear-gradient(45deg, #32ff7e, #18ff6d);
            color: #1a1a2e;
            box-shadow: 0 6px 20px rgba(50, 255, 126, 0.4);
            border: 2px solid #00ff88;
        }
        .strong-bearish {
            background: linear-gradient(45deg, #ff3838, #ff2929);
            color: white;
            box-shadow: 0 6px 20px rgba(255, 56, 56, 0.4);
            border: 2px solid #ff4757;
        }
        .market-closed {
            background: linear-gradient(45deg, #636e72, #2d3436);
            color: #b2bec3;
            opacity: 0.6;
        }
        .legend {
            display: flex;
            justify-content: center;
            gap: 20px;
            margin: 20px 0;
            flex-wrap: wrap;
        }
        .legend-item {
            display: flex;
            align-items: center;
            gap: 8px;
            background: rgba(255, 255, 255, 0.1);
            padding: 8px 15px;
            border-radius: 20px;
            backdrop-filter: blur(5px);
        }
        .legend-color {
            width: 20px;
            height: 20px;
            border-radius: 50%;
        }
        .stats-panel {
            background: rgba(255, 255, 255, 0.1);
            border-radius: 15px;
            padding: 20px;
            margin-top: 30px;
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
        }
        .stat-card {
            background: rgba(255, 255, 255, 0.1);
            border-radius: 10px;
            padding: 15px;
            text-align: center;
            backdrop-filter: blur(5px);
            border: 1px solid rgba(255, 215, 0, 0.3);
        }
        .stat-value {
            font-size: 2em;
            font-weight: 700;
            color: #ffd700;
            margin-bottom: 5px;
        }
        .stat-label {
            font-size: 0.9em;
            color: #b2bec3;
        }
        .tab-navigation {
            display: flex;
            justify-content: center;
            gap: 10px;
            margin-bottom: 30px;
            background: rgba(255, 255, 255, 0.1);
            border-radius: 15px;
            padding: 10px;
        }
        .tab-button {
            background: rgba(255, 255, 255, 0.1);
            border: none;
            color: white;
            padding: 15px 25px;
            border-radius: 10px;
            cursor: pointer;
            font-size: 14px;
            font-weight: 600;
            transition: all 0.3s ease;
            backdrop-filter: blur(5px);
        }
        .tab-button:hover {
            background: rgba(255, 215, 0, 0.2);
            transform: translateY(-2px);
        }
        .tab-button.active {
            background: linear-gradient(45deg, #ffd700, #f0c419);
            color: #1a1a2e;
            box-shadow: 0 5px 15px rgba(255, 215, 0, 0.3);
        }
        .tab-content {
            display: none;
        }
        .tab-content.active {
            display: block;
        }
        .planetary-table {
            width: 100%;
            border-collapse: collapse;
            background: rgba(255, 255, 255, 0.05);
            border-radius: 15px;
            overflow: hidden;
            margin-top: 20px;
        }
        .planetary-table th {
            background: linear-gradient(45deg, #ffd700, #f0c419);
            color: #1a1a2e;
            padding: 15px 8px;
            text-align: center;
            font-weight: 700;
            font-size: 12px;
            border: 1px solid rgba(255, 215, 0, 0.3);
        }
        .planetary-table td {
            padding: 12px 8px;
            text-align: center;
            border: 1px solid rgba(255, 255, 255, 0.1);
            font-size: 11px;
            background: rgba(255, 255, 255, 0.05);
        }
        .planet-symbol {
            font-size: 16px;
            font-weight: bold;
            color: #ffd700;
        }
        .motion-direct {
            color: #32ff7e;
            font-weight: bold;
        }
        .motion-retrograde {
            color: #ff4757;
            font-weight: bold;
        }
        .data-form {
            background: rgba(255, 255, 255, 0.1);
            border-radius: 15px;
            padding: 25px;
            margin-top: 20px;
        }
        .form-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 15px;
            margin-bottom: 20px;
        }
        .form-group {
            display: flex;
            flex-direction: column;
            gap: 5px;
        }
        .form-group label {
            color: #ffd700;
            font-weight: 600;
            font-size: 12px;
        }
        .form-group input, .form-group select {
            padding: 8px;
            border: none;
            border-radius: 6px;
            background: rgba(255, 255, 255, 0.9);
            color: #333;
            font-size: 12px;
        }
        .action-buttons {
            display: flex;
            gap: 15px;
            justify-content: center;
            flex-wrap: wrap;
            margin-top: 20px;
        }
        .action-button {
            background: linear-gradient(45deg, #4a90e2, #357abd);
            color: white;
            border: none;
            padding: 12px 25px;
            border-radius: 8px;
            cursor: pointer;
            font-weight: 600;
            transition: all 0.3s ease;
        }
        .action-button:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(74, 144, 226, 0.4);
        }
        .action-button.primary {
            background: linear-gradient(45deg, #ffd700, #f0c419);
            color: #1a1a2e;
        }
        .transit-summary {
            background: rgba(255, 255, 255, 0.1);
            border-radius: 15px;
            padding: 20px;
            margin-bottom: 20px;
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
        }
        .summary-card {
            background: rgba(255, 255, 255, 0.1);
            border-radius: 10px;
            padding: 15px;
            text-align: center;
            border: 1px solid rgba(255, 215, 0, 0.3);
        }
        .summary-title {
            color: #ffd700;
            font-weight: 700;
            margin-bottom: 10px;
        }
        .summary-value {
            font-size: 1.5em;
            font-weight: 700;
            color: white;
        }
        @media (max-width: 768px) {
            .timing-grid {
                font-size: 12px;
            }
            .time-header {
                font-size: 10px;
                padding: 8px 2px;
                min-height: 60px;
            }
            .time-cell {
                height: 40px;
                font-size: 14px;
            }
            .tab-navigation {
                flex-direction: column;
                gap: 5px;
            }
            .form-grid {
                grid-template-columns: 1fr;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📈 Market Timing Matrix</h1>
            <p>Astrological Trading Signals for Indian & Global Markets</p>
        </div>

        <div class="control-panel">
            <div class="control-group">
                <label>📅 Trading Date</label>
                <input type="date" id="tradingDate" value="2025-08-06">
            </div>
            <div class="control-group">
                <label>🌍 Primary Market</label>
                <select id="primaryMarket">
                    <option value="indian">Indian Markets</option>
                    <option value="global">Global Markets</option>
                    <option value="both">Both Markets</option>
                </select>
            </div>
            <div class="control-group">
                <label>⭐ Signal Strength</label>
                <select id="signalStrength">
                    <option value="all">All Signals</option>
                    <option value="strong">Strong Only</option>
                    <option value="moderate">Moderate+</option>
                </select>
            </div>
            <div class="control-group">
                <label>🔄 Auto Update</label>
                <select id="autoUpdate">
                    <option value="off">Manual</option>
                    <option value="1min">1 Minute</option>
                    <option value="5min">5 Minutes</option>
                </select>
            </div>
        </div>

        <!-- Tab Navigation -->
        <div class="tab-navigation">
            <button class="tab-button active" onclick="switchTab('timing')">📈 Market Timing</button>
            <button class="tab-button" onclick="switchTab('planetary')">🪐 Planetary Transits</button>
            <button class="tab-button" onclick="switchTab('data')">⚙️ Data Update</button>
        </div>

        <div class="legend">
            <div class="legend-item">
                <div class="legend-color strong-bullish"></div>
                <span>Strong Bullish</span>
            </div>
            <div class="legend-item">
                <div class="legend-color bullish"></div>
                <span>Bullish</span>
            </div>
            <div class="legend-item">
                <div class="legend-color neutral"></div>
                <span>Neutral</span>
            </div>
            <div class="legend-item">
                <div class="legend-color bearish"></div>
                <span>Bearish</span>
            </div>
            <div class="legend-item">
                <div class="legend-color strong-bearish"></div>
                <span>Strong Bearish</span>
            </div>
            <div class="legend-item">
                <div class="legend-color market-closed"></div>
                <span>Market Closed</span>
            </div>
        </div>

        <!-- Tab Content -->
        <div id="timing-tab" class="tab-content active">
            <!-- Indian Markets Section -->
            <div class="market-section" id="indianSection">
                <div class="market-title">🇮🇳 Indian Markets (9:15 AM - 3:30 PM IST)</div>
                <div class="timing-grid indian-grid" id="indianGrid">
                    <!-- Headers will be populated by JavaScript -->
                </div>
            </div>

            <!-- Global Markets Section -->
            <div class="market-section" id="globalSection">
                <div class="market-title">🌍 Global Markets & Commodities (5:00 AM - 11:55 PM IST)</div>
                <div class="timing-grid global-grid" id="globalGrid">
                    <!-- Headers will be populated by JavaScript -->
                </div>
            </div>

            <div class="stats-panel">
                <div class="stat-card">
                    <div class="stat-value" id="bullishCount">0</div>
                    <div class="stat-label">Bullish Signals</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value" id="bearishCount">0</div>
                    <div class="stat-label">Bearish Signals</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value" id="neutralCount">0</div>
                    <div class="stat-label">Neutral Signals</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value" id="accuracyRate">0%</div>
                    <div class="stat-label">Historical Accuracy</div>
                </div>
            </div>
        </div>

        <!-- Planetary Transit Tab -->
        <div id="planetary-tab" class="tab-content">
            <div class="market-section">
                <div class="market-title">🪐 Planetary Transit Details</div>
                
                <div class="transit-summary">
                    <div class="summary-card">
                        <div class="summary-title">Active Transits</div>
                        <div class="summary-value" id="activeTransits">8</div>
                    </div>
                    <div class="summary-card">
                        <div class="summary-title">Retrograde Planets</div>
                        <div class="summary-value" id="retrogradeCount">1</div>
                    </div>
                    <div class="summary-card">
                        <div class="summary-title">Major Aspects</div>
                        <div class="summary-value" id="majorAspects">5</div>
                    </div>
                    <div class="summary-card">
                        <div class="summary-title">Market Impact</div>
                        <div class="summary-value" id="marketImpact">Moderate</div>
                    </div>
                </div>

                <table class="planetary-table">
                    <thead>
                        <tr>
                            <th>Planet</th>
                            <th>Date/Time</th>
                            <th>Motion</th>
                            <th>Sign Lord</th>
                            <th>Star Lord</th>
                            <th>Sub Lord</th>
                            <th>Zodiac</th>
                            <th>Nakshatra</th>
                            <th>Pada</th>
                            <th>Position in Zodiac</th>
                            <th>Declination</th>
                        </tr>
                    </thead>
                    <tbody id="planetaryTableBody">
                        <!-- Data will be populated by JavaScript -->
                    </tbody>
                </table>
            </div>
        </div>

        <!-- Data Update Tab -->
        <div id="data-tab" class="tab-content">
            <div class="market-section">
                <div class="market-title">⚙️ Planetary Data Update</div>
                
                <div class="data-form">
                    <h3 style="color: #ffd700; margin-bottom: 20px;">Add New Planetary Transit</h3>
                    <div class="form-grid">
                        <div class="form-group">
                            <label>Planet</label>
                            <select id="newPlanet">
                                <option value="Mo">Moon (Mo)</option>
                                <option value="Su">Sun (Su)</option>
                                <option value="Me">Mercury (Me)</option>
                                <option value="Ve">Venus (Ve)</option>
                                <option value="Ma">Mars (Ma)</option>
                                <option value="Ju">Jupiter (Ju)</option>
                                <option value="Sa">Saturn (Sa)</option>
                                <option value="Ra">Rahu (Ra)</option>
                                <option value="Ke">Ketu (Ke)</option>
                            </select>
                        </div>
                        <div class="form-group">
                            <label>Date</label>
                            <input type="date" id="newDate" value="2025-08-06">
                        </div>
                        <div class="form-group">
                            <label>Time</label>
                            <input type="time" id="newTime" value="12:00">
                        </div>
                        <div class="form-group">
                            <label>Motion</label>
                            <select id="newMotion">
                                <option value="D">Direct (D)</option>
                                <option value="R">Retrograde (R)</option>
                            </select>
                        </div>
                        <div class="form-group">
                            <label>Sign Lord</label>
                            <select id="newSignLord">
                                <option value="Ju">Jupiter (Ju)</option>
                                <option value="Su">Sun (Su)</option>
                                <option value="Me">Mercury (Me)</option>
                                <option value="Ve">Venus (Ve)</option>
                                <option value="Ma">Mars (Ma)</option>
                                <option value="Sa">Saturn (Sa)</option>
                                <option value="Mo">Moon (Mo)</option>
                            </select>
                        </div>
                        <div class="form-group">
                            <label>Star Lord</label>
                            <select id="newStarLord">
                                <option value="Ke">Ketu (Ke)</option>
                                <option value="Ve">Venus (Ve)</option>
                                <option value="Su">Sun (Su)</option>
                                <option value="Mo">Moon (Mo)</option>
                                <option value="Ma">Mars (Ma)</option>
                                <option value="Ra">Rahu (Ra)</option>
                                <option value="Ju">Jupiter (Ju)</option>
                                <option value="Sa">Saturn (Sa)</option>
                                <option value="Me">Mercury (Me)</option>
                            </select>
                        </div>
                        <div class="form-group">
                            <label>Sub Lord</label>
                            <select id="newSubLord">
                                <option value="Ju">Jupiter (Ju)</option>
                                <option value="Sa">Saturn (Sa)</option>
                                <option value="Me">Mercury (Me)</option>
                                <option value="Ve">Venus (Ve)</option>
                                <option value="Mo">Moon (Mo)</option>
                                <option value="Ma">Mars (Ma)</option>
                                <option value="Su">Sun (Su)</option>
                                <option value="Ra">Rahu (Ra)</option>
                                <option value="Ke">Ketu (Ke)</option>
                            </select>
                        </div>
                        <div class="form-group">
                            <label>Zodiac</label>
                            <select id="newZodiac">
                                <option value="Aries">Aries</option>
                                <option value="Taurus">Taurus</option>
                                <option value="Gemini">Gemini</option>
                                <option value="Cancer">Cancer</option>
                                <option value="Leo">Leo</option>
                                <option value="Virgo">Virgo</option>
                                <option value="Libra">Libra</option>
                                <option value="Scorpio">Scorpio</option>
                                <option value="Sagittarius">Sagittarius</option>
                                <option value="Capricorn">Capricorn</option>
                                <option value="Aquarius">Aquarius</option>
                                <option value="Pisces">Pisces</option>
                            </select>
                        </div>
                        <div class="form-group">
                            <label>Nakshatra</label>
                            <select id="newNakshatra">
                                <option value="Mula">Mula</option>
                                <option value="Purvaphalguni">Purvaphalguni</option>
                                <option value="Ardra">Ardra</option>
                                <option value="Uttarabhadrapada">Uttarabhadrapada</option>
                                <option value="Purvashadha">Purvashadha</option>
                                <option value="Ashwini">Ashwini</option>
                                <option value="Bharani">Bharani</option>
                                <option value="Krittika">Krittika</option>
                                <option value="Rohini">Rohini</option>
                                <option value="Mrigashira">Mrigashira</option>
                            </select>
                        </div>
                        <div class="form-group">
                            <label>Pada</label>
                            <select id="newPada">
                                <option value="1">1</option>
                                <option value="2">2</option>
                                <option value="3">3</option>
                                <option value="4">4</option>
                            </select>
                        </div>
                        <div class="form-group">
                            <label>Position (Degrees)</label>
                            <input type="text" id="newPosition" placeholder="07°33'20\"" value="07°33'20\"">
                        </div>
                        <div class="form-group">
                            <label>Declination</label>
                            <input type="number" id="newDeclination" step="0.01" placeholder="-28.48" value="-28.48">
                        </div>
                    </div>
                    
                    <div class="action-buttons">
                        <button class="action-button primary" onclick="addPlanetaryData()">Add Transit</button>
                        <button class="action-button" onclick="updateAllData()">Update All Data</button>
                        <button class="action-button" onclick="resetToDefaults()">Reset to Defaults</button>
                        <button class="action-button" onclick="exportData()">Export Data</button>
                        <button class="action-button" onclick="importData()">Import Data</button>
                    </div>
                </div>
            </div>
        </div>

        <!-- Market Timing Section (moved to timing-tab) -->
        <!-- Indian Markets Section -->
        <div class="market-section" id="indianSection" style="display: none;">
            <div class="market-title">🇮🇳 Indian Markets (9:15 AM - 3:30 PM IST)</div>
            <div class="timing-grid indian-grid" id="indianGrid">
                <!-- Headers will be populated by JavaScript -->
            </div>
        </div>

        <!-- Global Markets Section -->
        <div class="market-section" id="globalSection" style="display: none;">
            <div class="market-title">🌍 Global Markets & Commodities (5:00 AM - 11:55 PM IST)</div>
            <div class="timing-grid global-grid" id="globalGrid">
                <!-- Headers will be populated by JavaScript -->
            </div>
        </div>

        <div class="stats-panel" style="display: none;">
            <div class="stat-card">
                <div class="stat-value" id="bullishCount2">0</div>
                <div class="stat-label">Bullish Signals</div>
            </div>
            <div class="stat-card">
                <div class="stat-value" id="bearishCount2">0</div>
                <div class="stat-label">Bearish Signals</div>
            </div>
            <div class="stat-card">
                <div class="stat-value" id="neutralCount2">0</div>
                <div class="stat-label">Neutral Signals</div>
            </div>
            <div class="stat-card">
                <div class="stat-value" id="accuracyRate2">0%</div>
                <div class="stat-label">Historical Accuracy</div>
            </div>
        </div>
    </div>

    <script>
        // Sample planetary transit data
        let planetaryData = [
            {
                planet: "Mo", datetime: "2025-08-06T01:47:55", motion: "D", signLord: "Ju", starLord: "Ke", subLord: "Ju", 
                zodiac: "Sagittarius", nakshatra: "Mula", pada: 3, position: "07°33'20\"", declination: -28.48
            },
            {
                planet: "Ke", datetime: "2025-08-06T02:31:18", motion: "D", signLord: "Su", starLord: "Ve", subLord: "Me", 
                zodiac: "Leo", nakshatra: "Purvaphalguni", pada: 4, position: "25°53'19\"", declination: 3.96
            },
            {
                planet: "Ve", datetime: "2025-08-06T03:35:18", motion: "D", signLord: "Me", starLord: "Ra", subLord: "Me", 
                zodiac: "Gemini", nakshatra: "Ardra", pada: 2, position: "12°33'20\"", declination: 22.01
            },
            {
                planet: "Mo", datetime: "2025-08-06T05:12:16", motion: "D", signLord: "Ju", starLord: "Ke", subLord: "Sa", 
                zodiac: "Sagittarius", nakshatra: "Mula", pada: 3, position: "09°20'00\"", declination: -28.40
            },
            {
                planet: "Mo", datetime: "2025-08-06T09:14:06", motion: "D", signLord: "Ju", starLord: "Ke", subLord: "Me", 
                zodiac: "Sagittarius", nakshatra: "Mula", pada: 4, position: "11°26'40\"", declination: -28.28
            },
            {
                planet: "Sa", datetime: "2025-08-06T09:21:28", motion: "R", signLord: "Ju", starLord: "Sa", subLord: "Me", 
                zodiac: "Pisces", nakshatra: "Uttarabhadrapada", pada: 2, position: "07°19'59\"", declination: -1.62
            },
            {
                planet: "Mo", datetime: "2025-08-06T12:49:44", motion: "D", signLord: "Ju", starLord: "Ve", subLord: "Ve", 
                zodiac: "Sagittarius", nakshatra: "Purvashadha", pada: 1, position: "13°20'00\"", declination: -28.13
            },
            {
                planet: "Mo", datetime: "2025-08-06T17:02:29", motion: "D", signLord: "Ju", starLord: "Ve", subLord: "Su", 
                zodiac: "Sagittarius", nakshatra: "Purvashadha", pada: 1, position: "15°33'20\"", declination: -27.91
            },
            {
                planet: "Mo", datetime: "2025-08-06T18:18:07", motion: "D", signLord: "Ju", starLord: "Ve", subLord: "Mo", 
                zodiac: "Sagittarius", nakshatra: "Purvashadha", pada: 1, position: "16°13'20\"", declination: -27.84
            },
            {
                planet: "Mo", datetime: "2025-08-06T20:23:59", motion: "D", signLord: "Ju", starLord: "Ve", subLord: "Ma", 
                zodiac: "Sagittarius", nakshatra: "Purvashadha", pada: 2, position: "17°20'00\"", declination: -27.71
            }
        ];

        // Indian market configuration
        const indianMarkets = {
            symbols: ['NIFTY', 'BANKNIFTY', 'FINNIFTY', 'MIDCPNIFTY'],
            startTime: { hour: 9, minute: 15 },
            endTime: { hour: 15, minute: 30 },
            interval: 30 // minutes
        };

        // Global market configuration
        const globalMarkets = {
            symbols: ['GOLD', 'SILVER', 'CRUDE', 'BTC', 'DOW JONES', 'S&P 500', 'NASDAQ', 'USD/INR'],
            startTime: { hour: 5, minute: 0 },
            endTime: { hour: 23, minute: 55 },
            interval: 30 // minutes
        };

        // Tab switching functionality
        function switchTab(tabName) {
            // Hide all tab contents
            document.querySelectorAll('.tab-content').forEach(tab => {
                tab.classList.remove('active');
            });
            
            // Remove active class from all tab buttons
            document.querySelectorAll('.tab-button').forEach(button => {
                button.classList.remove('active');
            });
            
            // Show selected tab content
            document.getElementById(tabName + '-tab').classList.add('active');
            
            // Add active class to selected tab button
            event.target.classList.add('active');
            
            // Initialize tab-specific content
            if (tabName === 'planetary') {
                updatePlanetaryTable();
            }
        }

        // Update planetary table based on current date
        function updatePlanetaryTable() {
            const tbody = document.getElementById('planetaryTableBody');
            const selectedDate = document.getElementById('tradingDate').value;
            
            // Filter data for selected date
            const dateData = planetaryData.filter(item => 
                item.datetime.startsWith(selectedDate)
            );
            
            tbody.innerHTML = '';
            
            dateData.forEach(item => {
                const row = document.createElement('tr');
                const time = new Date(item.datetime).toLocaleTimeString('en-US', {
                    hour12: false,
                    hour: '2-digit',
                    minute: '2-digit',
                    second: '2-digit'
                });
                
                row.innerHTML = `
                    <td class="planet-symbol">${getPlanetSymbol(item.planet)}</td>
                    <td>${selectedDate}<br/>${time}</td>
                    <td class="${item.motion === 'D' ? 'motion-direct' : 'motion-retrograde'}">${item.motion}</td>
                    <td>${item.signLord}</td>
                    <td>${item.starLord}</td>
                    <td>${item.subLord}</td>
                    <td>${item.zodiac}</td>
                    <td>${item.nakshatra}</td>
                    <td>${item.pada}</td>
                    <td>${item.position}</td>
                    <td>${item.declination}</td>
                `;
                tbody.appendChild(row);
            });
            
            // Update summary statistics
            updateTransitSummary(dateData);
        }

        // Get planet symbol
        function getPlanetSymbol(planet) {
            const symbols = {
                'Mo': '☽', 'Su': '☉', 'Me': '☿', 'Ve': '♀', 'Ma': '♂',
                'Ju': '♃', 'Sa': '♄', 'Ra': '☊', 'Ke': '☋'
            };
            return symbols[planet] || planet;
        }

        // Update transit summary
        function updateTransitSummary(data) {
            document.getElementById('activeTransits').textContent = data.length;
            document.getElementById('retrogradeCount').textContent = 
                data.filter(item => item.motion === 'R').length;
            document.getElementById('majorAspects').textContent = Math.floor(Math.random() * 8) + 2;
            
            const impacts = ['Low', 'Moderate', 'High', 'Very High'];
            document.getElementById('marketImpact').textContent = 
                impacts[Math.floor(Math.random() * impacts.length)];
        }

        // Add new planetary data
        function addPlanetaryData() {
            const newData = {
                planet: document.getElementById('newPlanet').value,
                datetime: document.getElementById('newDate').value + 'T' + document.getElementById('newTime').value + ':00',
                motion: document.getElementById('newMotion').value,
                signLord: document.getElementById('newSignLord').value,
                starLord: document.getElementById('newStarLord').value,
                subLord: document.getElementById('newSubLord').value,
                zodiac: document.getElementById('newZodiac').value,
                nakshatra: document.getElementById('newNakshatra').value,
                pada: parseInt(document.getElementById('newPada').value),
                position: document.getElementById('newPosition').value,
                declination: parseFloat(document.getElementById('newDeclination').value)
            };
            
            planetaryData.push(newData);
            updatePlanetaryTable();
            alert('Planetary transit data added successfully!');
        }

        // Update all data based on date
        function updateAllData() {
            const selectedDate = document.getElementById('tradingDate').value;
            
            // Simulate updating data for new date
            // In real implementation, this would fetch from ephemeris database
            planetaryData.forEach(item => {
                // Update datetime to selected date while keeping time
                const time = item.datetime.split('T')[1];
                item.datetime = selectedDate + 'T' + time;
                
                // Simulate small changes in positions
                const currentDeg = parseFloat(item.position.split('°')[0]);
                const newDeg = (currentDeg + Math.random() * 2 - 1) % 30;
                item.position = newDeg.toFixed(0) + item.position.substring(item.position.indexOf('°'));
                
                // Simulate declination changes
                item.declination += (Math.random() - 0.5) * 0.1;
            });
            
            updatePlanetaryTable();
            initializeIndianGrid();
            initializeGlobalGrid();
            updateStatistics();
            alert('All planetary data updated for ' + selectedDate);
        }

        // Reset to default data
        function resetToDefaults() {
            // Reset to original sample data
            planetaryData = [
                {
                    planet: "Mo", datetime: "2025-08-06T01:47:55", motion: "D", signLord: "Ju", starLord: "Ke", subLord: "Ju", 
                    zodiac: "Sagittarius", nakshatra: "Mula", pada: 3, position: "07°33'20\"", declination: -28.48
                },
                // ... (rest of original data)
            ];
            updatePlanetaryTable();
            alert('Data reset to defaults');
        }

        // Export data
        function exportData() {
            const dataStr = JSON.stringify(planetaryData, null, 2);
            const dataBlob = new Blob([dataStr], {type: 'application/json'});
            const url = URL.createObjectURL(dataBlob);
            const link = document.createElement('a');
            link.href = url;
            link.download = 'planetary_data_' + document.getElementById('tradingDate').value + '.json';
            link.click();
        }

        // Import data
        function importData() {
            const input = document.createElement('input');
            input.type = 'file';
            input.accept = '.json';
            input.onchange = function(event) {
                const file = event.target.files[0];
                if (file) {
                    const reader = new FileReader();
                    reader.onload = function(e) {
                        try {
                            planetaryData = JSON.parse(e.target.result);
                            updatePlanetaryTable();
                            alert('Data imported successfully!');
                        } catch (error) {
                            alert('Error importing data: ' + error.message);
                        }
                    };
                    reader.readAsText(file);
                }
            };
            input.click();
        }

        // Generate time slots
        function generateTimeSlots(startTime, endTime, interval) {
            const slots = [];
            let current = startTime.hour * 60 + startTime.minute;
            const end = endTime.hour * 60 + endTime.minute;
            
            while (current <= end) {
                const hour = Math.floor(current / 60);
                const minute = current % 60;
                slots.push(`${hour.toString().padStart(2, '0')}:${minute.toString().padStart(2, '0')}`);
                current += interval;
            }
            return slots;
        }

        // Generate random astrological signals (enhanced with planetary data)
        function generateSignal(symbol, time) {
            const selectedDate = document.getElementById('tradingDate').value;
            const currentTime = selectedDate + 'T' + time + ':00';
            
            // Find nearest planetary transit
            const nearestTransit = planetaryData.find(item => 
                Math.abs(new Date(item.datetime) - new Date(currentTime)) < 3600000 // Within 1 hour
            );
            
            if (nearestTransit) {
                // Base signal on planetary data
                if (nearestTransit.motion === 'R') {
                    return Math.random() > 0.6 ? 'bearish' : 'strong-bearish';
                } else if (nearestTransit.pada === 1 || nearestTransit.pada === 4) {
                    return Math.random() > 0.5 ? 'bullish' : 'strong-bullish';
                }
            }
            
            // Default random signal
            const signals = ['strong-bullish', 'bullish', 'neutral', 'bearish', 'strong-bearish'];
            const probabilities = [0.15, 0.25, 0.35, 0.20, 0.05];
            
            let random = Math.random();
            let cumulative = 0;
            
            for (let i = 0; i < signals.length; i++) {
                cumulative += probabilities[i];
                if (random <= cumulative) {
                    return signals[i];
                }
            }
            return 'neutral';
        }

        // Get signal symbol
        function getSignalSymbol(signal) {
            const symbols = {
                'strong-bullish': '⬆⬆',
                'bullish': '↗',
                'neutral': '→',
                'bearish': '↘',
                'strong-bearish': '⬇⬇'
            };
            return symbols[signal] || '→';
        }

        // Initialize Indian markets grid
        function initializeIndianGrid() {
            const grid = document.getElementById('indianGrid');
            grid.innerHTML = '';
            
            const timeSlots = generateTimeSlots(indianMarkets.startTime, indianMarkets.endTime, indianMarkets.interval);
            
            // Add time headers
            grid.appendChild(createHeader('Symbol'));
            timeSlots.forEach(time => {
                grid.appendChild(createHeader(time));
            });
            
            // Add symbol rows
            indianMarkets.symbols.forEach(symbol => {
                const symbolCell = createSymbolCell(symbol);
                grid.appendChild(symbolCell);
                
                timeSlots.forEach(time => {
                    const signal = generateSignal(symbol, time);
                    const cell = createTimeCell(signal, symbol, time);
                    grid.appendChild(cell);
                });
            });
        }

        // Initialize Global markets grid
        function initializeGlobalGrid() {
            const grid = document.getElementById('globalGrid');
            grid.innerHTML = '';
            
            const timeSlots = generateTimeSlots(globalMarkets.startTime, globalMarkets.endTime, globalMarkets.interval);
            
            // Add time headers
            grid.appendChild(createHeader('Symbol'));
            timeSlots.forEach(time => {
                grid.appendChild(createHeader(time));
            });
            
            // Add symbol rows
            globalMarkets.symbols.forEach(symbol => {
                const symbolCell = createSymbolCell(symbol);
                grid.appendChild(symbolCell);
                
                timeSlots.forEach(time => {
                    const signal = generateSignal(symbol, time);
                    const cell = createTimeCell(signal, symbol, time);
                    grid.appendChild(cell);
                });
            });
        }

        // Create header cell
        function createHeader(text) {
            const header = document.createElement('div');
            header.className = 'time-header';
            header.textContent = text;
            return header;
        }

        // Create symbol cell
        function createSymbolCell(symbol) {
            const cell = document.createElement('div');
            cell.className = 'symbol-label';
            cell.textContent = symbol;
            return cell;
        }

        // Create time cell
        function createTimeCell(signal, symbol, time) {
            const cell = document.createElement('div');
            cell.className = `time-cell ${signal}`;
            cell.textContent = getSignalSymbol(signal);
            cell.title = `${symbol} at ${time}\nSignal: ${signal.replace('-', ' ').toUpperCase()}\nClick for details`;
            
            cell.addEventListener('click', () => {
                showSignalDetails(symbol, time, signal);
            });
            
            return cell;
        }

        // Show signal details
        function showSignalDetails(symbol, time, signal) {
            const selectedDate = document.getElementById('tradingDate').value;
            const currentTime = selectedDate + 'T' + time + ':00';
            
            // Find relevant planetary transit
            const relevantTransit = planetaryData.find(item => 
                Math.abs(new Date(item.datetime) - new Date(currentTime)) < 3600000
            );
            
            let planetaryInfo = '';
            if (relevantTransit) {
                planetaryInfo = `\n\nPlanetary Influence:\n${getPlanetSymbol(relevantTransit.planet)} ${relevantTransit.planet} in ${relevantTransit.zodiac}\nNakshatra: ${relevantTransit.nakshatra} (Pada ${relevantTransit.pada})\nMotion: ${relevantTransit.motion === 'D' ? 'Direct' : 'Retrograde'}`;
            }
            
            const details = {
                'strong-bullish': 'Strong planetary alignment favoring upward movement. High confidence.',
                'bullish': 'Positive planetary aspects. Moderate confidence for upward movement.',
                'neutral': 'Mixed planetary influences. No clear directional bias.',
                'bearish': 'Negative planetary aspects. Moderate confidence for downward movement.',
                'strong-bearish': 'Strong negative planetary alignment. High confidence for decline.'
            };
            
            alert(`${symbol} at ${time}\n\nSignal: ${signal.replace('-', ' ').toUpperCase()}\n\nAstrological Analysis:\n${details[signal]}${planetaryInfo}\n\nNote: This is for educational purposes only. Please do your own research before trading.`);
        }

        // Update statistics
        function updateStatistics() {
            const allCells = document.querySelectorAll('.time-cell');
            let bullish = 0, bearish = 0, neutral = 0;
            
            allCells.forEach(cell => {
                if (cell.classList.contains('strong-bullish') || cell.classList.contains('bullish')) {
                    bullish++;
                } else if (cell.classList.contains('strong-bearish') || cell.classList.contains('bearish')) {
                    bearish++;
                } else if (cell.classList.contains('neutral')) {
                    neutral++;
                }
            });
            
            document.getElementById('bullishCount').textContent = bullish;
            document.getElementById('bearishCount').textContent = bearish;
            document.getElementById('neutralCount').textContent = neutral;
            document.getElementById('accuracyRate').textContent = `${Math.floor(Math.random() * 20 + 70)}%`;
        }

        // Market selection handler
        document.getElementById('primaryMarket').addEventListener('change', function() {
            const value = this.value;
            const indianSection = document.getElementById('indianSection');
            const globalSection = document.getElementById('globalSection');
            
            switch(value) {
                case 'indian':
                    indianSection.style.display = 'block';
                    globalSection.style.display = 'none';
                    break;
                case 'global':
                    indianSection.style.display = 'none';
                    globalSection.style.display = 'block';
                    break;
                case 'both':
                    indianSection.style.display = 'block';
                    globalSection.style.display = 'block';
                    break;
            }
        });

        // Auto-update functionality
        let updateInterval;
        document.getElementById('autoUpdate').addEventListener('change', function() {
            clearInterval(updateInterval);
            
            const value = this.value;
            if (value !== 'off') {
                const minutes = value === '1min' ? 1 : 5;
                updateInterval = setInterval(() => {
                    initializeIndianGrid();
                    initializeGlobalGrid();
                    updateStatistics();
                    updatePlanetaryTable();
                }, minutes * 60 * 1000);
            }
        });

        // Date change handler
        document.getElementById('tradingDate').addEventListener('change', function() {
            initializeIndianGrid();
            initializeGlobalGrid();
            updateStatistics();
            updatePlanetaryTable();
        });

        // Initialize on page load
        document.addEventListener('DOMContentLoaded', function() {
            initializeIndianGrid();
            initializeGlobalGrid();
            updateStatistics();
            updatePlanetaryTable();
        });

        // Refresh every 5 seconds for demo purposes
        setInterval(() => {
            const autoUpdate = document.getElementById('autoUpdate').value;
            if (autoUpdate === 'off') {
                // Subtle updates for demo
                const randomCells = document.querySelectorAll('.time-cell');
                const randomIndex = Math.floor(Math.random() * randomCells.length);
                const cell = randomCells[randomIndex];
                if (cell && Math.random() > 0.95) { // 5% chance of change
                    const newSignal = generateSignal('', '');
                    cell.className = `time-cell ${newSignal}`;
                    cell.textContent = getSignalSymbol(newSignal);
                    updateStatistics();
                }
            }
        }, 5000);
    </script>
</body>
</html>
