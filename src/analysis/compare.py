import time


def compare_execution_time(fct_vanilla, fct_with_module, repeats=10):
    """
    Compare the average execution time of two functions over a number of repetitions.

    The difference is computed with the average times rather than with the times of a
    single execution, so that the influence of system variations is minimal.

    Parameters
    ----------
    fct_vanilla : function without external modules
    fct_with_module : function using a module like pandas
    repeats : int - number of times each function should be executed (default: 10)

    Returns
    -------
    tuple containing :
        - the average time for fct_vanilla
        - the average time for fct_with_module
        - the difference between the two average execution times

    """
    total_time_vanilla = 0
    total_time_other = 0

    for _ in range(repeats):
        start = time.perf_counter()
        fct_vanilla()
        total_time_vanilla += time.perf_counter() - start

        start = time.perf_counter()
        fct_with_module()
        total_time_other += time.perf_counter() - start

    avg_time_vanilla = total_time_vanilla / repeats
    avg_time_other = total_time_other / repeats

    return {
        "vanilla": avg_time_vanilla,
        "modules": avg_time_other,
        "difference": avg_time_vanilla - avg_time_other
    }
