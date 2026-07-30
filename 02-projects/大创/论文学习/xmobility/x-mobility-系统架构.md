---
type: paper-note
topic: X-Mobility 整体系统架构
tags:
  - 大创
  - 论文
  - X-Mobility
  - 系统架构
  - 数据流
status: reviewed
rating: 5
---

# X-Mobility — 系统架构

## 总结
- 整个系统由 **六个模块** 组成：Encoder → RSSM 世界模型 → Route Encoder → Policy Fusion → Policy → 多任务 Decoder
- 训练时使用多任务 Decoder 辅助学习，推理时全部删除
- Route 由外部规划器生成，不是模型学习得到的

### 知识点 1：六个模块概览

#### 要点

```
                 Camera
                    |
                    ▼
             Image Encoder
                    |
                    ▼
             Latent Feature
                    |
                    ▼
            RSSM World Model
                    |
                    ▼
            History Latent State
                    |
      ┌─────────────┴─────────────┐
      ▼                           ▼
 Route Encoder               Multi-task Decoder
      │                           │
      ▼                           ▼
 Route Feature          Depth / Semantic / RGB ...
      │
      ▼
 Policy Fusion
      │
      ▼
 Policy Head
      ├────────► Action
      └────────► Path
```

**六个模块：**

| 模块 | 功能 | 训练时 | 推理时 |
|------|------|--------|--------|
| 1. Image Encoder | 将 Camera RGB 编码为 latent feature | ✅ | ✅ |
| 2. RSSM 世界模型 | 学习环境动态，维护历史隐状态 | ✅ | ✅ |
| 3. Route Encoder | 将 Route 路径点编码为 route feature | ✅ | ✅ |
| 4. Policy Fusion | 融合 latent + route feature | ✅ | ✅ |
| 5. Policy Head | 输出 Action(v, ω) + 未来 Path | ✅ | ✅ |
| 6. 多任务 Decoder | 辅助学习：重建 RGB/Semantic/Depth/Occupancy | ✅ | ❌ 删除 |

### 知识点 2：完整数据流（训练与推理）

#### 要点

```
                        ROS2 Layer
────────────────────────────────────────────────────────
Goal
 │
 ▼
Planner（Nav2 或 compose_mapless_route）
 │
 ▼
Route (20个路径点)
 │
 ▼
VectorNet
 │
 ▼
Route Feature
────────────────────────────────────────────────────────
               Neural Network
────────────────────────────────────────────────────────
Camera
 │
 ▼
Image Encoder
 │
 ▼
Latent z
 │
 ▼
RSSM World Model
 │
 ▼
History Latent h
 │
 ├───────────────┐
 │               │
 ▼               ▼
Multi-task     Route Feature
Decoder             │
 │                  │
 └──────────┬───────┘
            ▼
      Policy Fusion
            │
            ▼
       Policy Network
      ├──────────────┐
      ▼              ▼
 Future Path      Action(v, ω)
      │              │
      │         ROS2 /cmd_vel
      │
      └────► RViz 可视化
```

#### 注意事项
- 多任务 Decoder 仅在训练阶段使用，推理阶段全部删除以节省计算
- Path 是 Policy 的输出（预测结果），不是输入——仅用于可视化，不直接控制机器人
- Route 来自外部规划器（Nav2 或 compose_mapless_route），模型本身不生成 Route

## 疑问
- ❓ 推理时删除 Decoder 后，RSSM 的隐状态质量是否会因为缺少重建损失的回传而下降？

## 关联
- [[x-mobility-概述]]
- [[x-mobility-输入处理]]
- [[x-mobility-rssm世界模型]]
- [[x-mobility-策略网络]]
- [[x-mobility-训练流程]]
- [[x-mobility-推理部署]]
