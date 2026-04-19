---
date: 2026-01-25
tags:
  - 函数
  - matlab
---
# 参数
一个由字符串组成的[[编程/数据结构/数组]]。
核心就是要注意，它可以动态改变左边的变量名，所以使用参数是要注意下面的事例参考
## 举例说明
### 正确示范
```
data_name={'ALay_05km','CLay_05km','Mlay_05km',' L2_CPro','L2_APro','L1','VFM',' CLay_01km','MLay_333m'};

for ii =1:length(mycell)

	if ~isempty(mycell{ii})

		eval([data_name{ii},'=mycell{ii};']);%
		
		%此时生成等式ALay_05km=mycell{ii}
		%注意这里左边需要动态改变的变量名不能放在引号里面。
	
	end

end
```
### 错误示范
```
eval(['data_name{ii}=mycell{ii};']);%
		
		% 此时生成等式data_name{ii}=mycell{ii},显然错误。
```

# 输出
将这些字符串拼接起来后，生成一个语法句子。然后会直接执行这个语法句子。
# 用法
```
a1=1:10

b=1

eval(['a',num2str(b)])%可以动态生成变量，非常牛逼，但是容易报错。

eval(['c=[]'])% 甚至还可以动态生成等式
```

和[[循环]]结合可以达到事半功倍的效果。