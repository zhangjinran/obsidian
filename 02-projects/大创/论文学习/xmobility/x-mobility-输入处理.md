---
type: paper-note
topic: X-Mobility 输入处理（Camera Encoder + Route Encoder）
tags:
  - 大创
  - 论文
  - X-Mobility
  - Encoder
  - VectorNet
  - Route
status: reviewed
rating: 5
---

# X-Mobility — 输入处理

## 总结
- 模型真正输入只有两个东西：**Camera RGB** 和 **Route 路径点**
- Camera 经 Image Encoder（CNN/DINOv2）编码为 latent feature
- Route 经 VectorNet 编码为 route feature
- Goal 仅存在于 ROS 层，Route 由规划器根据 Goal 生成后输入模型

### 知识点 1：Camera 输入处理

#### 要点
- **输入**：机器人前视 RGB 图像（如 640×480）
- **编码器**：CNN（论文）/ DINOv2（源码实现）
- **输出**：latent feature（隐空间特征向量）

```
Image (640×480 RGB)
  │
  ▼
CNN / DINOv2
  │
  ▼
latent feature (如 768 维)
```

#### 注意事项
- 源码中使用 DINOv2 作为图像编码器，这与论文中描述的 CNN 可能不同
- DINOv2 的 ViT 架构提供更丰富的视觉语义理解

### 知识点 2：Route 输入处理

#### 要点

**Route 不是 Goal。** Route 是规划器生成的一组有序路径点：

```
[x0, y0] → [x1, y1] → [x2, y2] → ... → [xn, yn]
```

**编码方式**：源码采用 **VectorNet** 架构。

为什么用 VectorNet？

因为 Route 的本质是 **折线（polyline）**：

```
P1 → P2 → P3 → P4
```

VectorNet 将其编码为向量化表示：

```
[(P1, P2), (P2, P3), (P3, P4)]
```

最终输出：

```
route_feature
```

#### 公式
Route 是规划器生成的路径点序列（论文中未明确说明长度，源码实现约为 20 个点）：

$$
\text{Route} = \{(x_0, y_0), (x_1, y_1), \dots, (x_n, y_n)\}
$$

VectorNet 编码：

$$
\text{route\_feature} = \text{VectorNet}(\text{Route})
$$

#### 注意事项
- Route 不是模型学习得到的，而是外部规划器人为提供的
- 源码中 Route 的来源是 Nav2 的全局规划器或 `compose_mapless_route` 节点
- Goal 只存在于 ROS 层：用户给定 Goal → Planner 生成 Route → Route 输入模型

## 疑问
- ❓ VectorNet 是端到端训练还是预训练固定的？如果联合训练，Route 路径点的梯度如何影响规划器？

## 关联
- [[x-mobility-系统架构]]
- [[x-mobility-rssm世界模型]]
- [[x-mobility-策略网络]]
- [[02-projects/大创/代码学习/x_mobility/encoders]]
- [[02-projects/大创/代码学习/x_mobility/vector_net]]
- [[DINOv2]]
