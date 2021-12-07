# FastAPI Benchmark

Small project for benchmarking FastAPI operations under varying circumstances.

# Quick start
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Serve the API through Gunicorn using 1 worker (edit serve.sh to change number of workers)
sh serve.sh

# In another terminal, run a stress test against the synchronous or asynchronous endpoint.
# (open http://localhost:8089 after running to start the test)

# Load JSON file from disk and return
sh stress_sync_json.sh
sh stress_async_json.sh

# Make HTTP request and return
sh stress_sync_http.sh
sh stress_async_http.sh

```