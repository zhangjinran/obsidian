---
type: course-review
created: 2026-07-06T10:00
modified: 2026-07-06T10:00
tags: [course-review, GIS]
course: "地理信息系统"
instructor: ""
semester: "大二下学期"
topic: "Ripley's K 函数推导"
status: reviewing
rating: 4
---

# Ripley's K 函数推导

## 总结
K 函数分析不同尺度上的空间集聚性，L 函数标准化后更方便比较。

## 前置符号
- $A$：研究区总面积；$n$：点位总数；$\lambda = n/A$：点密度
- 指示函数：$k(i,j) = 1$ 若 $\text{dist}(i,j) \leq d$，否则为 0

## K 函数定义
$$K(d) = \frac{1}{\lambda} E[N(d)]$$

其中 $N(d)$ 为以某点为圆心、$d$ 为半径的邻域内其他点的数量。

## CSR 随机期望
泊松随机过程：$E[N(d)] = \lambda \cdot \pi d^2$，因此 $E[K(d)] = \pi d^2$

## 样本观测 K 值
$$\hat{K}(d) = \frac{A \cdot S}{n(n-1)}$$

其中 $S = \sum_{i=1}^n \sum_{j \neq i}^n k(i,j)$ 为有效有序点对计数。分母用 $n(n-1)$ 而非 $n^2$ 是对点对比例的无偏估计。

## L 函数标准化
$$L(d) = \sqrt{\frac{\hat{K}(d)}{\pi}}$$

随机基准期望：$E[L(d)] = d$

## 判别规则
- $L(d) > d$：$d$ 尺度上集聚
- $L(d) = d$：完全空间随机
- $L(d) < d$：$d$ 尺度上均匀离散

## 关联
- [[矢量数据分析]]
