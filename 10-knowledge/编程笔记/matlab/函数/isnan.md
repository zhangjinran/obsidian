---
date: 2026-01-25
tags:
  - 函数
  - matlab
---
# 参数
[[knowledge/编程笔记/python/数据结构/数组]]
# 输出
生成结果为1，0的[[逻辑数组]]
# 用法
```
生成相同维度的逻辑矩阵,只识别nan，只要结果是nan，就是true也就是1，否则都是0.

a=[1,0,0,nan];

b=[1,2;1,nan];

isnan(a)

isnan(b)
```