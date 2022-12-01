from typing import Callable


def pipe(functions: Callable) -> Callable:
    def output_function(input):
        result = input
        for f in functions:
            result = f(result)
        return result

    return output_function
