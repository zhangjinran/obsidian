---
date: 2026-02-02
tags:
  - 大创
  - python
---
# 文件位置
# 架构
主要就是扩散模型相关的代码，主要有两个功能
- 功能1：编码，然后模拟扩散过程加入噪声，并预测噪声
- 功能2：去噪和去编码
## 代码架构
-  model.x_mobility.conditional_unet1d 中的 ConditionalUnet1D模型。
- model.x_mobility.utils 中的 pack_sequence_dim函数
## 物理架构
- 前向传播函数实现的是功能1，
	- encode_policy将向量进行归一化一些处理即编码
	- 然后添加噪声
	- 调用unet模型预测噪声
- denoising_and_decode实现的是功能2
	- denoising进行去噪，
	- denode_policy将之前的归一化进行恢复，即反归一化。
	- 输出路径和动作策略。