#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Paper Reading Framework CLI - Install skill to AI assistants
"""

import os
import shutil
import sys
from pathlib import Path
from typing import Dict, List, Optional


# AI Assistant configurations
AI_ASSISTANTS = {
    "claude": {
        "name": "Claude Code",
        "dirs": [".claude/skills/paper-reading"],
        "description": "Install for Claude Code (claude.ai/code)"
    },
    "cursor": {
        "name": "Cursor",
        "dirs": [".cursor/commands", ".shared/paper-reading"],
        "description": "Install for Cursor IDE"
    },
    "windsurf": {
        "name": "Windsurf",
        "dirs": [".windsurf/workflows", ".shared/paper-reading"],
        "description": "Install for Windsurf IDE"
    },
    "antigravity": {
        "name": "Antigravity",
        "dirs": [".agent/workflows", ".shared/paper-reading"],
        "description": "Install for Antigravity (.agent + .shared)"
    },
    "copilot": {
        "name": "GitHub Copilot",
        "dirs": [".github/prompts"],
        "description": "Install for GitHub Copilot"
    },
    "kiro": {
        "name": "Kiro",
        "dirs": [".kiro/steering", ".shared/paper-reading"],
        "description": "Install for Kiro"
    },
    "codex": {
        "name": "Codex",
        "dirs": [".codex/skills/paper-reading"],
        "description": "Install for Codex (Skills)"
    },
    "gemini": {
        "name": "Gemini CLI",
        "dirs": [".gemini/skills/paper-reading", ".shared/paper-reading"],
        "description": "Install for Gemini CLI"
    }
}


def get_package_root() -> Path:
    """Get the root directory of the installed package"""
    # Try to find the package installation location
    try:
        import paper_reading_framework
        package_path = Path(paper_reading_framework.__file__).parent.parent
        # Look for .claude directory in package root
        claude_dir = package_path / ".claude" / "skills" / "paper-reading"
        if claude_dir.exists():
            return package_path
    except ImportError:
        pass
    
    # Try to find in site-packages
    import site
    for site_packages in site.getsitepackages():
        package_path = Path(site_packages) / "paper_reading_framework"
        if package_path.exists():
            claude_dir = package_path / ".claude" / "skills" / "paper-reading"
            if claude_dir.exists():
                return package_path
    
    # Fallback: look for .claude in current directory or parent
    current = Path.cwd()
    for path in [current, current.parent, current.parent.parent]:
        claude_dir = path / ".claude" / "skills" / "paper-reading"
        if claude_dir.exists():
            return path
    
    # If not found, assume we're in the source directory
    return Path(__file__).parent.parent.parent


def get_skill_source_dir() -> Path:
    """Get the source directory of the skill"""
    package_root = get_package_root()
    skill_dir = package_root / ".claude" / "skills" / "paper-reading"
    
    if not skill_dir.exists():
        # Try alternative locations
        alt_locations = [
            package_root / "skills" / "paper_reading",
            package_root / "src" / "skills" / "paper_reading",
        ]
        for alt in alt_locations:
            if alt.exists():
                return alt
    
    return skill_dir


def copy_skill_files(source: Path, target: Path, assistant: str):
    """Copy skill files to target directory"""
    if not source.exists():
        print(f"Error: Source directory not found: {source}")
        return False
    
    target.mkdir(parents=True, exist_ok=True)
    
    # Copy SKILL.md or skill.md
    skill_md = source / "SKILL.md"
    if not skill_md.exists():
        skill_md = source / "skill.md"
    
    if skill_md.exists():
        target_skill_md = target / "SKILL.md"
        if assistant == "cursor":
            target_skill_md = target / "paper-reading.md"
        elif assistant == "windsurf":
            target_skill_md = target / "paper-reading.md"
        elif assistant == "antigravity":
            target_skill_md = target / "paper-reading.md"
        elif assistant == "copilot":
            target_skill_md = target / "paper-reading.prompt.md"
        elif assistant == "kiro":
            target_skill_md = target / "paper-reading.md"
        
        shutil.copy2(skill_md, target_skill_md)
        print(f"  ✓ Copied {skill_md.name} to {target_skill_md}")
    
    # Copy scripts directory
    scripts_dir = source / "scripts"
    if scripts_dir.exists():
        target_scripts = target / "scripts"
        if target_scripts.exists():
            shutil.rmtree(target_scripts)
        shutil.copytree(scripts_dir, target_scripts)
        print(f"  ✓ Copied scripts/ directory")
    
    return True


def install_to_assistant(assistant: str, project_dir: Optional[Path] = None) -> bool:
    """Install skill to a specific AI assistant"""
    if assistant not in AI_ASSISTANTS:
        print(f"Error: Unknown assistant '{assistant}'")
        print(f"Available assistants: {', '.join(AI_ASSISTANTS.keys())}")
        return False
    
    if project_dir is None:
        project_dir = Path.cwd()
    else:
        project_dir = Path(project_dir)
    
    if not project_dir.exists():
        print(f"Error: Project directory not found: {project_dir}")
        return False
    
    config = AI_ASSISTANTS[assistant]
    source_dir = get_skill_source_dir()
    
    print(f"\nInstalling paper-reading skill for {config['name']}...")
    print(f"Project directory: {project_dir}")
    print(f"Source directory: {source_dir}")
    
    success = True
    for target_dir_rel in config["dirs"]:
        target_dir = project_dir / target_dir_rel
        target_dir.parent.mkdir(parents=True, exist_ok=True)
        
        if not copy_skill_files(source_dir, target_dir, assistant):
            success = False
    
    if success:
        print(f"\n✓ Successfully installed paper-reading skill for {config['name']}!")
        print(f"  You can now use the skill in {config['name']}.")
    else:
        print(f"\n✗ Installation failed for {config['name']}.")
    
    return success


def install_all(project_dir: Optional[Path] = None) -> bool:
    """Install skill to all AI assistants"""
    if project_dir is None:
        project_dir = Path.cwd()
    else:
        project_dir = Path(project_dir)
    
    print("Installing paper-reading skill to all AI assistants...")
    print(f"Project directory: {project_dir}\n")
    
    results = {}
    for assistant in AI_ASSISTANTS.keys():
        results[assistant] = install_to_assistant(assistant, project_dir)
        print()
    
    success_count = sum(1 for v in results.values() if v)
    total_count = len(results)
    
    print("=" * 60)
    print(f"Installation complete: {success_count}/{total_count} assistants")
    
    return success_count == total_count


def list_assistants():
    """List all available AI assistants"""
    print("Available AI assistants:\n")
    for key, config in AI_ASSISTANTS.items():
        print(f"  {key:15} - {config['description']}")


def main():
    """CLI entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Paper Reading Framework - Install skill to AI assistants",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  paper-reading init --ai claude      # Install for Claude Code
  paper-reading init --ai cursor      # Install for Cursor
  paper-reading init --ai all         # Install for all assistants
  paper-reading list                  # List available assistants
        """
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Command to run")
    
    # init command
    init_parser = subparsers.add_parser("init", help="Install skill to AI assistant")
    init_parser.add_argument(
        "--ai",
        choices=list(AI_ASSISTANTS.keys()) + ["all"],
        required=True,
        help="AI assistant to install for"
    )
    init_parser.add_argument(
        "--dir",
        type=str,
        help="Project directory (default: current directory)"
    )
    
    # list command
    list_parser = subparsers.add_parser("list", help="List available AI assistants")
    
    args = parser.parse_args()
    
    if args.command == "list":
        list_assistants()
    elif args.command == "init":
        project_dir = Path(args.dir) if args.dir else None
        if args.ai == "all":
            success = install_all(project_dir)
            sys.exit(0 if success else 1)
        else:
            success = install_to_assistant(args.ai, project_dir)
            sys.exit(0 if success else 1)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
