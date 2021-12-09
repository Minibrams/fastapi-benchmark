# FastAPI Benchmark

Comparing FastAPI behaviour and performance under various synchronous/asynchronous settings.

# Quick start
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Serve the API through Gunicorn using 1 worker (edit serve.sh to change number of workers)
sh serve.sh

# In another terminal, run a stress test against a synchronous or asynchronous endpoint:

# Make HTTP request and return
sh stress_sync_http.sh
sh stress_async_http.sh
sh stress_async_http_sync.sh

# Load JSON file from disk and return
sh stress_sync_json.sh
sh stress_async_json.sh

```

### Notes
The service will start reporting `anyio.BrokenResourceError` about 30 seconds into each test. 
This is likely caused by the logging middleware, see [this issue](https://github.com/tiangolo/fastapi/issues/4041#issuecomment-947247194). Removing the middleware gets rid of the error and improves performance slightly, but the logging is needed to keep track of threads for the test results.

# Scenarios

Following is a number of different scenario designed to shed light on how a FastAPI application behaves when doing different kinds of IO in different kinds of endpoints.

In all the scenarios, the IO being done is making a HTTP request to a simple GoLang API that waits for 1000 milliseconds before responding.

## TL;DR results
|                             | sync endpoint w. sync io | async endpoint w. async io | async endpoint w. sync io |
|-----------------------------|--------------------------|----------------------------|---------------------------|
| *Num. users*                | 500                      | 500                        | 500                       |
| *Test runtime*              | 1 minute                 | 1 minute                   | 1 minute                  |
| *Num. requests*             | 2122                     | 3190                       | 785                       |
| *Num. failures*             | 0 (0%)                   | 0 (0%)                     | 732 (93.2%)               |
| *Avg. num. requests/sec*    | 35.6                     | 53.2                       | 13.1                      |
| *Avg. num. failures/sec*    | 0                        | 0                          | 12.2                      |
| *Median response time*      | 1300 ms                  | 8300 ms                    | 27000 ms                  |
| *Num. threads spawned*      | 41                       | 1                          | 1                         |
| *Avg. num. active threads*  | 41                       | 1                          | 1                         |

## Synchronous IO in synchronous endpoints (`stress_sync_http.sh`)
**Description:** Making synchronous HTTP GET requests from synchronous endpoints (using `httpx.Client()` for making requests)

```python
@app.get('/http/sync')
def http_sync():
    with httpx.Client() as http:
        return http.get('http://165.227.149.214:8090?waitms=1000').content
```

The simulated users make GET requests to our FastAPI endpoint `/sync/http`.
The endpoint, in turn, makes a synchronous GET request to `http://165.227.149.214:8090?waitms=1000`, a simple GoLang API that waits for the provided number of milliseconds on each request.
   - You can also run the GoLang server locally with `serve_external_http.sh`.

### Results
  - Num. users: 500
  - Test runtime: 1 minute
  - Num. requests: 2122
  - Num. failures: 0
  - Average requests/second: 35.6
  - Average failures/second: 0
  - Median response time: 1300 ms
  - Average num. active threads: 41
  - Num. unique threads created: 41

### Observations
  - Synchronous IO in synchronous endpoints is **not** blocking, since the max number of requests in this timespan would be 60.

## Asynchronous requests in asynchronous endpoints (`stress_async_http.sh`)
**Description:** Making asynchronous HTTP GET requests from synchronous endpoints (using `httpx.AsyncClient()` for making requests)

```python
@app.get('/async/http')
async def http_async():
    async with httpx.AsyncClient() as http:
        return (await http.get('http://165.227.149.214:8090?waitms=1000')).content
```

The simulated users make GET requests to our FastAPI endpoint `/async/http`.
The endpoint, in turn, awaits an asynchronous GET request to `http://165.227.149.214:8090?waitms=1000`, a simple GoLang API that waits for the provided number of milliseconds on each request.
   - You can also run the GoLang server locally with `serve_external_http.sh`.

### Results
  - Num. users: 500
  - Test runtime: 1 minute
  - Num. requests: 3190
  - Num. failures: 0
  - Average requests/second: 53.2
  - Average failures/second: 0
  - Median response time: 8300 ms
  - Average num. active threads: 1
  - Num. unique threads created: 1

### Observations
  - More requests were handled than by `/sync/http`, but response times were significantly worse (9000 ms vs. 1300 ms)
  - All requests were being handled by a single thread; `async def` endpoints are not multithreaded like their `def` endpoint counterparts are

## Synchronous requests in asynchronous endpoints (`stress_async_http_sync.sh`)
**Description:** Making synchronous HTTP GET requests from asynchronous endpoints (using `httpx.Client()` for making requests)

```python
@app.get('/http/async/sync')
async def http_sync():
    with httpx.Client() as http:
        return http.get('http://165.227.149.214:8090?waitms=1000').content
```


The simulated users make GET requests to our FastAPI endpoint `/async/http/sync`.
The endpoint, in turn, makes a synchronous GET request to `http://165.227.149.214:8090?waitms=1000`, a simple GoLang API that waits for the provided number of milliseconds on each request.
   - You can also run the GoLang server locally with `serve_external_http.sh`.

### Results
  - Num. users: 500
  - Test runtime: 1 minute
  - Num. requests: 785
  - Num. failures: 732 (timeouts, connection reset, remote disconnected)
  - Average requests/second: 13.08
  - Average failures/second: 12.2
  - Median response time: 27000 ms
  - Average num. active threads: 1
  - Num. unique threads created: 1

### Observations
  - Synchronous IO in asynchronous endpoints **is blocking**
  - Blocked requests cause other requests to time out and fail
