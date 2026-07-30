"""Re-download the paper"""
import sys
from pathlib import Path

# 添加项目根目录到路径
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from src.paper.fetcher import PaperFetcher

# Delete old file if exists
old_file = project_root / "papers/2301.12345.pdf"
if old_file.exists():
    old_file.unlink()
    print(f"Deleted old file: {old_file}")

# Re-download
fetcher = PaperFetcher()
filepath = fetcher.download_arxiv_paper("2301.12345")
if filepath:
    print(f"Successfully downloaded: {filepath}")
    print(f"File size: {filepath.stat().st_size} bytes")
else:
    print("Download failed")
