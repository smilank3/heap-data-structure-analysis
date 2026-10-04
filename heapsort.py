"""
Heapsort, with Quicksort and Merge Sort for comparison.

Run:  python heapsort.py
"""

import random
import time


# ----------------------------------------------------------------------
# Heapsort
# ----------------------------------------------------------------------

def max_heapify(arr, i, heap_size):
    """Fix the max-heap starting at index i.

    The left child is at 2i+1 and the right child is at 2i+2.
    If a child is bigger than the current value, swap them.
    Repeat until the heap is correct.
    Time: O(log n).
    """
    while True:
        left = 2 * i + 1
        right = 2 * i + 2
        largest = i

        if left < heap_size and arr[left] > arr[largest]:
            largest = left
        if right < heap_size and arr[right] > arr[largest]:
            largest = right

        if largest == i:
            return
        arr[i], arr[largest] = arr[largest], arr[i]
        i = largest  # Use a loop instead of recursion.


def build_max_heap(arr):
    """Convert the array into a max-heap.

    The second half of the array contains leaf nodes,
    so we only need to fix the other nodes.
    Time: O(n).
    """
    for i in range(len(arr) // 2 - 1, -1, -1):
        max_heapify(arr, i, len(arr))


def heapsort(arr):
    """Sort the array from smallest to largest.

    Time: O(n log n) in all cases.
    Extra space: O(1).
    """
    build_max_heap(arr)

    # Move the biggest value to the end and make the heap smaller.
    for end in range(len(arr) - 1, 0, -1):
        arr[0], arr[end] = arr[end], arr[0]
        max_heapify(arr, 0, end)

    return arr


# ----------------------------------------------------------------------
# Comparison algorithms
# ----------------------------------------------------------------------

def quicksort(arr):
    """Sort the array using Quicksort with a random pivot."""
    def helper(low, high):
        while low < high:
            r = random.randint(low, high)
            arr[r], arr[high] = arr[high], arr[r]
            pivot = arr[high]
            i = low - 1
            for j in range(low, high):
                if arr[j] <= pivot:
                    i += 1
                    arr[i], arr[j] = arr[j], arr[i]
            arr[i + 1], arr[high] = arr[high], arr[i + 1]
            p = i + 1

            # Work on the smaller part first to use less memory.
            if p - low < high - p:
                helper(low, p - 1)
                low = p + 1
            else:
                helper(p + 1, high)
                high = p - 1

    helper(0, len(arr) - 1)
    return arr


def merge_sort(arr):
    """Sort the array using Merge Sort.

    This method keeps equal values in their original order.
    It creates a new list, so it uses O(n) extra space.
    """
    if len(arr) <= 1:
        return arr

    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])

    merged = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:      # Keep equal values in the same order.
            merged.append(left[i]); i += 1
        else:
            merged.append(right[j]); j += 1
    merged.extend(left[i:])
    merged.extend(right[j:])
    return merged


# ----------------------------------------------------------------------
# Tests and benchmark
# ----------------------------------------------------------------------

def run_tests():
    rng = random.Random(0)
    cases = {
        "empty": [],
        "single": [1],
        "sorted": list(range(50)),
        "reverse": list(range(50, 0, -1)),
        "duplicates": [rng.randint(0, 3) for _ in range(50)],
        "all equal": [7] * 50,
        "negatives": [rng.randint(-100, 100) for _ in range(50)],
        "random": [rng.randint(0, 1000) for _ in range(200)],
    }

    failures = 0
    for name, data in cases.items():
        for label, fn in (("heapsort", heapsort), ("quicksort", quicksort),
                          ("merge_sort", merge_sort)):
            if fn(data.copy()) != sorted(data):
                print(f"  FAIL: {label} on {name}")
                failures += 1

    print(f"Correctness: {len(cases)} cases x 3 algorithms -> "
          f"{'all passed' if failures == 0 else f'{failures} FAILURES'}\n")
    return failures == 0


def make_datasets(n, seed=42):
    rng = random.Random(seed)
    return {
        "Random": [rng.randint(0, 10 * n) for _ in range(n)],
        "Sorted": list(range(n)),
        "Reverse": list(range(n, 0, -1)),
    }


def time_sort(fn, data, repeats=3):
    """Run the sort several times and return the fastest time in milliseconds."""
    best = float("inf")
    for _ in range(repeats):
        working = data.copy()
        start = time.perf_counter()
        fn(working)
        best = min(best, time.perf_counter() - start)
    return best * 1000


def run_benchmark(sizes=(1000, 5000, 10000, 20000)):
    algorithms = [("Heapsort", heapsort), ("Quicksort", quicksort),
                  ("Merge Sort", merge_sort)]

    print("EXECUTION TIME (ms, best of 3)")
    print(f"{'n':>7} {'Distribution':<13} " +
          " ".join(f"{name:>12}" for name, _ in algorithms))
    print("-" * 70)

    for n in sizes:
        for label, data in make_datasets(n).items():
            row = " ".join(f"{time_sort(fn, data):12.2f}" for _, fn in algorithms)
            print(f"{n:>7} {label:<13} {row}")
        print()


if __name__ == "__main__":
    print()
    if run_tests():
        run_benchmark()
