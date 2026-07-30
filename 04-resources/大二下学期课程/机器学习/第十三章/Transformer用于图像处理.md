---
type: course-review
created: 2026-06-26T10:00
modified: 2026-06-26T10:00
tags: [course-review, 机器学习, 第十三章]
course: "机器学习"
instructor: ""
semester: "大二下学期"
topic: "Transformer 用于图像处理"
status: to-review
rating: 3
---

# 机器学习 — 第十三章：Transformer 用于图像处理（自学）

## 总结
Transformer 被引入计算机视觉领域，在图像分类、目标检测等任务上达到了与 CNN 相当甚至更好的效果。

## 知识点 1：Vision Transformer (ViT)

### 要点
- 将图像划分为固定大小的 patches（如 $16 \times 16$），线性投影为 patch 嵌入
- 添加位置编码后输入标准 Transformer 编码器
- 在 ImageNet 分类上首次超越 CNN

## 知识点 2：DETR

### 要点
- 将目标检测视为集合预测问题
- 用 Transformer 的编码器-解码器结构替代了候选区域和锚框
- 简化了检测流程，无需 NMS 后处理

## 关联
- [[Transformer]]
- [[注意力机制]]
- [[第十三章 注意力机制]]
