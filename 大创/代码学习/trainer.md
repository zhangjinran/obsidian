---
date: 2026-02-01
tags:
  - 大创
  - python
---
# 文件位置
model/trainer.py
# 架构
这个代码用于组织model的。
## 代码架构
直接下属的函数和类包括
- XMobilityLoss
- [[x_mobility|XMobility]]
- XMobilityMetrics
- visuallization.py中的
	- visualise_semantic
	- visualise_rgb
	- visualise_attention
	- visualise_depth
## ==物理架构（得重写）

### 1.**模型定义与前向传播**

- **`forward(self, batch)`**：
    
    - 负责模型的前向传播，调用 `self.model(batch)` 返回模型的输出。
        

### 2. 推理与预测

- **`inference_prediction(self, batch, enable_semantic_inference=True, enable_rgb_inference=False)`**：
    
    - 就是使用模型，但是不使用观测数据，只用历史数据预测结果
        
- **`inference(self, batch, enable_semantic, enable_rgb, enable_depth)`**：
    
    - 就是使用模型，用观测数据，还有历史数据生成结果
        

### 3. **训练与验证过程**

- **`shared_step(self, batch)`**：
    
    - 执行前向传播和损失计算，返回损失和输出。
        
- **`training_step(self, batch, batch_idx)`**：
    
    - 执行训练步骤，包括前向传播、损失计算、日志记录和可视化，并返回总损失。
        
- **`validation_step(self, batch, batch_idx)`**：
    
    - 执行验证步骤，进行前向传播和损失计算，并返回验证损失。
        
- **`test_step(self, batch, batch_idx)`**：
    
    - 执行测试步骤，进行前向传播和损失计算，但不进行评估。
        

### 4. **日志记录与可视化**

- **`log_and_visualize(self, batch, output, losses, batch_idx, prefix='train')`**：
    
    - 记录损失、评估指标，并在验证阶段生成可视化视频（如语义分割、RGB、深度图等）。
        
- **`log_video(self, name, viz)`**：
    
    - 将生成的视频数据上传到 **WandB**，以便在训练过程中进行监控和分析。
        
- **`visualise(self, batch, output, batch_idx, prefix='train')`**：
    
    - 根据模型输出生成可视化视频，包括语义分割、RGB图像、深度图和注意力图。
        

### 5. **损失函数与优化**

- **`loss_reducing(self, loss)`**：
    
    - 将损失字典中的各个损失值进行求和，返回总损失值。
        
- **`configure_optimizers(self)`**：
    
    - 配置优化器（AdamW）和学习率调度器（OneCycleLR）用于训练过程。
        
- **`_add_weight_decay(self, model, weight_decay=0.01, skip_list=None)`**：
    
    - 配置权重衰减（L2[[正则化]]），确保某些参数不进行衰减。
        

### 6. **分布式训练与日志同步**

- **`sync_dist=True`**（在 `log` 和 `log_dict` 中使用）：
    
    - 确保在分布式训练中，多个设备上的日志信息是同步的，避免重复记录日志。