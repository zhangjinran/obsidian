---
date: 2026-03-02
tags:
  - 课程
  - 卫星算法
  - cmake
aliases:
  - 头文件
---
# 头文件的内容
- 包括的文件叫头文件就是后缀名有.h的文件。
- 头文件里的内容就是函数、类或者模版类的声明。
- 这个相当于是在[[编译]]过程中包括了函数的声明。这样的话编译就能通过。编译的时候就知道这里有个函数。
# cmake中的应用
- 在cmake语法里就是会使用`include_directories( ${PROJECT_SOURCE_DIR}/lib/ )`去增加头文件的搜索范围。这样在正式代码中包括这个目录下的头文件就不会报错。
# cpp文件中的应用
在cpp文件中存在两种include语法。
- “headfilename.h”
- <headfilename.h>
## 区别
- 前者的搜索范围和顺序是优先搜索cpp文件所在的目录，然后搜索cmake语法里用include_directories包括的目录，最后搜索系统的标准库目录。
- 后者直接搜索 `include_directories` 添加的路径，然后系统默认路径。
# 头文件命名习惯
- **标准库头文件**（如 `iostream`、`cstdlib`、`stdexcept`、`cstring`）**通常不带 `.h` 后缀**。因为这些头文件本身就不带.h后缀。
- 而自定义文件为了便于标识都带了.h后缀。