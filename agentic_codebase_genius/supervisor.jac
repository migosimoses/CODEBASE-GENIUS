"""
Supervisor Walker - lightweight Jac-side orchestrator placeholder

This file contains a minimal Jac walker used as a placeholder. The
actual heavy processing is performed by the Python FastAPI bridge in
this workspace. This keeps the Jac file syntax-valid for `jac build`.
"""

walker supervisor {
    has repo_url: str;
    has output_dir: str = "./docs";
    has status: str = "initialized";
    has current_doc_path: str = "";
    has error_message: str = "";

    ability init() {
        // placeholder init; Python bridge handles real initialization
        self.status = "initialized";
        print("supervisor: placeholder init");
    }

    ability validate_url(url: str) -> bool {
        if url.startswith("http://") or url.startswith("https://") or url.startswith("git@") {
            return true;
        }
        return false;
    }

    ability process_repository(target_dir: str = "./tmp_repo") -> dict {
        // Direct processing is delegated to the Python FastAPI bridge in this setup.
        if not self.validate_url(self.repo_url) {
            self.status = "error";
            self.error_message = "Invalid repository URL";
            return {"success": false, "message": self.error_message};
        }
        self.status = "requested";
        return {"success": false, "message": "use_python_bridge"};
    }

    ability get_status() -> str {
        return self.status;
    }
}
