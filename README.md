# FastAPI Benchmark

Small project for benchmarking FastAPI operations under varying circumstances.

# Quick start
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Serve the API through Gunicorn using 4 workers
sh serve.sh

# In another terminal, run a stress test against the synchronous or asynchronous endpoint.
# (open http://localhost:8089 after running to start the test)
sh stress_sync.sh
sh stress_async.sh
```