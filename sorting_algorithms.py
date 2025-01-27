# sorting_algorithms.py


from typing import List
from constant import *


def bubble_sort(arr: List[int]) -> int:
    steps = 0
    flage = False
    size = len(arr)
    for i in range(size - 1):
        for j in range(size - i - 1):
            steps += 1
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                steps += 2
                flage = True
                steps += 1
        steps += 1
        if not(flage):
            break
    return steps


def selection_sort(arr: List[int]) -> int:
    length = len(arr)
    steps = 0
    for i in range(length):
        min_index = i
        steps += 1
        for j in range(i + 1, length):
            steps += 1
            if arr[j] < arr[min_index]:
                min_index = j
                steps += 1
        arr[min_index], arr[i] = arr[i], arr[min_index]
        steps += 2
    return steps


def insertion_sort(arr: List[int]) -> int:
    steps = 0
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        steps += 2
        while j >= 0 and arr[j] > key:
            steps += 2
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
        steps += 1
    return steps


def merge(arr: List[int], left: int, mid: int, right: int) -> int:
    steps = 0
    temp = []
    i, j = left, mid + 1

    while i <= mid and j <= right:
        steps += 1
        if arr[i] <= arr[j]:
            temp.append(arr[i])
            i += 1
            steps += 2
        else:
            temp.append(arr[j])
            j += 1
            steps += 2

    while i <= mid:
        steps += 2
        temp.append(arr[i])
        i += 1

    while j <= right:
        steps += 2
        temp.append(arr[j])
        j += 1

    arr[left:right + 1] = temp
    steps += len(temp)
    return steps


def merge_sort_recursive(arr: List[int], left: int, right: int) -> int:
    steps = 0
    if left < right:
        mid = (left + right) // 2
        steps += merge_sort_recursive(arr, left, mid)
        steps += merge_sort_recursive(arr, mid + 1, right)
        steps += merge(arr, left, mid, right)
    return steps


def merge_sort(arr: List[int]) -> int:
    return merge_sort_recursive(arr, 0, len(arr) - 1)



def heapify(arr: List[int], n: int, i: int) -> int:
    steps = 0
    largest = i
    left = 2 * i + 1
    right = 2 * i + 2
    steps += 3
    if left < n and arr[left] > arr[largest]:
        largest = left
        steps += 2
    if right < n and arr[right] > arr[largest]:
        largest = right
        steps += 2
    if largest != i:
        arr[i], arr[largest] = arr[largest], arr[i]
        steps += 2
        steps += heapify(arr, n, largest)
    return steps


def heap_sort(arr: List[int]) -> int:
    steps = 0
    n = len(arr)
    for i in range(n // 2 - 1, -1, -1):
        steps += heapify(arr, n, i)

    for i in range(n - 1, 0, -1):
        arr[0], arr[i] = arr[i], arr[0]
        steps += 2
        steps += heapify(arr, i, 0)
    return steps



def partition(arr: List[int], low: int, high: int) -> (int, int):

    steps = 0
    pivot = arr[high]
    i = low - 1
    steps += 2

    for j in range(low, high):
        steps += 1
        if arr[j] < pivot:
            i += 1
            steps += 2
            if i != j:
                arr[i], arr[j] = arr[j], arr[i]
                steps += 2

    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    steps += 2

    return i + 1, steps

def quick_sort_recursive(arr: List[int], low: int, high: int) -> int:
    steps = 0
    if low < high:
        pivot_index, partition_steps = partition(arr, low, high)
        steps += partition_steps


        steps += quick_sort_recursive(arr, low, pivot_index - 1)
        steps += quick_sort_recursive(arr, pivot_index + 1, high)

    return steps

def quick_sort(arr: List[int]) -> int:
    return quick_sort_recursive(arr, 0, len(arr) - 1)

def counting_sort_for_radix(arr: List[int], exp: int) -> int:

    n = len(arr)
    steps = 0

    output = [0] * n
    steps += n
    count = [0] * 10
    steps += 10

    for i in range(n):
        steps += 1
        index = (arr[i] // exp) % 10
        count[index] += 1
        steps += 1

    for i in range(1, 10):
        steps += 1
        count[i] += count[i - 1]
        steps += 1

    i = n - 1
    while i >= 0:
        steps += 1
        index = (arr[i] // exp) % 10
        output[count[index] - 1] = arr[i]
        steps += 1
        count[index] -= 1
        steps += 1
        i -= 1

    for i in range(n):
        steps += 1
        arr[i] = output[i]
        steps += 1

    return steps


def radix_sort(arr: List[int]) -> int:

    if len(arr) < 2:
        return 0

    max_val = max(arr)
    steps = 0
    steps += len(arr)

    exp = 1
    while max_val // exp > 0:
        steps += 1
        steps += counting_sort_for_radix(arr, exp)
        exp *= 10
        steps += 1

    return steps


def counting_sort(arr: List[int]) -> int:
    if len(arr) < 2:
        return 0

    steps = 0
    max_val = max(arr)
    steps += len(arr)

    count = [0] * (max_val + 1)
    steps += (max_val + 1)

    for x in arr:
        steps += 1
        count[x] += 1
        steps += 1

    total = 0
    for i in range(len(count)):
        steps += 1
        old_count = count[i]
        count[i] = total
        steps += 1
        total += old_count
        steps += 1

    output = [0] * len(arr)
    steps += len(arr)

    for x in arr:
        steps += 1
        output[count[x]] = x
        steps += 1
        count[x] += 1
        steps += 1

    for i in range(len(arr)):
        steps += 1
        arr[i] = output[i]
        steps += 1

    return steps


algorithm_functions = {
    "Bubble Sort": bubble_sort,
    "Insertion Sort": insertion_sort,
    "Merge Sort": merge_sort,
    "Quick Sort": quick_sort,
    "Heap Sort": heap_sort,
    "Selection Sort": selection_sort,
    "Radix Sort": radix_sort,
    "Counting Sort": counting_sort
}


