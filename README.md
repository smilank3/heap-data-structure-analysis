# Heap Data Structures

Heapsort and a binary-heap priority queue, with a task scheduler simulation.

All numbers below come from the run saved as `heapsort_result.png` and `priority_queue.png`.

## Files

| File | Purpose |
| --- | --- |
| `heapsort.py` | Heapsort, Quicksort, and Merge Sort, with correctness tests and a running-time comparison |
| `priority_queue.py` | `Task`, `MaxPriorityQueue`, automated tests, and the scheduler simulation |
| `REPORT.md` | Design choices, complexity analysis, and explanations of the results |
| `heapsort_result.png` & `priority_queue.png` | Console output from run of both programs |

## Requirements

Python 3.8 or newer. Uses only the standard library; no extra packages are needed.

## How to run

```bash
python heapsort.py          # run tests, then compare sorting times
python priority_queue.py    # run tests, then the demo and scheduler
```

Both scripts run their tests first and continue only if the tests pass. Running both programs takes well under a minute.

## Using the priority queue

```python
from priority_queue import Task, MaxPriorityQueue

pq = MaxPriorityQueue()
pq.insert(Task(task_id="A", priority=3, arrival_time=0, deadline=20, duration=2))
pq.insert(Task(task_id="B", priority=7, arrival_time=1, deadline=15, duration=1))

pq.peek()                      # view the highest-priority task, O(1)
pq.increase_key("A", 9)         # raise A's priority, O(log n)
pq.decrease_key("A", 1)         # lower A's priority, O(log n)
task = pq.extract_max()        # remove the highest-priority task, O(log n)
pq.is_empty()                  # check whether the queue is empty, O(1)
len(pq)                       # count the tasks in the queue
```

Tasks with **equal priority are returned in an unspecified order**. The heap does not keep them in arrival order. To support FIFO (first in, first out) among equal-priority tasks, add a secondary sort key.

## Complexity summary

**Heapsort:** `O(n log n)` is an upper bound for every input. The worst case is `Θ(n log n)`. When all values are equal, this implementation takes `Θ(n)` because heapify stops immediately. For distinct keys, `Θ(n log n)` is a tight bound, supported by a separate result (Schaffer & Sedgewick, 1993). Building the max-heap takes `O(n)`, and the `n-1` extractions together take at most `O(n log n)`.

**Auxiliary space** means memory used in addition to the input:

| Algorithm | Auxiliary space |
| --- | --- |
| Heapsort | `O(1)` — heapify uses a loop, so it needs no recursion frames |
| Quicksort (this implementation) | `O(log n)` — the recursion stack stays small because only the smaller partition is processed recursively |
| Merge Sort | `O(n)` |

**Priority queue:** total storage is `O(n)`, including the heap list and the index dictionary.

| Operation | Time |
| --- | --- |
| `insert` | Expected amortized `O(log n)`, including an amortized `O(1)` append |
| `extract_max` | Expected amortized `O(log n)` |
| `increase_key` / `decrease_key` | Expected `O(log n)`, using an expected `O(1)` dictionary lookup |
| `peek` | `O(1)` |
| `is_empty` | `O(1)` |

Here, **expected** accounts for dictionary operations. **Amortized** means the cost is averaged over a sequence of operations; an occasional list resize can make one operation more expensive. The sift itself takes at most `O(log n)`.

## Summary of findings

**Heapsort was the slowest of the three algorithms in all twelve tested configurations.** At n = 20,000, it took 1.55 to 1.77 times as long as Quicksort, even though both have `n log n` average-case growth. The ratio stayed fairly steady from n = 5,000 upward.

| n = 20,000 | Heapsort | Quicksort | Merge Sort |
| --- | --- | --- | --- |
| Random | 33.51 | 21.64 | 26.69 |
| Sorted | 34.79 | 19.67 | 16.83 |
| Reverse | 31.58 | 20.00 | 17.56 |

Times are in milliseconds, using the best of three runs.

**Growth closely matched `n log n`.** Doubling the input from 10,000 to 20,000 predicts a time increase of about 2.15 times. Across random, sorted, and reverse-sorted inputs, the measured increases were:

- Heapsort: 2.16, 2.15, and 2.16.
- Merge Sort: 2.10, 2.11, and 2.13.
- Quicksort: 2.22, 1.99, and 2.15.

**Merge Sort's times varied most with input order.** The table shows the percentage difference between the fastest and slowest input distributions:

| Size | Heapsort | Quicksort | Merge Sort |
| --- | --- | --- | --- |
| n = 10,000 | 10.3% | 6.3% | 59.8% |
| n = 20,000 | 10.2% | 10.0% | 58.6% |

At n = 20,000, Merge Sort was about 37% faster on sorted input than on random input: 16.83 ms compared with 26.69 ms. It is not adaptive in the same way as Timsort. However, when every value in one sorted run is smaller than every value in the other, the merge finishes the first run early. It then copies the remaining values in bulk instead of comparing them one by one.

**The roughly 10% differences do not prove that Heapsort's work is independent of input order.** The differences are small, similar at both larger sizes, and comparable to the timing variation seen elsewhere in the results. A fixed heap shape limits how far heapify can move, but the values still affect how far it actually moves. Input order can change the work performed; it cannot make this Heapsort implementation exceed its `O(n log n)` upper bound.

Counting comparisons would give an exact measure of comparison work for a given input and set of algorithm choices, without machine timing noise. It would not measure every cause of running-time differences. These timings show no clear change in growth pattern caused by input distribution for any of the three algorithms within the tested sizes.

**The n = 1,000 results are too short to support strong conclusions.** Every recorded time is below 2 ms, so small timing disturbances can produce large percentage differences. All three algorithms showed a 55–67% difference across distributions at that size, compared with roughly 10% for Heapsort and Quicksort at the larger sizes. The n = 1,000 row is therefore not used for conclusions.

**The reason Heapsort is slower is a possible explanation, not a measured finding.** A common explanation is its memory-access pattern: the children of index `i` are at `2i+1` and `2i+2`, so the distance between accessed positions roughly doubles as heapify moves down the tree. This can be less cache-friendly than sequential scans. Another possible factor is that standard Heapsort uses roughly twice as many comparisons as Quicksort on average.

**These experiments measure running time only.** They count neither cache misses nor comparisons. The results fit these possible explanations, but do not prove them.

**Heapsort offers a useful combination of time and space guarantees.** It has an `O(n log n)` upper bound for every input and uses `O(1)` auxiliary space. Merge Sort has the same time bound but needs `O(n)` extra space. This Quicksort uses `O(log n)` stack space but can take `O(n²)` time in the worst case. Introsort uses Heapsort as a fallback when Quicksort's recursion becomes too deep.

**`increase_key` needs an index map to reach `O(log n)`.** A heap alone may need `O(n)` time to find a particular task. The heap property compares parents with children, but does not tell you where a specific task is stored. This implementation keeps a `task_id → heap index` dictionary and updates it after every swap. Without the map, searching for the task would make the priority-change operation `O(n)`.

**Automated tests check the queue, in addition to the demo.** The tests cover an empty queue, duplicate and unknown task IDs, and key changes in the wrong direction. A randomized workload also runs 10,000 operations. After each step, it checks that extractions return the highest priority, every parent has a priority at least as high as its children, and the index map matches the heap. Checking the map matters because it could otherwise become incorrect without an obvious error.

**The scheduler showed a limitation of the scheduling policy.** Eight of ten tasks met their deadlines, and **all ten completed**. The other two finished late; they were not starved. Both had priority 1 and early deadlines, but higher-priority tasks ran first.

Starvation means a task keeps waiting and never runs. It can happen if higher-priority tasks keep arriving, but it did not happen in this fixed set of ten tasks.

Two possible changes use the same heap structure:

- Use a min-heap ordered by deadline.
- Use ageing: raise waiting tasks' priorities with `increase_key` as their deadlines approach.

Earliest-deadline-first has a general single-processor optimality guarantee **with preemption**, under the required scheduling assumptions. Preemption means a running task can be paused so another task can run. This simulator is **non-preemptive**: each selected task runs until it finishes. Ordering its queue by deadline may improve deadline performance, but does not give it that optimality guarantee.

## References

Cormen, T. H., Leiserson, C. E., Rivest, R. L., & Stein, C. (2022). *Introduction to algorithms* (4th ed.). MIT Press.

Schaffer, R., & Sedgewick, R. (1993). The analysis of heapsort. *Journal of Algorithms, 15*(1), 76–100.

Williams, J. W. J. (1964). Algorithm 232: Heapsort. *Communications of the ACM, 7*(6), 347–348.

