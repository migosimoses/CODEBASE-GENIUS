"""
Utility functions and data structures for Codebase Genius
"""

import os
from dataclasses import dataclass, field
from enum import Enum
from typing import List, Dict, Any, Optional


class LanguageType(Enum):
    """Supported programming languages"""
    PYTHON = "python"
    JAC = "jac"
    JAVASCRIPT = "javascript"
    TYPESCRIPT = "typescript"
    JAVA = "java"
    GO = "go"
    RUST = "rust"
    CPP = "cpp"
    UNKNOWN = "unknown"


@dataclass
class FileNode:
    """Represents a file in the repository"""
    path: str
    name: str
    is_dir: bool
    language: LanguageType = LanguageType.UNKNOWN
    size: int = 0
    depth: int = 0
    children: List['FileNode'] = field(default_factory=list)
    parent: Optional['FileNode'] = None

    def add_child(self, child: 'FileNode') -> None:
        """Add a child node"""
        child.parent = self
        self.children.append(child)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            'path': self.path,
            'name': self.name,
            'is_dir': self.is_dir,
            'language': self.language.value if isinstance(self.language, LanguageType) else self.language,
            'size': self.size,
            'depth': self.depth,
            'children': [c.to_dict() for c in self.children],
        }


@dataclass
class CodeEntity:
    """Represents a code entity (function, class, method, etc.)"""
    name: str
    entity_type: str  # 'function', 'class', 'method', 'variable', etc.
    file_path: str
    line_number: int
    end_line: int = 0
    language: LanguageType = LanguageType.UNKNOWN
    docstring: str = ""
    signature: str = ""
    modifiers: List[str] = field(default_factory=list)
    parent_entity: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            'name': self.name,
            'type': self.entity_type,
            'file_path': self.file_path,
            'line_number': self.line_number,
            'end_line': self.end_line,
            'language': self.language.value if isinstance(self.language, LanguageType) else self.language,
            'docstring': self.docstring,
            'signature': self.signature,
            'modifiers': self.modifiers,
            'parent_entity': self.parent_entity,
        }


@dataclass
class CodeRelationship:
    """Represents a relationship between code entities"""
    source_entity: str
    target_entity: str
    relationship_type: str  # 'calls', 'extends', 'implements', 'imports', etc.
    source_file: str
    target_file: str
    line_number: int = 0

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            'source_entity': self.source_entity,
            'target_entity': self.target_entity,
            'relationship_type': self.relationship_type,
            'source_file': self.source_file,
            'target_file': self.target_file,
            'line_number': self.line_number,
        }


def get_language_from_extension(filename: str) -> LanguageType:
    """Determine language from file extension"""
    ext_map = {
        '.py': LanguageType.PYTHON,
        '.jac': LanguageType.JAC,
        '.js': LanguageType.JAVASCRIPT,
        '.ts': LanguageType.TYPESCRIPT,
        '.java': LanguageType.JAVA,
        '.go': LanguageType.GO,
        '.rs': LanguageType.RUST,
        '.cpp': LanguageType.CPP,
        '.cc': LanguageType.CPP,
        '.h': LanguageType.CPP,
    }
    _, ext = os.path.splitext(filename)
    return ext_map.get(ext.lower(), LanguageType.UNKNOWN)


def should_ignore(path: str) -> bool:
    """Check if path should be ignored"""
    ignore_patterns = {
        '__pycache__', '.git', '.venv', 'venv', 'node_modules',
        '.pytest_cache', '.egg-info', 'dist', 'build',
        '.mypy_cache', '.tox', '.coverage',
    }
    for part in path.split(os.sep):
        if part in ignore_patterns:
            return True
    return False


def build_file_tree(root_path: str, max_depth: int = 10, current_depth: int = 0) -> Optional[FileNode]:
    """Build a tree of files and directories"""
    if current_depth > max_depth or should_ignore(root_path):
        return None

    try:
        name = os.path.basename(root_path) or root_path
        is_dir = os.path.isdir(root_path)
        size = 0

        node = FileNode(
            path=root_path,
            name=name,
            is_dir=is_dir,
            language=LanguageType.UNKNOWN if is_dir else get_language_from_extension(name),
            size=size,
            depth=current_depth,
        )

        if is_dir:
            try:
                for item in os.listdir(root_path):
                    item_path = os.path.join(root_path, item)
                    child = build_file_tree(item_path, max_depth, current_depth + 1)
                    if child:
                        node.add_child(child)
            except PermissionError:
                pass
        else:
            try:
                size = os.path.getsize(root_path)
                node.size = size
            except (OSError, IOError):
                pass

        return node
    except Exception:
        return None


def count_entities_in_tree(node: Optional[FileNode], language: Optional[LanguageType] = None) -> int:
    """Count entities in file tree"""
    if not node:
        return 0
    
    count = 0
    if not node.is_dir and (language is None or node.language == language):
        count = 1
    
    for child in node.children:
        count += count_entities_in_tree(child, language)
    
    return count


def get_file_list_by_language(node: Optional[FileNode], language: LanguageType) -> List[str]:
    """Get all files of a specific language"""
    if not node:
        return []
    
    files = []
    if not node.is_dir and node.language == language:
        files.append(node.path)
    
    for child in node.children:
        files.extend(get_file_list_by_language(child, language))
    
    return files
