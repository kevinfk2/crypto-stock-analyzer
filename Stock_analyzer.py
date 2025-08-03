"""
股票技术分析主程序
提供完整的股票技术分析功能
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.data_fetcher import StockDataFetcher, get_popular_stocks
from src.technical_analyzer import analyze_stock_technical
from src.visualizer import create_analysis_report_chart, StockVisualizer
import pandas as pd
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')


class StockAnalysisSystem:
    """股票分析系统"""
    
    def __init__(self):
        """初始化系统"""
        self.data_fetcher = StockDataFetcher()
        self.visualizer = StockVisualizer()
        self.popular_stocks = get_popular_stocks()
        
    def show_welcome(self):
        """显示欢迎信息"""
        print("=" * 60)
        print("🚀 股票技术分析系统 v1.0")
        print("=" * 60)
        print("📈 功能特色:")
        print("  • 实时股票数据获取")
        print("  • 30+ 技术指标计算")
        print("  • 智能交易信号生成")
        print("  • 专业图表可视化")
        print("  • 多股票对比分析")
        print("=" * 60)
    
    def show_popular_stocks(self):
        """显示热门股票"""
        print("\n📊 热门股票分类:")
        for category, stocks in self.popular_stocks.items():
            print(f"\n🔸 {category}:")
            for i, stock in enumerate(stocks, 1):
                print(f"  {i}. {stock}")
    
    def get_user_choice(self) -> str:
        """获取用户选择"""
        print("\n" + "=" * 50)
        print("📋 请选择操作:")
        print("1. 分析单只股票")
        print("2. 批量分析多只股票")
        print("3. 股票对比分析")
        print("4. 查看热门股票")
        print("5. 自定义股票代码")
        print("0. 退出系统")
        print("=" * 50)
        
        choice = input("请输入选项 (0-5): ").strip()
        return choice
    
    def analyze_single_stock(self):
        """分析单只股票"""
        print("\n🎯 单只股票分析")
        print("-" * 30)
        
        # 获取股票代码
        symbol = input("请输入股票代码 (如 AAPL, TSLA): ").strip().upper()
        if not symbol:
            print("❌ 股票代码不能为空")
            return
        
        # 获取时间周期
        print("\n时间周期选项:")
        print("1. 1个月 (1mo)")
        print("2. 3个月 (3mo)")
        print("3. 6个月 (6mo)")
        print("4. 1年 (1y)")
        print("5. 2年 (2y)")
        
        period_choice = input("请选择时间周期 (1-5, 默认3): ").strip()
        period_map = {'1': '1mo', '2': '3mo', '3': '6mo', '4': '1y', '5': '2y'}
        period = period_map.get(period_choice, '3mo')
        
        print(f"\n🔄 正在分析 {symbol} (周期: {period})...")
        
        # 获取数据
        data = self.data_fetcher.get_stock_data(symbol, period)
        if data is None:
            print(f"❌ 无法获取 {symbol} 的数据")
            return
        
        # 获取股票基本信息
        stock_info = self.data_fetcher.get_stock_info(symbol)
        
        # 进行技术分析
        analysis_result = analyze_stock_technical(data, symbol)
        
        # 显示分析结果
        self.display_analysis_result(analysis_result, stock_info)
        
        # 询问是否生成图表
        show_chart = input("\n是否生成技术分析图表? (y/n, 默认y): ").strip().lower()
        if show_chart != 'n':
            create_analysis_report_chart(analysis_result)
    
    def analyze_multiple_stocks(self):
        """批量分析多只股票"""
        print("\n📊 批量股票分析")
        print("-" * 30)
        
        # 获取股票列表
        symbols_input = input("请输入股票代码 (用逗号分隔，如 AAPL,TSLA,GOOGL): ").strip()
        if not symbols_input:
            print("❌ 请输入至少一个股票代码")
            return
        
        symbols = [s.strip().upper() for s in symbols_input.split(',')]
        period = '3mo'  # 默认3个月
        
        print(f"\n🔄 正在批量分析 {len(symbols)} 只股票...")
        
        results = []
        for symbol in symbols:
            print(f"\n📈 分析 {symbol}...")
            data = self.data_fetcher.get_stock_data(symbol, period)
            if data is not None:
                result = analyze_stock_technical(data, symbol)
                results.append(result)
            else:
                print(f"❌ 跳过 {symbol} (数据获取失败)")
        
        if not results:
            print("❌ 没有成功分析的股票")
            return
        
        # 显示批量分析结果
        self.display_batch_results(results)
    
    def compare_stocks(self):
        """股票对比分析"""
        print("\n🔄 股票对比分析")
        print("-" * 30)
        
        symbols_input = input("请输入要对比的股票代码 (用逗号分隔): ").strip()
        if not symbols_input:
            print("❌ 请输入股票代码")
            return
        
        symbols = [s.strip().upper() for s in symbols_input.split(',')]
        if len(symbols) < 2:
            print("❌ 至少需要2只股票进行对比")
            return
        
        period = '6mo'  # 对比使用6个月数据
        
        print(f"\n🔄 正在获取对比数据...")
        stocks_data = {}
        
        for symbol in symbols:
            data = self.data_fetcher.get_stock_data(symbol, period)
            if data is not None:
                stocks_data[symbol] = data
                print(f"✅ {symbol} 数据获取成功")
            else:
                print(f"❌ {symbol} 数据获取失败")
        
        if len(stocks_data) < 2:
            print("❌ 可用数据不足，无法进行对比")
            return
        
        # 生成对比图表
        self.visualizer.plot_multi_stock_comparison(stocks_data)
        
        # 显示对比摘要
        self.display_comparison_summary(stocks_data)
    
    def display_analysis_result(self, result: dict, stock_info: dict):
        """显示分析结果"""
        print(f"\n" + "=" * 60)
        print(f"📊 {result['symbol']} 技术分析报告")
        print(f"📅 分析日期: {result['analysis_date']}")
        print("=" * 60)
        
        # 基本信息
        if 'name' in stock_info:
            print(f"🏢 公司名称: {stock_info['name']}")
        if 'sector' in stock_info:
            print(f"🏭 所属行业: {stock_info['sector']}")
        
        # 价格信息
        print(f"\n💰 价格信息:")
        print(f"  当前价格: ${result['current_price']}")
        
        change_emoji = "📈" if result['price_change'] > 0 else "📉" if result['price_change'] < 0 else "➡️"
        print(f"  日变化: {change_emoji} ${result['price_change']:+.2f} ({result['price_change_pct']:+.2f}%)")
        print(f"  成交量: {result['volume']:,}")
        
        # 技术指标摘要
        print(f"\n📊 关键技术指标:")
        indicators = result['indicators']
        
        if 'RSI_14' in indicators:
            rsi = indicators['RSI_14']
            rsi_status = "超买" if rsi > 70 else "超卖" if rsi < 30 else "正常"
            print(f"  RSI(14): {rsi:.1f} ({rsi_status})")
        
        if 'MACD' in indicators:
            print(f"  MACD: {indicators['MACD']:.3f}")
        
        if 'BB_percent' in indicators:
            bb = indicators['BB_percent']
            bb_status = "高位" if bb > 0.8 else "低位" if bb < 0.2 else "中位"
            print(f"  布林带位置: {bb:.2f} ({bb_status})")
        
        if 'MFI' in indicators:
            mfi = indicators['MFI']
            mfi_status = "超买" if mfi > 80 else "超卖" if mfi < 20 else "正常"
            print(f"  资金流量指数: {mfi:.1f} ({mfi_status})")
        
        # 移动平均线状态
        print(f"\n📈 移动平均线状态:")
        for period in [5, 20, 50]:
            key = f'Price_vs_SMA_{period}'
            if key in indicators:
                pct = indicators[key]
                status = "✅" if pct > 0 else "❌"
                print(f"  SMA{period}: {status} {pct:+.2f}%")
        
        # 交易信号
        signals = result['signals']
        score = signals['score']
        
        print(f"\n🎯 交易信号分析:")
        print(f"🟢 买入信号 ({len(signals['buy'])}):")
        for signal in signals['buy']:
            print(f"  • {signal}")
        
        print(f"\n🔴 卖出信号 ({len(signals['sell'])}):")
        for signal in signals['sell']:
            print(f"  • {signal}")
        
        print(f"\n🟡 中性信号 ({len(signals['neutral'])}):")
        for signal in signals['neutral']:
            print(f"  • {signal}")
        
        # 综合建议
        if score > 30:
            recommendation = "🚀 强烈买入"
            color = "🟢"
        elif score > 10:
            recommendation = "📈 买入"
            color = "🟢"
        elif score > -10:
            recommendation = "⚖️ 持有/观望"
            color = "🟡"
        elif score > -30:
            recommendation = "📉 卖出"
            color = "🔴"
        else:
            recommendation = "🔻 强烈卖出"
            color = "🔴"
        
        print(f"\n{color} 综合评分: {score}/100")
        print(f"💡 投资建议: {recommendation}")
        
        print(f"\n⚠️ 风险提示:")
        print(f"  • 技术分析仅供参考，不构成投资建议")
        print(f"  • 股市有风险，投资需谨慎")
        print(f"  • 建议结合基本面分析做出投资决策")
    
    def display_batch_results(self, results: list):
        """显示批量分析结果"""
        print(f"\n" + "=" * 80)
        print(f"📊 批量分析结果 ({len(results)} 只股票)")
        print("=" * 80)
        
        # 按评分排序
        sorted_results = sorted(results, key=lambda x: x['signals']['score'], reverse=True)
        
        print(f"{'排名':<4} {'股票':<8} {'当前价格':<10} {'日涨跌':<10} {'评分':<8} {'建议':<12}")
        print("-" * 80)
        
        for i, result in enumerate(sorted_results, 1):
            symbol = result['symbol']
            price = f"${result['current_price']:.2f}"
            change = f"{result['price_change_pct']:+.2f}%"
            score = result['signals']['score']
            
            if score > 10:
                recommendation = "买入"
            elif score > -10:
                recommendation = "持有"
            else:
                recommendation = "卖出"
            
            print(f"{i:<4} {symbol:<8} {price:<10} {change:<10} {score:<8} {recommendation:<12}")
        
        print("-" * 80)
        
        # 统计信息
        buy_count = sum(1 for r in results if r['signals']['score'] > 10)
        hold_count = sum(1 for r in results if -10 <= r['signals']['score'] <= 10)
        sell_count = sum(1 for r in results if r['signals']['score'] < -10)
        
        print(f"📈 买入推荐: {buy_count} 只")
        print(f"⚖️ 持有推荐: {hold_count} 只")
        print(f"📉 卖出推荐: {sell_count} 只")
    
    def display_comparison_summary(self, stocks_data: dict):
        """显示对比摘要"""
        print(f"\n📊 股票对比摘要:")
        print("-" * 50)
        
        for symbol, data in stocks_data.items():
            if len(data) > 1:
                start_price = data['Close'].iloc[0]
                end_price = data['Close'].iloc[-1]
                total_return = (end_price / start_price - 1) * 100
                
                avg_volume = data['Volume'].mean()
                volatility = data['Close'].pct_change().std() * 100
                
                print(f"{symbol}:")
                print(f"  总收益率: {total_return:+.2f}%")
                print(f"  平均成交量: {avg_volume:,.0f}")
                print(f"  波动率: {volatility:.2f}%")
                print()
    
    def run(self):
        """运行主程序"""
        self.show_welcome()
        
        while True:
            try:
                choice = self.get_user_choice()
                
                if choice == '0':
                    print("\n👋 感谢使用股票技术分析系统！")
                    break
                elif choice == '1':
                    self.analyze_single_stock()
                elif choice == '2':
                    self.analyze_multiple_stocks()
                elif choice == '3':
                    self.compare_stocks()
                elif choice == '4':
                    self.show_popular_stocks()
                elif choice == '5':
                    symbol = input("请输入自定义股票代码: ").strip().upper()
                    if symbol:
                        # 验证股票代码
                        if self.data_fetcher.validate_symbol(symbol):
                            print(f"✅ {symbol} 是有效的股票代码")
                        else:
                            print(f"❌ {symbol} 不是有效的股票代码")
                else:
                    print("❌ 无效选项，请重新选择")
                
                input("\n按回车键继续...")
                
            except KeyboardInterrupt:
                print("\n\n👋 程序已退出")
                break
            except Exception as e:
                print(f"\n❌ 发生错误: {e}")
                input("按回车键继续...")


if __name__ == "__main__":
    # 启动股票分析系统
    system = StockAnalysisSystem()
    system.run()