"""Setup standard skill directory structure"""
import sys
from pathlib import Path
import shutil

# 添加项目根目录到路径
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

# Create directory structure
base_dir = project_root / "skills/paper_reading"
dirs = [
    base_dir / "data" / "input_data",
    base_dir / "data" / "output_data",
    base_dir / "scripts",
]

for dir_path in dirs:
    dir_path.mkdir(parents=True, exist_ok=True)
    print(f"Created: {dir_path}")

print("\nDirectory structure created successfully!")
