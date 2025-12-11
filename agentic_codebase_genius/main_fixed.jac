"""
Codebase Genius - Main HTTP Server Entry Point (fixed)
"""

import:py from supervisor import CodeGeniusSupervisor;

node root {
    has supervisor: dict = {};
    
    can create_supervisor() {
        """Initialize supervisor"""
        self.supervisor = CodeGeniusSupervisor("./docs");
    }
    
    can process_repository(repo_url: str) -> dict {
        """Process a repository"""
        if not self.supervisor {
            self.create_supervisor();
        }
        self.supervisor.repo_url = repo_url;
        return self.supervisor.process_repository();
    }
    
    can get_documentation() -> str {
        """Get current documentation"""
        if self.supervisor {
            return self.supervisor.get_documentation() or "No documentation available";
        }
        return "Supervisor not initialized";
    }
    
    can list_docs() -> list {
        """List all generated documentation"""
        import os;
        docs_dir = "./docs";
        if os.path.exists(docs_dir) {
            return [f for f in os.listdir(docs_dir) if f.endswith('.md')];
        }
        return [];
    }
}

walker api_handler {
    has endpoint: str;
    has method: str;
    has params: dict;
    has response: dict = {};

    ability handle_generate(repo_url: str) -> dict {
        """Handle documentation generation request"""
        print("Generating docs for: " + repo_url);
        
        return {
            "status": "success",
            "message": "Documentation generation started",
            "repo_url": repo_url
        };
    }

    ability handle_status() -> dict {
        """Handle status request"""
        return {
            "status": "ready",
            "version": "0.1.0",
            "timestamp": "2025-12-11"
        };
    }

    ability handle_list() -> dict {
        """Handle list docs request"""
        import os;
        docs = [];
        if os.path.exists("./docs") {
            docs = [f for f in os.listdir("./docs") if f.endswith('.md')];
        }
        return {
            "status": "success",
            "count": len(docs),
            "docs": docs
        };
    }

    ability handle_health() -> dict {
        """Handle health check"""
        return {
            "status": "healthy",
            "service": "Codebase Genius",
            "version": "0.1.0"
        };
    }
}

walker init_server {
    has ready: bool = False;

    ability startup_sequence() {
        """Initialize server startup"""
        print("========================================");
        print("Codebase Genius - Multi-Agent System");
        print("========================================");
        print("\nServer initialized");
        print("Agents ready");
        print("API endpoints active\n");
        print("Endpoints:");
        print("  POST /generate - Generate documentation");
        print("  GET  /status - Get processing status");
        print("  GET  /list - List generated docs");
        print("  GET  /health - Health check\n");
        self.ready = True;
    }
}

# Server startup
spawn init_server as init;
init.startup_sequence();
