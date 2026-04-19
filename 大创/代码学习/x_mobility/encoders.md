---
date: 2026-02-02
tags:
  - 大创
  - python
---
# 文件位置
model/x_mobility/encoders.py
# 架构
这个文件主要作用是对输入的图片和速度进行编码处理，将其转化为特征、注意力权重等，便于模型进行处理。

## 代码架构
主要就是这个model.x_mobility.utils中的pack_sequence_dim和 unpack_sequence_dim两个函数。
## 物理架构

- 用observationEncoder这个类，将下述三个编码器集成起来，进行编码
	- 速度编码器SpeedEncoder
	- 采用DINO v2模型的图形编码器
	- 采用depth anything模型的图形编码器