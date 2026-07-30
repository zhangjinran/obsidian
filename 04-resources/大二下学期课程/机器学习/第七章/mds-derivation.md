---
type: course-review
created: 2026-06-22T10:00
modified: 2026-06-22T10:00
tags: [course-review, 机器学习, 第七章]
course: "机器学习"
instructor: ""
semester: "大二下学期"
topic: "MDS 公式推导"
status: reviewed
rating: 4
---

# 经典 MDS 公式完整推导

## 符号约定

- $m$ 个样本，降维后样本向量 $\boldsymbol{z}_i \in \mathbb{R}^{d'}$
- 距离平方：$\mathrm{dist}_{ij}^2 = \|\boldsymbol{z}_i - \boldsymbol{z}_j\|_2^2$（样本 $i,j$ 欧氏距离平方）
- 内积矩阵 $\boldsymbol{B} \in \mathbb{R}^{m \times m}$，元素 $b_{ij} = \boldsymbol{z}_i^T \boldsymbol{z}_j$
- 记：
  $$d_{ij}^2 = \mathrm{dist}_{ij}^2,\quad d_{i\cdot}^2 = \sum_j d_{ij}^2,\quad d_{\cdot j}^2 = \sum_i d_{ij}^2,\quad d_{\cdot\cdot}^2 = \sum_i \sum_j d_{ij}^2$$

---

## 步骤 1：展开欧氏距离平方

$$
\begin{aligned}
d_{ij}^2 &= \|\boldsymbol{z}_i - \boldsymbol{z}_j\|^2 \\
&= (\boldsymbol{z}_i - \boldsymbol{z}_j)^T (\boldsymbol{z}_i - \boldsymbol{z}_j) \\
&= \boldsymbol{z}_i^T \boldsymbol{z}_i - 2\boldsymbol{z}_i^T \boldsymbol{z}_j + \boldsymbol{z}_j^T \boldsymbol{z}_j \\
&= b_{ii} - 2b_{ij} + b_{jj}
\end{aligned}
$$

移项得到核心关系式：

$$
\boxed{b_{ij} = \frac{1}{2}(b_{ii} + b_{jj} - d_{ij}^2)} \tag{1}
$$

---

## 步骤 2：对行、列分别求和（消去对角元 $b_{ii}, b_{jj}$）

### ① 固定 $i$，对 $j=1 \cdots m$ 求和

$$\sum_j d_{ij}^2 = \sum_j b_{ii} - 2\sum_j b_{ij} + \sum_j b_{jj}$$

- $\sum_j b_{ii} = m \cdot b_{ii}$
- $\sum_j b_{ij} = \sum_j \boldsymbol{z}_i^T \boldsymbol{z}_j = \boldsymbol{z}_i^T (\sum_j \boldsymbol{z}_j)$

MDS 强制样本中心化：$\sum_i \boldsymbol{z}_i = \boldsymbol{0}$（全体样本均值为 0，消除平移自由度），因此 $\sum_j b_{ij} = 0$

- 记 $T = \sum_j b_{jj} = \sum_j \boldsymbol{z}_j^T \boldsymbol{z}_j$（所有样本模长平方和）

代入化简：

$$d_{i\cdot}^2 = m \cdot b_{ii} + T \quad\Rightarrow\quad b_{ii} = \frac{1}{m} d_{i\cdot}^2 - \frac{T}{m} \tag{2}$$

### ② 固定 $j$，对 $i=1 \cdots m$ 求和

同理可得：

$$d_{\cdot j}^2 = m \cdot b_{jj} + T \quad\Rightarrow\quad b_{jj} = \frac{1}{m} d_{\cdot j}^2 - \frac{T}{m} \tag{3}$$

### ③ 全部 $i,j$ 双重求和

$$\sum_{i,j} d_{ij}^2 = \sum_i d_{i\cdot}^2 = \sum_j d_{\cdot j}^2 = mT + mT = 2mT$$

解出：

$$T = \frac{1}{2m} d_{\cdot\cdot}^2 \tag{4}$$

---

## 步骤 3：代入式 (1)

将 (2)(3)(4) 代入 (1)：

$$
\begin{aligned}
b_{ij} &= \frac{1}{2} \left[ \left(\frac{d_{i\cdot}^2}{m} - \frac{T}{m}\right) + \left(\frac{d_{\cdot j}^2}{m} - \frac{T}{m}\right) - d_{ij}^2 \right] \\
&= -\frac{1}{2} \left[ d_{ij}^2 - \frac{d_{i\cdot}^2}{m} - \frac{d_{\cdot j}^2}{m} + \frac{2T}{m} \right]
\end{aligned}
$$

将 $T = \frac{d_{\cdot\cdot}^2}{2m}$ 代入最后一项：

$$\frac{2T}{m} = \frac{2}{m} \cdot \frac{d_{\cdot\cdot}^2}{2m} = \frac{d_{\cdot\cdot}^2}{m^2}$$

---

## 步骤 4：整理得到 $b_{ij}$ 公式

$$
\boxed{b_{ij} = -\frac{1}{2} \left[ \mathrm{dist}_{ij}^2 - \frac{1}{m}\sum_i \mathrm{dist}_{ij}^2 - \frac{1}{m}\sum_j \mathrm{dist}_{ij}^2 + \frac{1}{m^2}\sum_i\sum_j \mathrm{dist}_{ij}^2 \right]}
$$

---

## 矩阵形式（双中心化矩阵 $\boldsymbol{J}$）

上面逐元素公式等价于矩阵运算：

$$
\boldsymbol{B} = -\frac{1}{2} \boldsymbol{J} \boldsymbol{D}^{(2)} \boldsymbol{J}
$$

其中：
- $\boldsymbol{D}^{(2)}$：元素为 $d_{ij}^2$ 的距离平方矩阵
- $\boldsymbol{J} = \boldsymbol{I}_m - \frac{1}{m}\boldsymbol{1}\boldsymbol{1}^T$ 是中心化投影矩阵，$\boldsymbol{1}$ 为全 1 列向量

左乘 $\boldsymbol{J}$ 做行中心化，右乘 $\boldsymbol{J}$ 做列中心化（双中心化），对应公式里减去行均值、列均值、加回全局均值。

---

## 后续分解求 $\boldsymbol{Z}$

$\boldsymbol{B} = Z^T Z$ 是半正定对称矩阵，做特征分解：

$$\boldsymbol{B} = V \Lambda V^T$$

$\Lambda = \mathrm{diag}(\lambda_1, \lambda_2, \dots, \lambda_m)$ 为特征值对角阵，取前 $d'$ 个正特征值开根号：

$$\boldsymbol{Z} = V_{:,1:d'} \cdot \mathrm{diag}(\sqrt{\lambda_1}, \sqrt{\lambda_2}, \dots, \sqrt{\lambda_{d'}})$$

$\boldsymbol{Z}$ 每一列就是降维后的样本 $\boldsymbol{z}_i$。

---

## 关键前提说明

推导成立的核心约束：**降维后样本集中心化（均值为 0）**

$$\sum_{i=1}^m \boldsymbol{z}_i = \boldsymbol{0}$$

这一步消去了空间整体平移带来的冗余自由度，是 MDS 必须做的预处理，也是求和时交叉项消失的根本原因。

## 关联
- [[多维标定（MDS）]]
