---
type: paper-note
topic: X-Mobility 推理流程与部署
tags:
  - 大创
  - 论文
  - X-Mobility
  - 推理
  - ROS2
  - 部署
status: reviewed
rating: 5
---

# X-Mobility — 推理部署

## 总结
- 推理时多任务 Decoder 全部删除，只保留 Encoder + RSSM + Route Encoder + Policy
- ROS2 层负责：Goal → Planner → Route → 模型输入
- 模型输出 Action → `/cmd_vel`，Path → RViz 可视化
- Goal、Route、Path 三者容易混淆，需要清晰区分

### 知识点 1：推理流程图

#### 要点

```
ROS2 Layer:
Goal
  │
  ▼
Planner (Nav2 / compose_mapless_route)
  │
  ▼
Route (路径点序列)
  │
  ▼
VectorNet
  │
  ▼
Route Feature

Neural Network:
Camera
  │
  ▼
Image Encoder
  │
  ▼
RSSM
  │
  ▼
latent → Fusion → Policy
                    │
               ├────┴────┐
               ▼         ▼
             Path     Action (v, ω)
               │         │
               │    ROS2 /cmd_vel
               ▼
           RViz 可视化
```

#### 注意事项
- 推理阶段 Decoder 已删除，RSSM 仅产生 latent，不产生重建图像
- Route 由外部规划器在 ROS 层实时生成，不是模型的一部分

### 知识点 2：Goal、Route、Path 三者关系

#### 要点
这是整个论文最容易被混淆的概念。三者的关系是：

```
Goal                 — 最终目的地（用户指定）
  │
  ▼
Planner
  │
  ▼
Route                — 规划器生成的路径点（模型输入）
  │
  ▼
Policy
  │
  ├──► Action        — 控制指令（发布到 cmd_vel）
  └──► Path          — 预测的未来轨迹（仅可视化）
```

| 概念 | 来源 | 作用 | 是否是模型输入 |
|------|------|------|:-------------:|
| **Goal** | 用户指定（ROS 层） | 最终目的地（如 (20, 10)） | ❌ |
| **Route** | Planner（Nav2）生成 | 一系列路径点，作为模型的导航意图输入 | ✅ |
| **Path** | Policy 网络输出 | 预测的未来 5 个轨迹点 | ❌（是输出） |

#### 示例

```
Goal: (20, 10)                        # 用户说：去坐标 (20, 10)
  │
  ▼
Planner → Route:                      # 规划器生成一条路径
  [(0,0), (2,1), (5,3), (10,5), ...]
  │
  ▼
Policy → Action: (0.5 m/s, 0.1 rad/s) # 模型输出当前动作
       → Path: [(1,1), (2,2), ...]    # 模型预测未来轨迹（可视化用）
```

### 知识点 3：ROS2 集成要点

#### 要点
| 组件 | Topic/Service | 说明 |
|------|--------------|------|
| Goal 输入 | `/goal_pose` 或导航接口 | 用户指定目标点 |
| Route 生成 | 全局规划器 | Nav2 或 `compose_mapless_route` |
| Action 输出 | `/cmd_vel` | Twist 消息（v, ω） |
| Path 可视化 | `/path` 或 RViz 接口 | 用于调试和监控 |

## 疑问
- ❓ 如果规划器失效（如 Route 生成失败），模型如何退化？是否有 fallback 机制？
- ❓ 推理时 RSSM 的隐状态是否需要重置？还是在多次推理间持续累积？

## 关联
- [[x-mobility-系统架构]]
- [[x-mobility-策略网络]]
- [[x-mobility-训练流程]]
- [[x-mobility-设计思想]]
