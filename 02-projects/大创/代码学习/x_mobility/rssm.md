---
date: 2026-02-02
tags:
  - 大创
  - python
---
# 文件位置

# 架构
rssm不知道是干嘛的，只知道是一个模型，用来对于时间序列进行处理的。和马尔科夫过程有一定关系。
## 代码架构
下属的代码架构就只有model.x_mobility.utils中的 stack_list_of_dict_tensor函数了。
## 物理架构
### 一、类之间的关系

`RSSM  
├── prior        → DistributionModel  
└── posterior    → DistributionModel`

👉 **DistributionModel 是 RSSM 的概率头（distribution head）。**

---

### 二、DistributionModel（分布生成模块）

#### 结构

`Linear → LeakyReLU → Linear → split → (mu, sigma)`

#### 函数

##### `forward(x)`

作用：

> 将输入特征映射为高斯分布参数 `(mu, sigma)`。

被调用位置：

`RSSM.imagine_step → prior RSSM.observe_step → posterior`

---

### 三、RSSM（主模型）

#### 内部子模块

```
pre_gru_net              # 状态预处理 
recurrent_model (GRU)    # 时间建模核心 
prior_action_module      # prior 的动作编码 posterior_action_module  # posterior 的动作编码 
prior                    # 先验分布 
posterior                # 后验分布`
```
---

### 四、核心调用链（最重要）

 forward    
	↓ 
observe_step
    ↓ 
imagine_step
    ↓ 
sample_from_distribution`

---

### 五、函数级结构

---

#### `forward(...)` —— 总调度器

职责：

- 初始化 hidden_state 和 latent_state
    
- 按时间步循环
    
- 调用 `observe_step`
    
- 汇总序列输出
    

调用：

`forward → observe_step`

---

#### `observe_step(...)` —— 单步观测更新

职责：

1️⃣ 先得到先验分布（prior）  
2️⃣ 再结合观测得到 posterior  
3️⃣ 采样 latent state

调用链：

```
observe_step  
├── imagine_step  
├── posterior_action_module  
├── posterior.forward  
└── sample_from_distribution`
```


返回：

`{prior, posterior}`

---

#### `imagine_step(...)` —— 单步预测

职责：

- 用 GRU 更新 hidden_state
    
- 基于 hidden_state + action 得到 prior 分布
    
- 从 prior 采样状态
    

调用链：

```
imagine_step  
├── pre_gru_net  
├── GRU  
├── prior_action_module  
├── prior.forward  
└── sample_from_distribution`
```

---

#### `sample_from_distribution(mu, sigma, use_sample)`

静态工具函数。

作用：

`sample = mu + sigma * noise`

或直接返回 `mu`。

被调用：

`imagine_step observe_step`
