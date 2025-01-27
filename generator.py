#generator.py

import random
import os
import time
import csv
from typing import List
import plot_graphs
import sorting_algorithms
from constant import *





def generate_random_array(size: int) -> List[int]:
    return random.sample(range(1, size + 1), size)

def generate_sorted_array(size: int) -> List[int]:
    return list(range(1, size + 1))

def generate_reversed_array(size: int) -> List[int]:
    return list(range(size, 0, -1))

def generate_input_array_file(arr: List[int], size: int, test_case: int, scenario: str) -> None:
    os.makedirs("input_arrays", exist_ok=True)
    filename = f"input_arrays/input_case_{test_case + 1}_{scenario}.txt"

    with open(filename, "w") as input_file:
        input_file.write(f"array with size = {size} : {{")
        input_file.write(", ".join(map(str, arr)))
        input_file.write("}")




def run_sorting_test(arr: List[int], algorithm_name: str, scenario: str, size: int, output_file: csv.writer) -> None:
    test_arr = arr.copy()

    start_time = time.time()

    steps = sorting_algorithms.algorithm_functions[algorithm_name](test_arr)

    end_time = time.time()
    execution_time = (end_time - start_time) * 1000

    output_file.writerow([algorithm_name, scenario, size, steps, execution_time, sorting_algorithms.algorithm_complexities[algorithm_name]])






def main():
    with open("sorting_efficiency_comparison.csv", "w", newline="") as output_file:
        writer = csv.writer(output_file)
        writer.writerow(["Algorithm", "Scenario", "Input Size", "Steps", "Execution Time (ms)", "Asymptotic Notation"])
        #sorted_arr = generate_sorted_array(INPUT_SIZES[len(INPUT_SIZES)-1])
        #random_arr = generate_random_array(INPUT_SIZES[len(INPUT_SIZES)-1])
        #reversed_arr = generate_reversed_array(INPUT_SIZES[len(INPUT_SIZES)-1])

        for test_case in range(NUM_TEST_CASES):
            input_size = INPUT_SIZES[test_case]

            scenarios = [SORTED, RANDOM, REVERSED]
            for scenario in scenarios:
                if scenario == SORTED:
                    arr = generate_sorted_array(input_size)
                elif scenario == RANDOM:
                    arr = generate_random_array(input_size)
                    generate_input_array_file(arr, input_size, test_case, scenario)
                elif scenario == REVERSED:
                    arr = generate_reversed_array(input_size)


                for algorithm_name in algorithm_names:
                    run_sorting_test(arr, algorithm_name, scenario, input_size, writer)

                writer.writerow([])

    print("Comparison completed. Results written to sorting_efficiency_comparison.csv")
    print("Input array files generated in 'input_arrays' directory.")
    plot_graphs.main()


if __name__ == "__main__":
    main()


# tobch