---
date: 2026-02-02
tags:
  - 大创
  - python
---
# 文件位置
model/x_mobility/x_mobility.py
# 架构
x-mobility的模型文件，是核心文件。
## 代码架构
直接下属的函数和类包括
-  model.x_mobility.decoders 中的 类：
	- StyleGanDecoder, 
	- RgbHead, 
	- SegmentationHead
- model.x_mobility.diffusion_rgb 中的 RGBDiffuser
- model.x_mobility.action_policy 中的 ActionPolicy
-  model.x_mobility.[[encoders]] 中的ObservationEncoder
-  model.x_mobility.rssm 中的RSSM
- model.x_mobility.utils 中的函数：
	- pack_sequence_dim, 
	- unpack_sequence_dim
## 物理架构
- forward前向传播函数，处理输入数据，并生成结果，
	- [[encoders]]中的observationencoder对图像和速度进行编码
	- [[rssm]]处理时间序列
	- [[action_policy]]利用处理的数据，生成动作命令和路径输出。
- inference推理函数，就是使用模型的时候就可以调用此函数。处理输入的数据或者图像等，生成动作策略和动作路径，语义分割、RGB还有深度图像结果。
- inference_prediction推理预测函数，和inference的区别就在于，前者并不使用观测数据，只使用历史数据，因而只是对于结果进行预测而已。生成的结果中也并不包含动作策略和动作路径以及深度图像结果。

