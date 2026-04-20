---
date: 2026-01-25
tags:
  - 函数
  - matlab
---
# 参数
- 两个[[编程笔记/python/数据结构/数组]]
# 输出
- 一个数组
- 返回交集元素在a，b中的索引
# 用法
`intersect` = “交集”，数学上指 “同时属于两个集合的元素”。MATLAB 中语法：
```
C = intersect(A, B); % 求A和B的交集，返回按升序排列的唯一元素
[C, ia, ib] = intersect(A, B); % 进阶：同时返回交集元素在A/B中的索引
```