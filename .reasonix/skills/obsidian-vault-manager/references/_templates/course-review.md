---
type: course-review
created: {{date:YYYY-MM-DDTHH:mm}}
modified: {{date:YYYY-MM-DDTHH:mm}}
tags: [course-review]
course: ""
instructor: ""
semester: ""
topic: ""
status: to-review
rating:
---

# {{course}} — {{topic}}

## 总结
- 知识点 1：简要概括
- 知识点 2：简要概括
- 知识点 3：简要概括

## 知识点 1：
> 每个知识点可按需选用多个子模块，**要点与推导可同时使用**。

**要点子模块** — 概念、定义、分类等文本说明
### 要点
- 一级要点
  - 二级要点
  - 二级要点
- 一级要点
  - 二级要点
    - 三级要点

**推导子模块** — 数学推导、定理证明
### 推导
#### 目标
要推导的公式/结论
#### 前置知识
- 前置概念
#### 步骤
1. 第 1 步：起始公式
2. 第 2 步：关键变换
3. 第 3 步：中间结果
4. 第 4 步：最终结论
#### 关键 Insight
- 核心技巧

**公式子模块** — 独立公式展示
### 公式
$$

$$

**示例子模块** — 具体应用举例
### 示例
- 例子

**注意事项子模块** — 易错点、边界情况
### 注意事项
- 易错点

## 知识点 2：
### 公式
### 示例
### 注意事项

## 疑问
- ❓

## 关联
- [[ ]]

---

## 使用示例

以下是一篇完整的课程复习笔记，展示了如何运用本模板。

---

type: course-review
created: 2026-02-03T10:00
modified: 2026-06-20T10:00
tags: [course-review, 机器学习, 第二章]
course: "机器学习"
instructor: ""
semester: "大二下学期"
topic: "监督学习的计算理论"
status: reviewed
rating: 4

# 机器学习 — 第二章：监督学习的计算理论

## 总结
- **Hoeffding 不等式** 给出了从样本误差推断总体误差的理论工具
- **可学习的两个条件**：$E_{in} \approx 0$（拟合）且 $E_{in} \approx E_{out}$（泛化），但 $M$（假设数）对二者存在 tradeoff
- **VC 维** 将无穷假设空间压缩为多项式量级的增长函数，使学习可行
- **VC 界** 导出 $E_{out} \le E_{in} + \Omega$（训练误差 + 复杂度惩罚）

### 知识点 1：基本设定与 Hoeffding 不等式
#### 要点
- $A$：学习算法；$H$：假设空间；$D$：训练集；$g \in H$：学习到的假设；$f$：真实映射（未知）
- $E_{in}(g)$：训练误差（可计算）；$E_{out}(g)$：泛化误差（不可计算）
- **Hoeffding 不等式**：$P[|\nu - \mu| > \epsilon] \leq 2e^{-2\epsilon^2 N}$

#### 推导
**目标**：用可计算的 $E_{in}$ 推断不可计算的 $E_{out}$
**步骤**：抽球类比 → Hoeffding → $N$ 够大时 $E_{in} \approx E_{out}$
**关键 Insight**：对固定假设 $h$，该不等式保证 $E_{in}(h)$ 可推断 $E_{out}(h)$

### 知识点 2：可学习条件与 M 的困境
#### 要点
- **并集不等式**：$P(A_1\cup...\cup A_M) \leq \sum P(A_i)$
- **条件一（test）**：$M$ 有限 + $N$ 够大 → $E_{in} \approx E_{out}$
- **条件二（train）**：能从 $H$ 选出 $g$ 使 $E_{in}(g) \approx 0$
- $M$ 矛盾：M 小则 test 易 train 难，M 大则 train 易 test 难

#### 推导
**目标**：从单假设推广到多假设
**步骤**：$P \leq 2e^{-2\epsilon^2 N} \to P \leq 2M e^{-2\epsilon^2 N}$
**关键 Insight**：$H$ 无穷假设时上界 $\infty$ 无意义→需化为有限

### 知识点 3：VC 维——从无穷到有限
#### 要点
- **对分 (dichotomy)**：$H$ 对 $N$ 个样本产生的一组标记结果
- **增长函数 $m_H(N)$**：有效假设数的最大值
- **打散 (shatter)**：$m_H(N)=2^N$；**Break Point $k$**：使 $m_H(N)<2^N$ 的最小 $N$

#### 推导
**目标**：$2^N \to N^{k-1}$，使上界收敛
**步骤**：无穷 $M$ → 有效对分数 → $m_H(N) \leq 2^N$ → break point $k$ → $m_H(N) \leq N^{k-1}$
**关键 Insight**：break point 是将无穷压缩为有限的关键

#### 示例
二维直线 $k=4$ → $m_H(N) \leq N^3$

### 知识点 4：VC 界与 VC 维
#### 要点
- **VC 维**：$VC(H)=\max\{N:m_H(N)=2^N\}=k-1$
- **VC 界**：$P[|E_{in}-E_{out}|>\epsilon] \leq 4(2N)^{VC(H)} e^{-\frac18\epsilon^2 N}$
- **$E_{out} \le E_{in} + \Omega$**：$\Omega = \sqrt{\frac8N \ln\frac{4(2N)^{VC(H)}}{\delta}}$

#### 推导
**目标**：概率形式 → 误差区间形式 $E_{out} \le E_{in} + \Omega$
**步骤**：令上界 $=\delta$ → 取对数 → 解 $\epsilon$ → 代入补事件
**关键 Insight**：泛化误差 = 训练误差 + 复杂度惩罚

#### 示例
- 二维直线：VC 维 = 3；感知机：VC 维 = $d+1$

#### 注意事项
- VC 界非常宽松，实际 $N\approx10\cdot VC(H)$ 即够
