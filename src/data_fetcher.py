"""
数据获取模块
负责从各种数据源获取股票数据
"""

import yfinance as yf
import pandas as pd
import time
import random
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
import warnings
warnings.filterwarnings('ignore')


class StockDataFetcher:
    """股票数据获取器"""
    
    def __init__(self, retry_count: int = 5, retry_delay: float = 3.0):
        """
        初始化数据获取器
        
        Args:
            retry_count: 重试次数 (默认5次)
            retry_delay: 基础重试延迟(秒，默认3秒)
        """
        self.retry_count = retry_count
        self.retry_delay = retry_delay
    
    def get_stock_data(self, symbol: str, period: str = "1y", 
                      interval: str = "1d") -> Optional[pd.DataFrame]:
        """
        获取股票数据
        
        Args:
            symbol: 股票代码 (如 'AAPL', 'TSLA')
            period: 时间周期 ('1d', '5d', '1mo', '3mo', '6mo', '1y', '2y', '5y', '10y', 'ytd', 'max')
            interval: 数据间隔 ('1m', '2m', '5m', '15m', '30m', '60m', '90m', '1h', '1d', '5d', '1wk', '1mo', '3mo')
        
        Returns:
            DataFrame: 包含OHLCV数据的DataFrame，失败返回None
        """
        for attempt in range(self.retry_count):
            try:
                print(f"📊 获取 {symbol} 数据 (周期: {period}, 间隔: {interval}) - 第 {attempt + 1} 次尝试...")
                
                # 添加随机延迟避免请求过于频繁
                if attempt > 0:
                    random_delay = random.uniform(0.5, 2.0)
                    time.sleep(random_delay)
                
                ticker = yf.Ticker(symbol)
                data = ticker.history(period=period, interval=interval, auto_adjust=True, 
                                    prepost=False, actions=False)
                
                if not data.empty:
                    print(f"✅ 成功获取 {len(data)} 条数据")
                    return data
                else:
                    print(f"⚠️ 获取到空数据，可能股票代码无效")
                    
            except Exception as e:
                error_msg = str(e).lower()
                print(f"❌ 第 {attempt + 1} 次尝试失败: {e}")
                
                if attempt < self.retry_count - 1:
                    # 指数退避策略：每次重试延迟时间递增
                    delay = self.retry_delay * (2 ** attempt) + random.uniform(1, 3)
                    
                    # 如果是"Too Many Requests"错误，延迟更长时间
                    if "too many requests" in error_msg or "429" in error_msg:
                        delay = max(delay, 10 + random.uniform(5, 15))
                        print(f"🚫 检测到请求频率限制，延长等待时间...")
                    
                    print(f"⏳ {delay:.1f} 秒后重试...")
                    time.sleep(delay)
        
        print(f"❌ 获取 {symbol} 数据失败，已尝试 {self.retry_count} 次")
        return None
    
    def get_stock_info(self, symbol: str) -> Dict[str, Any]:
        """
        获取股票基本信息
        
        Args:
            symbol: 股票代码
            
        Returns:
            Dict: 股票基本信息
        """
        try:
            ticker = yf.Ticker(symbol)
            info = ticker.info
            
            # 提取关键信息
            key_info = {
                'symbol': symbol,
                'name': info.get('longName', 'N/A'),
                'sector': info.get('sector', 'N/A'),
                'industry': info.get('industry', 'N/A'),
                'market_cap': info.get('marketCap', 0),
                'current_price': info.get('currentPrice', 0),
                'previous_close': info.get('previousClose', 0),
                'day_high': info.get('dayHigh', 0),
                'day_low': info.get('dayLow', 0),
                'volume': info.get('volume', 0),
                'avg_volume': info.get('averageVolume', 0),
                'pe_ratio': info.get('trailingPE', 0),
                'dividend_yield': info.get('dividendYield', 0),
                '52_week_high': info.get('fiftyTwoWeekHigh', 0),
                '52_week_low': info.get('fiftyTwoWeekLow', 0),
            }
            
            return key_info
            
        except Exception as e:
            print(f"❌ 获取 {symbol} 基本信息失败: {e}")
            return {'symbol': symbol, 'error': str(e)}
    
    def get_multiple_stocks(self, symbols: list, period: str = "1y") -> Dict[str, pd.DataFrame]:
        """
        批量获取多只股票数据
        
        Args:
            symbols: 股票代码列表
            period: 时间周期
            
        Returns:
            Dict: 股票代码为键，DataFrame为值的字典
        """
        results = {}
        total_symbols = len(symbols)
        
        print(f"🔄 开始批量获取 {total_symbols} 只股票数据...")
        
        for i, symbol in enumerate(symbols, 1):
            print(f"\n📈 处理第 {i}/{total_symbols} 只股票: {symbol}")
            
            data = self.get_stock_data(symbol, period)
            if data is not None:
                results[symbol] = data
                print(f"✅ {symbol} 数据获取成功")
            else:
                print(f"❌ {symbol} 数据获取失败")
            
            # 批量请求时增加更长的延迟，避免API限制
            if i < total_symbols:  # 不是最后一个
                delay = random.uniform(2.0, 5.0)
                print(f"⏳ 等待 {delay:.1f} 秒后处理下一只股票...")
                time.sleep(delay)
        
        print(f"\n🎯 批量获取完成: 成功 {len(results)}/{total_symbols} 只股票")
        return results
    
    def validate_symbol(self, symbol: str) -> bool:
        """
        验证股票代码是否有效
        
        Args:
            symbol: 股票代码
            
        Returns:
            bool: 是否有效
        """
        try:
            ticker = yf.Ticker(symbol)
            info = ticker.info
            return 'symbol' in info or 'shortName' in info
        except:
            return False


# 常用股票代码
POPULAR_STOCKS = {
    '美股科技': ['AAPL', 'GOOGL', 'MSFT', 'TSLA', 'AMZN', 'META', 'NVDA', 'NFLX'],
    '美股指数': ['^GSPC', '^DJI', '^IXIC', '^RUT'],  # S&P500, 道琼斯, 纳斯达克, 罗素2000
    '中概股': ['BABA', 'JD', 'PDD', 'BIDU', 'NIO', 'XPEV', 'LI'],
    '港股': ['0700.HK', '0941.HK', '9988.HK', '1810.HK'],  # 腾讯, 中国移动, 阿里巴巴-SW, 小米
}


def get_popular_stocks() -> Dict[str, list]:
    """获取常用股票代码分类"""
    return POPULAR_STOCKS


if __name__ == "__main__":
    # 测试代码
    fetcher = StockDataFetcher()
    
    # 测试获取单只股票
    data = fetcher.get_stock_data("AAPL", "1mo")
    if data is not None:
        print(f"AAPL 最新价格: ${data['Close'].iloc[-1]:.2f}")
    
    # 测试获取股票信息
    info = fetcher.get_stock_info("AAPL")
    print(f"公司名称: {info.get('name', 'N/A')}")