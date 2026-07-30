---
name: paper-reading
description: 下载并分析学术论文（arXiv），使用 Moonshot AI 生成笔记、摘要和阅读指南
---
# Paper Reading - 论文阅读

下载并分析学术论文（主要支持 arXiv），生成笔记、摘要、代码项目和阅读指南。

## 功能
1. **论文下载**: 从 arXiv 自动下载论文 PDF
2. **论文解析**: 提取标题、作者、摘要、章节等结构化信息
3. **AI 分析**: 使用 Moonshot AI 进行深度分析（全面分析、关键点提取、实现指南）
4. **知识内化**: 生成 Markdown 笔记和摘要
5. **代码生成**: 基于论文分析生成实现代码框架
6. **辅助阅读**: 生成阅读指南和术语解释

## 使用方式

### Python API
```python
from .scripts.paper_skill import PaperSkill
skill = PaperSkill()
result = skill.download_and_analyze("2301.12345")
```

### 命令行
```bash
python .reasonix/skills/paper-reading/scripts/paper_skill.py 2301.12345
```

## 配置
需要 Moonshot AI API Key，在 `config.yaml` 中设置：
```yaml
moonshot:
  api_key: "your-api-key-here"
  base_url: "https://api.moonshot.cn/v1"
  model: "moonshot-v1-32k"
```

## 输出
分析结果保存在 `data/papers/<paper_id>/` 下：
- 笔记: `notes/YYYYMMDD_HHMMSS_note.md`
- 摘要: `summaries/summary.md`
- 代码: `code/`
- 阅读指南: `guides/reading_guide.md`

## 依赖
- Python 3.8+
- requests, PyYAML
- Moonshot AI API Key

## 注意事项
- 需要有效的 Moonshot AI API Key
- 下载论文需要网络连接
- 长论文建议使用 moonshot-v1-128k 模型
