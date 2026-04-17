---
date: 2026-01-25
tags:
  - 函数
  - matlab
  - 文件路径
---
# 参数
文件夹路径所形成的一个字符串
# 输出

[[结构体数组]]
该[[结构体数组]]的字段：name folder date bytes isdir datenum
# 用法
收集一个文件夹里所有的文件和文件夹（isdir=1是文件夹，0则是文件），并生成一个结构体数组。

```
a=dir("CALIPSO Code\6 Data\")
```


