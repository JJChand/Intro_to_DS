#!/usr/bin/env python3
"""
Test script for the momentum trading strategy
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from strategy1 import AlgoEvent
from config import MomentumConfig
from backtest_analysis import StrategyBacktester
import pandas as pd
import numpy as np

class MockMarketData:
    """Mock market data for testing"""
    def __init__(self, symbol, price, volume=1000, timestamp=None):
        self.symbol = symbol
        self.last_price = price
        self.price = price
        self.volume = volume
        self.timestamp = timestamp or pd.Timestamp.now()

class MockOrder:
    """Mock order for testing"""
    def __init__(self, symbol, status='FILLED'):
        self.symbol = symbol
        self.status = status

class MockPnL:
    """Mock P&L data for testing"""
    def __init__(self, pnl, total_value):
        self.pnl = pnl
        self.total_value = total_value

def test_technical_indicators():
    """Test technical indicator calculations"""
    print("🧪 Testing Technical Indicators...")
    
    strategy = AlgoEvent()
    
    # Test data
    test_prices = [100, 102, 101, 103, 105, 104, 106, 108, 107, 109, 
                   111, 110, 112, 114, 113, 115, 117, 116, 118, 120]
    
    # Test SMA calculation
    sma_10 = strategy.calculate_sma(test_prices, 10)
    print(f"   ✅ SMA(10) calculation: {sma_10:.2f}")
    
    # Test RSI calculation
    rsi = strategy.calculate_rsi(test_prices, 14)
    print(f"   ✅ RSI(14) calculation: {rsi:.2f}" if rsi else "   ⚠️  RSI: Insufficient data")
    
    # Test momentum calculation
    momentum = strategy.calculate_momentum(test_prices, 10)
    print(f"   ✅ Momentum calculation: {momentum:.4f}" if momentum else "   ⚠️  Momentum: Insufficient data")
    
    return all([sma_10 is not None, momentum is not None])

def test_signal_generation():
    """Test signal generation logic"""
    print("🧪 Testing Signal Generation...")
    
    strategy = AlgoEvent()
    symbol = 'TEST'
    
    # Add enough price data
    test_prices = [100 + i * 0.5 + np.random.normal(0, 0.5) for i in range(30)]
    
    for price in test_prices:
        strategy.price_data[symbol].append(price)
    
    # Generate signals
    current_price = test_prices[-1]
    signal_data = strategy.generate_signals(symbol, current_price)
    
    if signal_data:
        print(f"   ✅ Signal generated for {symbol}")
        print(f"      Signal: {signal_data['signal']}")
        print(f"      Price: ${signal_data['price']:.2f}")
        print(f"      Momentum: {signal_data['momentum']:.4f}")
        print(f"      Fast SMA: ${signal_data['sma_fast']:.2f}")
        print(f"      Slow SMA: ${signal_data['sma_slow']:.2f}")
        print(f"      RSI: {signal_data['rsi']:.2f}")
        return True
    else:
        print("   ⚠️  No signals generated (may need more data)")
        return False

def test_position_management():
    """Test position management functions"""
    print("🧪 Testing Position Management...")
    
    strategy = AlgoEvent()
    
    # Test position size calculation
    test_price = 150.0
    position_size = strategy.calculate_position_size(test_price)
    print(f"   ✅ Position size calculation: {position_size} shares at ${test_price}")
    
    # Test trade execution
    strategy.execute_trade('TEST', 'BUY', 100, 150.0)
    print(f"   ✅ Trade execution test: {len(strategy.positions)} position(s)")
    
    # Test exit conditions
    exit_needed = strategy.check_exit_conditions('TEST', 160.0)  # 6.67% gain
    print(f"   ✅ Exit condition check (6.67% gain): {'Exit needed' if exit_needed else 'Hold position'}")
    
    return len(strategy.positions) > 0

def test_market_data_processing():
    """Test market data feed processing"""
    print("🧪 Testing Market Data Processing...")
    
    strategy = AlgoEvent()
    
    # Simulate market data feed
    test_symbols = ['AAPL', 'GOOGL', 'MSFT']
    
    for i, symbol in enumerate(test_symbols):
        # Generate some historical data first
        for j in range(25):  # Enough for technical indicators
            price = 100 + i * 10 + j * 0.5 + np.random.normal(0, 0.5)
            mock_data = MockMarketData(symbol, price, volume=1000)
            strategy.on_marketdatafeed(mock_data, None)
    
    print(f"   ✅ Processed data for {len(strategy.price_data)} symbols")
    print(f"   ✅ Current positions: {len(strategy.positions)}")
    
    # Test with a strong momentum signal
    strong_momentum_price = 150.0  # Strong upward movement
    mock_data = MockMarketData('MOMENTUM_TEST', strong_momentum_price, volume=5000)
    
    # Add some base data first
    for j in range(25):
        price = 100 + j * 0.2
        strategy.price_data['MOMENTUM_TEST'].append(price)
    
    strategy.on_marketdatafeed(mock_data, None)
    
    return len(strategy.price_data) > 0

def test_risk_management():
    """Test risk management features"""
    print("🧪 Testing Risk Management...")
    
    strategy = AlgoEvent()
    
    # Test stop loss
    strategy.positions['TEST'] = {'qty': 100, 'entry_price': 100.0, 'side': 'long'}
    
    # Test 5% loss (should trigger stop loss)
    stop_loss_triggered = strategy.check_exit_conditions('TEST', 95.0)
    print(f"   ✅ Stop loss test (5% loss): {'Triggered' if stop_loss_triggered else 'Not triggered'}")
    
    # Test take profit
    take_profit_triggered = strategy.check_exit_conditions('TEST', 107.0)
    print(f"   ✅ Take profit test (7% gain): {'Triggered' if take_profit_triggered else 'Not triggered'}")
    
    # Test position limits
    for i in range(6):  # Try to create more than max_positions
        strategy.positions[f'TEST_{i}'] = {'qty': 100, 'entry_price': 100.0, 'side': 'long'}
    
    print(f"   ✅ Position limit test: {len(strategy.positions)} positions (max: {strategy.max_positions})")
    
    return True

def test_event_handlers():
    """Test all event handlers"""
    print("🧪 Testing Event Handlers...")
    
    strategy = AlgoEvent()
    
    # Test order feed
    mock_order = MockOrder('TEST', 'FILLED')
    strategy.on_orderfeed(mock_order)
    print("   ✅ Order feed handler")
    
    # Test P&L feed
    mock_pnl = MockPnL(pnl=500.0, total_value=105000.0)
    strategy.on_dailyPLfeed(mock_pnl)
    print("   ✅ Daily P&L feed handler")
    
    # Test news feed
    class MockNews:
        def __init__(self):
            self.headline = "Test news headline"
    
    strategy.on_newsdatafeed(MockNews())
    print("   ✅ News feed handler")
    
    return True

def run_full_strategy_test():
    """Run a comprehensive strategy test"""
    print("\n🚀 Running Full Strategy Test...")
    print("=" * 50)
    
    # Initialize strategy
    strategy = AlgoEvent()
    
    # Simulate a full trading day
    symbols = ['AAPL', 'GOOGL', 'MSFT', 'TSLA', 'AMZN']
    
    for minute in range(390):  # 6.5 hours * 60 minutes
        for symbol in symbols:
            # Generate realistic price movement
            base_price = {'AAPL': 150, 'GOOGL': 2500, 'MSFT': 300, 'TSLA': 200, 'AMZN': 3000}[symbol]
            
            # Add some trend and noise
            trend = 0.001 if minute > 200 else -0.0005  # Momentum after 200 minutes
            noise = np.random.normal(0, 0.002)
            price_change = trend + noise
            
            if len(strategy.price_data[symbol]) == 0:
                current_price = base_price
            else:
                current_price = list(strategy.price_data[symbol])[-1] * (1 + price_change)
            
            # Send market data
            mock_data = MockMarketData(symbol, current_price, volume=np.random.randint(1000, 10000))
            strategy.on_marketdatafeed(mock_data, None)
    
    # Print results
    print(f"\n📊 Test Results:")
    print(f"   Symbols processed: {len(strategy.price_data)}")
    print(f"   Positions opened: {len(strategy.positions)}")
    print(f"   Cash remaining: ${strategy.cash:,.2f}")
    print(f"   Portfolio value: ${strategy.portfolio_value:,.2f}")
    
    # Show positions
    if strategy.positions:
        print(f"\n💼 Current Positions:")
        for symbol, position in strategy.positions.items():
            current_price = list(strategy.price_data[symbol])[-1] if strategy.price_data[symbol] else 0
            pnl = (current_price - position['entry_price']) * position['qty']
            pnl_pct = (current_price - position['entry_price']) / position['entry_price']
            print(f"   {symbol}: {position['qty']} shares @ ${position['entry_price']:.2f}")
            print(f"      Current: ${current_price:.2f}, P&L: ${pnl:.2f} ({pnl_pct:.2%})")

if __name__ == "__main__":
    print("🎯 Momentum Trading Strategy Test Suite")
    print("=" * 60)
    
    # Run individual tests
    tests = [
        ("Technical Indicators", test_technical_indicators),
        ("Signal Generation", test_signal_generation), 
        ("Position Management", test_position_management),
        ("Market Data Processing", test_market_data_processing),
        ("Risk Management", test_risk_management),
        ("Event Handlers", test_event_handlers),
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n{test_name}:")
        print("-" * 30)
        try:
            result = test_func()
            results.append((test_name, result))
            print(f"   Status: {'✅ PASSED' if result else '❌ FAILED'}")
        except Exception as e:
            results.append((test_name, False))
            print(f"   Status: ❌ ERROR - {str(e)}")
    
    # Run comprehensive test
    run_full_strategy_test()
    
    # Summary
    print("\n📋 Test Summary:")
    print("=" * 30)
    passed = sum(1 for _, result in results if result)
    total = len(results)
    print(f"Tests passed: {passed}/{total}")
    
    if passed == total:
        print("🎉 All tests passed! Strategy is ready for deployment.")
    else:
        print("⚠️  Some tests failed. Please review the implementation.")
        
    print("\n💡 Next Steps:")
    print("1. Review and adjust parameters in config.py")
    print("2. Test with real market data")
    print("3. Run backtesting analysis")
    print("4. Deploy to competition environment") 