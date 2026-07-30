---
type: paper-note
topic: X-Mobility RSSM 世界模型与多任务 Decoder
tags:
  - 大创
  - 论文
  - X-Mobility
  - RSSM
  - 世界模型
  - 多任务学习
status: reviewed
rating: 5
---

# X-Mobility — RSSM 世界模型与多任务 Decoder

## 总结
- **RSSM（Recurrent State Space Model）** 是 X-Mobility 最大的核心贡献
- 它维护一个历史隐状态 $h_t$，表示机器人当前的**世界状态**
- 更新方式融合了历史信息、当前视觉、过去动作，比单帧图片丰富得多
- 多任务 Decoder 通过重建 RGB/Semantic/Depth/Occupancy 来提升隐状态质量

### 知识点 1：RSSM 的核心思想

#### 要点
RSSM 维护：

$$
h_t
$$

表示：机器人当前世界状态（包含环境几何、历史、动态信息）。

更新方式：

```
Image_t → Encoder → z_t → RSSM → h_t
```

其中：

$$
h_t = f(h_{t-1}, z_t, a_{t-1})
$$

这意味着 RSSM 的隐状态包含三种信息：

| 信息来源 | 含义 |
|---------|------|
| $h_{t-1}$ | 历史状态信息（过去的世界状态） |
| $z_t$ | 当前视觉信息（当前帧的图像特征） |
| $a_{t-1}$ | 过去动作信息（上一步的控制指令） |

#### 注意事项
- RSSM 本质是一个**循环神经网络（RNN）**，使用了类似 GRU 的门控机制
- 它学习的是**世界动力学**——给定当前状态和动作，预测下一状态，而不是直接预测动作

### 知识点 2：RSSM 与纯视觉方法的区别

#### 要点
| 方法 | 输入 | 环境理解 |
|------|------|---------|
| 纯 CNN（End-to-End） | 单帧图像 | ❌ 无历史，无动态理解 |
| RSSM | 图像序列 + 动作历史 | ✅ 包含历史、动态、几何信息 |

纯 CNN 方法：

```
Image_t → Action_t
```

RSSM 方法：

```
Image_t + h_{t-1} + a_{t-1} → h_t → Action_t
```

### 知识点 3：多任务 Decoder

#### 要点
RSSM 训练时，不仅预测 RGB，还预测多种辅助任务：

```
latent (z_t)
  │
  ├──► RGB Decoder        — 重建原始图像
  ├──► Semantic Decoder   — 预测语义分割
  ├──► Depth Decoder      — 预测深度图
  └──► Occupancy Decoder  — 预测占据网格
```

**这些 Decoder 的作用：**
- 强制隐状态保留底层视觉细节（RGB 重建）
- 强制隐状态包含高层语义理解（Semantic）
- 强制隐状态包含几何信息（Depth + Occupancy）

#### 注意事项
- 多任务 Decoder **仅在训练阶段使用**
- 推理时：**全部删除**，只保留 Encoder + RSSM + Policy
- 这属于 **多任务学习（Multi-task Learning）** 技巧，通过辅助任务提升主任务性能

### 知识点 4：为什么随机数据对 RSSM 重要？

#### 要点
RSSM 学习的是：

$$
(z_t, a_t) \rightarrow z_{t+1}
$$

动作是否正确**不重要**。重要的是动作空间要**全覆盖**：

| 动作类型 | 对世界模型的作用 |
|---------|----------------|
| 撞墙 | 学习碰撞动力学 |
| 倒车 | 学习后退运动学 |
| 旋转 | 学习角速度变化 |
| 前进 | 学习线性运动 |

因此 Random Dataset（随机动作采集）比 Teacher Dataset 更多（160K vs 100K）。

#### 注意事项
- 随机数据的动作不需要有意义，只需要覆盖机器人所有可能的运动模式
- 这让世界模型学到的是**物理动力学**而不是**导航策略**

## 疑问
- ❓ RSSM 会不会在长时间运行中出现隐状态漂移（latent drift）？是否有重置或正则化机制？
- ❓ 多任务 Decoder 的权重如何分配？各 Loss 之间的平衡策略是什么？

## 关联
- [[x-mobility-系统架构]]
- [[x-mobility-训练流程]]
- [[x-mobility-输入处理]]
- [[02-projects/大创/代码学习/x_mobility/rssm]]
- [[世界导航模型]]
