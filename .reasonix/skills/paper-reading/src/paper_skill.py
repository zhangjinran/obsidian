"""
Paper Reading Skill - 论文阅读技能
为 Cursor 等 AI IDE 提供统一的论文下载和分析接口
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Optional, Dict, Any

# 添加项目根目录到路径（从 skill 目录向上两级）
skill_dir = Path(__file__).parent.parent.parent
sys.path.insert(0, str(skill_dir))

from src.paper.fetcher import PaperFetcher
from src.paper.parser import PaperParser
from src.api.moonshot_client import MoonshotClient
from src.knowledge.internalizer import KnowledgeInternalizer
from src.implementation.code_generator import CodeGenerator
from src.reading.glossary_extractor import GlossaryExtractor, GlossaryExplainer
from src.reading.guide_generator import GuideGenerator


class PaperSkill:
    """论文阅读技能 - 统一的 API 接口"""
    
    def __init__(self, config_path: Optional[str] = None):
        """初始化技能
        
        Args:
            config_path: 配置文件路径（默认: 项目根目录的 config.yaml）
        """
        if config_path is None:
            config_path = str(skill_dir / "config.yaml")
        
        self.config_path = config_path
        self.fetcher = PaperFetcher(config_path=config_path)
        self.parser = PaperParser()
        self.client = MoonshotClient(config_path=config_path)
        self.internalizer = KnowledgeInternalizer(config_path=config_path)
        self.code_generator = CodeGenerator(config_path=config_path)
    
    def download_and_analyze(self, arxiv_id: str) -> Dict[str, Any]:
        """
        下载论文并运行完整分析（一键操作）
        
        Args:
            arxiv_id: arXiv ID 或 URL（如 "2301.12345" 或 "https://arxiv.org/abs/2301.12345"）
        
        Returns:
            包含所有生成文件路径的字典
        """
        print(f"开始处理论文: {arxiv_id}")
        print("=" * 60)
        
        # 1. 下载论文
        print("\n[1/5] 下载论文...")
        paper_path = self.fetcher.download_arxiv_paper(arxiv_id)
        if not paper_path:
            return {"error": "论文下载失败"}
        
        print(f"论文已下载: {paper_path}")
        
        # 2. 解析论文
        print("\n[2/5] 解析论文...")
        paper_info = self.parser.parse_paper(str(paper_path))
        if not paper_info:
            return {"error": "论文解析失败"}
        
        paper_id = paper_info.get("paper_id") or Path(paper_path).parent.name
        print(f"论文标题: {paper_info.get('title', 'Unknown')}")
        print(f"论文 ID: {paper_id}")
        
        # 3. AI 分析
        print("\n[3/5] AI 深度分析...")
        analysis = self.client.analyze_paper(paper_info, analysis_type="full")
        key_points = self.client.extract_key_points(paper_info)
        implementation_guide = self.client.generate_implementation_guide(paper_info)
        
        # 4. 辅助阅读（如果启用）
        print("\n[4/5] 生成辅助阅读材料...")
        reading_guide = None
        try:
            glossary_extractor = GlossaryExtractor()
            terms = glossary_extractor.extract_terms(paper_info.get("text", ""))
            
            if terms:
                explainer = GlossaryExplainer(self.client)
                explained_terms = explainer.explain_terms(terms[:20], paper_info)
                
                guide_generator = GuideGenerator(self.client)
                reading_guide = guide_generator.generate_guide(paper_info, explained_terms)
        except Exception as e:
            print(f"辅助阅读生成失败（可忽略）: {e}")
        
        # 5. 知识内化
        print("\n[5/5] 知识内化...")
        note_path = self.internalizer.create_note(paper_info, analysis, key_points, paper_id=paper_id)
        summary_path = self.internalizer.create_summary(paper_info, analysis, paper_id=paper_id)
        self.internalizer.update_knowledge_graph(paper_info, key_points, paper_id=paper_id)
        
        # 6. 代码生成
        print("\n[6/6] 生成代码项目...")
        code_dir = self.code_generator.create_project_structure(
            paper_info.get("title", "Unknown"),
            implementation_guide,
            language="python",
            paper_id=paper_id
        )
        self.code_generator.save_implementation_guide(code_dir, implementation_guide, paper_id=paper_id)
        
        # 返回结果
        result = {
            "success": True,
            "paper_id": paper_id,
            "paper_path": str(paper_path),
            "note_path": str(note_path) if note_path else None,
            "summary_path": str(summary_path) if summary_path else None,
            "code_dir": str(code_dir) if code_dir else None,
            "reading_guide_path": str(reading_guide) if reading_guide else None,
            "knowledge_graph_path": str(self.internalizer.knowledge_dir / "knowledge_graph.json"),
        }
        
        print("\n" + "=" * 60)
        print("处理完成！")
        print("=" * 60)
        print(f"笔记: {result['note_path']}")
        print(f"摘要: {result['summary_path']}")
        print(f"代码: {result['code_dir']}")
        if result['reading_guide_path']:
            print(f"阅读指南: {result['reading_guide_path']}")
        
        return result
    
    def download_paper(self, arxiv_id: str) -> Optional[Path]:
        """
        仅下载论文
        
        Args:
            arxiv_id: arXiv ID 或 URL
        
        Returns:
            下载的文件路径
        """
        return self.fetcher.download_arxiv_paper(arxiv_id)
    
    def analyze_paper(self, paper_path: str, analysis_type: str = "full") -> Dict[str, Any]:
        """
        分析已有论文
        
        Args:
            paper_path: 论文文件路径
            analysis_type: 分析类型 ("full", "summary", "innovation", "implementation")
        
        Returns:
            分析结果
        """
        paper_info = self.parser.parse_paper(paper_path)
        if not paper_info:
            return {"error": "论文解析失败"}
        
        if analysis_type == "full":
            analysis = self.client.analyze_paper(paper_info, analysis_type="full")
            key_points = self.client.extract_key_points(paper_info)
            implementation_guide = self.client.generate_implementation_guide(paper_info)
            return {
                "analysis": analysis,
                "key_points": key_points,
                "implementation_guide": implementation_guide,
            }
        else:
            analysis = self.client.analyze_paper(paper_info, analysis_type=analysis_type)
            return {"analysis": analysis}
    
    def quick_summary(self, arxiv_id: str) -> str:
        """
        快速获取论文摘要（不下载，仅分析）
        
        Args:
            arxiv_id: arXiv ID
        
        Returns:
            论文摘要文本
        """
        # 先下载
        paper_path = self.download_paper(arxiv_id)
        if not paper_path:
            return "下载失败"
        
        # 解析和分析
        paper_info = self.parser.parse_paper(str(paper_path))
        if not paper_info:
            return "解析失败"
        
        analysis = self.client.analyze_paper(paper_info, analysis_type="summary")
        return analysis.get("summary", "无法生成摘要")


def main():
    """命令行入口"""
    import argparse
    
    parser = argparse.ArgumentParser(description="论文阅读技能 - 快速下载和分析论文")
    parser.add_argument("arxiv_id", help="arXiv ID 或 URL")
    parser.add_argument("--action", choices=["download", "analyze", "full"], 
                       default="full", help="操作类型 (默认: full)")
    parser.add_argument("--type", choices=["summary", "innovation", "implementation"],
                       help="分析类型（仅用于 analyze 操作）")
    
    args = parser.parse_args()
    
    skill = PaperSkill()
    
    if args.action == "download":
        result = skill.download_paper(args.arxiv_id)
        if result:
            print(f"下载成功: {result}")
        else:
            print("下载失败")
    elif args.action == "analyze":
        # 需要先下载
        paper_path = skill.download_paper(args.arxiv_id)
        if not paper_path:
            print("下载失败")
            return
        result = skill.analyze_paper(str(paper_path), args.type or "summary")
        print(result)
    else:  # full
        result = skill.download_and_analyze(args.arxiv_id)
        if result.get("error"):
            print(f"错误: {result['error']}")
        else:
            print("\n处理成功！")


if __name__ == "__main__":
    main()
