"""
Doc Genie - Generates documentation from code analysis
"""

from typing import Dict, Optional, List
from datetime import datetime


class DocGenie:
    """Generates markdown documentation"""

    def __init__(self):
        self.doc_content = ""

    def generate_documentation(self, analysis_data: Dict) -> str:
        """Generate complete documentation"""
        doc_sections = []
        
        doc_sections.append(self._generate_header(analysis_data))
        doc_sections.append(self._generate_overview(analysis_data))
        doc_sections.append(self._generate_structure_section(analysis_data))
        doc_sections.append(self._generate_key_entities(analysis_data))
        doc_sections.append(self._generate_statistics(analysis_data))
        
        self.doc_content = '\n\n'.join(doc_sections)
        return self.doc_content

    def _generate_header(self, data: Dict) -> str:
        """Generate documentation header"""
        repo_name = data.get('repo_name', 'Repository')
        return f"# {repo_name} Documentation\n\nGenerated: {datetime.now().isoformat()}"

    def _generate_overview(self, data: Dict) -> str:
        """Generate overview section"""
        readme = data.get('readme', 'No README available.')
        primary_lang = data.get('primary_language', 'Unknown')
        return f"## Overview\n\nPrimary Language: **{primary_lang}**\n\n### README\n{readme}"

    def _generate_structure_section(self, data: Dict) -> str:
        """Generate project structure section"""
        return "## Project Structure\n\n```\nRepository structure diagram here\n```"

    def _generate_key_entities(self, data: Dict) -> str:
        """Generate key entities section"""
        entities = data.get('entities', [])
        if not entities:
            return "## Key Entities\n\nNo entities found."
        
        content = "## Key Entities\n\n"
        for entity in entities[:10]:  # Limit to 10
            content += f"- **{entity.get('name', 'Unknown')}** ({entity.get('type', 'unknown')}) - Line {entity.get('line_number', '?')}\n"
        
        return content

    def _generate_statistics(self, data: Dict) -> str:
        """Generate statistics section"""
        entity_count = data.get('entity_count', 0)
        file_count = data.get('file_count', 0)
        
        return f"""## Statistics

- **Total Files**: {file_count}
- **Total Entities**: {entity_count}
- **Last Updated**: {datetime.now().isoformat()}
"""

    def save_documentation(self, file_path: str) -> bool:
        """Save documentation to file"""
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(self.doc_content)
            return True
        except Exception as e:
            print(f"Error saving documentation: {e}")
            return False
