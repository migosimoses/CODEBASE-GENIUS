"""
Codebase Genius - Minimal Main Entry

Simple Jac init_server placeholder; keeps `jac build` happy.
"""

walker init_server {
    ability startup_sequence() {
        print("Codebase Genius - server started (minimal)");
    }
}

spawn init_server as init;
init.startup_sequence();
