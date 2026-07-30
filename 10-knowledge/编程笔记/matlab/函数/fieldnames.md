---
date: 2026-01-25
tags:
  - 函数
  - matlab
---
# 参数
[[结构体]]
# 输出
[[元胞]]
# 用法
```
a=struct();

a.lat=1;

a.pro=2;
b=fieldnames(a)%将结构体的字段名生成一个元组。
%b={'lat','pro'}
```
可以与[[isempty]]配合判断结构体是否为空