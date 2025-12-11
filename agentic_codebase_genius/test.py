"""
Test suite for Codebase Genius
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from utils import FileNode, LanguageType, build_file_tree
from repo_mapper import RepoMapper
from code_analyzer import CodeAnalyzer
from doc_genie import DocGenie
from supervisor import CodeGeniusSupervisor


def test_file_tree():
    """Test file tree building"""
    print("Testing file tree building...")
    tree = build_file_tree(os.getcwd(), max_depth=2)
    assert tree is not None
    print(f"✓ File tree created: {tree.name}")


def test_code_analyzer():
    """Test code analyzer"""
    print("Testing code analyzer...")
    analyzer = CodeAnalyzer()
    current_file = __file__
    entities = analyzer.analyze_python_file(current_file)
    print(f"✓ Analyzer found {len(entities)} entities in test file")


def test_doc_genie():
    """Test documentation generation"""
    print("Testing documentation generation...")
    genie = DocGenie()
    test_data = {
        'repo_name': 'test_repo',
        'primary_language': 'python',
        'readme': 'This is a test repository',
        'entities': [
            {'name': 'test_func', 'type': 'function', 'line_number': 10}
        ],
        'entity_count': 1,
        'file_count': 5,
    }
    doc = genie.generate_documentation(test_data)
    assert len(doc) > 0
    print(f"✓ Generated documentation ({len(doc)} chars)")


def test_supervisor():
    """Test supervisor initialization"""
    print("Testing supervisor...")
    supervisor = CodeGeniusSupervisor()
    print("✓ Supervisor initialized")


def main():
    """Run all tests"""
    print("=" * 50)
    print("Codebase Genius Test Suite")
    print("=" * 50)
    
    try:
        test_file_tree()
        test_code_analyzer()
        test_doc_genie()
        test_supervisor()
        print("\n✅ All tests passed!")
        return 0
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
