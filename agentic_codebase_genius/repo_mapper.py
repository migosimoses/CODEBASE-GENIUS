"""
Repository Mapper - Clones and analyzes repository structure
"""

import os
import tempfile
import subprocess
from typing import Dict, List, Optional, Tuple
try:
    from utils import FileNode, build_file_tree, LanguageType
except ImportError:
    from .utils import FileNode, build_file_tree, LanguageType


class RepoMapper:
    """Maps and analyzes repository structure"""

    def __init__(self):
        self.temp_dir = None
        self.repo_path = None
        self.file_tree = None

    def clone_repository(self, repo_url: str) -> Tuple[bool, str]:
        """Clone a Git repository"""
        try:
            self.temp_dir = tempfile.mkdtemp(prefix="codebase_genius_")
            result = subprocess.run(
                ["git", "clone", "--depth", "1", repo_url, self.temp_dir],
                capture_output=True,
                text=True,
                timeout=60,
            )
            if result.returncode == 0:
                self.repo_path = self.temp_dir
                return True, self.temp_dir
            else:
                return False, f"Git clone failed: {result.stderr}"
        except Exception as e:
            return False, f"Clone error: {str(e)}"

    def build_tree(self) -> Optional[FileNode]:
        """Build file tree from repository"""
        if not self.repo_path:
            return None
        self.file_tree = build_file_tree(self.repo_path, max_depth=10)
        return self.file_tree

    def read_readme(self) -> Optional[str]:
        """Read README file from repository"""
        if not self.repo_path:
            return None
        
        readme_names = ["README.md", "README.txt", "README"]
        for name in readme_names:
            path = os.path.join(self.repo_path, name)
            if os.path.isfile(path):
                try:
                    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                        return f.read()
                except Exception:
                    pass
        return None

    def summarize_readme(self, readme_content: Optional[str]) -> str:
        """Summarize README content"""
        if not readme_content:
            return "No README found."
        
        lines = readme_content.split('\n')[:20]
        summary = '\n'.join(lines)
        if len(readme_content.split('\n')) > 20:
            summary += "\n... (truncated)"
        return summary

    def identify_entry_points(self) -> List[str]:
        """Identify main entry points"""
        entry_points = []
        if not self.repo_path:
            return entry_points
        
        common_entry_files = ["main.py", "index.js", "app.py", "server.py", "start.js"]
        for root, dirs, files in os.walk(self.repo_path):
            for file in files:
                if file in common_entry_files:
                    entry_points.append(os.path.join(root, file))
        
        return entry_points[:5]

    def identify_primary_language(self) -> LanguageType:
        """Identify primary programming language"""
        if not self.file_tree:
            return LanguageType.UNKNOWN
        
        lang_counts = {}
        self._count_languages(self.file_tree, lang_counts)
        
        if not lang_counts:
            return LanguageType.UNKNOWN
        
        most_common = max(lang_counts.items(), key=lambda x: x[1])
        return most_common[0]

    def _count_languages(self, node: Optional[FileNode], counts: Dict) -> None:
        """Recursively count language files"""
        if not node:
            return
        
        if not node.is_dir and node.language != LanguageType.UNKNOWN:
            counts[node.language] = counts.get(node.language, 0) + 1
        
        for child in node.children:
            self._count_languages(child, counts)

    def get_repository_summary(self) -> Dict:
        """Get complete repository summary"""
        return {
            'repo_path': self.repo_path,
            'primary_language': self.identify_primary_language().value,
            'entry_points': self.identify_entry_points(),
            'readme': self.summarize_readme(self.read_readme()),
            'file_tree': self.file_tree.to_dict() if self.file_tree else None,
        }

    def cleanup(self) -> None:
        """Clean up temporary files"""
        if self.temp_dir and os.path.exists(self.temp_dir):
            import shutil
            try:
                shutil.rmtree(self.temp_dir)
            except Exception:
                pass
