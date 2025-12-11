"""
Supervisor - Orchestrates the documentation pipeline
"""

import os
import tempfile
from typing import Dict, Tuple, Optional
from .repo_mapper import RepoMapper
from .code_analyzer import CodeAnalyzer
from .doc_genie import DocGenie


class CodeGeniusSupervisor:
    """Orchestrates the entire documentation generation workflow"""

    def __init__(self, output_dir: str = "./docs"):
        self.output_dir = output_dir
        self.repo_mapper = RepoMapper()
        self.code_analyzer = CodeAnalyzer()
        self.doc_genie = DocGenie()
        self.current_doc = None

    def process_repository(self, repo_url: str) -> Tuple[bool, str, Optional[str]]:
        """Process a repository end-to-end"""
        try:
            # Stage 1: Clone and map
            success, result = self.repo_mapper.clone_repository(repo_url)
            if not success:
                return False, f"Failed to clone repository: {result}", None
            
            # Build file tree
            file_tree = self.repo_mapper.build_tree()
            repo_summary = self.repo_mapper.get_repository_summary()
            
            # Stage 2: Analyze code
            analysis_result = self.code_analyzer.analyze_repository(file_tree)
            
            # Stage 3: Generate documentation
            combined_data = {**repo_summary, **analysis_result}
            combined_data['repo_name'] = repo_url.split('/')[-1].replace('.git', '')
            
            doc_content = self.doc_genie.generate_documentation(combined_data)
            
            # Stage 4: Save output
            os.makedirs(self.output_dir, exist_ok=True)
            repo_name = combined_data['repo_name']
            output_file = os.path.join(self.output_dir, f"{repo_name}_documentation.md")
            
            if self.doc_genie.save_documentation(output_file):
                self.current_doc = output_file
                return True, "Documentation generated successfully", output_file
            else:
                return False, "Failed to save documentation", None
        
        except Exception as e:
            return False, f"Error processing repository: {str(e)}", None
        finally:
            self.repo_mapper.cleanup()

    def get_documentation(self) -> Optional[str]:
        """Get current documentation content"""
        if self.current_doc and os.path.exists(self.current_doc):
            try:
                with open(self.current_doc, 'r', encoding='utf-8') as f:
                    return f.read()
            except Exception:
                return None
        return None

    def list_generated_docs(self) -> list:
        """List all generated documentation files"""
        if os.path.exists(self.output_dir):
            return [f for f in os.listdir(self.output_dir) if f.endswith('_documentation.md')]
        return []
