# Structure Audit

检查知识库目录结构是否符合 vault-schema.yaml。

## 触发条件
"检查 vault 结构"、"审计目录"、"目录健康检查"

## 步骤

1. 读取 `references/schema/vault-schema.yaml`，确认当前目录定义
2. 执行脚本：`bash scripts/structure/structure-check.sh .`
3. 读取脚本输出的审计报告，呈现给用户

## Do Not
- 自动删除目录
- 自动移动文件
- 自动修改 schema
