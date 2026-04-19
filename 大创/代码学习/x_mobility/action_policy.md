---
date: 2026-02-02
tags:
  - 大创
  - python
---
# 文件位置

# 架构
主要就是生成动作命令和路径指令的，是核心函数。
## 代码架构
- model.x_mobility.[[vector_net]]中的VectorNetSubGraph，这个是路径编码器的格式。

- model.x_mobility.[[diffusion_policy]]中的DiffusionPolicy，这个是扩散模型。

- model.x_mobility.utils两个函数pack_sequence_dim, unpack_sequence_dim
## 物理架构
- 提供了三个特征融合模型，用来融合潜在特征和路径特征
	- 直接融合
	- MLP融合机制，MLP就是多层感知机，就是神经网络
	- 自注意力融合机制
- 然后利用上述特征生成路径和命令
	- MLP路径策略网络
	- 扩散模型策略网络
- 最后将这些步骤整合起来在actionpolicy类中。

