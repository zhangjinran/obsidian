---
type: course-review
created: 2026-02-09T10:00
modified: 2026-06-20T10:00
tags: [course-review, 机器学习, 第七章]
course: "机器学习"
instructor: ""
semester: "大二下学期"
topic: "多维标定（MDS）"
status: reviewed
rating: 4
---

# 机器学习 — 第七章：多维标定（MDS）

## 总结
- **核心思想**：寻找一个低维子空间，使样本在此空间的距离与原始空间中样本间距离保持不变
- **应用**：MDS 保留了原样本间的距离，非常适合做数据可视化（如知觉图）

## 知识点 1：MDS 原理

### 要点
- **目标**：在低维空间中保持高维样本间的距离关系
- **推导**：

![[Pasted image 20260528171821.png]]
![[Pasted image 20260528171913.png]]
![[Pasted image 20260528171941.png]]

### 注意事项
- MDS 是度量型的（保持距离），不关心数据的绝对位置，只关心相对距离

## 推导
完整数学推导见 [[mds-derivation|MDS 公式推导]]

## 关联
- [[mds-derivation]] — $b_{ij}$ 公式的完整推导
- [[主成分分析（PCA）]] — 另一种经典降维方法
- [[流形学习简介]] — Isomap 在 MDS 基础上引入测地线距离
- [[第七章 维度归约]]
