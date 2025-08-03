"""
加密货币技术分析器
专业的加密货币技术分析工具，支持Bitget和Binance数据源
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from crypto_data_fetcher import CryptoDataFetcher, get_popular_cryptos
from technical_analyzer import TechnicalAnalyzer
from visualizer import StockVisualizer
import pandas as pd
from datetime import datetime


def analyze_crypto(symbol: str, granularity: str = "1day", limit: int = 100):
    """
    分析单个加密货币
    
    Args:
        symbol: 加密货币符号 (如 BTCUSDT)
        granularity: 数据粒度 (如 1day, 1hour)
        limit: 数据条数
        
    Returns:
        tuple: (数据, 指标, 信号) 或 None
    """
    print(f"\n{'='*60}")
    print(f"🚀 加密货币技术分析: {symbol.upper()}")
    print(f"📊 数据源: Bitget (主要) / Binance (备选)")
    print(f"⏰ 数据粒度: {granularity}, 条数: {limit}")
    print(f"🕒 分析时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*60}")
    
    try:
        # 1. 获取数据
        fetcher = CryptoDataFetcher()
        data = fetcher.get_crypto_data(symbol, granularity=granularity, limit=limit)
        
        if data is None:
            print(f"❌ 无法获取 {symbol} 的数据")
            return None
            
        print(f"\n📈 数据概览:")
        print(f"   时间范围: {data.index[0].strftime('%Y-%m-%d')} 到 {data.index[-1].strftime('%Y-%m-%d')}")
        print(f"   数据条数: {len(data)} 条")
        print(f"   最新价格: ${data['Close'].iloc[-1]:,.4f}")
        print(f"   最高价格: ${data['High'].max():,.4f}")
        print(f"   最低价格: ${data['Low'].min():,.4f}")
        
        # 2. 技术分析
        print("\n🔧 开始技术分析...")
        analyzer = TechnicalAnalyzer(data)
        
        # 计算技术指标
        indicators = analyzer.calculate_all_indicators()
        
        # 生成交易信号
        signals = analyzer.generate_trading_signals()
        
        # 3. 显示结果
        print(f"\n📈 {symbol} 技术分析结果:")
        print(f"数据时间范围: {data.index[0].strftime('%Y-%m-%d')} 到 {data.index[-1].strftime('%Y-%m-%d')}")
        print(f"总数据条数: {len(data)}")
        
        # 显示最新价格信息
        latest = data.iloc[-1]
        print(f"\n💰 最新价格信息:")
        print(f"收盘价: ${latest['Close']:.2f}")
        print(f"开盘价: ${latest['Open']:.2f}")
        print(f"最高价: ${latest['High']:.2f}")
        print(f"最低价: ${latest['Low']:.2f}")
        print(f"成交量: {latest['Volume']:,.0f}")
        
        # 显示技术指标
        print(f"\n📊 技术指标:")
        # 获取指标摘要
        indicator_summary = analyzer.get_indicator_summary()
        
        # 显示主要技术指标
        if 'SMA_20' in indicator_summary:
            print(f"SMA(20): ${indicator_summary['SMA_20']:.2f}")
        if 'EMA_12' in indicator_summary:
            print(f"EMA(12): ${indicator_summary['EMA_12']:.2f}")
        if 'RSI_14' in indicator_summary:
            print(f"RSI(14): {indicator_summary['RSI_14']:.2f}")
        if 'MACD' in indicator_summary:
            print(f"MACD: {indicator_summary['MACD']:.4f}")
        if 'MACD_signal' in indicator_summary:
            print(f"MACD信号线: {indicator_summary['MACD_signal']:.4f}")
        if 'BB_percent' in indicator_summary:
            print(f"布林带位置: {indicator_summary['BB_percent']:.2f}")
        if 'ATR' in indicator_summary:
            print(f"ATR: {indicator_summary['ATR']:.4f}")
        if 'MFI' in indicator_summary:
            print(f"MFI: {indicator_summary['MFI']:.2f}")
        
        # 显示价格相对于均线的位置
        for key, value in indicator_summary.items():
            if key.startswith('Price_vs_SMA'):
                period = key.split('_')[-1]
                print(f"价格相对{period}: {value:+.2f}%")
        
        # 显示交易信号
        print(f"\n🎯 交易信号:")
        if isinstance(signals, dict):
            # 处理字典格式的信号
            buy_signals = signals.get('buy', [])
            sell_signals = signals.get('sell', [])
            neutral_signals = signals.get('neutral', [])
            score = signals.get('score', 0)
            
            print(f"\n🟢 买入信号 ({len(buy_signals)} 个):")
            for signal in buy_signals:
                print(f"   • {signal}")
            
            print(f"\n🔴 卖出信号 ({len(sell_signals)} 个):")
            for signal in sell_signals:
                print(f"   • {signal}")
            
            print(f"\n⚪ 中性信号 ({len(neutral_signals)} 个):")
            for signal in neutral_signals:
                print(f"   • {signal}")
            
            print(f"\n📊 综合评分: {score}/100")
            
            # 根据评分给出建议
            if score >= 60:
                recommendation = "强烈买入 🟢"
            elif score >= 30:
                recommendation = "买入 🟡"
            elif score >= -30:
                recommendation = "持有 ⚪"
            elif score >= -60:
                recommendation = "卖出 🟠"
            else:
                recommendation = "强烈卖出 🔴"
            print(f"💡 投资建议: {recommendation}")
        else:
            print("❌ 信号格式异常")
        
        print(f"\n✅ 分析完成!")
        return data, indicators, signals
        
    except Exception as e:
        print(f"❌ 技术分析失败: {e}")
        return None


def show_popular_cryptos():
    """显示常用加密货币列表"""
    print(f"\n📋 常用加密货币列表:")
    print(f"{'='*60}")
    
    try:
        categories = get_popular_cryptos()
        
        for category, cryptos in categories.items():
            print(f"\n🏷️  {category}:")
            for crypto in cryptos:
                print(f"   • {crypto}")
        
        print(f"\n💡 提示: 可以使用这些符号进行分析 (如: BTCUSDT)")
        
    except Exception as e:
        print(f"❌ 获取加密货币列表失败: {e}")


def main():
    """主函数 - 专业加密货币分析器"""
    print("🚀 专业加密货币技术分析器")
    print("=" * 60)
    print("📊 支持数据源: Bitget (主要) / Binance (备选)")
    print("🔧 技术指标: SMA, EMA, RSI, MACD, 布林带等")
    print("🎯 智能信号: 买入/卖出/持有建议")
    print("=" * 60)
    
    while True:
        print("\n🎛️  操作菜单:")
        print("1. 📈 分析加密货币")
        print("2. 📋 查看常用币种")
        print("3. 🔍 快速分析 (BTC)")
        print("4. 🔍 快速分析 (ETH)")
        print("5. ❌ 退出程序")
        
        try:
            choice = input("\n请选择操作 (1-5): ").strip()
            
            if choice == '1':
                symbol = input("请输入币种符号 (如 BTCUSDT): ").strip().upper()
                if not symbol:
                    print("❌ 请输入有效的符号")
                    continue
                    
                print("\n⏰ 数据粒度选项:")
                print("1. 1day (日线)")
                print("2. 1hour (小时线)")
                print("3. 15min (15分钟线)")
                
                granularity_choice = input("选择粒度 (1-3, 默认1): ").strip() or "1"
                granularity_map = {"1": "1day", "2": "1hour", "3": "15min"}
                granularity = granularity_map.get(granularity_choice, "1day")
                
                try:
                    limit = int(input("数据条数 (默认100): ").strip() or "100")
                    limit = min(max(limit, 10), 1000)  # 限制在10-1000之间
                except ValueError:
                    limit = 100
                    
                analyze_crypto(symbol, granularity, limit)
                
            elif choice == '2':
                show_popular_cryptos()
                
            elif choice == '3':
                print("\n🚀 快速分析 BTC...")
                analyze_crypto("BTCUSDT", "1day", 100)
                
            elif choice == '4':
                print("\n🚀 快速分析 ETH...")
                analyze_crypto("ETHUSDT", "1day", 100)
                
            elif choice == '5':
                print("\n👋 感谢使用专业加密货币分析器!")
                print("💡 提示: 投资有风险，决策需谨慎")
                break
                
            else:
                print("❌ 无效选择，请输入 1-5")
                
        except KeyboardInterrupt:
            print("\n\n👋 程序已退出")
            break
        except Exception as e:
            print(f"❌ 程序错误: {e}")
            print("🔄 请重试...")


if __name__ == "__main__":
    main()