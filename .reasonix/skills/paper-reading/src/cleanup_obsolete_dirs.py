"""
清理废弃的目录结构
删除 data/ 下已废弃的空目录
"""

import sys
from pathlib import Path

# 添加项目根目录到路径
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

def cleanup_obsolete_dirs():
    """清理废弃的空目录"""
    
    # 要删除的废弃目录（相对于项目根目录）
    project_root = Path(__file__).parent.parent.parent
    obsolete_dirs = [
        project_root / "data/notes",
        project_root / "data/code",
        project_root / "data/summaries",
        project_root / "data/guides",
        # project_root / "data/knowledge",  # 可选：如果不需要全局知识图谱，取消注释
    ]
    
    print("=" * 60)
    print("清理废弃目录")
    print("=" * 60)
    
    deleted_count = 0
    skipped_count = 0
    
    for dir_path in obsolete_dirs:
        path = Path(dir_path) if not isinstance(dir_path, Path) else dir_path
        
        if not path.exists():
            print(f"[跳过] 目录不存在: {dir_path}")
            skipped_count += 1
            continue
        
        # 检查目录是否为空
        if any(path.iterdir()):
            print(f"[跳过] 目录不为空: {dir_path}")
            skipped_count += 1
            continue
        
        # 删除空目录
        try:
            path.rmdir()
            print(f"[删除] {dir_path}")
            deleted_count += 1
        except Exception as e:
            print(f"[错误] 无法删除 {dir_path}: {e}")
    
    print("=" * 60)
    print(f"完成: 删除 {deleted_count} 个目录，跳过 {skipped_count} 个目录")
    print("=" * 60)


if __name__ == "__main__":
    import sys
    
    print("此脚本将删除以下废弃的空目录：")
    print("  - data/notes/")
    print("  - data/code/")
    print("  - data/summaries/")
    print("  - data/guides/")
    print()
    
    if len(sys.argv) > 1 and sys.argv[1] == "--yes":
        cleanup_obsolete_dirs()
    else:
        print("这是预览模式，不会实际删除目录。")
        print("要实际执行删除，请运行: python cleanup_obsolete_dirs.py --yes")
        print()
        cleanup_obsolete_dirs()
