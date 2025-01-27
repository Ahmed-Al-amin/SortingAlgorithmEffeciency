NUM_TEST_CASES = 10
INPUT_SIZES = [10, 20, 30, 40, 50, 100, 200, 300, 400, 500]

RANDOM = 'random'
SORTED = 'sorted'
REVERSED = 'reversed'

algorithm_names = ["Bubble Sort", "Insertion Sort", "Merge Sort", "Quick Sort", "Heap Sort", "Selection Sort", "Radix Sort", "Counting Sort" ]
algorithm_complexities = {
    "Bubble Sort": "O(n^2)",
    "Insertion Sort": "O(n^2)",
    "Merge Sort": "O(n log n)",
    "Quick Sort": "O(n log n) (avg), O(n^2) (worst)",
    "Heap Sort": "O(n log n)",
    "Selection Sort": "O(n^2)",
    "Radix Sort": "O(n * d)",
    "Counting Sort": "O(n + k)"
}