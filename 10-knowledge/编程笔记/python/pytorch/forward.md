---
date: 2026-02-03
tags:
  - 函数
  - 类
  - python
  - 语法
  - pytorch
---
# 最核心结论

在 **PyTorch** 中：

`y = model(x)`

**并不是直接调用 `forward`**，而是：

`model(x)  
↓
`nn.Module.__call__()  
↓
`forward(x)`
## 解释
- 也就是因为继承了父辈Module，所以调用model的时候是先调用从父辈继承来的[[魔术方法#`__call__`|__call__()]]函数，然后在`__call__()`函数中会调用`forward（）`函数。
- 所以最后观感上就是直接调用了forward函数
