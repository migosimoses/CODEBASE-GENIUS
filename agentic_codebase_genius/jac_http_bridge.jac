import requests, json;

# Minimal bridge: POSTs to the Python FastAPI `/process` endpoint directly from entry.
with entry {
    repo = "https://github.com/octocat/Hello-World.git";
    try {
        resp = requests.post("http://127.0.0.1:5000/process", json={"repo_url": repo});
        print("jac_bridge: status=" + str(resp.status_code));
        if resp.text {
            print(resp.text);
        }
    } except Exception as e {
        print("jac_bridge: error " + str(e));
    }
}
