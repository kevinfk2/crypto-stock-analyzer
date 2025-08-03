# 加密货币与股票技术分析系统

专业的金融市场技术分析工具，支持加密货币和股票的实时数据获取、30+技术指标计算、智能交易信号生成和专业图表可视化。

## 🚀 功能特色

### 股票分析功能
- ✅ **实时股票数据获取** - 支持全球股票市场数据
- ✅ **30+ 技术指标** - 涵盖趋势、动量、波动性、成交量指标
- ✅ **智能交易信号** - 自动生成买入/卖出/持有建议
- ✅ **专业图表** - 多种可视化图表和技术分析报告
- ✅ **批量分析** - 支持多股票对比和批量分析

### 加密货币分析功能
- ✅ **多数据源支持** - Binance、Bitget等主流交易所
- ✅ **实时价格监控** - 24/7加密货币价格跟踪
- ✅ **技术指标分析** - RSI、MACD、布林带、KDJ等
- ✅ **交易信号生成** - 智能买卖点提示
- ✅ **可视化图表** - K线图、技术指标图、相关性分析
- ✅ **风险评估** - 综合评分和投资建议

## 📁 项目结构

```
stock_analysis/
├── Stock_analyzer.py       # 股票分析主程序
├── crypto_analyzer.py      # 加密货币分析主程序
├── requirements.txt        # 依赖包列表
├── README.md              # 项目说明
├── VISUALIZATION_GUIDE.md # 可视化使用指南
├── .gitignore             # Git忽略文件
├── charts/                # 图表输出目录
│   └── README.md          # 图表说明
└── src/                   # 源代码目录
    ├── __init__.py        # 包初始化
    ├── data_fetcher.py    # 股票数据获取模块
    ├── technical_analyzer.py # 技术分析模块
    ├── crypto_data_fetcher.py # 加密货币数据获取
    └── crypto_visualizer.py  # 加密货币可视化模块
```

## 🛠️ 安装和使用

### 1. 环境准备

```bash
# 激活虚拟环境 (如果有)
# Windows
practice_env\Scripts\activate

# 安装依赖
pip install -r requirements.txt
```

### 2. 运行程序

#### 股票分析
```bash
python Stock_analyzer.py
```

#### 加密货币分析
```bash
python crypto_analyzer.py
```

### 3. 功能菜单

#### 股票分析功能菜单：
```
📋 请选择操作:
1. 分析单只股票      # 深度分析单只股票
2. 批量分析多只股票   # 批量分析并排名
3. 股票对比分析      # 多股票走势对比
4. 查看热门股票      # 显示分类股票列表
5. 自定义股票代码    # 验证股票代码有效性
0. 退出系统
```

#### 加密货币分析功能：
- 实时价格获取和技术指标计算
- 综合评分和投资建议
- 风险等级评估
- 可视化图表生成（需要运行可视化模块）

## 📊 pandas-ta 主要功能

### 支持的技术指标类别

1. **趋势指标 (Trend)**
   - SMA (简单移动平均)
   - EMA (指数移动平均)
   - WMA (加权移动平均)
   - DEMA (双指数移动平均)
   - TEMA (三指数移动平均)

2. **震荡指标 (Oscillators)**
   - RSI (相对强弱指标)
   - Stochastic (随机指标)
   - CCI (商品通道指数)
   - Williams %R
   - ROC (变化率)

3. **波动性指标 (Volatility)**
   - Bollinger Bands (布林带)
   - ATR (平均真实波幅)
   - Keltner Channels

4. **成交量指标 (Volume)**
   - OBV (能量潮)
   - AD (累积/派发线)
   - MFI (资金流量指数)
   - VWAP (成交量加权平均价格)

5. **支撑阻力 (Support/Resistance)**
   - Pivot Points
   - Fibonacci Retracements

## 💡 基本使用方法

### 1. 导入库

```python
import pandas as pd
import pandas_ta as ta
import yfinance as yf
```

### 2. 获取数据

```python
# 获取股票数据
data = yf.download("AAPL", period="1y")
```

### 3. 计算技术指标

```python
# 计算RSI
data['RSI'] = ta.rsi(data['Close'], length=14)

# 计算移动平均线
data['SMA_20'] = ta.sma(data['Close'], length=20)

# 计算MACD
macd = ta.macd(data['Close'])
data = pd.concat([data, macd], axis=1)

# 计算布林带
bb = ta.bbands(data['Close'], length=20, std=2)
data = pd.concat([data, bb], axis=1)
```

### 4. 批量计算指标

```python
# 使用ta.Strategy批量计算
MyStrategy = ta.Strategy(
    name="My Strategy",
    ta=[
        {"kind": "sma", "length": 20},
        {"kind": "ema", "length": 12},
        {"kind": "rsi", "length": 14},
        {"kind": "macd", "fast": 12, "slow": 26, "signal": 9},
        {"kind": "bbands", "length": 20, "std": 2}
    ]
)

# 应用策略
data.ta.strategy(MyStrategy)
```

## 📈 常用指标说明

### RSI (相对强弱指标)
- **用途**: 判断超买超卖
- **范围**: 0-100
- **信号**: >70超买，<30超卖

### MACD (移动平均收敛发散)
- **用途**: 趋势跟踪和动量分析
- **信号**: 金叉看涨，死叉看跌

### 布林带 (Bollinger Bands)
- **用途**: 判断价格波动范围
- **信号**: 价格触及上轨可能回调，触及下轨可能反弹

### 移动平均线 (Moving Averages)
- **用途**: 趋势识别
- **信号**: 价格在均线上方为上升趋势

## 🔧 高级用法

### 1. 自定义指标

```python
def custom_indicator(close, length=14):
    return ta.sma(close, length) * 1.1

# 使用自定义指标
data['Custom'] = custom_indicator(data['Close'])
```

### 2. 指标组合策略

```python
# 多指标组合信号
def generate_signals(data):
    signals = []
    
    # RSI信号
    if data['RSI'].iloc[-1] < 30:
        signals.append("RSI超卖")
    
    # MACD信号
    if data['MACD_12_26_9'].iloc[-1] > data['MACDs_12_26_9'].iloc[-1]:
        signals.append("MACD金叉")
    
    return signals
```

## 📚 学习资源

- [pandas-ta 官方文档](https://github.com/twopirllc/pandas-ta)
- [技术分析基础知识](https://www.investopedia.com/technical-analysis-4689657)
- [yfinance 文档](https://pypi.org/project/yfinance/)

## 🚀 快速开始

### 分析股票示例
```bash
# 激活虚拟环境
practice_env\Scripts\activate

# 运行股票分析
python Stock_analyzer.py

# 输入股票代码，如：AAPL
```

### 分析加密货币示例
```bash
# 运行加密货币分析
python crypto_analyzer.py

# 程序会自动分析BTC并显示结果
```

### 生成可视化图表
```python
# 导入可视化模块
import sys
sys.path.append('src')
from crypto_visualizer import CryptoVisualizer

# 创建可视化对象
visualizer = CryptoVisualizer()

# 生成BTC技术分析图表
visualizer.plot_technical_analysis('BTC')
```

## 📝 注意事项

- 确保网络连接正常，以便获取实时数据
- 技术分析结果仅供参考，不构成投资建议
- 建议结合基本面分析做出投资决策
- 加密货币市场波动较大，请注意风险控制

## 🤝 贡献

欢迎提交 Issue 和 Pull Request 来改进这个项目。

## 📄 许可证

本项目采用 [MIT 许可证](LICENSE) - 详见 LICENSE 文件。

## ⚠️ 免责声明

本项目仅用于学习和研究目的，不构成投资建议。股票和加密货币投资有风险，请谨慎决策。

---
*Powered by Claude-4*