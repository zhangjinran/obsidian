# Template Management

在 vault 中新增或修改笔记类型。

## 触发条件

用户说"新增笔记类型"、"我想加一种新的笔记"、"添加模板"。

## 步骤

### 1. 确定新类型
确定新类型的 `type` 名称和用途

### 2. 编辑 frontmatter-schemas
编辑 `references/frontmatter/schemas.md`：
- 在目录中新增条目
- 在末尾（Validation Rules 之前）新增章节：字段定义 + 模板链接

### 3. 新建模板文件
在 `references/_templates/` 下新建模板文件，并在 `references/templates.md` 索引中新增条目

### 4. 验证一致性
`type` 名称在 schemas / 索引 / 模板文件三处一致，字段与模板对应

### 5. 更新创建笔记列表
更新 SKILL.md 中可用笔记类型的列表
