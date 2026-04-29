---
date: 2026-02-10
tags:
  - 论文
  - 大气
  - 组会
---
好，这里给你一套**完整、严格对齐论文的方法架构（从原始 CALIPSO → 时间序列）**。我不会再碎片讲，而是给你一条**可以直接实现的工程流程**，每一步都对应你当前的数据状态。

---

# 总体目标（先定清楚）

你最终要得到的是：

```text
X(time) 或 X(time, lat, height)
```

用于：

- anomaly（去季节）
    
- trend（趋势）
    

---

# 一、完整流程总览（论文等价流程）

```text
Step 0：原始 profile 数据（CALIPSO）
    ↓
Step 1：读取 time / lat / profile
    ↓
Step 2：时间分箱（month）
    ↓
Step 3：空间分箱（lat_bin, height）
    ↓
Step 4：构建月平均剖面 (time, lat, height)
    ↓
Step 5：空间平均 → 时间序列 X(time)
    ↓
Step 6：去季节化 anomaly
    ↓
Step 7：趋势分析 trend
```

---

# 二、Step 0：原始数据（你当前状态）

输入：

```text
CAL_LID_L2_05kmAPro / ALay
```

你现在已经有：

```text
✔ lat
✔ height
✔ profile value（TAB / extinction）
```

缺：

```text
❗ time（关键）
```

---

# 三、Step 1：恢复时间（必须完成）

## 输入：

HDF 原始文件

## 输出：

```text
time(N)
lat(N)
profile(N, height)
```

---

## 核心操作：

```matlab
time_raw = hdfread(file, 'Profile_UTC_Time');
time = datenum(1993,1,1) + time_raw;
```

---

## 结果：

每个 profile 都有：

```text
(time_i, lat_i, profile_i)
```

👉 到这里，你才进入论文体系

---

# 四、Step 2：时间分箱（month）

## 目标：

```text
每个 profile → 属于哪个月
```

---

## 操作：

```matlab
[year, month, ~] = datevec(time);
month_id = year * 100 + month;
```

---

## 输出：

```text
month_id(N)
```

例如：

```text
200701, 200701, 200702 ...
```

---

# 五、Step 3：空间分箱（关键步骤）

论文是：

```text
2° × 2° grid
```

你现在可以简化为：

```text
lat_bin（例如每2°）
height（已有）
```

---

## 操作：

```matlab
lat_bin = floor(lat / 2) * 2;
```

---

## 输出：

```text
每个 profile 属于：
(month, lat_bin)
```

---

# 六、Step 4：构建月平均剖面（核心）

## 目标：

构造：

```text
X(time, lat, height)
```

---

## 逻辑：

```text
for 每个月:
    for 每个纬度带:
        收集所有 profile
        在 height 上做平均
```

---

## 数学表达：

[  
X(m, lat, z) = mean{ profile_i(z) \mid i ∈ (month=m, lat_bin) }  
]

---

## 输出：

```text
X(month, lat_bin, height)
```

👉 这是论文的“monthly gridded data”的等价版本（你是 lat-height）

---

# 七、Step 5：空间平均 → 时间序列（论文第一步）

现在你有：

```text
X(time, lat, height)
```

---

## 如果做 global mean：

[  
X_{global}(t) = \sum X(t, lat, z) \cdot cos(lat)  
]

---

## MATLAB：

```matlab
w = cosd(lat_bin);

X_global = sum(X .* w, 2) / sum(w);
```

（根据维度调整）

---

## 输出：

```text
X(time)
```

👉 这就是论文 Figure 5 的基础

---

# 八、Step 6：去季节化（anomaly）

## 目标：

去掉季节周期

---

## 方法：

```matlab
X_reshape = reshape(X_global, [], 12);
monthly_mean = mean(X_reshape, 1);

X_anomaly = X_global - repmat(monthly_mean, size(X_reshape,1), 1);
X_anomaly = X_anomaly(:);
```

---

## 输出：

```text
X_anomaly(time)
```

---

# 九、Step 7：趋势（trend）

```matlab
t = (1:length(X_anomaly))';
coef = polyfit(t, X_anomaly, 1);

trend = coef(1);
```

---

# 十、你可以扩展的方向（结合你现在研究）

你现在是做：

```text
气溶胶 / 云垂直结构
```

可以直接扩展：

---

## ✔ 方向1：time–height 图

```text
X(time, height)
```

👉 对应论文 Figure 9

---

## ✔ 方向2：某一高度层时间序列

```text
X(time, z=3km)
```

---

## ✔ 方向3：不同纬度对比

```text
X(time, lat_band)
```

---

# 十一、整个流程的本质（最重要理解）

> ❗ **时间序列不是“画出来的”，而是“通过分组统计构造出来的”**

---

# 十二、你当前的“唯一阻塞点”

```text
❗ Step 1：时间没有读出来
```

---

# 十三、你现在该做什么（只做这一件事）

👉 在 MATLAB 中：

```matlab
info = hdfinfo(file);

for i = 1:length(info.SDS)
    disp(info.SDS(i).Name)
end
```

---

# 十四、我接下来会帮你做什么

当你把变量列表给我：

我会：

1. ✔ 精确指出时间字段
    
2. ✔ 给你读取代码
    
3. ✔ 带你直接进入 Step 2（分月）
    

---

# 最后一句（给你定心）

你现在已经完成了：

```text
✔ 空间理解
✔ 论文逻辑理解
✔ 数据结构理解
```

只差：

```text
time 这一维
```

一旦补上，你整个流程会**一下子打通**。