---
date: 2026-03-02
tags:
  - 课程
  - 卫星算法
---
`std::map` 是 C++ 标准库中的关联容器，它以**键值对**形式存储数据，并根据键自动排序，每个键唯一。下面汇总其常用操作。

---

### 1. 头文件与声明
```cpp
#include <map>
#include <string>

std::map<int, std::string> m1;               // 空 map
std::map<std::string, double> m2;            // 键为 string，值为 double
std::map<int, std::string> m3 = { {1, "a"}, {2, "b"} };  // 初始化列表
```

---

### 2. 插入元素
```cpp
// 方式1：insert
m1.insert({3, "c"});
m1.insert(std::make_pair(4, "d"));

// 方式2：operator[]
m1[5] = "e";      // 键5不存在则插入，存在则覆盖
m1[6];            // 仅插入键6，值为默认构造的字符串
```

---

### 3. 访问元素
```cpp
// 使用 operator[]（若键不存在会插入默认值，慎用）
std::cout << m1[3];   // 输出 "c"

// 使用 at()（键不存在抛出 std::out_of_range）
std::cout << m1.at(4);

// 通过迭代器
auto it = m1.find(3);
if (it != m1.end())
    std::cout << it->first << " => " << it->second;
```

---

### 4. 查找元素
```cpp
// find：返回迭代器，找不到返回 end()
auto it = m1.find(10);
if (it == m1.end()) std::cout << "不存在";

// count：返回键出现次数（0或1）
if (m1.count(3)) std::cout << "存在";
```

---

### 5. 删除元素
```cpp
// 按键删除
m1.erase(3);

// 通过迭代器删除
auto it = m1.find(4);
if (it != m1.end()) m1.erase(it);

// 清空
m1.clear();
```

---

### 6. 遍历
```cpp
// C++11 范围for
for (const auto& pair : m1) {
    std::cout << pair.first << " -> " << pair.second << '\n';
}

// 使用迭代器
for (auto it = m1.begin(); it != m1.end(); ++it) {
    std::cout << it->first << " -> " << it->second << '\n';
}
```

---

### 7. 大小与判空
```cpp
size_t sz = m1.size();   // 元素个数
bool empty = m1.empty(); // 是否为空
```

---

### 8. 自定义排序
默认按键升序，可通过第三个模板参数指定比较函数（如降序）：
```cpp
std::map<int, std::string, std::greater<int>> m; // 键降序
```
也可自定义函数对象或 lambda。

---

### 9. 嵌套 map（常用于 GNSS 星历存储）
```cpp
// 卫星号 → (时间 → 星历)
std::map<std::string, std::map<int, double>> satData;

// 插入：G01 在时间 100 处值为 1.23
satData["G01"][100] = 1.23;

// 遍历所有卫星的所有时间点
for (const auto& sat : satData) {
    for (const auto& timeEph : sat.second) {
        std::cout << sat.first << " @ " << timeEph.first << " = " << timeEph.second << '\n';
    }
}
```

---

### 10. 注意事项
- **键唯一**：重复插入相同键，新值会覆盖旧值。
- **自动排序**：键类型必须支持 `<` 操作（或提供比较器）。
- **效率**：插入、查找、删除均为 O(log n)。
- **迭代器有效性**：插入和删除可能使部分迭代器失效，需谨慎。

`std::map` 非常适合需要按键快速查找且保持顺序的场景，如 GNSS 星历数据按卫星和时间索引的存储与检索。