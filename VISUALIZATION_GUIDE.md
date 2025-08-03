# 加密货币可视化模块使用指南

## 📊 模块概述

`crypto_visualizer.py` 是一个专门为加密货币技术分析设计的可视化模块，提供了丰富的图表功能来展示价格走势、技术指标和交易信号。

## 🎨 主要功能

### 1. K线图 + 技术指标
- **功能**: 绘制完整的技术分析图表
- **包含**: K线图、移动平均线、布林带、RSI、MACD、成交量
- **方法**: `plot_candlestick_with_indicators()`

### 2. 多币种价格对比
- **功能**: 对比多个加密货币的价格走势
- **特点**: 标准化价格显示，便于比较
- **方法**: `plot_price_comparison()`

### 3. 相关性热力图
- **功能**: 显示多个币种之间的价格相关性
- **特点**: 颜色编码，直观显示相关程度
- **方法**: `plot_correlation_heatmap()`

### 4. 交易信号图
- **功能**: 在价格图上标记买入/卖出信号
- **特点**: 绿色买入点，红色卖出点
- **方法**: `plot_trading_signals()`

### 5. 单独指标图
- **RSI指标**: `plot_rsi()`
- **MACD指标**: `plot_macd()`

## 🚀 快速开始

### 基本使用示例

```python
import sys
sys.path.append('src')

from crypto_data_fetcher import CryptoDataFetcher
from technical_analyzer import TechnicalAnalyzer
from crypto_visualizer import CryptoVisualizer, create_charts_directory

# 1. 获取数据
fetcher = CryptoDataFetcher()
data = fetcher.get_crypto_data("BTCUSDT", granularity="1day", limit=100)

# 2. 计算技术指标
analyzer = TechnicalAnalyzer(data)
indicators = analyzer.add_indicators_to_data()

# 3. 创建可视化器
visualizer = CryptoVisualizer(figsize=(16, 12))

# 4. 生成图表
charts_dir = create_charts_directory()
save_path = f"{charts_dir}/btc_analysis.png"
visualizer.plot_candlestick_with_indicators(data, indicators, "BTCUSDT", save_path)
```

### 多币种对比示例

```python
# 获取多个币种数据
symbols = ["BTCUSDT", "ETHUSDT", "ADAUSDT"]
data_dict = {}

for symbol in symbols:
    data = fetcher.get_crypto_data(symbol, granularity="1day", limit=60)
    if data is not None:
        data_dict[symbol] = data

# 生成对比图表
visualizer = CryptoVisualizer(figsize=(16, 10))
visualizer.plot_price_comparison(data_dict, symbols, "price_comparison.png")
visualizer.plot_correlation_heatmap(data_dict, symbols, "correlation.png")
```

### 交易信号示例

```python
# 生成交易信号
analyzer = TechnicalAnalyzer(data)
indicators = analyzer.add_indicators_to_data()

# 创建信号点位
signal_points = {
    'buy_points': [
        {'date': '2024-01-15', 'price': 42000},
        {'date': '2024-01-20', 'price': 41500}
    ],
    'sell_points': [
        {'date': '2024-01-25', 'price': 45000},
        {'date': '2024-01-30', 'price': 46000}
    ]
}

# 绘制交易信号图
visualizer.plot_trading_signals(data, signal_points, "BTCUSDT", "signals.png")
```

## 🎛️ 演示脚本

运行 `crypto_chart_demo.py` 可以体验所有可视化功能：

```bash
python crypto_chart_demo.py
```

演示菜单包括：
1. 📈 BTC技术分析图表
2. 📊 多币种对比图表  
3. 🎯 ETH交易信号图表
4. 🚀 生成所有图表

## 📁 文件结构

```
stock_analysis/
├── src/
│   ├── crypto_visualizer.py      # 可视化模块
│   ├── crypto_data_fetcher.py    # 数据获取
│   └── technical_analyzer.py     # 技术分析
├── crypto_chart_demo.py          # 演示脚本
├── charts/                       # 图表保存目录
└── VISUALIZATION_GUIDE.md        # 本使用指南
```

## 🎨 图表特性

### 技术指标图表
- **K线图**: 开盘、最高、最低、收盘价
- **移动平均线**: SMA_20, SMA_50, EMA_12, EMA_26
- **布林带**: 上轨、中轨、下轨
- **RSI**: 相对强弱指数 (0-100)
- **MACD**: MACD线、信号线、柱状图
- **成交量**: 底部成交量柱状图

### 视觉设计
- **中文字体支持**: 自动配置中文显示
- **颜色方案**: 专业的金融图表配色
- **网格线**: 便于读取数值
- **图例**: 清晰的指标说明
- **标题**: 包含币种和时间信息

### 保存功能
- **自动创建目录**: charts/ 目录自动创建
- **高分辨率**: 300 DPI 保存质量
- **PNG格式**: 兼容性好，质量高

## ⚙️ 自定义配置

### 图表尺寸
```python
# 默认尺寸
visualizer = CryptoVisualizer(figsize=(16, 12))

# 自定义尺寸
visualizer = CryptoVisualizer(figsize=(20, 15))
```

### 颜色主题
可以在 `CryptoVisualizer` 类中修改颜色配置：
- 上涨K线: 红色 (#FF4444)
- 下跌K线: 绿色 (#00AA00)  
- 移动平均线: 蓝色、橙色
- 布林带: 紫色

### 指标参数
技术指标参数在 `TechnicalAnalyzer` 中配置：
- RSI周期: 14
- MACD参数: (12, 26, 9)
- 布林带周期: 20
- 移动平均线: 20, 50

## 🔧 故障排除

### 常见问题

1. **字体显示问题**
   - 模块会自动尝试加载中文字体
   - 如果显示异常，检查系统字体安装

2. **图表保存失败**
   - 确保有写入权限
   - 检查磁盘空间

3. **数据格式错误**
   - 确保传入的是 pandas DataFrame
   - 检查必需的列名 (Open, High, Low, Close, Volume)

4. **指标计算失败**
   - 确保数据量足够 (建议至少50条)
   - 检查数据中是否有缺失值

### 调试模式
```python
# 启用详细日志
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 📈 性能优化

- **数据量**: 建议单次处理不超过1000条数据
- **图表尺寸**: 过大的图表会影响生成速度
- **指标数量**: 可以选择性计算需要的指标

## 🎯 最佳实践

1. **数据准备**: 确保数据质量和完整性
2. **指标选择**: 根据分析需求选择合适的指标
3. **图表保存**: 使用有意义的文件名
4. **批量处理**: 对于多个币种，可以批量生成图表
5. **定期更新**: 定期更新数据和重新生成图表

---

🎉 **恭喜！** 您现在已经掌握了加密货币可视化模块的使用方法。开始创建专业的技术分析图表吧！