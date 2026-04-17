---
date: 2026-01-25
tags:
  - 函数
  - matlab
---
# 参数
第一个参数是[[函数句柄]]，第二个参数是[[元胞]]
# 输出
函数句柄对于元胞内的每一个元素遍历后的结果。
# 用法
```
mycell = {[], 'L1数据', [], [1,2,3]};

  

% 错误写法：直接写isempty（无@）

%cellfun(isempty, mycell); % 运行会报错！

% 报错信息：输入参数的数目不足。（因为Matlab试图执行isempty()，但没传参）

  

% 正确写法：加@创建函数句柄

cellfun(@isempty, mycell) % 正常运行，返回[true,false,true,false]
```