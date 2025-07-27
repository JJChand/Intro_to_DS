# Trading Strategy Configuration

class MomentumConfig:
    """Configuration class for momentum trading strategy"""
    
    # Technical Indicator Parameters
    LOOKBACK_PERIOD = 20        # Period for momentum calculation
    FAST_MA_PERIOD = 10         # Fast moving average period
    SLOW_MA_PERIOD = 20         # Slow moving average period
    RSI_PERIOD = 14             # RSI calculation period
    
    # Signal Generation
    MOMENTUM_THRESHOLD = 0.02   # 2% momentum threshold for signals
    RSI_OVERSOLD = 30          # RSI oversold level
    RSI_OVERBOUGHT = 70        # RSI overbought level
    
    # Position Management
    POSITION_SIZE = 0.1         # 10% of portfolio per position
    MAX_POSITIONS = 5           # Maximum number of open positions
    MIN_TRADE_INTERVAL = 300    # 5 minutes minimum between trades (seconds)
    
    # Risk Management
    STOP_LOSS_PCT = 0.03        # 3% stop loss
    TAKE_PROFIT_PCT = 0.06      # 6% take profit
    DAILY_LOSS_LIMIT = 0.05     # 5% daily loss limit
    MAX_DRAWDOWN = 0.15         # 15% maximum drawdown
    
    # Portfolio Settings
    INITIAL_CAPITAL = 100000    # Starting capital
    
    # Market Filters
    MIN_VOLUME = 1000           # Minimum daily volume
    MIN_PRICE = 5.0             # Minimum stock price
    MAX_PRICE = 1000.0          # Maximum stock price
    
    # Advanced Parameters
    VOLUME_CONFIRMATION = True   # Use volume confirmation for signals
    NEWS_SENTIMENT_WEIGHT = 0.1  # Weight for news sentiment (0-1)
    
    # Logging
    LOG_LEVEL = 'INFO'          # Logging level
    LOG_TRADES = True           # Log all trades
    LOG_SIGNALS = True          # Log all signals
    
    @classmethod
    def get_config_dict(cls):
        """Return configuration as dictionary"""
        return {
            attr: getattr(cls, attr) 
            for attr in dir(cls) 
            if not attr.startswith('_') and not callable(getattr(cls, attr))
        } 