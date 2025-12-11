"""
Code Analyzer - Analyzes code structure and entities
"""

import ast
import os
import re
from typing import Dict, List, Set, Tuple, Optional
from .utils import CodeEntity, CodeRelationship, LanguageType, FileNode


class CodeAnalyzer:
    """Analyzes code files and extracts entities"""

    def __init__(self):
        self.entities: Dict[str, CodeEntity] = {}
        self.relationships: List[CodeRelationship] = []
        self.stats = {}

    def analyze_python_file(self, file_path: str) -> List[CodeEntity]:
        """Analyze a Python file and extract entities"""
        entities = []
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            tree = ast.parse(content)
            
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    entity = CodeEntity(
                        name=node.name,
                        entity_type='function',
                        file_path=file_path,
                        line_number=node.lineno,
                        end_line=node.end_lineno or node.lineno,
                        language=LanguageType.PYTHON,
                        docstring=ast.get_docstring(node) or "",
                    )
                    entities.append(entity)
                    self.entities[f"{file_path}::{node.name}"] = entity
                
                elif isinstance(node, ast.ClassDef):
                    entity = CodeEntity(
                        name=node.name,
                        entity_type='class',
                        file_path=file_path,
                        line_number=node.lineno,
                        end_line=node.end_lineno or node.lineno,
                        language=LanguageType.PYTHON,
                        docstring=ast.get_docstring(node) or "",
                    )
                    entities.append(entity)
                    self.entities[f"{file_path}::{node.name}"] = entity
        except Exception as e:
            print(f"Error analyzing {file_path}: {e}")
        
        return entities

    def analyze_jac_file(self, file_path: str) -> List[CodeEntity]:
        """Analyze a JAC file and extract entities"""
        entities = []
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            # Simple regex-based parsing for JAC
            node_pattern = r'node\s+(\w+)'
            walker_pattern = r'walker\s+(\w+)'
            
            for match in re.finditer(node_pattern, content):
                entity = CodeEntity(
                    name=match.group(1),
                    entity_type='node',
                    file_path=file_path,
                    line_number=content[:match.start()].count('\n') + 1,
                    language=LanguageType.JAC,
                )
                entities.append(entity)
            
            for match in re.finditer(walker_pattern, content):
                entity = CodeEntity(
                    name=match.group(1),
                    entity_type='walker',
                    file_path=file_path,
                    line_number=content[:match.start()].count('\n') + 1,
                    language=LanguageType.JAC,
                )
                entities.append(entity)
        except Exception as e:
            print(f"Error analyzing {file_path}: {e}")
        
        return entities

    def analyze_directory(self, root_path: str) -> Dict[str, List[CodeEntity]]:
        """Analyze all code files in a directory"""
        results = {}
        for root, dirs, files in os.walk(root_path):
            # Skip ignored directories
            dirs[:] = [d for d in dirs if d not in {'__pycache__', '.git', 'node_modules', 'venv', '.venv'}]
            
            for file in files:
                file_path = os.path.join(root, file)
                if file.endswith('.py'):
                    results[file_path] = self.analyze_python_file(file_path)
                elif file.endswith('.jac'):
                    results[file_path] = self.analyze_jac_file(file_path)
        
        return results

    def analyze_repository(self, file_tree: Optional[FileNode]) -> Dict:
        """Analyze entire repository"""
        if not file_tree:
            return {}
        
        file_paths = self._collect_code_files(file_tree)
        all_entities = []
        
        for file_path in file_paths:
            if file_path.endswith('.py'):
                all_entities.extend(self.analyze_python_file(file_path))
            elif file_path.endswith('.jac'):
                all_entities.extend(self.analyze_jac_file(file_path))
        
        return {
            'entities': [e.to_dict() for e in all_entities],
            'entity_count': len(all_entities),
            'file_count': len(file_paths),
        }

    def _collect_code_files(self, node: Optional[FileNode]) -> List[str]:
        """Collect all code files from tree"""
        files = []
        if not node:
            return files
        
        if not node.is_dir and node.name.endswith(('.py', '.jac')):
            files.append(node.path)
        
        for child in node.children:
            files.extend(self._collect_code_files(child))
        
        return files

    def get_call_graph(self) -> Dict[str, List[str]]:
        """Build a simplified call graph"""
        return {}

    def get_ccg_stats(self) -> Dict:
        """Get Code Context Graph statistics"""
        return {
            'total_entities': len(self.entities),
            'total_relationships': len(self.relationships),
            'entity_types': {},
        }
