"""
加密货币数据获取模块
支持从Bitget和Binance获取加密货币数据
"""

import requests
import pandas as pd
import time
import random
from datetime import datetime, timedelta
from typing import Optional, Dict, Any, List
import warnings
warnings.filterwarnings('ignore')


class CryptoDataFetcher:
    """加密货币数据获取器 - 主要使用Bitget API，备选Binance API"""
    
    def __init__(self, retry_count: int = 5, retry_delay: float = 2.0):
        """
        初始化加密货币数据获取器
        
        Args:
            retry_count: 重试次数 (默认5次)
            retry_delay: 基础重试延迟(秒，默认2秒)
        """
        self.retry_count = retry_count
        self.retry_delay = retry_delay
        
        # Bitget API基础URL (免费，无需API密钥)
        self.bitget_base_url = "https://api.bitget.com/api/v2"
        
        # Binance API基础URL (免费，无需API密钥，作为备选)
        self.binance_base_url = "https://api.binance.com/api/v3"
    
    def get_crypto_data_bitget(self, symbol: str, granularity: str = "1day", 
                              limit: int = 200) -> Optional[pd.DataFrame]:
        """
        从Bitget获取加密货币K线数据
        
        Args:
            symbol: 交易对符号 (如 'BTCUSDT', 'ETHUSDT')
            granularity: K线粒度 ('1min', '5min', '15min', '30min', '1h', '4h', '6h', '12h', '1day', '1week')
            limit: 数据条数 (最大200)
            
        Returns:
            DataFrame: 包含OHLCV数据的DataFrame，失败返回None
        """
        for attempt in range(self.retry_count):
            try:
                print(f"📊 从Bitget获取 {symbol} 数据 (粒度: {granularity}, 条数: {limit}) - 第 {attempt + 1} 次尝试...")
                
                # 添加随机延迟避免请求过于频繁
                if attempt > 0:
                    random_delay = random.uniform(1.0, 3.0)
                    time.sleep(random_delay)
                
                # 获取K线数据
                url = f"{self.bitget_base_url}/spot/market/candles"
                params = {
                    'symbol': symbol.upper(),
                    'granularity': granularity,
                    'limit': min(limit, 200)  # Bitget限制最大200条
                }
                
                response = requests.get(url, params=params, timeout=30)
                response.raise_for_status()
                
                result = response.json()
                
                if result.get('code') == '00000' and result.get('data') and len(result['data']) > 0:
                    # 转换为DataFrame
                    df = self._convert_bitget_to_ohlcv(result['data'], symbol)
                    print(f"✅ 成功获取 {len(df)} 条数据")
                    return df
                else:
                    print(f"⚠️ 获取到空数据或API返回错误: {result.get('msg', '未知错误')}")
                    
            except Exception as e:
                error_msg = str(e).lower()
                print(f"❌ 第 {attempt + 1} 次尝试失败: {e}")
                
                if attempt < self.retry_count - 1:
                    # 指数退避策略
                    delay = self.retry_delay * (2 ** attempt) + random.uniform(1, 3)
                    
                    # 如果是请求频率限制，延迟更长时间
                    if "429" in error_msg or "rate limit" in error_msg:
                        delay = max(delay, 10 + random.uniform(5, 15))
                        print(f"🚫 检测到请求频率限制，延长等待时间...")
                    
                    print(f"⏳ {delay:.1f} 秒后重试...")
                    time.sleep(delay)
        
        print(f"❌ 获取 {symbol} 数据失败，已尝试 {self.retry_count} 次")
        return None
    
    def get_crypto_data(self, symbol: str, granularity: str = "1day", 
                       limit: int = 200) -> Optional[pd.DataFrame]:
        """
        获取加密货币数据 - 优先使用Bitget，失败时使用Binance
        
        Args:
            symbol: 交易对符号 (如 'BTCUSDT', 'ETHUSDT')
            granularity: K线粒度 (Bitget格式: '1day', '1h' 等)
            limit: 数据条数
            
        Returns:
            DataFrame: 包含OHLCV数据的DataFrame，失败返回None
        """
        print(f"🎯 开始获取 {symbol} 数据...")
        
        # 首先尝试Bitget
        print("🔄 尝试从Bitget获取数据...")
        data = self.get_crypto_data_bitget(symbol, granularity, limit)
        
        if data is not None:
            print("✅ Bitget数据获取成功")
            return data
        
        # Bitget失败，尝试Binance
        print("🔄 Bitget失败，尝试从Binance获取数据...")
        
        # 转换粒度格式 (Bitget -> Binance)
        granularity_map = {
            '1min': '1m', '5min': '5m', '15min': '15m', '30min': '30m',
            '1h': '1h', '4h': '4h', '6h': '6h', '12h': '12h',
            '1day': '1d', '1week': '1w'
        }
        binance_interval = granularity_map.get(granularity, '1d')
        
        data = self.get_crypto_data_binance(symbol, binance_interval, limit)
        
        if data is not None:
            print("✅ Binance数据获取成功")
            return data
        
        print("❌ 所有数据源都失败")
        return None
    
    def get_crypto_data_binance(self, symbol: str, interval: str = "1d", 
                               limit: int = 500) -> Optional[pd.DataFrame]:
        """
        从Binance获取加密货币K线数据
        
        Args:
            symbol: 交易对符号 (如 'BTCUSDT', 'ETHUSDT')
            interval: K线间隔 ('1m', '3m', '5m', '15m', '30m', '1h', '2h', '4h', '6h', '8h', '12h', '1d', '3d', '1w', '1M')
            limit: 数据条数 (最大1000)
            
        Returns:
            DataFrame: 包含OHLCV数据的DataFrame，失败返回None
        """
        for attempt in range(self.retry_count):
            try:
                print(f"📊 从Binance获取 {symbol} 数据 (间隔: {interval}, 条数: {limit}) - 第 {attempt + 1} 次尝试...")
                
                # 添加随机延迟避免请求过于频繁
                if attempt > 0:
                    random_delay = random.uniform(0.5, 2.0)
                    time.sleep(random_delay)
                
                url = f"{self.binance_base_url}/klines"
                params = {
                    'symbol': symbol.upper(),
                    'interval': interval,
                    'limit': min(limit, 1000)  # Binance限制最大1000条
                }
                
                response = requests.get(url, params=params, timeout=30)
                response.raise_for_status()
                
                data = response.json()
                
                if data and len(data) > 0:
                    # 转换为DataFrame
                    df = self._convert_binance_to_ohlcv(data, symbol)
                    print(f"✅ 成功获取 {len(df)} 条数据")
                    return df
                else:
                    print(f"⚠️ 获取到空数据")
                    
            except Exception as e:
                error_msg = str(e).lower()
                print(f"❌ 第 {attempt + 1} 次尝试失败: {e}")
                
                if attempt < self.retry_count - 1:
                    # 指数退避策略
                    delay = self.retry_delay * (2 ** attempt) + random.uniform(1, 2)
                    
                    # 如果是请求频率限制，延迟更长时间
                    if "429" in error_msg or "rate limit" in error_msg:
                        delay = max(delay, 5 + random.uniform(2, 8))
                        print(f"🚫 检测到请求频率限制，延长等待时间...")
                    
                    print(f"⏳ {delay:.1f} 秒后重试...")
                    time.sleep(delay)
        
        print(f"❌ 获取 {symbol} 数据失败，已尝试 {self.retry_count} 次")
        return None
    
    def get_crypto_info(self, symbol: str) -> Dict[str, Any]:
        """
        获取加密货币基本信息 - 从Bitget获取ticker信息
        
        Args:
            symbol: 交易对符号 (如 'BTCUSDT', 'ETHUSDT')
            
        Returns:
            Dict: 加密货币基本信息
        """
        try:
            # 从Bitget获取ticker信息
            url = f"{self.bitget_base_url}/spot/market/tickers"
            params = {'symbol': symbol.upper()}
            
            response = requests.get(url, params=params, timeout=30)
            response.raise_for_status()
            
            result = response.json()
            
            if result.get('code') == '00000' and result.get('data'):
                data_list = result['data']
                
                # 如果返回的是列表，找到匹配的交易对
                if isinstance(data_list, list):
                    data = None
                    for item in data_list:
                        if item.get('symbol') == symbol.upper():
                            data = item
                            break
                    
                    if data is None:
                        print(f"⚠️ 未找到交易对 {symbol} 的数据")
                        return {'symbol': symbol, 'error': f'未找到交易对 {symbol}'}
                else:
                    data = data_list
                
                # 提取关键信息
                key_info = {
                    'symbol': symbol.upper(),
                    'current_price': float(data.get('lastPr', 0)),
                    'price_change_24h': float(data.get('change24h', 0)),
                    'price_change_percentage_24h': float(data.get('changeUtc24h', 0)),
                    'high_24h': float(data.get('high24h', 0)),
                    'low_24h': float(data.get('low24h', 0)),
                    'volume_24h': float(data.get('baseVolume', 0)),
                    'quote_volume_24h': float(data.get('quoteVolume', 0)),
                    'bid_price': float(data.get('bidPr', 0)),
                    'ask_price': float(data.get('askPr', 0)),
                    'open_price': float(data.get('openUtc0', 0)),
                    'timestamp': data.get('ts', 0)
                }
                
                return key_info
            else:
                print(f"⚠️ Bitget API返回错误: {result.get('msg', '未知错误')}")
                return {'symbol': symbol, 'error': result.get('msg', '未知错误')}
            
        except Exception as e:
            print(f"❌ 获取 {symbol} 基本信息失败: {e}")
            return {'symbol': symbol, 'error': str(e)}
    
    def get_multiple_cryptos(self, symbols: List[str], granularity: str = "1day", 
                           limit: int = 200) -> Dict[str, pd.DataFrame]:
        """
        批量获取多个加密货币数据
        
        Args:
            symbols: 加密货币符号列表 (如 ['BTCUSDT', 'ETHUSDT'])
            granularity: K线粒度 (默认 '1day')
            limit: 数据条数 (默认 200)
            
        Returns:
            Dict: 加密货币符号为键，DataFrame为值的字典
        """
        results = {}
        total_symbols = len(symbols)
        
        print(f"🔄 开始批量获取 {total_symbols} 个加密货币数据...")
        
        for i, symbol in enumerate(symbols, 1):
            print(f"\n📈 处理第 {i}/{total_symbols} 个: {symbol}")
            
            # 使用主要获取方法（优先Bitget，备选Binance）
            data = self.get_crypto_data(symbol, granularity, limit)
            
            if data is not None:
                results[symbol] = data
                print(f"✅ {symbol} 数据获取成功")
            else:
                print(f"❌ {symbol} 数据获取失败")
            
            # 批量请求时增加延迟，避免API限制
            if i < total_symbols:  # 不是最后一个
                delay = random.uniform(3.0, 6.0)  # 增加延迟时间
                print(f"⏳ 等待 {delay:.1f} 秒后处理下一个...")
                time.sleep(delay)
        
        print(f"\n🎯 批量获取完成: 成功 {len(results)}/{total_symbols} 个加密货币")
        return results
    
    def _convert_bitget_to_ohlcv(self, data: List, symbol: str) -> pd.DataFrame:
        """
        将Bitget K线数据转换为标准OHLCV格式
        
        Args:
            data: Bitget API返回的K线数据
            symbol: 交易对符号
            
        Returns:
            DataFrame: 标准OHLCV格式的DataFrame
        """
        df_data = []
        for kline in data:
            # Bitget K线数据格式: [timestamp, open, high, low, close, volume, quoteVolume]
            df_data.append({
                'timestamp': pd.to_datetime(int(kline[0]), unit='ms'),
                'Open': float(kline[1]),
                'High': float(kline[2]),
                'Low': float(kline[3]),
                'Close': float(kline[4]),
                'Volume': float(kline[5])
            })
        
        df = pd.DataFrame(df_data)
        df.set_index('timestamp', inplace=True)
        
        # 按时间排序（从旧到新）
        df = df.sort_index()
        
        return df
    
    def _convert_binance_to_ohlcv(self, data: List, symbol: str) -> pd.DataFrame:
        """
        将Binance K线数据转换为标准OHLCV格式
        
        Args:
            data: Binance API返回的K线数据
            symbol: 交易对符号
            
        Returns:
            DataFrame: 标准OHLCV格式的DataFrame
        """
        df_data = []
        for kline in data:
            df_data.append({
                'timestamp': pd.to_datetime(int(kline[0]), unit='ms'),
                'Open': float(kline[1]),
                'High': float(kline[2]),
                'Low': float(kline[3]),
                'Close': float(kline[4]),
                'Volume': float(kline[5])
            })
        
        df = pd.DataFrame(df_data)
        df.set_index('timestamp', inplace=True)
        
        return df


# 常用加密货币交易对符号
POPULAR_CRYPTOS = {
    '主流币': ['BTCUSDT', 'ETHUSDT', 'BNBUSDT', 'ADAUSDT', 'SOLUSDT', 'DOTUSDT', 'DOGEUSDT', 'AVAXUSDT'],
    'DeFi币': ['UNIUSDT', 'LINKUSDT', 'AAVEUSDT', 'COMPUSDT', 'MKRUSDT', 'CRVUSDT', 'SUSHIUSDT'],
    'Layer1/Layer2': ['MATICUSDT', 'OPUSDT', 'ARBUSDT', 'LRCUSDT', 'ATOMUSDT', 'NEARUSDT'],
    '稳定币对': ['USDCUSDT', 'BUSDUSDT', 'DAIUSDT', 'TUSDUSDT'],
    'Meme币': ['DOGEUSDT', 'SHIBUSDT', 'PEPEUSDT', 'FLOKIUSDT'],
    '新兴币': ['APTUSDT', 'SUIUSDT', 'OPUSDT', 'ARBUSDT', 'LDOUSDT']
}


def get_popular_cryptos() -> Dict[str, List[str]]:
    """获取常用加密货币交易对符号分类"""
    return POPULAR_CRYPTOS


def create_fetcher(retry_count: int = 3, retry_delay: float = 2.0) -> CryptoDataFetcher:
    """
    创建加密货币数据获取器实例
    
    Args:
        retry_count: 重试次数 (默认3次)
        retry_delay: 基础重试延迟(秒，默认2秒)
        
    Returns:
        CryptoDataFetcher: 配置好的数据获取器实例
    """
    return CryptoDataFetcher(retry_count=retry_count, retry_delay=retry_delay)


def quick_get_crypto_data(symbol: str, days: int = 30) -> Optional[pd.DataFrame]:
    """
    快速获取加密货币数据的便捷函数
    
    Args:
        symbol: 交易对符号 (如 'BTCUSDT', 'ETHUSDT')
        days: 获取天数 (默认30天)
        
    Returns:
        DataFrame: OHLCV数据，失败返回None
    """
    fetcher = create_fetcher()
    return fetcher.get_crypto_data(symbol, granularity="1day", limit=days)


def quick_get_crypto_info(symbol: str) -> Dict[str, Any]:
    """
    快速获取加密货币基本信息的便捷函数
    
    Args:
        symbol: 交易对符号 (如 'BTCUSDT', 'ETHUSDT')
        
    Returns:
        Dict: 基本信息字典
    """
    fetcher = create_fetcher()
    return fetcher.get_crypto_info(symbol)