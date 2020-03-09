from line_profiler import LineProfiler


def line_profile(func):
    """
    Provide a line-by-line profiler as a decorator
    TODO: Disable on production
    """
    def profiled_func(*args, **kwargs):
        try:
            profiler = LineProfiler()
            profiler.add_function(func)
            profiler.enable_by_count()
            return func(*args, **kwargs)
        finally:
            profiler.print_stats()
    return profiled_func
