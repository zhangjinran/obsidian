---
type: paper-note
topic: X-Mobility 数据集与两阶段训练流程
tags:
  - 大创
  - 论文
  - X-Mobility
  - 训练
  - Loss
  - 数据集
status: reviewed
rating: 5
---

# X-Mobility — 数据集与训练流程

## 总结
- 数据集来自 **Isaac Sim** 仿真环境，分为 Random Dataset 和 Teacher Dataset
- 训练分为两个阶段：**Stage1 训练世界模型**（Encoder + RSSM + Decoder），**Stage2 训练策略**（Policy）
- Stage1 使用随机动作数据学习环境动力学；Stage2 使用专家示范数据模仿导航策略

### 知识点 1：数据集

#### 要点

**数据来源**：Isaac Sim 仿真环境

| 数据集 | 数据量 | 采集方式 | 作用 |
|--------|--------|---------|------|
| Random Dataset | **160K** | 随机动作采集 | 训练世界模型 |
| Teacher Dataset | **100K** | Nav2 专家策略采集 | 训练 Policy |

**每条数据包含：**

```
{
  RGB,        # 前视图像
  Semantic,   # 语义分割图
  Route,      # 规划路径
  Path,       # 未来轨迹（GT）
  Action,     # 控制指令 (v, ω)
  Speed       # 当前速度
}
```

#### 注意事项
- Random Dataset 的动作是**随机生成的**，不包含任何导航意图（撞墙、倒车、旋转等）
- Teacher Dataset 由 Nav2 规划器生成的专家轨迹采集

### 知识点 2：Stage1 — 世界模型训练

#### 要点

**训练目标**：学习世界动力学

**训练模块**：

```
Encoder + RSSM + Decoder
```

**输入输出**：

```
输入：RGB 序列 + Action 序列
输出：未来隐状态预测
```

**Loss 组成（L_world）：**

$$
\mathcal{L}_{\text{world}} = \mathcal{L}_{\text{KL}} + \mathcal{L}_{\text{Image}} + \mathcal{L}_{\text{Semantic}} + \mathcal{L}_{\text{Depth}} + \mathcal{L}_{\text{Occupancy}}
$$

| Loss 项 | 含义 |
|---------|------|
| $\mathcal{L}_{\text{KL}}$ | 状态预测与状态估计的 KL 散度一致性约束 |
| $\mathcal{L}_{\text{Image}}$ | RGB 图像重建损失 |
| $\mathcal{L}_{\text{Semantic}}$ | 语义分割预测损失 |
| $\mathcal{L}_{\text{Depth}}$ | 深度图预测损失 |
| $\mathcal{L}_{\text{Occupancy}}$ | 占据网格预测损失 |

**使用数据**：Random Dataset（160K）

### 知识点 3：Stage2 — 策略学习

#### 要点

**训练目标**：学习导航策略

**固定/微调**：

```
Encoder — 固定（或微调）
RSSM   — 固定（或微调）
Policy — 训练
```

**输入输出**：

```
输入：latent (RSSM) + route (VectorNet)
输出：action + path
```

**Loss 组成（L_policy）：**

$$
\mathcal{L}_{\text{policy}} = \mathcal{L}_{\text{Action}} + \mathcal{L}_{\text{Path}}
$$

| Loss 项 | 公式 | 含义 |
|---------|------|------|
| $\mathcal{L}_{\text{Action}}$ | $\|\hat{a} - a\|^2$ | 动作预测与专家动作的 MSE |
| $\mathcal{L}_{\text{Path}}$ | $\|\hat{p} - p\|^2$ | 未来轨迹预测与 GT 的 MSE |

**使用数据**：Teacher Dataset（100K）

#### 注意事项
- Stage2 是 **模仿学习（Imitation Learning）**——通过最小化与专家动作的差异来学习
- Path Loss 属于 **Auxiliary Task**，帮助 Policy 学习长期运动

### 知识点 4：完整 Loss 总结

#### 公式

$$
\mathcal{L}_{\text{total}} = \mathcal{L}_{\text{world}} + \mathcal{L}_{\text{policy}}
$$

展开：

$$
\mathcal{L}_{\text{total}} = (\mathcal{L}_{\text{KL}} + \mathcal{L}_{\text{Image}} + \mathcal{L}_{\text{Semantic}} + \mathcal{L}_{\text{Depth}} + \mathcal{L}_{\text{Occupancy}}) + (\mathcal{L}_{\text{Action}} + \mathcal{L}_{\text{Path}})
$$

各 Loss 在训练阶段的启用情况：

| Loss | Stage1 | Stage2 |
|------|--------|--------|
| $\mathcal{L}_{\text{KL}}$ | ✅ | ❌ |
| $\mathcal{L}_{\text{Image}}$ | ✅ | ❌ |
| $\mathcal{L}_{\text{Semantic}}$ | ✅ | ❌ |
| $\mathcal{L}_{\text{Depth}}$ | ✅ | ❌ |
| $\mathcal{L}_{\text{Occupancy}}$ | ✅ | ❌ |
| $\mathcal{L}_{\text{Action}}$ | ❌ | ✅ |
| $\mathcal{L}_{\text{Path}}$ | ❌ | ✅ |

## 疑问
- ❓ Stage2 中 Encoder 和 RSSM 是固定还是微调？论文和源码是否有差异？
- ❓ Random Dataset 160K 和 Teacher Dataset 100K 的比例对性能有什么影响？

## 关联
- [[x-mobility-rssm世界模型]]
- [[x-mobility-策略网络]]
- [[x-mobility-设计思想]]
- [[02-projects/大创/代码学习/dataset/isaacsim_dataset]]
- [[02-projects/大创/代码学习/x_mobility/rssm]]
