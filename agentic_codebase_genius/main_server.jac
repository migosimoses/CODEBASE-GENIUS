walker ui_helper {
    ability ui_link() {
        return "http://127.0.0.1:5000/";
    }
}

def startup {
    print("Codebase Genius - Jac server starting (UI available at http://127.0.0.1:5000)");
}

with entry {
    startup();
    # spawn ui helper on startup
    spawn ui_helper as uih;
}
