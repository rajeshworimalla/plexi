import inspect
from radon.complexity import cc_visit
from config import filter_search_jobs

def analyze_cyclomatic_complexity():
    # Get the function source code using the inspect module
    source_code = inspect.getsource(filter_search_jobs)

    # Analyze the function's complexity using Radon's cc_visit
    result = cc_visit(source_code)

    # Initialize complexity value
    cyclomatic_complexity = 0

    # Radon result provides detailed info on each block in the function
    for item in result:
        cyclomatic_complexity += item.complexity  # Cyclomatic complexity for the function

    # Print results: cyclomatic complexity
    print(f"Function: filter_search_jobs")
    print(f"Cyclomatic Complexity: {cyclomatic_complexity}")

if __name__ == '__main__':
    analyze_cyclomatic_complexity()
