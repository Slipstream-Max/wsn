# 无线传感器网络分簇模拟系统

这是一个基于LEACH (Low-Energy Adaptive Clustering Hierarchy) 协议的无线传感器网络 (WSN) 分簇模拟系统。该系统通过Python实现，可视化展示了LEACH协议在无线传感器网络中的工作过程。

## 技术背景

**LEACH协议** 是一种经典的无线传感器网络分层路由协议，它通过以下机制实现能量均衡：

1. **轮次机制**：将网络运行时间分为多个轮次
2. **概率选举**：每个节点根据概率公式决定自己是否成为簇头
3. **簇形成**：非簇头节点加入到最近的簇头形成簇
4. **数据传输**：普通节点将数据传输到簇头，簇头聚合后传输到基站

该模拟系统完整实现了LEACH协议的核心机制，包括簇头选举、簇形成、能量消耗模型及节点寿命跟踪。

## 功能特性

- 完整的LEACH协议实现
- 详细的能量消耗模型（电路能耗、传输能耗、聚合能耗）
- 支持多种无线传输模型（自由空间/多径衰减）
- 动态调整簇头数量
- 节点生命周期跟踪
- 直观的网络拓扑可视化
- 灵活的命令行参数设置

## 安装与依赖

### 依赖库

```
matplotlib
numpy
```

### 安装依赖

#### 使用pip安装

```bash
pip install matplotlib numpy
```

#### 使用uv包管理器（推荐）

[uv](https://github.com/astral-sh/uv) 是一个超快速的Python包管理器，用Rust编写，可以替代pip，提供更快的依赖安装速度。

1. 安装uv

```bash
# 在Linux/macOS上安装
curl -sSf https://astral.sh/uv/install.sh | bash

# 在Windows上安装
# 使用PowerShell
curl.exe -sSf https://astral.sh/uv/install.ps1 | powershell -c -

# 或使用pip安装
pip install uv
```

2. 使用uv安装项目依赖

```bash
# 安装指定包并运行
uv run main.py
```

3. uv的优势
   - 比pip快5-100倍
   - 支持从lockfile安装
   - 更好的依赖解析
   - 内建虚拟环境管理

## 使用方法

### 基本使用

```bash
python main.py
```

### 带参数使用

```bash
python main.py --nodes 50 --width 100 --height 100 --cluster-percentage 0.05 --rounds 200
```

### 命令行参数

| 参数 | 描述 | 默认值 |
|------|------|--------|
| `--nodes` | 网络中节点的数量 | 100 |
| `--width` | 模拟区域宽度 | 100 |
| `--height` | 模拟区域高度 | 100 |
| `--cluster-percentage` | 簇头比例 | 0.05 |
| `--rounds` | 模拟总轮次 | 10 |

## 输出与可视化

系统将输出以下信息：

- 节点初始坐标
- 每轮簇头选举结果
- 节点能量耗尽信息
- 实时存活节点统计
- 节点平均剩余能量

同时，系统会在以下情况生成可视化图表：

- 每10轮生成一次网络拓扑图
- 当节点死亡时生成网络拓扑图

可视化图表包含以下内容：

- 存活普通节点（彩色圆点）
- 簇头节点（彩色星形）
- 死亡节点（灰色叉号）
- 基站位置（红色三角形）
- 节点到簇头的连接关系

## 能量模型

该模拟采用了与LEACH论文一致的能量消耗模型：

- **电路能耗**：接收和发送数据的电路能耗
- **自由空间模型**：短距离通信能耗模型 (d² 衰减)
- **多径衰减模型**：长距离通信能耗模型 (d⁴ 衰减)
- **数据聚合能耗**：簇头聚合数据的能耗

## 示例场景

### 50节点网络生命周期分析

```bash
python main.py --nodes 50 --rounds 200 --cluster-percentage 0.05
```

该命令将模拟50个节点组成的网络，运行200轮，并使用5%的簇头比例。通过观察不同轮次的节点死亡情况，可以分析网络的生命周期特性。

## 扩展方向

- 加入节点剩余能量感知的簇头选举机制
- 实现节点移动性
- 添加多基站支持
- 支持异构节点
- 能效对比分析工具
- 网络生命周期优化

## 参考文献

1. W. R. Heinzelman, A. Chandrakasan, and H. Balakrishnan, "Energy-efficient communication protocol for wireless microsensor networks," in Proceedings of the 33rd Annual Hawaii International Conference on System Sciences, 2000.

2. W. B. Heinzelman, A. P. Chandrakasan, and H. Balakrishnan, "An application-specific protocol architecture for wireless microsensor networks," IEEE Transactions on Wireless Communications, vol. 1, no. 4, pp. 660-670, Oct 2002.
