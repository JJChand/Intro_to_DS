# 📈 Momentum Trading Strategy

A comprehensive algorithmic trading strategy implementation for momentum-based trading competitions.

## 🎯 Strategy Overview

This momentum trading strategy uses technical indicators to identify and capitalize on price momentum in financial markets. The strategy combines multiple indicators to generate high-probability trading signals while maintaining strict risk management.

### Key Components:
- **Technical Indicators**: SMA, RSI, Price Momentum
- **Signal Generation**: Multi-factor momentum analysis
- **Risk Management**: Stop-loss, take-profit, position sizing
- **Portfolio Management**: Position limits and diversification

## 🔧 Technical Indicators

### 1. Simple Moving Averages (SMA)
- **Fast SMA**: 10-period (default)
- **Slow SMA**: 20-period (default)
- **Signal**: Buy when fast SMA > slow SMA (uptrend)

### 2. Relative Strength Index (RSI)
- **Period**: 14 (default)
- **Overbought**: 70
- **Oversold**: 30
- **Usage**: Momentum confirmation and reversal detection

### 3. Price Momentum
- **Lookback**: 20 periods (default)
- **Threshold**: 2% (default)
- **Calculation**: (Current Price - Past Price) / Past Price

## 📊 Signal Generation Logic

### Buy Signal Conditions:
1. **Momentum > 2%** (strong upward momentum)
2. **Fast SMA > Slow SMA** (uptrend confirmation)
3. **30 < RSI < 70** (not overbought/oversold)
4. **Current Price > Fast SMA** (price above trend)

### Sell Signal Conditions:
1. **Momentum < -2%** (strong downward momentum)
2. **Fast SMA < Slow SMA** (downtrend confirmation)
3. **30 < RSI < 70** (not overbought/oversold)
4. **Current Price < Fast SMA** (price below trend)

## 🛡️ Risk Management

### Position Sizing
- **Default**: 10% of portfolio per position
- **Dynamic**: Adjusts based on volatility and performance
- **Maximum Positions**: 5 concurrent positions

### Stop Loss & Take Profit
- **Stop Loss**: 3% loss per position
- **Take Profit**: 6% gain per position
- **Trailing Stop**: Available for advanced setups

### Portfolio Protection
- **Daily Loss Limit**: 5% of portfolio value
- **Maximum Drawdown**: 15% portfolio protection
- **Position Concentration**: No more than 20% in single position

## 🏗️ File Structure

```
DS/Algo_trading_competiton/
├── strategy1.py           # Main strategy implementation
├── config.py             # Configuration parameters
├── backtest_analysis.py  # Backtesting and analysis tools
├── test_strategy.py      # Strategy testing suite
└── README.md            # This documentation
```

## 🚀 Getting Started

### 1. Setup Environment
```bash
# Activate your conda environment
conda activate datascience

# Install required packages
pip install pandas numpy matplotlib seaborn
```

### 2. Configuration
Edit `config.py` to adjust strategy parameters:

```python
# Example configuration
MOMENTUM_THRESHOLD = 0.02    # 2% momentum threshold
POSITION_SIZE = 0.1          # 10% position size
STOP_LOSS_PCT = 0.03         # 3% stop loss
```

### 3. Run Tests
```bash
python test_strategy.py
```

### 4. Backtest Analysis
```bash
python backtest_analysis.py
```

## 📈 Performance Optimization

### Parameter Tuning
The strategy includes several parameters that can be optimized:

| Parameter | Default | Range | Impact |
|-----------|---------|-------|--------|
| Momentum Threshold | 2% | 1-5% | Signal sensitivity |
| Fast SMA Period | 10 | 5-15 | Trend responsiveness |
| Slow SMA Period | 20 | 15-30 | Trend stability |
| RSI Period | 14 | 10-20 | Momentum sensitivity |
| Position Size | 10% | 5-20% | Risk/reward ratio |

### Backtesting Results
Run the backtesting module to see performance metrics:

- **Sharpe Ratio**: Risk-adjusted returns
- **Maximum Drawdown**: Worst-case loss
- **Win Rate**: Percentage of profitable trades
- **Profit Factor**: Ratio of gross profit to gross loss

## 🎮 Competition Deployment

### 1. API Integration
Update the `place_order()` method in `strategy1.py` to integrate with your competition's API:

```python
def place_order(self, symbol, side, quantity, price):
    # Replace with actual API calls
    order_data = {
        'symbol': symbol,
        'side': side,
        'quantity': quantity,
        'price': price,
        'type': 'MARKET'
    }
    
    # API call to broker
    response = api.place_order(order_data)
    return response
```

### 2. Real-time Data
Ensure your data feeds are connected to live market data:

- Market data feed: Real-time price/volume data
- News feed: Sentiment analysis integration
- Economic data: Macro indicators

### 3. Monitoring
Implement monitoring and alerting:

```python
# Add to strategy for monitoring
if daily_pnl < -self.portfolio_value * 0.05:
    self.logger.warning("Daily loss limit reached!")
    # Send alert or reduce position sizes
```

## 🔍 Advanced Features

### News Sentiment Integration
```python
def analyze_news_sentiment(self, news_text):
    # Implement sentiment analysis
    sentiment_score = sentiment_analyzer.analyze(news_text)
    return sentiment_score
```

### Volume Confirmation
```python
def confirm_with_volume(self, symbol, signal):
    # Check if volume supports the signal
    recent_volume = self.volume_data[symbol]
    volume_trend = self.calculate_volume_trend(recent_volume)
    return volume_trend > 1.5  # 50% above average
```

### Machine Learning Enhancement
```python
def ml_signal_filter(self, technical_signals):
    # Use ML model to filter signals
    features = self.extract_features(technical_signals)
    prediction = self.ml_model.predict(features)
    return prediction > 0.7  # 70% confidence threshold
```

## 📚 Strategy Theory

### Momentum Explained
Momentum trading is based on the principle that stocks that have performed well recently will continue to perform well in the near future, and vice versa.

**Key Concepts:**
- **Trend Following**: Capitalize on existing trends
- **Breakout Trading**: Enter positions on momentum breakouts
- **Mean Reversion**: Exit before momentum reverses

### Why This Strategy Works
1. **Market Psychology**: Momentum reflects investor sentiment
2. **Information Cascades**: News and events create momentum
3. **Technical Patterns**: Chart patterns often predict continuation
4. **Risk Management**: Strict controls limit downside

## ⚠️ Risks and Limitations

### Market Risks
- **Whipsaws**: False signals in choppy markets
- **Trend Reversals**: Momentum can change quickly
- **Gap Risk**: Overnight gaps can bypass stop losses

### Strategy Risks
- **Over-optimization**: Curve-fitting to historical data
- **Correlation Risk**: Multiple positions in correlated assets
- **Liquidity Risk**: Difficulty exiting positions in illiquid markets

### Mitigation Strategies
- **Diversification**: Multiple uncorrelated positions
- **Position Sizing**: Limit exposure per trade
- **Market Filters**: Avoid trading in adverse conditions

## 🎯 Competition Tips

### 1. Start Conservative
- Begin with smaller position sizes
- Test thoroughly before scaling up
- Monitor performance closely

### 2. Adapt Quickly
- Adjust parameters based on market conditions
- Learn from losing trades
- Stay flexible with your approach

### 3. Risk Management First
- Never risk more than you can afford to lose
- Keep detailed logs of all trades
- Have exit strategies for all positions

## 📞 Support and Troubleshooting

### Common Issues
1. **No Signals Generated**: Check if enough historical data is available
2. **Orders Not Executing**: Verify API connection and permissions
3. **Poor Performance**: Review and optimize parameters

### Debug Mode
Enable detailed logging in `config.py`:
```python
LOG_LEVEL = 'DEBUG'
LOG_TRADES = True
LOG_SIGNALS = True
```

## 📈 Next Steps

1. **Backtest Thoroughly**: Test on various market conditions
2. **Paper Trade**: Practice with simulated money first
3. **Start Small**: Begin with minimal capital
4. **Monitor and Adjust**: Continuously improve the strategy
5. **Scale Gradually**: Increase position sizes as confidence grows

---

**Good luck with your algorithmic trading competition! 🚀**

*Remember: Past performance doesn't guarantee future results. Always trade responsibly.*