[一步步教你在 Windows 上轻松安装 Anaconda以及使用常用conda命令（超详细）_windows anaconda-CSDN博客](https://blog.csdn.net/Natsuago/article/details/143081283)

# 问题（需要换源）
# ✅ 正确做法（精确修复，不用重装）

## ① 删除所有 channel（必须干净）

conda config --remove-key channels

---

## ② 只保留现代仓库（不要 free！）

conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/main  
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/r  
conda config --add channels conda-forge

---

## ③ 设置严格优先级（关键）

conda config --set channel_priority strict

---

## ④ 清缓存（必须）

conda clean -a -y

---

## ⑤ 再测试

conda search python=3.10

👉 **这一步是判生死的**