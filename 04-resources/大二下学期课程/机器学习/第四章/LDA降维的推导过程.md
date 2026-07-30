---
type: course-review
created: 2026-06-20T10:00
modified: 2026-06-20T10:00
tags: [course-review, 机器学习, 第四章]
course: "机器学习"
instructor: ""
semester: "大二下学期"
topic: "LDA 降维的推导过程"
status: reviewed
rating: 4
---

# 机器学习 — 第四章：LDA 降维的推导过程

## 总结
LDA 降维上限为 $C-1$ 的完整数学推导。核心逻辑链：

```
S_B 的秩 ≤ C-1
  → S_w^{-1}S_B 的秩 ≤ C-1
  → 非零特征值数量 ≤ C-1
  → LDA 最多降维到 C-1 维
```

## 前置基础 1：特征值与特征向量

### 要点
- **定义**：$n$ 阶方阵 $A$，若存在非零向量 $w$、常数 $\lambda$ 满足 $Aw = \lambda w$，则 $\lambda$ 为特征值，$w$ 为特征向量
  - 几何含义：矩阵 $A$ 作用在 $w$ 上只拉伸不旋转，$\lambda$ 是拉伸倍数
- **求解**：$(A-\lambda I)w = 0$ 有非零解 $\iff \det(A-\lambda I)=0$
- **核心性质**：非零特征值对应的特征向量属于矩阵的列空间；矩阵秩 = 列空间维度；非零特征值数量 ≤ 矩阵的秩

## 前置基础 2：两条秩不等式

### 要点
- **乘积秩不等式**：$\text{rank}(AB) \le \min\{\text{rank}(A), \text{rank}(B)\}$
- **和秩不等式**：$\text{rank}(\sum M_i) \le \sum \text{rank}(M_i)$

## 推导 1：类间散度矩阵 $S_B$ 的秩上限

### 要点
- $S_B = \sum_{i=1}^C n_i(\mu_i - \bar\mu)(\mu_i - \bar\mu)^T = \sum M_i$
  - 每个 $M_i$ 是向量外积矩阵，$\text{rank}(M_i)=1$
- **由和秩不等式**：$\text{rank}(S_B) \le \sum 1 = C$
- **收紧上界**：所有类中心偏移向量满足 $\sum n_i(\mu_i - \bar\mu) = 0$，最多 $C-1$ 个线性无关
- **结论**：$\text{rank}(S_B) \le C-1$

### 推导
#### 关键 Insight
类中心偏移向量存在一个线性约束，使 $S_B$ 的有效方向比类别数少 1

## 推导 2：$T = S_w^{-1}S_B$ 的秩上限

### 要点
- $S_w$ 可逆（样本充足时），$\text{rank}(S_w^{-1}) = d$
- **由乘积秩不等式**：$\text{rank}(T) \le \min\{\text{rank}(S_w^{-1}), \text{rank}(S_B)\} \le C-1$

### 推导
#### 目标
证明 $S_w^{-1}S_B$ 的非零特征值不超过 $C-1$ 个
#### 步骤
1. $\text{rank}(S_B) \le C-1$（由推导 1）
2. $\text{rank}(S_w^{-1}S_B) \le \text{rank}(S_B) \le C-1$
3. 非零特征值数量 ≤ $\text{rank}(T) \le C-1$
4. 零特征值对应方向投影后各类完全重合，无法区分 → 舍弃
#### 关键 Insight
LDA 最多只能降维到 $C-1$ 维，这是数学上被秩约束决定的

## 最终结论

### 要点
类间散度矩阵 $S_B$ 最多只有 $C-1$ 个线性无关方向 → $S_w^{-1}S_B$ 秩 ≤ $C-1$ → 非零特征值 ≤ $C-1$ → LDA 最多降维到 $C-1$ 维

这是 LDA 和 PCA 维度上限不同的根本数学原因。

### 实例
- 二分类 $C=2$：最多 1 个有效特征向量，LDA 只能降到 1 维
- 三分类 $C=3$：最多 2 个有效特征向量，LDA 最多降到 2 维

## 关联
- [[线性判别分析LDA]]
- [[第四讲 线性模型]]
