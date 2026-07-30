"""
快速开始脚本
用于测试 SIGGRAPH 信息获取功能
"""

import sys
from pathlib import Path

# 添加项目根目录到路径
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from src.paper.fetcher import PaperFetcher


def main():
    """快速测试 SIGGRAPH 信息获取"""
    print("=" * 60)
    print("论文阅读试验田 - 快速开始")
    print("=" * 60)
    print("\n正在获取 SIGGRAPH 网站信息...\n")
    
    try:
        fetcher = PaperFetcher()
        info = fetcher.fetch_siggraph_info()
        
        if "error" in info:
            print(f"❌ 错误: {info.get('error', 'Unknown error')}")
            print(f"   提示: {info.get('message', '')}")
            return
        
        print("✅ 成功获取 SIGGRAPH 信息！\n")
        print(f"网站标题: {info.get('title', 'N/A')}\n")
        
        # 显示最新新闻
        news_list = info.get('latest_news', [])
        if news_list:
            print(f"📰 最新新闻 ({len(news_list)} 条):")
            for i, news in enumerate(news_list[:5], 1):
                print(f"   {i}. {news.get('title', 'N/A')}")
            print()
        
        # 显示会议信息
        conf_list = info.get('conferences', [])
        if conf_list:
            print(f"🎯 会议信息 ({len(conf_list)} 条):")
            for i, conf in enumerate(conf_list[:5], 1):
                print(f"   {i}. {conf.get('title', 'N/A')}")
            print()
        
        # 显示论文链接
        papers_list = info.get('papers_links', [])
        if papers_list:
            print(f"📚 论文相关链接 ({len(papers_list)} 条):")
            for i, link in enumerate(papers_list[:10], 1):
                print(f"   {i}. {link.get('text', 'N/A')}")
                print(f"      URL: {link.get('url', 'N/A')}")
            print()
        
        print("=" * 60)
        print("下一步:")
        print("1. 配置 MOONSHOT_API_KEY (在 .env 文件中)")
        print("2. 运行: python src/main.py full <论文路径>")
        print("=" * 60)
        
    except Exception as e:
        print(f"❌ 发生错误: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
