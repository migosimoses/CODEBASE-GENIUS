# How to Run Codebase Genius

## Quick Start (5 minutes)

### 1. **Verify Installation**
```bash
cd "/mnt/c/Users/admin/Desktop/CODEBASE GENIUS"
source jac-env/bin/activate

# Test imports
python -c "
import sys
sys.path.insert(0, 'agentic_codebase_genius')
from utils import FileNode, LanguageType
from api import process_repository
print('✅ System ready!')
"
```

---

## Option A: Process a Repository (Python API)

### Step 1: Activate Environment
```bash
cd "/mnt/c/Users/admin/Desktop/CODEBASE GENIUS"
source jac-env/bin/activate
```

### Step 2: Run Processing
```bash
python << 'PYEOF'
import sys
sys.path.insert(0, 'agentic_codebase_genius')
from api import process_repository
import os

# Process a repository
repo_url = "https://github.com/torvalds/linux.git"  # Or any other repo
print(f"\n📦 Processing: {repo_url}\n")

success, message, doc_path = process_repository(repo_url, "./docs")

print(f"\n{'✅ SUCCESS' if success else '❌ FAILED'}")
print(f"Message: {message}")
if doc_path:
    print(f"Document: {doc_path}")
    
    # Display generated documentation
    if os.path.exists(doc_path):
        print(f"\n{'='*60}")
        with open(doc_path, 'r') as f:
            print(f.read()[:1000])  # First 1000 chars
        print(f"{'='*60}\n")
PYEOF
```

**Alternative - Simple one-liner:**
```bash
python -c "
import sys
sys.path.insert(0, 'agentic_codebase_genius')
from api import process_repository
success, msg, path = process_repository('https://github.com/user/repo.git')
print(f'Status: {success}\nMessage: {msg}\nPath: {path}')
"
```

---

## Option B: Run Test Suite

### Basic Tests
```bash
cd "/mnt/c/Users/admin/Desktop/CODEBASE GENIUS"
source jac-env/bin/activate
python -c "
import sys
sys.path.insert(0, 'agentic_codebase_genius')

print('Testing Codebase Genius...\n')

# Test 1: FileNode
from utils import FileNode, LanguageType
node = FileNode('test.py', 'test.py', False, LanguageType.PYTHON)
print(f'✓ FileNode: {node.name}')

# Test 2: CodeEntity
from utils import CodeEntity
entity = CodeEntity('test_func', 'function', 'test.py', 10)
print(f'✓ CodeEntity: {entity.name}')

# Test 3: RepoMapper
from repo_mapper import RepoMapper
mapper = RepoMapper()
print(f'✓ RepoMapper initialized')

# Test 4: CodeAnalyzer
from code_analyzer import CodeAnalyzer
analyzer = CodeAnalyzer()
print(f'✓ CodeAnalyzer initialized')

# Test 5: DocGenie
from doc_genie import DocGenie
genie = DocGenie()
doc = genie.generate_documentation({
    'repo_name': 'test',
    'primary_language': 'python',
    'entity_count': 5,
    'file_count': 10
})
print(f'✓ DocGenie: Generated {len(doc)} chars')

# Test 6: Supervisor
from supervisor import CodeGeniusSupervisor
supervisor = CodeGeniusSupervisor('./test_docs')
print(f'✓ Supervisor initialized')

print('\n✅ All tests passed!')
"
```

---

## Option C: Deploy HTTP Server

### Using Jac Server
```bash
cd "/mnt/c/Users/admin/Desktop/CODEBASE GENIUS"
source jac-env/bin/activate

# Start server
jac serve agentic_codebase_genius/main.jac
```

**Expected Output:**
```
==================================================
Codebase Genius - Multi-Agent System
==================================================

✓ Server initialized
✓ Agents ready
✓ API endpoints active

Endpoints:
  POST /generate - Generate documentation
  GET  /status - Get processing status
  GET  /list - List generated docs
  GET  /health - Health check
```

### API Calls (in another terminal)
```bash
# Health check
curl http://localhost:8000/health

# Generate documentation
curl -X POST "http://localhost:8000/generate?repo_url=https://github.com/user/repo.git"

# Get status
curl http://localhost:8000/status

# List generated docs
curl http://localhost:8000/list
```

---

## Option D: Run Streamlit UI

### Launch Dashboard
```bash
cd "/mnt/c/Users/admin/Desktop/CODEBASE GENIUS"
source jac-env/bin/activate

streamlit run frontend/app.py
```

**Expected Output:**
```
You can now view your Streamlit app in your browser.
URL: http://localhost:8501
```

Then open http://localhost:8501 in your browser.

---

## Option E: Analyze a Local Directory

### Process Local Repo
```bash
python << 'PYEOF'
import sys
sys.path.insert(0, 'agentic_codebase_genius')
from repo_mapper import RepoMapper
from code_analyzer import CodeAnalyzer
from doc_genie import DocGenie
import os

# Analyze local directory
repo_path = "/path/to/your/repo"  # Change this

print(f"Analyzing: {repo_path}\n")

# Build file tree
mapper = RepoMapper()
mapper.repo_path = repo_path
mapper.build_file_tree()
mapper.read_readme()
mapper.identify_entry_points()
mapper.identify_primary_language()

print(f"✓ Primary language: {mapper.primary_language}")
print(f"✓ Entry points: {len(mapper.entry_points)}")
print(f"✓ README: {len(mapper.readme_content)} chars")

# Analyze code
analyzer = CodeAnalyzer()
analysis = analyzer.analyze_repository(mapper.file_tree)

print(f"✓ Entities found: {analysis['entity_count']}")
print(f"✓ Files analyzed: {analysis['file_count']}")

# Generate docs
genie = DocGenie()
doc_content = genie.generate_documentation({
    'repo_name': os.path.basename(repo_path),
    'primary_language': mapper.primary_language,
    'readme': mapper.readme_content,
    'entities': analysis['entities'],
    'entity_count': analysis['entity_count'],
    'file_count': analysis['file_count']
})

# Save
output_file = f"./docs/{os.path.basename(repo_path)}_analysis.md"
os.makedirs('./docs', exist_ok=True)
with open(output_file, 'w') as f:
    f.write(doc_content)

print(f"\n✅ Documentation saved: {output_file}")
PYEOF
```

---

## Troubleshooting

### Issue: `ModuleNotFoundError: No module named 'jaclang'`
**Solution:** Activate virtual environment
```bash
source jac-env/bin/activate
```

### Issue: `ImportError: attempted relative import with no known parent package`
**Solution:** Add to sys.path
```bash
python -c "
import sys
sys.path.insert(0, 'agentic_codebase_genius')
# then import
"
```

### Issue: Git clone fails
**Solution:** 
- Ensure git is installed: `git --version`
- Check repository URL is valid
- Verify internet connection

### Issue: Port already in use (HTTP server)
**Solution:** Use different port
```bash
jac serve agentic_codebase_genius/main.jac --port 9000
```

---

## Environment Variables

Edit `agentic_codebase_genius/.env`:
```env
OUTPUT_DIR=./docs
MAX_RECURSION_DEPTH=10
INCLUDE_TEST_FILES=false
CLONE_TIMEOUT=60
```

---

## Common Workflows

### Workflow 1: Quick Test
```bash
source jac-env/bin/activate
python agentic_codebase_genius/test.py
```

### Workflow 2: Process Single Repo
```bash
python -c "
import sys
sys.path.insert(0, 'agentic_codebase_genius')
from api import process_repository
process_repository('https://github.com/user/repo.git')
"
```

### Workflow 3: Batch Processing
```bash
python << 'PYEOF'
import sys
sys.path.insert(0, 'agentic_codebase_genius')
from api import process_repository

repos = [
    'https://github.com/repo1/url.git',
    'https://github.com/repo2/url.git',
    'https://github.com/repo3/url.git',
]

for repo in repos:
    success, msg, path = process_repository(repo)
    status = "✓" if success else "✗"
    print(f"{status} {repo}")
PYEOF
```

### Workflow 4: Start Server + UI
```bash
# Terminal 1: Start server
source jac-env/bin/activate
jac serve agentic_codebase_genius/main.jac

# Terminal 2: Start UI
source jac-env/bin/activate
streamlit run frontend/app.py
```

---

## Performance Tips

1. **For large repos:** Increase timeout
   ```python
   # In supervisor.py, increase CLONE_TIMEOUT
   CLONE_TIMEOUT=300  # 5 minutes
   ```

2. **For shallow analysis:** Reduce recursion depth
   ```env
   MAX_RECURSION_DEPTH=5  # Default: 10
   ```

3. **Parallel processing:** Process multiple repos
   ```bash
   # Run multiple instances with different repos
   python process_repo.py repo1.git &
   python process_repo.py repo2.git &
   python process_repo.py repo3.git &
   ```

---

## Next Steps

- ✅ Verify installation: `python -c "from agentic_codebase_genius import *"`
- ✅ Run tests: `python test.py`
- ✅ Process your first repo
- ✅ Deploy the server
- ✅ Scale to production

**Status:** System ready for immediate use! 🚀
