"""
Paper Reading Skill 使用示例
演示如何在 Cursor 等 AI IDE 中使用论文阅读技能
"""

import sys
from pathlib import Path

# 添加项目根目录到路径
skill_dir = Path(__file__).parent.parent.parent
sys.path.insert(0, str(skill_dir))

from skills.paper_reading.scripts.paper_skill import PaperSkill


def example_download_and_analyze():
    """示例 1: 下载并完整分析一篇论文"""
    skill = PaperSkill()
    
    result = skill.download_and_analyze("2301.12345")
    
    if result.get("success"):
        print("✓ 分析完成！")
        print(f"  笔记: {result['note_path']}")
        print(f"  代码: {result['code_dir']}")
        print(f"  摘要: {result['summary_path']}")
    else:
        print(f"✗ 失败: {result.get('error')}")


def example_quick_summary():
    """示例 2: 快速获取论文摘要"""
    skill = PaperSkill()
    
    summary = skill.quick_summary("2301.12345")
    print("论文摘要:")
    print(summary)


def example_download_only():
    """示例 3: 仅下载论文"""
    skill = PaperSkill()
    
    paper_path = skill.download_paper("2301.12345")
    if paper_path:
        print(f"✓ 下载成功: {paper_path}")
    else:
        print("✗ 下载失败")


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Paper Reading Skill 使用示例")
    parser.add_argument("example", choices=["download_and_analyze", "quick_summary", "download_only"],
                       help="要运行的示例")
    
    args = parser.parse_args()
    
    if args.example == "download_and_analyze":
        example_download_and_analyze()
    elif args.example == "quick_summary":
        example_quick_summary()
    elif args.example == "download_only":
        example_download_only()
