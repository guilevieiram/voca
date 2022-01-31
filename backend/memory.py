import tracemalloc
import app

def trace_mem():
    first_size, first_peak = tracemalloc.get_traced_memory()
    peak = first_peak/(1024*1024)
    first = first_size/(1024*1024)
    print("Peak size (MB): ", peak)
    print("First size (MB), ", first)

tracemalloc.start()

try:
    app.endpoint.run()
finally:
    trace_mem()
