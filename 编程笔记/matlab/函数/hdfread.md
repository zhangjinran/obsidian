---
date: 2026-01-25
tags:
  - 函数
  - matlab
  - 文件
---
# 参数
- 文件路径
- 需要读取的变量名
# 输出
输出读取的变量内容。执行该语句后，会返回一个**数值数组**
# 用法
```

%拼接完整路径 
full_file_path = [data_struct.path.L1,'/',fileName1]; 
% 读取经度数据 
Lon = hdfread(full_file_path, '/Longitude'); % 查看数据维度和内容 
disp(size(Lon)); % 输出 [1000,1]（1000条廓线，每条1个经度值） 
disp(Lon(1:5)); % 输出前5条廓线的经度：比如 [10.1; 10.2; 10.3; 10.4; 10.5]