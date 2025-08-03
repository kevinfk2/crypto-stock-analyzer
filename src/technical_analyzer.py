"""
技术分析模块
计算各种技术指标和生成交易信号
"""

import pandas as pd
import numpy as np
import ta
from typing import Dict, List, Tuple, Optional
import warnings
warnings.filterwarnings('ignore')


class TechnicalAnalyzer:
    """技术分析器"""
    
    def __init__(self, data: pd.DataFrame):
        """
        初始化技术分析器
        
        Args:
            data: 包含OHLCV数据的DataFrame
        """
        self.data = data.copy()
        self.indicators = {}
        
    def calculate_trend_indicators(self) -> Dict[str, pd.Series]:
        """
        计算趋势指标
        
        Returns:
            Dict: 趋势指标字典
        """
        indicators = {}
        
        # 简单移动平均线
        for period in [5, 10, 20, 50, 100, 200]:
            indicators[f'SMA_{period}'] = ta.trend.sma_indicator(self.data['Close'], window=period)
        
        # 指数移动平均线
        for period in [12, 26, 50]:
            indicators[f'EMA_{period}'] = ta.trend.ema_indicator(self.data['Close'], window=period)
        
        # MACD
        indicators['MACD'] = ta.trend.macd(self.data['Close'])
        indicators['MACD_signal'] = ta.trend.macd_signal(self.data['Close'])
        indicators['MACD_histogram'] = ta.trend.macd_diff(self.data['Close'])
        
        # 布林带
        bb = ta.volatility.BollingerBands(self.data['Close'])
        indicators['BB_upper'] = bb.bollinger_hband()
        indicators['BB_middle'] = bb.bollinger_mavg()
        indicators['BB_lower'] = bb.bollinger_lband()
        indicators['BB_percent'] = bb.bollinger_pband()
        indicators['BB_width'] = bb.bollinger_wband()
        
        # 抛物线SAR
        indicators['PSAR'] = ta.trend.psar_up(self.data['High'], self.data['Low'], self.data['Close'])
        
        # 一目均衡表
        indicators['Ichimoku_a'] = ta.trend.ichimoku_a(self.data['High'], self.data['Low'])
        indicators['Ichimoku_b'] = ta.trend.ichimoku_b(self.data['High'], self.data['Low'])
        
        self.indicators.update(indicators)
        return indicators
    
    def calculate_momentum_indicators(self) -> Dict[str, pd.Series]:
        """
        计算动量指标
        
        Returns:
            Dict: 动量指标字典
        """
        indicators = {}
        
        # RSI
        for period in [14, 21]:
            indicators[f'RSI_{period}'] = ta.momentum.rsi(self.data['Close'], window=period)
        
        # 随机指标
        indicators['Stoch_K'] = ta.momentum.stoch(self.data['High'], self.data['Low'], self.data['Close'])
        indicators['Stoch_D'] = ta.momentum.stoch_signal(self.data['High'], self.data['Low'], self.data['Close'])
        
        # Williams %R
        indicators['Williams_R'] = ta.momentum.williams_r(self.data['High'], self.data['Low'], self.data['Close'])
        
        # 商品通道指数CCI
        indicators['CCI'] = ta.trend.cci(self.data['High'], self.data['Low'], self.data['Close'])
        
        # 动量指标
        indicators['Momentum'] = ta.momentum.roc(self.data['Close'], window=10)
        
        # 终极振荡器
        indicators['Ultimate_Oscillator'] = ta.momentum.ultimate_oscillator(
            self.data['High'], self.data['Low'], self.data['Close']
        )
        
        self.indicators.update(indicators)
        return indicators
    
    def calculate_volatility_indicators(self) -> Dict[str, pd.Series]:
        """
        计算波动性指标
        
        Returns:
            Dict: 波动性指标字典
        """
        indicators = {}
        
        # 平均真实范围ATR
        indicators['ATR'] = ta.volatility.average_true_range(
            self.data['High'], self.data['Low'], self.data['Close']
        )
        
        # 唐奇安通道
        indicators['Donchian_high'] = ta.volatility.donchian_channel_hband(
            self.data['High'], self.data['Low'], self.data['Close']
        )
        indicators['Donchian_low'] = ta.volatility.donchian_channel_lband(
            self.data['High'], self.data['Low'], self.data['Close']
        )
        indicators['Donchian_middle'] = ta.volatility.donchian_channel_mband(
            self.data['High'], self.data['Low'], self.data['Close']
        )
        
        # 肯特纳通道
        indicators['Keltner_high'] = ta.volatility.keltner_channel_hband(
            self.data['High'], self.data['Low'], self.data['Close']
        )
        indicators['Keltner_low'] = ta.volatility.keltner_channel_lband(
            self.data['High'], self.data['Low'], self.data['Close']
        )
        indicators['Keltner_middle'] = ta.volatility.keltner_channel_mband(
            self.data['High'], self.data['Low'], self.data['Close']
        )
        
        self.indicators.update(indicators)
        return indicators
    
    def calculate_volume_indicators(self) -> Dict[str, pd.Series]:
        """
        计算成交量指标
        
        Returns:
            Dict: 成交量指标字典
        """
        indicators = {}
        
        # 能量潮OBV
        indicators['OBV'] = ta.volume.on_balance_volume(self.data['Close'], self.data['Volume'])
        
        # 累积/派发线A/D
        indicators['AD'] = ta.volume.acc_dist_index(
            self.data['High'], self.data['Low'], self.data['Close'], self.data['Volume']
        )
        
        # 资金流量指数MFI
        indicators['MFI'] = ta.volume.money_flow_index(
            self.data['High'], self.data['Low'], self.data['Close'], self.data['Volume']
        )
        
        # 成交量加权平均价格VWAP
        indicators['VWAP'] = ta.volume.volume_weighted_average_price(
            self.data['High'], self.data['Low'], self.data['Close'], self.data['Volume']
        )
        
        # 简易波动指标EMV
        indicators['EMV'] = ta.volume.ease_of_movement(
            self.data['High'], self.data['Low'], self.data['Volume']
        )
        
        # 成交量震荡器
        indicators['Volume_SMA'] = ta.trend.sma_indicator(self.data['Volume'], window=20)
        
        self.indicators.update(indicators)
        return indicators
    
    def calculate_all_indicators(self) -> Dict[str, pd.Series]:
        """
        计算所有技术指标
        
        Returns:
            Dict: 所有指标字典
        """
        print("🔄 计算趋势指标...")
        self.calculate_trend_indicators()
        
        print("🔄 计算动量指标...")
        self.calculate_momentum_indicators()
        
        print("🔄 计算波动性指标...")
        self.calculate_volatility_indicators()
        
        print("🔄 计算成交量指标...")
        self.calculate_volume_indicators()
        
        print("✅ 所有技术指标计算完成")
        return self.indicators
    
    def generate_trading_signals(self) -> Dict[str, List[str]]:
        """
        生成交易信号
        
        Returns:
            Dict: 包含买入、卖出、中性信号的字典
        """
        if not self.indicators:
            self.calculate_all_indicators()
        
        signals = {'buy': [], 'sell': [], 'neutral': [], 'score': 0}
        
        # 获取最新数据
        latest_idx = -1
        prev_idx = -2 if len(self.data) > 1 else -1
        
        try:
            # RSI信号
            rsi = self.indicators['RSI_14'].iloc[latest_idx]
            if not pd.isna(rsi):
                if rsi < 30:
                    signals['buy'].append(f"RSI超卖 ({rsi:.1f})")
                    signals['score'] += 20
                elif rsi > 70:
                    signals['sell'].append(f"RSI超买 ({rsi:.1f})")
                    signals['score'] -= 20
                else:
                    signals['neutral'].append(f"RSI正常 ({rsi:.1f})")
            
            # MACD信号
            macd_current = self.indicators['MACD'].iloc[latest_idx]
            macd_signal_current = self.indicators['MACD_signal'].iloc[latest_idx]
            macd_prev = self.indicators['MACD'].iloc[prev_idx]
            macd_signal_prev = self.indicators['MACD_signal'].iloc[prev_idx]
            
            if not any(pd.isna([macd_current, macd_signal_current, macd_prev, macd_signal_prev])):
                if macd_current > macd_signal_current and macd_prev <= macd_signal_prev:
                    signals['buy'].append("MACD金叉")
                    signals['score'] += 25
                elif macd_current < macd_signal_current and macd_prev >= macd_signal_prev:
                    signals['sell'].append("MACD死叉")
                    signals['score'] -= 25
            
            # 布林带信号
            bb_percent = self.indicators['BB_percent'].iloc[latest_idx]
            if not pd.isna(bb_percent):
                if bb_percent > 0.8:
                    signals['sell'].append(f"布林带高位 ({bb_percent:.2f})")
                    signals['score'] -= 15
                elif bb_percent < 0.2:
                    signals['buy'].append(f"布林带低位 ({bb_percent:.2f})")
                    signals['score'] += 15
            
            # 移动平均线信号
            close_price = self.data['Close'].iloc[latest_idx]
            sma_20 = self.indicators['SMA_20'].iloc[latest_idx]
            sma_50 = self.indicators['SMA_50'].iloc[latest_idx]
            
            if not any(pd.isna([close_price, sma_20, sma_50])):
                above_sma20 = close_price > sma_20
                above_sma50 = close_price > sma_50
                
                if above_sma20 and above_sma50:
                    signals['buy'].append("价格高于主要均线")
                    signals['score'] += 15
                elif not above_sma20 and not above_sma50:
                    signals['sell'].append("价格低于主要均线")
                    signals['score'] -= 15
            
            # Williams %R信号
            wr = self.indicators['Williams_R'].iloc[latest_idx]
            if not pd.isna(wr):
                if wr > -20:
                    signals['sell'].append(f"Williams %R超买 ({wr:.1f})")
                    signals['score'] -= 10
                elif wr < -80:
                    signals['buy'].append(f"Williams %R超卖 ({wr:.1f})")
                    signals['score'] += 10
            
            # MFI信号
            mfi = self.indicators['MFI'].iloc[latest_idx]
            if not pd.isna(mfi):
                if mfi > 80:
                    signals['sell'].append(f"MFI超买 ({mfi:.1f})")
                    signals['score'] -= 10
                elif mfi < 20:
                    signals['buy'].append(f"MFI超卖 ({mfi:.1f})")
                    signals['score'] += 10
        
        except Exception as e:
            print(f"⚠️ 信号生成过程中出现错误: {e}")
        
        return signals
    
    def get_indicator_summary(self) -> Dict[str, float]:
        """
        获取指标摘要
        
        Returns:
            Dict: 最新指标值摘要
        """
        if not self.indicators:
            self.calculate_all_indicators()
        
        summary = {}
        latest_idx = -1
        
        # 关键指标
        key_indicators = [
            'RSI_14', 'MACD', 'MACD_signal', 'BB_percent', 
            'ATR', 'MFI', 'Williams_R', 'CCI'
        ]
        
        for indicator in key_indicators:
            if indicator in self.indicators:
                value = self.indicators[indicator].iloc[latest_idx]
                if not pd.isna(value):
                    summary[indicator] = round(float(value), 3)
        
        # 价格相对于移动平均线的位置
        close_price = self.data['Close'].iloc[latest_idx]
        for period in [5, 20, 50]:
            sma_key = f'SMA_{period}'
            if sma_key in self.indicators:
                sma_value = self.indicators[sma_key].iloc[latest_idx]
                if not pd.isna(sma_value):
                    summary[f'Price_vs_{sma_key}'] = round((close_price / sma_value - 1) * 100, 2)
        
        return summary
    
    def add_indicators_to_data(self) -> pd.DataFrame:
        """
        将指标添加到原始数据中
        
        Returns:
            DataFrame: 包含所有指标的数据
        """
        if not self.indicators:
            self.calculate_all_indicators()
        
        result_data = self.data.copy()
        
        for name, series in self.indicators.items():
            result_data[name] = series
        
        return result_data


def analyze_stock_technical(data: pd.DataFrame, symbol: str = "") -> Dict:
    """
    对股票进行完整的技术分析
    
    Args:
        data: 股票OHLCV数据
        symbol: 股票代码
        
    Returns:
        Dict: 分析结果
    """
    analyzer = TechnicalAnalyzer(data)
    
    # 计算所有指标
    indicators = analyzer.calculate_all_indicators()
    
    # 生成交易信号
    signals = analyzer.generate_trading_signals()
    
    # 获取指标摘要
    summary = analyzer.get_indicator_summary()
    
    # 当前价格信息
    latest = data.iloc[-1]
    prev = data.iloc[-2] if len(data) > 1 else latest
    
    price_change = latest['Close'] - prev['Close']
    price_change_pct = (price_change / prev['Close']) * 100
    
    result = {
        'symbol': symbol,
        'analysis_date': data.index[-1].strftime('%Y-%m-%d'),
        'current_price': round(latest['Close'], 2),
        'price_change': round(price_change, 2),
        'price_change_pct': round(price_change_pct, 2),
        'volume': int(latest['Volume']),
        'indicators': summary,
        'signals': signals,
        'data_with_indicators': analyzer.add_indicators_to_data()
    }
    
    return result


if __name__ == "__main__":
    # 测试代码
    import sys
    sys.path.append('..')
    from data_fetcher import StockDataFetcher
    
    fetcher = StockDataFetcher()
    data = fetcher.get_stock_data("AAPL", "3mo")
    
    if data is not None:
        result = analyze_stock_technical(data, "AAPL")
        print(f"分析结果: {result['symbol']}")
        print(f"当前价格: ${result['current_price']}")
        print(f"信号评分: {result['signals']['score']}")