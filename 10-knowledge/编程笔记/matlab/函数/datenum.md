---
date: 2026-01-25
tags:
  - 函数
  - matlab
---
# 参数
- 字符串
- 时间格式：'yyyy','yyyymm','yyyymmdd','yyyymmddHH','yyyymmddHHMM',
'yyyymmddHHMMSS'
# 输出
matlab自定义的时间格式
# 用法
**将 “人类可读的时间字符串 / 日期向量” 转换为 MATLAB 内部的 “日期序列号”（一个数字）**。

- MATLAB 时间序列号的规则：以「公元 0 年 1 月 1 日」为 0，每过 1 天数值 + 1（比如 2020 年 1 月 1 日的序列号约为 737791）；
- 优势：时间比较 / 计算只需对比数字（比如判断 `timeNum >= datelim_start`），比字符串对比简单
