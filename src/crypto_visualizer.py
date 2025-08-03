#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
加密货币可视化模块
专门用于加密货币技术分析的图表可视化
"""

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import seaborn as sns
from typing import Dict, Any, Optional, Tuple
import warnings
warnings.filterwarnings('ignore')

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False

class CryptoVisualizer:
    """加密货币可视化类"""
    
    def __init__(self, figsize: Tuple[int, int] = (15, 10)):
        """
        初始化可视化器
        
        Args:
            figsize: 图表大小 (宽, 高)
        """
        self.figsize = figsize
        self.colors = {
            'up': '#00ff88',      # 上涨绿色
            'down': '#ff4444',    # 下跌红色
            'ma': '#ffaa00',      # 均线橙色
            'volume': '#666666',  # 成交量灰色
            'signal': '#ff00ff',  # 信号紫色
            'grid': '#333333'     # 网格深灰
        }
        
    def plot_candlestick_with_indicators(self, data: pd.DataFrame, indicators: Dict[str, Any], 
                                       symbol: str, save_path: Optional[str] = None) -> None:
        """
        绘制K线图和技术指标
        
        Args:
            data: 价格数据
            indicators: 技术指标数据
            symbol: 加密货币符号
            save_path: 保存路径 (可选)
        """
        fig, axes = plt.subplots(4, 1, figsize=self.figsize, 
                                gridspec_kw={'height_ratios': [3, 1, 1, 1]})
        fig.suptitle(f'{symbol} 技术分析图表', fontsize=16, fontweight='bold')
        
        # 1. K线图和均线
        self._plot_candlestick(axes[0], data, indicators, symbol)
        
        # 2. 成交量
        self._plot_volume(axes[1], data)
        
        # 3. RSI指标
        self._plot_rsi(axes[2], indicators)
        
        # 4. MACD指标
        self._plot_macd(axes[3], indicators)
        
        # 调整布局
        plt.tight_layout()
        
        # 保存或显示
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"📊 图表已保存到: {save_path}")
        else:
            plt.show()
            
    def _plot_candlestick(self, ax, data: pd.DataFrame, indicators: Dict[str, Any], symbol: str) -> None:
        """绘制K线图和均线"""
        # 准备数据
        dates = data.index
        opens = data['Open']
        highs = data['High']
        lows = data['Low']
        closes = data['Close']
        
        # 绘制K线
        for i in range(len(data)):
            date = dates[i]
            open_price = opens.iloc[i]
            high_price = highs.iloc[i]
            low_price = lows.iloc[i]
            close_price = closes.iloc[i]
            
            # 确定颜色
            color = self.colors['up'] if close_price >= open_price else self.colors['down']
            
            # 绘制影线
            ax.plot([date, date], [low_price, high_price], color=color, linewidth=1)
            
            # 绘制实体
            body_height = abs(close_price - open_price)
            body_bottom = min(open_price, close_price)
            
            if close_price >= open_price:
                # 阳线 (空心)
                ax.add_patch(plt.Rectangle((date - timedelta(hours=8), body_bottom), 
                                         timedelta(hours=16), body_height, 
                                         facecolor='none', edgecolor=color, linewidth=1.5))
            else:
                # 阴线 (实心)
                ax.add_patch(plt.Rectangle((date - timedelta(hours=8), body_bottom), 
                                         timedelta(hours=16), body_height, 
                                         facecolor=color, edgecolor=color, linewidth=1.5))
        
        # 绘制均线
        if 'SMA_5' in indicators.columns:
            ax.plot(dates, indicators['SMA_5'], label='SMA(5)', color='#ff6b6b', linewidth=1)
        if 'SMA_20' in indicators.columns:
            ax.plot(dates, indicators['SMA_20'], label='SMA(20)', color='#4ecdc4', linewidth=1.5)
        if 'SMA_50' in indicators.columns:
            ax.plot(dates, indicators['SMA_50'], label='SMA(50)', color='#45b7d1', linewidth=2)
        
        # 绘制布林带
        if all(col in indicators.columns for col in ['BB_upper', 'BB_lower', 'BB_middle']):
            ax.plot(dates, indicators['BB_upper'], color='#ffa726', alpha=0.7, linewidth=1, label='布林带上轨')
            ax.plot(dates, indicators['BB_lower'], color='#ffa726', alpha=0.7, linewidth=1, label='布林带下轨')
            ax.fill_between(dates, indicators['BB_upper'], indicators['BB_lower'], 
                           alpha=0.1, color='#ffa726')
        
        ax.set_title(f'{symbol} K线图', fontsize=14, fontweight='bold')
        ax.set_ylabel('价格 (USDT)', fontsize=12)
        ax.legend(loc='upper left')
        ax.grid(True, alpha=0.3, color=self.colors['grid'])
        
        # 格式化x轴
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d'))
        ax.xaxis.set_major_locator(mdates.DayLocator(interval=max(1, len(data)//10)))
        
    def _plot_volume(self, ax, data: pd.DataFrame) -> None:
        """绘制成交量"""
        dates = data.index
        volumes = data['Volume']
        colors = [self.colors['up'] if data['Close'].iloc[i] >= data['Open'].iloc[i] 
                 else self.colors['down'] for i in range(len(data))]
        
        ax.bar(dates, volumes, color=colors, alpha=0.7, width=timedelta(hours=16))
        ax.set_title('成交量', fontsize=12, fontweight='bold')
        ax.set_ylabel('成交量', fontsize=10)
        ax.grid(True, alpha=0.3, color=self.colors['grid'])
        
        # 格式化y轴
        ax.ticklabel_format(style='scientific', axis='y', scilimits=(0,0))
        
    def _plot_rsi(self, ax, indicators: Dict[str, Any]) -> None:
        """绘制RSI指标"""
        if 'RSI_14' not in indicators.columns:
            ax.text(0.5, 0.5, 'RSI数据不可用', ha='center', va='center', transform=ax.transAxes)
            return
            
        dates = indicators.index
        rsi = indicators['RSI_14']
        
        ax.plot(dates, rsi, color='#9c27b0', linewidth=2, label='RSI(14)')
        ax.axhline(y=70, color='red', linestyle='--', alpha=0.7, label='超买线(70)')
        ax.axhline(y=30, color='green', linestyle='--', alpha=0.7, label='超卖线(30)')
        ax.axhline(y=50, color='gray', linestyle='-', alpha=0.5)
        
        # 填充超买超卖区域
        ax.fill_between(dates, 70, 100, alpha=0.1, color='red')
        ax.fill_between(dates, 0, 30, alpha=0.1, color='green')
        
        ax.set_title('RSI 相对强弱指标', fontsize=12, fontweight='bold')
        ax.set_ylabel('RSI', fontsize=10)
        ax.set_ylim(0, 100)
        ax.legend(loc='upper right')
        ax.grid(True, alpha=0.3, color=self.colors['grid'])
        
    def _plot_macd(self, ax, indicators: Dict[str, Any]) -> None:
        """绘制MACD指标"""
        required_cols = ['MACD', 'MACD_signal', 'MACD_histogram']
        if not all(col in indicators.columns for col in required_cols):
            ax.text(0.5, 0.5, 'MACD数据不可用', ha='center', va='center', transform=ax.transAxes)
            return
            
        dates = indicators.index
        macd = indicators['MACD']
        signal = indicators['MACD_signal']
        histogram = indicators['MACD_histogram']
        
        # 绘制MACD线和信号线
        ax.plot(dates, macd, color='#2196f3', linewidth=2, label='MACD')
        ax.plot(dates, signal, color='#ff9800', linewidth=2, label='Signal')
        
        # 绘制柱状图
        colors = ['green' if h >= 0 else 'red' for h in histogram]
        ax.bar(dates, histogram, color=colors, alpha=0.6, width=timedelta(hours=16), label='Histogram')
        
        ax.axhline(y=0, color='black', linestyle='-', alpha=0.5)
        ax.set_title('MACD 指标', fontsize=12, fontweight='bold')
        ax.set_ylabel('MACD', fontsize=10)
        ax.set_xlabel('日期', fontsize=10)
        ax.legend(loc='upper right')
        ax.grid(True, alpha=0.3, color=self.colors['grid'])
        
        # 格式化x轴
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d'))
        ax.xaxis.set_major_locator(mdates.DayLocator(interval=max(1, len(indicators)//10)))
        
    def plot_price_comparison(self, data_dict: Dict[str, pd.DataFrame], 
                            symbols: list, save_path: Optional[str] = None) -> None:
        """
        绘制多个加密货币价格对比图
        
        Args:
            data_dict: 包含多个币种数据的字典
            symbols: 币种符号列表
            save_path: 保存路径 (可选)
        """
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=self.figsize, 
                                      gridspec_kw={'height_ratios': [3, 1]})
        
        colors = ['#ff6b6b', '#4ecdc4', '#45b7d1', '#96ceb4', '#feca57']
        
        # 价格对比 (归一化)
        for i, symbol in enumerate(symbols):
            if symbol in data_dict:
                data = data_dict[symbol]
                # 归一化价格 (以第一个价格为基准)
                normalized_price = data['Close'] / data['Close'].iloc[0] * 100
                ax1.plot(data.index, normalized_price, 
                        color=colors[i % len(colors)], linewidth=2, label=symbol)
        
        ax1.set_title('加密货币价格对比 (归一化)', fontsize=14, fontweight='bold')
        ax1.set_ylabel('相对价格 (%)', fontsize=12)
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # 成交量对比
        for i, symbol in enumerate(symbols):
            if symbol in data_dict:
                data = data_dict[symbol]
                ax2.plot(data.index, data['Volume'], 
                        color=colors[i % len(colors)], linewidth=1, alpha=0.7, label=symbol)
        
        ax2.set_title('成交量对比', fontsize=12, fontweight='bold')
        ax2.set_ylabel('成交量', fontsize=10)
        ax2.set_xlabel('日期', fontsize=10)
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        ax2.ticklabel_format(style='scientific', axis='y', scilimits=(0,0))
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"📊 对比图表已保存到: {save_path}")
        else:
            plt.show()
            
    def plot_correlation_heatmap(self, data_dict: Dict[str, pd.DataFrame], 
                               symbols: list, save_path: Optional[str] = None) -> None:
        """
        绘制加密货币相关性热力图
        
        Args:
            data_dict: 包含多个币种数据的字典
            symbols: 币种符号列表
            save_path: 保存路径 (可选)
        """
        # 准备相关性数据
        price_data = {}
        for symbol in symbols:
            if symbol in data_dict:
                price_data[symbol] = data_dict[symbol]['Close']
        
        if len(price_data) < 2:
            print("❌ 需要至少2个币种的数据才能计算相关性")
            return
            
        # 创建DataFrame并计算相关性
        df = pd.DataFrame(price_data)
        correlation_matrix = df.corr()
        
        # 绘制热力图
        plt.figure(figsize=(10, 8))
        sns.heatmap(correlation_matrix, annot=True, cmap='RdYlBu_r', center=0,
                   square=True, linewidths=0.5, cbar_kws={"shrink": .8})
        
        plt.title('加密货币价格相关性热力图', fontsize=16, fontweight='bold', pad=20)
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"📊 相关性热力图已保存到: {save_path}")
        else:
            plt.show()
            
    def plot_trading_signals(self, data: pd.DataFrame, signals: Dict[str, Any], 
                           symbol: str, save_path: Optional[str] = None) -> None:
        """
        绘制交易信号图
        
        Args:
            data: 价格数据
            signals: 交易信号数据
            symbol: 加密货币符号
            save_path: 保存路径 (可选)
        """
        fig, ax = plt.subplots(figsize=(15, 8))
        
        # 绘制价格线
        ax.plot(data.index, data['Close'], color='#2196f3', linewidth=2, label='收盘价')
        
        # 如果有信号点位数据，绘制信号
        if 'buy_points' in signals and len(signals['buy_points']) > 0:
            buy_dates = [point['date'] for point in signals['buy_points']]
            buy_prices = [point['price'] for point in signals['buy_points']]
            ax.scatter(buy_dates, buy_prices, color='green', marker='^', 
                      s=100, label='买入信号', zorder=5)
        
        if 'sell_points' in signals and len(signals['sell_points']) > 0:
            sell_dates = [point['date'] for point in signals['sell_points']]
            sell_prices = [point['price'] for point in signals['sell_points']]
            ax.scatter(sell_dates, sell_prices, color='red', marker='v', 
                      s=100, label='卖出信号', zorder=5)
        
        ax.set_title(f'{symbol} 交易信号图', fontsize=16, fontweight='bold')
        ax.set_ylabel('价格 (USDT)', fontsize=12)
        ax.set_xlabel('日期', fontsize=12)
        ax.legend()
        ax.grid(True, alpha=0.3)
        
        # 格式化x轴
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d'))
        ax.xaxis.set_major_locator(mdates.DayLocator(interval=max(1, len(data)//15)))
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"📊 交易信号图已保存到: {save_path}")
        else:
            plt.show()


def create_charts_directory() -> str:
    """创建图表保存目录"""
    import os
    charts_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'charts')
    os.makedirs(charts_dir, exist_ok=True)
    return charts_dir


if __name__ == "__main__":
    print("🎨 加密货币可视化模块")
    print("=" * 50)
    print("📊 支持功能:")
    print("   • K线图和技术指标")
    print("   • 成交量分析")
    print("   • RSI和MACD指标")
    print("   • 多币种价格对比")
    print("   • 相关性热力图")
    print("   • 交易信号图")
    print("=" * 50)