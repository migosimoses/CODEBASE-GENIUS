"""
Codebase Genius - Multi-agent code documentation system
"""

__version__ = "0.1.0"

# Avoid importing heavy submodules at package import time to prevent
# circular import issues when running the package as a module.
# Import the concrete implementations directly when needed, for example:
# from agentic_codebase_genius.supervisor import CodeGeniusSupervisor
# from agentic_codebase_genius.api import create_supervisor, process_repository

__all__ = [
    "FileNode",
    "CodeEntity",
    "CodeRelationship",
    "LanguageType",
    "CodeGeniusSupervisor",
    "create_supervisor",
    "process_repository",
    "get_documentation",
    "list_generated_docs",
]
