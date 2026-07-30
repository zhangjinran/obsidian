---
type: course-review
created: 2026-06-25T10:00
modified: 2026-06-25T10:00
tags: [course-review, 机器学习, 第九章]
course: "机器学习"
instructor: ""
semester: "大二下学期"
topic: "BP 神经网络"
status: reviewing
rating: 4
---

# 机器学习 — 第九章：BP 神经网络

## 总结
BP（Back Propagation）通过误差逆传播调整权重，核心是链式法则求导 + 梯度下降。涵盖反向传播推导、SGD/BGD/MBGD、梯度爆炸与消失、自适应学习率（SGDM/RMSProp/Adam）、防过拟合方法。

---

## 知识点 1：BP 算法的基本思想

### 要点
- **目标**：最小化网络输出与真实标签之间的误差
- **方法**：计算输出层误差，沿网络反向传播到各隐藏层，用梯度下降更新权重和阈值
- **核心工具**：**链式法则**

### 推导
#### 步骤
1. **前向传播**：输入逐层传到输出层
2. **误差计算**：计算输出层误差
3. **反向传播**：用链式法则逐层计算梯度
4. **参数更新**：梯度下降更新权重和阈值
5. 重复 1-4 直到收敛

---

## 知识点 2：反向传播算法（手算示例）

### 要点
- 激活函数：Sigmoid；损失函数：平方误差（系数 $1/2$）
- 样本 $x_i = [0.05, 0.1]^T$，标签 $y_i = [0.01, 0.99]^T$，学习率 $\eta = 0.5$

![[Pasted image 20260625192249.png]]

### 推导
以权重 $w_5$ 为例：

$$\frac{\partial Loss}{\partial w_5} = \frac{\partial Loss}{\partial out_{o1}} \cdot \frac{\partial out_{o1}}{\partial net_{o1}} \cdot \frac{\partial net_{o1}}{\partial w_5}$$

**①** $\frac{\partial Loss}{\partial out_{o1}} = out_{o1} - y_{i1} = 0.7514 - 0.01 = 0.7414$

**②** $\frac{\partial out_{o1}}{\partial net_{o1}} = \sigma'(net) = \sigma(net)(1-\sigma(net)) = 0.7514 \times (1-0.7514) = 0.1868$
*Sigmoid 性质：$\sigma'(x) = \sigma(x)(1-\sigma(x))$*

**③** $\frac{\partial net_{o1}}{\partial w_5} = out_{h1} = 0.5933$

连乘得：
$$\frac{\partial Loss}{\partial w_5} = 0.7414 \times 0.1868 \times 0.5933 = 0.08217$$

更新权重：
$$w_5 \leftarrow w_5 - \eta \cdot \frac{\partial Loss}{\partial w_5} = 0.4 - 0.5 \times 0.08217 = 0.3589$$

### 误差信号 $\delta$
定义误差信号 $\delta^{(l)}$ 为损失函数对第 $l$ 层净输入 $net^{(l)}$ 的梯度。由于 Sigmoid + 平方误差的组合，$\delta^{(l)}$ 表现为该层预测值与真实值之差，故称为"误差"。

![[Pasted image 20260625192416.png]]

---

## 知识点 3：随机梯度下降与批量梯度下降

### 要点

#### 随机梯度下降 (SGD)
- 每次随机选一个样本计算损失并更新参数
- **优点**：迭代速度快
- **缺点**：单个样本不能代表全体趋势，可能收敛到局部最优；不易并行

$$Loss = \frac12 (y_{i1} - out_{o1})^2 + \frac12 (y_{i2} - out_{o2})^2$$
$$w_{ij}^{(t+1)} = w_{ij}^{(t)} - \eta \cdot \frac{\partial Loss}{\partial w_{ij}^{(t)}}$$

#### 批量梯度下降 (BGD)
- 使用全部 $m$ 个样本计算损失后更新参数
- **优点**：能并行计算，方向准确；凸函数时保证全局最优
- **缺点**：$m$ 很大时训练极慢

$$Loss = \frac{1}{2m} \sum_{k=1}^m \left[(y_{k1} - out_{xk,o1})^2 + (y_{k2} - out_{xk,o2})^2\right]$$
$$w_{ij}^{(t+1)} = w_{ij}^{(t)} - \eta \cdot \frac{1}{m} \sum_{k=1}^m \frac{\partial Loss_k}{\partial w_{ij}^{(t)}}$$

#### 小批量梯度下降 (MBGD)
- 每次迭代使用 Batch Size 个样本，折中 SGD 和 BGD

![[Pasted image 20260625192828.png]]

---

## 知识点 4：梯度爆炸与梯度消失

### 要点
- BP 反向传播时，各层激活函数导数逐层**连乘**
- **梯度爆炸**：若导数 $>1$，靠前隐层的误差信号越来越大
- **梯度消失**：若导数 $<1$，靠前隐层的误差信号越来越小

### 激活函数对比
| 函数 | 特点 | 问题 |
|------|------|------|
| Sigmoid | 输出非 0 均值 | 容易出现梯度弥散/消失，收敛慢 |
| Tanh | 输出是 0 中心的 | 比 Sigmoid 收敛快，仍有梯度弥散 |
| ReLU | 正方向梯度不变 | 解决梯度消失，计算快，但会造成神经元"死亡" |

---

## 知识点 5：自适应学习率

### 要点

#### SGDM（SGD with Momentum）
引入动量机制，积累历史梯度方向，加速收敛：

![[Pasted image 20260625193205.png]]

#### RMSProp
对梯度平方做指数加权平均，动态调整学习率：

$$v^{(t)} = \gamma v^{(t-1)} + (1 - \gamma) (g^{(t)})^2$$
$$w_{ij}^{(t+1)} = w_{ij}^{(t)} - \eta \cdot \frac{g^{(t)}}{\sqrt{v^{(t)} + \varepsilon}}$$

- $\gamma$：衰减系数，$\eta$：学习率，$\varepsilon$：防除零小常数

#### Adam（Adaptive Moment Estimation）
**结合动量法（一阶矩）和 RMSProp（二阶矩）**，是当前最常用的优化器。

$$m_t = \beta_1 m_{t-1} + (1 - \beta_1) g_t$$
$$v_t = \beta_2 v_{t-1} + (1 - \beta_2) g_t^2$$

偏差校正（Adam 的关键，解决初始估计偏小的问题）：
$$\hat{m}_t = \frac{m_t}{1 - \beta_1^t}, \quad \hat{v}_t = \frac{v_t}{1 - \beta_2^t}$$

参数更新：
$$w_{ij}^{(t+1)} = w_{ij}^{(t)} - \eta \cdot \frac{\hat{m}_t}{\sqrt{\hat{v}_t} + \varepsilon}$$

- $\beta_1$：一阶矩衰减率（默认 0.9）
- $\beta_2$：二阶矩衰减率（默认 0.999）
- $\varepsilon$：防除零（默认 $10^{-8}$）
- **偏差校正**：训练初期 $m_t$ 和 $v_t$ 从 0 开始初始化，会被低估；$\hat{m}_t$、$\hat{v}_t$ 校正后使更新步长合理

> ⚠️ 用户原公式缺少偏差校正项 $1-\beta_1^t$ 和 $1-\beta_2^t$，已补全

---

## 知识点 6：防止过拟合

### 要点

#### 早停 (Early Stopping)
- 训练集误差降低但验证集误差升高 → 停止训练，返回验证集误差最小的参数

#### 正则化 (Regularization)
- **L1/L2 正则化**：在损失函数中增加权重的约束
- **Dropout**：以一定概率"灭活"部分神经元，防止过拟合

#### 标签平滑 (Label Smoothing)
- 将 one-hot 标签替换为软标签，提高泛化能力（从数据角度正则化）

#### 批量归一化 (Batch Normalization)
- 对每个小批量的数据计算均值和方差，调整为标准正态分布
- 引入可学习参数 $\gamma$（缩放）和 $\beta$（平移）保留网络表达能力
- 降低数据绝对差异，使模型对初始权重和大学习率不再敏感

---

## 关联
- [[神经网络基本概念]]
- [[多层前馈神经网络]]
- [[第九章 神经网络]]
