---
date: 2026-02-09
tags:
  - 机器学习
---

# 前身：[[DINOv1]]
# 相对于前身的优化
- **双目标学习**：在DINOv1的**图像级**目标基础上，增加**块级**目标（类似掩码图像建模），提升局部特征的精细度[](https://collab.dvb.bayern/spaces/TUMdlma/pages/73379966/Exploring+Latest+Unsupervised+Computer+Vision+Models+for+Segmentation)。  
- **工程优化**：引入FlashAttention加速，使用Sinkhorn-Knopp算法替代中心化，应用KoLeo[[正则化]]使特征分布更均匀[](https://collab.dvb.bayern/spaces/TUMdlma/pages/73379966/Exploring+Latest+Unsupervised+Computer+Vision+Models+for+Segmentation)[](https://developer.aliyun.com/article/1210161)。  
- **大规模数据**：构建并清洗了包含1.42亿张图像的LVD-142M数据集[](https://developer.aliyun.com/article/1210161)。


