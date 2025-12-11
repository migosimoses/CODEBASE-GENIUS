"""
API module - Main entry point for the system
"""

from typing import Tuple, Optional, List
from .supervisor import CodeGeniusSupervisor

# Global supervisor instance
_supervisor: Optional[CodeGeniusSupervisor] = None


def create_supervisor(output_dir: str = "./docs") -> CodeGeniusSupervisor:
    """Create a new supervisor instance"""
    global _supervisor
    _supervisor = CodeGeniusSupervisor(output_dir)
    return _supervisor


def process_repository(repo_url: str, output_dir: str = "./docs") -> Tuple[bool, str, Optional[str]]:
    """Process a repository and generate documentation"""
    global _supervisor
    if not _supervisor:
        _supervisor = create_supervisor(output_dir)
    
    return _supervisor.process_repository(repo_url)


def get_documentation() -> Optional[str]:
    """Get the current documentation"""
    global _supervisor
    if not _supervisor:
        return None
    return _supervisor.get_documentation()


def list_generated_docs(output_dir: str = "./docs") -> List[str]:
    """List all generated documentation files"""
    global _supervisor
    if not _supervisor:
        _supervisor = create_supervisor(output_dir)
    return _supervisor.list_generated_docs()
