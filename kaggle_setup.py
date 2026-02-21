"""
BrajYatra AI — Kaggle Setup Script

Run this script in the FIRST cell of your Kaggle notebook.
It installs dependencies and starts the FastAPI server.

Usage in Kaggle notebook:
  Cell 1: !pip install -q transformers accelerate sentence-transformers faiss-cpu fastapi uvicorn pydantic requests ortools
  Cell 2: Run this file or paste its contents
"""

import subprocess
import sys
import os


def install_deps():
    """Install required packages."""
    packages = [
        "transformers",
        "accelerate",
        "sentence-transformers",
        "faiss-cpu",
        "fastapi",
        "uvicorn[standard]",
        "pydantic",
        "requests",
        "ortools",
        "scikit-learn",
    ]

    for pkg in packages:
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", "-q", pkg
        ])

    print("✅ All dependencies installed!")


def check_gpu():
    """Check if GPU is available."""
    try:
        import torch
        if torch.cuda.is_available():
            gpu_name = torch.cuda.get_device_name(0)
            gpu_mem = torch.cuda.get_device_properties(0).total_mem / (1024**3)
            print(f"✅ GPU: {gpu_name} ({gpu_mem:.1f} GB)")
            return True
        else:
            print("⚠️ No GPU detected. Running on CPU (will be slower).")
            return False
    except ImportError:
        print("⚠️ PyTorch not installed yet.")
        return False


def start_server(port=8000):
    """Start FastAPI server in background."""
    import threading
    import uvicorn
    from main import app

    def run():
        uvicorn.run(app, host="0.0.0.0", port=port, log_level="info")

    thread = threading.Thread(target=run, daemon=True)
    thread.start()
    print(f"✅ Server started on http://localhost:{port}")
    print(f"📖 API docs: http://localhost:{port}/docs")
    return thread


def test_endpoints(base_url="http://localhost:8000"):
    """Quick health check of all endpoints."""
    import requests
    import time

    time.sleep(5)  # Wait for server to start

    print("\n🧪 Testing endpoints...\n")

    tests = [
        ("GET", "/", None),
        ("GET", "/locations?city=Mathura", None),
        ("GET", "/weather/Mathura", None),
    ]

    for method, path, body in tests:
        try:
            url = f"{base_url}{path}"
            if method == "GET":
                r = requests.get(url, timeout=10)
            else:
                r = requests.post(url, json=body, timeout=30)

            status = "✅" if r.status_code == 200 else f"⚠️ {r.status_code}"
            print(f"  {status} {method} {path}")
        except Exception as e:
            print(f"  ❌ {method} {path} - {e}")

    print()


if __name__ == "__main__":
    print("🌍 BrajYatra AI — Kaggle Setup\n")
    check_gpu()
    print()
    print("To start, run in your notebook:")
    print("  1. install_deps()")
    print("  2. start_server()")
    print("  3. test_endpoints()")
