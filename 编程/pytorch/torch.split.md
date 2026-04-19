---
date: 2026-02-04
tags:
  - 函数
  - pytorch
  - python
---
# 输入参数
- tensor类型
- 分割的size，可以是数字或者数组
	- 如果是数字就是尽量均分成这么多块
	- 如果是数组，比如`[2,1]`,就是一块占2/3，一块占1/3.
- 分割的维度
# 输出参数
分割的结果，一般是tensor组成的元组。
# 实例
```
Example:

a = torch.arange(10).reshape(5, 2)
a

tensor([[0, 1],
        [2, 3],
        [4, 5],
        [6, 7],
        [8, 9]])


torch.split(a, 2)

(tensor([[0, 1],
         [2, 3]]),
 tensor([[4, 5],
         [6, 7]]),
 tensor([[8, 9]]))


torch.split(a, [1, 4])

(tensor([[0, 1]]),
 tensor([[2, 3],
         [4, 5],
         [6, 7],
         [8, 9]]))
```
