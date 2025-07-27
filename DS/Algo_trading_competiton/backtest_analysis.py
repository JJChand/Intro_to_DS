import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

class StrategyBacktester:
    """Backtesting and analysis for momentum trading strategy"""
    
    def __init__(self, strategy_results, benchmark_returns=None):
        self.results = strategy_results
        self.benchmark = benchmark_returns
        self.trades = []
        self.daily_returns = []
        self.positions_history = []
        
    def generate_sample_data(self, symbols=['AAPL', 'GOOGL', 'MSFT', 'TSLA', 'AMZN'], 
                           days=252, start_price=100):
        """Generate sample market data for backtesting"""
        np.random.seed(42)
        
        data = {}
        for symbol in symbols:
            dates = pd.date_range(start='2023-01-01', periods=days, freq='D')
            
            # Generate realistic price movements with momentum
            returns = np.random.normal(0.001, 0.02, days)  # Daily returns
            
            # Add momentum periods
            momentum_periods = np.random.choice(days, size=int(days*0.3), replace=False)
            for period in momentum_periods:
                # Create 5-10 day momentum streaks
                streak_length = np.random.randint(5, 11)
                direction = np.random.choice([-1, 1])
                for i in range(streak_length):
                    if period + i < days:
                        returns[period + i] += direction * 0.005
            
            # Calculate prices
            prices = [start_price]
            for ret in returns:
                prices.append(prices[-1] * (1 + ret))
            
            # Generate volume data
            volume = np.random.lognormal(10, 1, days + 1)
            
            data[symbol] = pd.DataFrame({
                'Date': dates.tolist() + [dates[-1] + timedelta(days=1)],
                'Price': prices,
                'Volume': volume,
                'Symbol': symbol
            })
        
        return data
    
    def calculate_performance_metrics(self, returns, benchmark_returns=None):
        """Calculate comprehensive performance metrics"""
        if len(returns) == 0:
            return {}
        
        returns = pd.Series(returns)
        
        metrics = {
            'Total Return': (returns + 1).prod() - 1,
            'Annualized Return': (returns + 1).prod() ** (252 / len(returns)) - 1,
            'Volatility': returns.std() * np.sqrt(252),
            'Sharpe Ratio': (returns.mean() * 252) / (returns.std() * np.sqrt(252)) if returns.std() > 0 else 0,
            'Max Drawdown': self.calculate_max_drawdown(returns),
            'Win Rate': (returns > 0).sum() / len(returns),
            'Average Win': returns[returns > 0].mean() if (returns > 0).any() else 0,
            'Average Loss': returns[returns < 0].mean() if (returns < 0).any() else 0,
            'Profit Factor': abs(returns[returns > 0].sum() / returns[returns < 0].sum()) if (returns < 0).any() else float('inf'),
            'Calmar Ratio': (returns.mean() * 252) / abs(self.calculate_max_drawdown(returns)) if self.calculate_max_drawdown(returns) != 0 else 0
        }
        
        if benchmark_returns is not None:
            benchmark_returns = pd.Series(benchmark_returns)
            metrics['Beta'] = returns.cov(benchmark_returns) / benchmark_returns.var()
            metrics['Alpha'] = metrics['Annualized Return'] - metrics['Beta'] * benchmark_returns.mean() * 252
            
        return metrics
    
    def calculate_max_drawdown(self, returns):
        """Calculate maximum drawdown"""
        cumulative = (1 + returns).cumprod()
        running_max = cumulative.expanding().max()
        drawdown = (cumulative - running_max) / running_max
        return drawdown.min()
    
    def analyze_trade_distribution(self, trades):
        """Analyze trade distribution and patterns"""
        if len(trades) == 0:
            return {}
        
        trade_df = pd.DataFrame(trades)
        
        analysis = {
            'Total Trades': len(trades),
            'Winning Trades': len(trade_df[trade_df['pnl'] > 0]),
            'Losing Trades': len(trade_df[trade_df['pnl'] < 0]),
            'Average Trade Duration': trade_df['duration'].mean(),
            'Best Trade': trade_df['pnl'].max(),
            'Worst Trade': trade_df['pnl'].min(),
            'Average Trade PnL': trade_df['pnl'].mean(),
            'Trade Frequency': len(trades) / 252,  # Trades per day
        }
        
        return analysis
    
    def plot_performance_dashboard(self, returns, trades=None, save_path=None):
        """Create comprehensive performance dashboard"""
        fig, axes = plt.subplots(2, 3, figsize=(18, 12))
        fig.suptitle('Momentum Trading Strategy Performance Dashboard', fontsize=16, fontweight='bold')
        
        returns = pd.Series(returns)
        cumulative_returns = (1 + returns).cumprod()
        
        # 1. Cumulative Returns
        axes[0, 0].plot(cumulative_returns.index, cumulative_returns.values, linewidth=2, color='blue')
        axes[0, 0].set_title('Cumulative Returns')
        axes[0, 0].set_ylabel('Cumulative Return')
        axes[0, 0].grid(True, alpha=0.3)
        
        # 2. Drawdown
        running_max = cumulative_returns.expanding().max()
        drawdown = (cumulative_returns - running_max) / running_max
        axes[0, 1].fill_between(drawdown.index, drawdown.values, 0, alpha=0.3, color='red')
        axes[0, 1].plot(drawdown.index, drawdown.values, color='red', linewidth=1)
        axes[0, 1].set_title('Drawdown')
        axes[0, 1].set_ylabel('Drawdown %')
        axes[0, 1].grid(True, alpha=0.3)
        
        # 3. Daily Returns Distribution
        axes[0, 2].hist(returns, bins=50, alpha=0.7, color='green', edgecolor='black')
        axes[0, 2].axvline(returns.mean(), color='red', linestyle='--', label=f'Mean: {returns.mean():.4f}')
        axes[0, 2].set_title('Daily Returns Distribution')
        axes[0, 2].set_xlabel('Daily Return')
        axes[0, 2].set_ylabel('Frequency')
        axes[0, 2].legend()
        axes[0, 2].grid(True, alpha=0.3)
        
        # 4. Rolling Sharpe Ratio
        rolling_sharpe = returns.rolling(30).mean() / returns.rolling(30).std() * np.sqrt(252)
        axes[1, 0].plot(rolling_sharpe.index, rolling_sharpe.values, color='purple', linewidth=2)
        axes[1, 0].set_title('30-Day Rolling Sharpe Ratio')
        axes[1, 0].set_ylabel('Sharpe Ratio')
        axes[1, 0].grid(True, alpha=0.3)
        
        # 5. Monthly Returns Heatmap
        if len(returns) > 30:
            monthly_returns = returns.resample('M').apply(lambda x: (1 + x).prod() - 1)
            monthly_table = monthly_returns.groupby([monthly_returns.index.year, monthly_returns.index.month]).first().unstack()
            sns.heatmap(monthly_table, annot=True, fmt='.2%', cmap='RdYlGn', center=0, ax=axes[1, 1])
            axes[1, 1].set_title('Monthly Returns Heatmap')
        else:
            axes[1, 1].text(0.5, 0.5, 'Insufficient data for monthly heatmap', ha='center', va='center')
            axes[1, 1].set_title('Monthly Returns Heatmap')
        
        # 6. Trade Analysis
        if trades and len(trades) > 0:
            trade_df = pd.DataFrame(trades)
            axes[1, 2].scatter(trade_df['duration'], trade_df['pnl'], alpha=0.6, c=trade_df['pnl'], cmap='RdYlGn')
            axes[1, 2].set_xlabel('Trade Duration (days)')
            axes[1, 2].set_ylabel('Trade P&L')
            axes[1, 2].set_title('Trade Analysis: Duration vs P&L')
            axes[1, 2].grid(True, alpha=0.3)
        else:
            axes[1, 2].text(0.5, 0.5, 'No trade data available', ha='center', va='center')
            axes[1, 2].set_title('Trade Analysis')
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        
        return fig
    
    def generate_performance_report(self, returns, trades=None, benchmark_returns=None):
        """Generate comprehensive performance report"""
        metrics = self.calculate_performance_metrics(returns, benchmark_returns)
        trade_analysis = self.analyze_trade_distribution(trades) if trades else {}
        
        report = f"""
╔═══════════════════════════════════════════════════════════════╗
║                    MOMENTUM STRATEGY PERFORMANCE REPORT        ║
╠═══════════════════════════════════════════════════════════════╣
║ PERFORMANCE METRICS                                           ║
╟───────────────────────────────────────────────────────────────╢
║ Total Return:          {metrics.get('Total Return', 0):.2%}                    ║
║ Annualized Return:     {metrics.get('Annualized Return', 0):.2%}                    ║
║ Volatility:            {metrics.get('Volatility', 0):.2%}                    ║
║ Sharpe Ratio:          {metrics.get('Sharpe Ratio', 0):.3f}                      ║
║ Max Drawdown:          {metrics.get('Max Drawdown', 0):.2%}                    ║
║ Calmar Ratio:          {metrics.get('Calmar Ratio', 0):.3f}                      ║
║ Win Rate:              {metrics.get('Win Rate', 0):.2%}                    ║
║ Profit Factor:         {metrics.get('Profit Factor', 0):.2f}                      ║
╟───────────────────────────────────────────────────────────────╢
║ TRADE ANALYSIS                                                ║
╟───────────────────────────────────────────────────────────────╢
║ Total Trades:          {trade_analysis.get('Total Trades', 0)}                         ║
║ Winning Trades:        {trade_analysis.get('Winning Trades', 0)}                         ║
║ Losing Trades:         {trade_analysis.get('Losing Trades', 0)}                         ║
║ Average Trade PnL:     ${trade_analysis.get('Average Trade PnL', 0):.2f}                    ║
║ Best Trade:            ${trade_analysis.get('Best Trade', 0):.2f}                    ║
║ Worst Trade:           ${trade_analysis.get('Worst Trade', 0):.2f}                    ║
║ Trade Frequency:       {trade_analysis.get('Trade Frequency', 0):.2f} trades/day            ║
╟───────────────────────────────────────────────────────────────╢
║ RISK METRICS                                                  ║
╟───────────────────────────────────────────────────────────────╢
║ Average Win:           {metrics.get('Average Win', 0):.2%}                    ║
║ Average Loss:          {metrics.get('Average Loss', 0):.2%}                    ║
║ Win/Loss Ratio:        {abs(metrics.get('Average Win', 0) / metrics.get('Average Loss', 1)):.2f}                      ║
╚═══════════════════════════════════════════════════════════════╝
        """
        
        return report, metrics, trade_analysis

def run_strategy_optimization():
    """Run parameter optimization for the momentum strategy"""
    print("🔍 Running Strategy Optimization...")
    
    # Parameter ranges to test
    momentum_thresholds = [0.01, 0.015, 0.02, 0.025, 0.03]
    fast_ma_periods = [5, 8, 10, 12, 15]
    slow_ma_periods = [15, 20, 25, 30]
    
    results = []
    
    for momentum_threshold in momentum_thresholds:
        for fast_ma in fast_ma_periods:
            for slow_ma in slow_ma_periods:
                if fast_ma >= slow_ma:
                    continue
                
                # Simulate strategy with these parameters
                # This would integrate with your actual strategy class
                simulated_return = np.random.normal(0.08, 0.15)  # Placeholder
                simulated_sharpe = np.random.normal(0.8, 0.3)   # Placeholder
                
                results.append({
                    'momentum_threshold': momentum_threshold,
                    'fast_ma': fast_ma,
                    'slow_ma': slow_ma,
                    'annual_return': simulated_return,
                    'sharpe_ratio': simulated_sharpe,
                    'score': simulated_return * 0.6 + simulated_sharpe * 0.4
                })
    
    # Find best parameters
    best_params = max(results, key=lambda x: x['score'])
    
    print(f"🏆 Best Parameters Found:")
    print(f"   Momentum Threshold: {best_params['momentum_threshold']}")
    print(f"   Fast MA Period: {best_params['fast_ma']}")
    print(f"   Slow MA Period: {best_params['slow_ma']}")
    print(f"   Expected Annual Return: {best_params['annual_return']:.2%}")
    print(f"   Expected Sharpe Ratio: {best_params['sharpe_ratio']:.3f}")
    
    return best_params

if __name__ == "__main__":
    # Example usage
    print("📊 Momentum Trading Strategy Analysis")
    print("=" * 50)
    
    # Generate sample data for demonstration
    backtester = StrategyBacktester({}, None)
    sample_data = backtester.generate_sample_data()
    
    # Generate sample returns for demonstration
    np.random.seed(42)
    sample_returns = np.random.normal(0.001, 0.02, 252)  # Daily returns for 1 year
    
    # Generate sample trades
    sample_trades = [
        {'symbol': 'AAPL', 'pnl': 150.0, 'duration': 5, 'entry_price': 150.0, 'exit_price': 153.0},
        {'symbol': 'GOOGL', 'pnl': -75.0, 'duration': 3, 'entry_price': 2500.0, 'exit_price': 2475.0},
        {'symbol': 'MSFT', 'pnl': 200.0, 'duration': 8, 'entry_price': 300.0, 'exit_price': 308.0},
    ]
    
    # Generate performance report
    report, metrics, trade_analysis = backtester.generate_performance_report(
        sample_returns, sample_trades
    )
    
    print(report)
    
    # Create performance dashboard
    fig = backtester.plot_performance_dashboard(sample_returns, sample_trades)
    plt.show()
    
    # Run optimization
    best_params = run_strategy_optimization() 