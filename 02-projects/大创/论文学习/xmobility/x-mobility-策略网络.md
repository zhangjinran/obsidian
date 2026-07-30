---
type: paper-note
topic: X-Mobility 策略网络（Policy Fusion + Action + Path）
tags:
  - 大创
  - 论文
  - X-Mobility
  - Policy
  - 策略网络
  - 模仿学习
status: reviewed
rating: 5
---

# X-Mobility — 策略网络

## 总结
- Policy 接收融合后的特征（RSSM latent + route feature），输出 Action 和 Path
- **Action**：机器人的即时控制指令 $(v, \omega)$，直接发布到 `/cmd_vel`
- **Path**：预测的未来 5 个轨迹点，属于辅助监督信号（Auxiliary Task），推理时仅用于可视化
- 训练采用模仿学习（L1/L2 Loss），而非强化学习

### 知识点 1：Policy Fusion

#### 要点
两个特征需要融合：

| 特征 | 来源 | 维度 | 含义 |
|------|------|------|------|
| RSSM latent $h_t$ | Encoder + RSSM | 高维（如 512~1024） | 当前世界状态（历史 + 视觉 + 动作） |
| route_feature | VectorNet | 中维（如 256~512） | 规划路径的编码表示 |

融合方式（源码中的 `PolicyStateFusion`）：

```
policy_state = Fusion(latent, route_feature)
```

然后送 Policy Head。

### 知识点 2：Action 输出

#### 要点
**Action** 是机器人线速度和角速度控制指令：

$$
\text{Action} = (v, \omega)
$$

例如：

```
v = 0.5 m/s
ω = 0.2 rad/s
```

动作指令直接发布到 ROS2 的 `/cmd_vel` topic。

#### 公式
训练时 Action Loss 使用 L2 Loss（MSE）：

$$
\mathcal{L}_{\text{Action}} = \|\hat{a} - a\|^2
$$

其中 $\hat{a}$ 是预测动作，$a$ 是专家动作（Teacher Dataset 中的 ground truth）。

### 知识点 3：Path 输出

#### 要点
**Path** 是 Policy 预测的未来轨迹点：

$$
\text{Path} = \{(x_1, y_1), (x_2, y_2), \dots, (x_5, y_5)\}
$$

共 **5 个点 × 2 维 = 10 维**。

**关键理解：**
- Path 是**输出**，不是输入
- Path 不用于控制机器人
- Path 仅用于 **RViz 可视化**

**Path 的作用：**
- 属于 **Auxiliary Task（辅助任务）**
- 帮助 Policy 学习**长期运动**（Action 只有当前一步，Path 覆盖未来几秒）
- 作为监督信号，防止 Policy 过拟合单步动作

#### 公式
Path Loss 同样使用 L2 Loss：

$$
\mathcal{L}_{\text{Path}} = \|\hat{p} - p\|^2
$$

#### 注意事项
- Path 是训练时的辅助监督，推理时虽然也输出但不用于控制
- Action 和 Path 可以共享 Policy 网络的中间层，在最终 head 处分叉

### 知识点 4：Action 和 Path 的关系

#### 要点

| | Action | Path |
|------|--------|------|
| **含义** | 当前时刻控制指令 | 未来 5 步预测轨迹 |
| **维度** | 2（v, ω） | 10（5×2） |
| **时间范围** | 当前一步 | 未来几秒 |
| **控制作用** | ✅ 直接控制机器人 | ❌ 仅可视化 |
| **训练 Loss** | MSE | MSE |

## 疑问
- ❓ Action 和 Path 的损失权重如何平衡？Path Loss 是否应该随着时间步增加而衰减？
- ❓ 是否可以用 Path 作为反馈信号来做更精细的控制（例如 Path 与规划 Route 偏差过大时降速）？

## 关联
- [[x-mobility-系统架构]]
- [[x-mobility-输入处理]]
- [[x-mobility-训练流程]]
- [[x-mobility-推理部署]]
- [[02-projects/大创/代码学习/x_mobility/action_policy]]
