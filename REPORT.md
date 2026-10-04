# Heap Data Structures: Implementation, Analysis, and Applications

All numbers in this report come from the run saved saved as `heapsort_result.png` and `priority_queue.png`..

## Part 1: Heapsort

### 1.1 Implementation

Heapsort is implemented in `heapsort.py` using three functions.

**`max_heapify(arr, i, heap_size)`** restores the max-heap property at index `i`. It assumes that the subtrees below this position are already heaps. The function compares `arr[i]` with its children at `2i+1` and `2i+2`. If a child is larger, it swaps the parent with the larger child and repeats at the child's position. It uses a loop instead of recursion, avoiding `O(log n)` recursion-stack space and keeping auxiliary space constant.

**`build_max_heap(arr)`** turns an unordered array into a max-heap. It calls `max_heapify` from index `n//2 - 1` down to 0. Positions from `n//2` onward are leaves. A single leaf already forms a valid heap, so these positions need no work.

**`heapsort(arr)`** first builds the max-heap. It then swaps the root, which holds the maximum value, with the last element of the active heap. It reduces the heap size by one and calls `max_heapify` on the new root. After `n-1` iterations, the array is sorted in ascending order, in place.

### 1.2 Time Complexity

**Building the max-heap takes `O(n)`.** Multiplying `n/2` heapify calls by `O(log n)` gives a loose `O(n log n)` bound, but assumes that every call travels the full tree height. Most calls do much less work.

A node at height `h` takes `O(h)` heapify work. A heap with `n` elements has at most `⌈n/2^(h+1)⌉` nodes at that height. The total work is bounded by:

```text
Σ (h = 0 to ⌊lg n⌋) ⌈n/2^(h+1)⌉ · O(h) = O(n)
```

The main part of the bound is `O(n · Σ h/2^h)`. Since `Σ (h = 0 to ∞) h/2^h = 2`, this part is `O(2n) = O(n)`. Rounding the node counts upward adds at most `O((log n)²)`, which does not change the final `O(n)` bound. Most nodes are near the leaves, where heapify does little work. Only a few nodes near the root can require the full `log n` descent. Here, `lg` means logarithm to base 2.

**The extraction phase takes `O(n log n)`.** There are `n-1` iterations. Each performs a constant-time swap and one `max_heapify` call on a heap of size `k`. Heapify takes at most `O(lg k)` work. Adding these upper bounds gives:

```text
Σ (k = 1 to n-1) lg k = lg((n-1)!) = O(n lg n)
```

Total time: `O(n) + O(n lg n) = O(n lg n)`.

**This calculation proves an upper bound.** It adds the maximum possible costs of heapify calls. It does not prove that every input takes that much work. A separate lower-bound argument is needed before calling the result `Θ(n log n)`.

- **Upper bound: `O(n log n)` for every input.** Array positions determine the heap's shape. A heap with `n` elements is a complete binary tree of height `⌊lg n⌋`, regardless of its values. Heapify therefore cannot move down more than `⌊lg n⌋` levels. Input order can affect how far it actually moves, but cannot make Heapsort exceed this upper bound. Quicksort differs because its partition sizes depend on the values and pivot rule.
- **Worst case: `Θ(n log n)`.** Some inputs force long descents during enough extractions to reach this bound.
- **All-equal input: `Θ(n)` for this implementation.** When all values are equal, no child is larger than its parent. Each heapify call stops after checking the immediate children, so the complete sort takes `Θ(n)` work. Thus, a claim of `Θ(n log n)` for every input would be incorrect.
- **Distinct keys: a separate `Ω(n log n)` lower bound.** For arrays with no repeated keys, the analysis of Schaffer and Sedgewick (1993) establishes a matching asymptotic lower bound. Combined with the upper bound, this gives `Θ(n log n)`. This result is cited here; it does not follow from the upper-bound calculation above.
- **Average case: `Θ(n log n)` under the stated input model.** The model is a uniformly random permutation of distinct keys. The distinct-key analysis supports this expected cost. An average-case statement therefore depends on an input distribution; it is not a statement about every input.

### 1.3 Space Complexity

Heapsort sorts **in place**. It uses the input array as the heap and needs only a constant number of index and temporary variables. Its auxiliary space is therefore `O(1)`. Using a loop for `max_heapify` preserves this bound. A recursive version would need `O(log n)` stack frames.

The three sorting implementations use different amounts of extra memory:

| Algorithm | Auxiliary space | Reason |
| --- | --- | --- |
| Heapsort | `O(1)` | A constant number of variables; heapify uses a loop |
| Quicksort (this implementation) | `O(log n)` | It recursively sorts the smaller partition and uses a loop for the larger one, keeping stack depth within `O(log n)` |
| Merge Sort | `O(n)` | Merging builds new lists; peak extra storage is linear |

This Quicksort still uses a recursion stack. Processing only the smaller partition recursively limits its depth to about `⌊lg n⌋`; it does not remove the stack.

Heapsort is **not stable**. Its extraction swaps can change the relative order of elements with equal keys.

### 1.4 Empirical Comparison

Heapsort, randomized Quicksort, and Merge Sort were timed on random, sorted, and reverse-sorted integer arrays. Each table entry is the best of three runs, in milliseconds.

| n | Distribution | Heapsort | Quicksort | Merge Sort |
| --- | --- | --- | --- | --- |
| 1,000 | Random | 1.07 | 0.85 | 0.97 |
| 1,000 | Sorted | 1.66 | 1.42 | 0.73 |
| 1,000 | Reverse | 1.29 | 1.03 | 1.16 |
| 5,000 | Random | 10.34 | 6.00 | 5.90 |
| 5,000 | Sorted | 7.55 | 4.72 | 3.92 |
| 5,000 | Reverse | 8.05 | 4.63 | 4.01 |
| 10,000 | Random | 15.49 | 9.76 | 12.72 |
| 10,000 | Sorted | 16.15 | 9.90 | 7.96 |
| 10,000 | Reverse | 14.64 | 9.31 | 8.25 |
| 20,000 | Random | 33.51 | 21.64 | 26.69 |
| 20,000 | Sorted | 34.79 | 19.67 | 16.83 |
| 20,000 | Reverse | 31.58 | 20.00 | 17.56 |

**Treat the n = 1,000 results cautiously.** Every recorded time is below 2 ms. At this size, all three algorithms show a 55–67% difference between their fastest and slowest distributions. Heapsort and Quicksort show differences of roughly 10% or less at n = 10,000 and n = 20,000. Short measurements are more sensitive to timing overhead and interruptions from other processes. The discussion therefore focuses on the larger sizes, whose patterns are more consistent.

**Heapsort was slowest in all twelve configurations.** At n = 20,000, it took 1.55 to 1.77 times as long as Quicksort, depending on distribution. At every tested configuration from n = 5,000 upward, the ratio stayed within that range. At n = 1,000, the ratio was smaller, at 1.17 to 1.26. Fixed overheads may explain some of this difference at the smaller size.

**Growth closely matched `n log n`.** Doubling the input from 10,000 to 20,000 predicts a time increase of about 2.15 times. The measured ratios were:

| Algorithm | Random | Sorted | Reverse |
| --- | --- | --- | --- |
| Heapsort | 2.16 | 2.15 | 2.16 |
| Quicksort | 2.22 | 1.99 | 2.15 |
| Merge Sort | 2.10 | 2.11 | 2.13 |

All three Heapsort ratios are within 0.02 of the predicted 2.1505. This is close agreement for a single benchmark run, so it should not be treated as exact proof of the growth rate. The increase from 5,000 to 10,000 is less consistent, with ratios from 1.50 to 2.16. At n = 5,000, the random-input times for Heapsort and Quicksort are somewhat higher than their sorted and reverse-sorted times. Measurement variation may contribute to that pattern.

**Input order affected the recorded times differently.** The table below shows the percentage difference between the fastest and slowest distributions at each size:

| Size | Heapsort | Quicksort | Merge Sort |
| --- | --- | --- | --- |
| n = 10,000 | 10.3% | 6.3% | 59.8% |
| n = 20,000 | 10.2% | 10.0% | 58.6% |

Heapsort and randomized Quicksort vary by about 10% or less, while Merge Sort varies by nearly 60%. Merge Sort shows the larger and more consistent difference, with an implementation-based explanation given below.

The smaller differences for Heapsort do not prove that its work is independent of input order. The fixed heap shape guarantees its height and its `O(n log n)` upper bound, but values still affect comparisons, swaps, and the distance travelled by heapify. These timings cannot separate all such effects from measurement noise. Counting comparisons would measure comparison work exactly for a given input and sequence of algorithm choices, without machine timing noise. It would not measure every cause of differences in elapsed time.

Within the tested sizes, no input distribution shows a clear change toward quadratic growth for any of the three algorithms. This describes the recorded measurements; it does not replace the theoretical analysis.

**Merge Sort was faster on ordered input than on random input.** At n = 20,000, it took 16.83 ms on sorted input and 17.56 ms on reverse-sorted input, compared with 26.69 ms on random input. Sorted input was about 37% faster; reverse-sorted input was about 34% faster. Ordered input was also faster at n = 5,000 and n = 10,000.

Merge Sort is not adaptive in the same way as Timsort. However, when every value in one sorted run is smaller than every value in the other, merging finishes one run early. It then uses a bulk `extend` instead of continuing to compare elements one by one. On this ordered input, its comparison count is closer to `n lg n / 2`. Merge Sort therefore showed the greatest sensitivity to input order in this comparison. At n = 1,000, sorted input was still fastest, but reverse-sorted input was slightly slower than random input. Given the short timings, that difference should be interpreted cautiously.

**Possible reasons Heapsort was slower.** A common explanation is its memory-access pattern. The children of index `i` are at `2i+1` and `2i+2`, so the distance between accessed positions roughly doubles as `max_heapify` moves down the heap. Quicksort's partition step and Merge Sort's merge step instead scan sequentially. Standard Heapsort also uses roughly twice as many comparisons as Quicksort on average. Each extraction moves an element from the bottom of the heap to the root before sifting it down again.

**These experiments measure elapsed time only.** They count neither cache misses nor comparisons. The results fit these possible explanations, but do not prove them. Hardware performance counters could measure cache behavior; an instrumented comparison counter could measure comparison work.

**Heapsort combines useful time and space guarantees.** Among these three implementations, it provides both an `O(n log n)` upper bound for every input and `O(1)` auxiliary space. Merge Sort has the same time bound but needs `O(n)` extra memory. This Quicksort needs `O(log n)` stack space and can take `O(n²)` time under an unlucky sequence of pivots. Introsort uses Heapsort as a fallback when Quicksort's recursion becomes too deep.

**Pivot choice matters.** A deterministic pivot rule does not automatically make Quicksort quadratic on sorted input. Choosing the first or last element does produce maximally unbalanced partitions on sorted input. Median-of-three is also deterministic, but handles sorted input well. This implementation selects a uniformly random pivot, helping it avoid a systematic disadvantage on sorted or reverse-sorted inputs.

## Part 2: Priority Queue

### 2.1 Data Structure Choice

The heap is stored in a **Python list**, which is a dynamic array. For a node at index `i`:

```text
parent   = (i - 1) // 2
children = 2i + 1, 2i + 2
```

An array suits a binary heap because the heap is a **complete binary tree**. Every level is full except possibly the last, which fills from left to right. Its nodes therefore fit into consecutive array positions without gaps. Parent and child positions are calculated with arithmetic instead of following separate tree links.

Compared with a tree of linked nodes, this representation avoids separate parent and child pointers for each node. A Python list still stores references to its `Task` objects, but these references occupy consecutive positions, improving locality. Appending takes amortized `O(1)` time.

The heap inserts at the end and removes from the end. An end `pop()` avoids shifting the other elements and has amortized `O(1)` cost. Removing from the front would take `O(n)` because the remaining elements must shift. This is why `extract_max` fills the root position with the last element.

### 2.2 Task Representation

```python
class Task:
    def __init__(self, task_id, priority, arrival_time, deadline, duration=1):
```

The scheduler uses all five fields:

- `task_id`: identifies the task and is used as the index dictionary's key.
- `priority`: determines the task's position in the heap.
- `arrival_time`: records when the task becomes available.
- `deadline`: records when the task should finish.
- `duration`: records how long the task occupies the processor.

### 2.3 Max-Heap Versus Min-Heap

The implementation uses a **max-heap** because its policy is **highest priority first**. The task with the largest priority value is at the root. Reading it takes `O(1)`, and removing it requires at most `O(log n)` heap adjustment.

A min-heap fits other policies. Earliest-deadline-first needs the smallest deadline at the root, while shortest-job-first needs the smallest duration. These use the same heap structure, with a different ordering key and reversed comparisons in `_sift_up` and `_sift_down`. The scheduling policy determines the choice.

### 2.4 Core Operations

| Operation | Time | Reason |
| --- | --- | --- |
| `insert(task)` | Expected amortized `O(log n)` | Amortized `O(1)` append, followed by at most `⌊lg n⌋` sift-up levels |
| `extract_max()` | Expected amortized `O(log n)` | Save the root, move the last element to it, and sift down at most `⌊lg n⌋` levels |
| `increase_key` / `decrease_key` | Expected `O(log n)` | Expected `O(1)` index lookup, followed by a sift in one direction |
| `peek()` | `O(1)` | The maximum is always at index 0 |
| `is_empty()` | `O(1)` | Check whether the list length is zero |

**Expected** accounts for the hash-table dictionary operations. **Amortized** accounts for occasional resizing of the list or dictionary. The sift itself always travels at most `O(log n)` levels.

**Total storage is `O(n)`.** The heap list holds `n` task references and the index dictionary holds `n` entries. Each task therefore has both a heap entry and a dictionary entry. This adds storage compared with a bare heap; the actual memory use is not necessarily exactly twice as large.

**`insert(task)`** appends the task and calls `_sift_up`. The new task swaps with its parent while its priority is higher. The tree height, `⌊lg n⌋`, limits the number of swaps. Appending is amortized `O(1)` because a Python list occasionally reallocates its storage. A single append that triggers resizing can take `O(n)`.

**`extract_max()`** saves the root and pops the last element. If tasks remain, it places that last element at the root and calls `_sift_down`. The tree height again limits the number of swaps. Removing from the end avoids shifting the rest of the list.

**`increase_key` / `decrease_key`** must locate a task before changing its priority. A bare heap may need an `O(n)` search: the heap property compares parents with children, but does not give the location of a particular task.

The implementation keeps a dictionary mapping each `task_id` to its heap position. `_swap` updates this dictionary after every swap so the positions stay correct. Dictionary lookup is **expected `O(1)`**. Python dictionaries are hash tables, and many colliding keys can make lookup slower. Under the expected-cost model, lookup followed by sifting takes `O(log n)` overall. Without the map, searching would make the operation `O(n)`.

An index map is not the only option. A caller-held handle that identifies the task's current heap position can also avoid the linear search.

Increasing a priority can move the task toward the root. Decreasing it can move the task toward the leaves. Only one sift direction is needed. `change_priority` chooses that direction. `increase_key` and `decrease_key` call it and reject changes in the wrong direction.

**`is_empty()`** checks whether the list length is zero. Python answers this in `O(1)` time.

**Equal priorities have no guaranteed order.** Their extraction order depends on the heap's history and does not preserve arrival order. FIFO ordering among ties would need a secondary key, such as an increasing sequence number. `arrival_time` could also be used if ties in arrival time are acceptable. The current order is repeatable for the same sequence of operations, but should not be treated as a fairness guarantee.

### 2.5 Verification

`priority_queue.py` runs automated tests before its demonstration. The tests cover:

- An empty queue, including exceptions from `extract_max` and `peek`.
- Inserting and extracting a single task.
- Duplicate task IDs.
- Unknown task IDs.
- `increase_key` and `decrease_key` used in the wrong direction.
- Inserting twenty equal-priority tasks and checking that all twenty are returned.

The main test runs 10,000 randomly mixed insertions, extractions, and priority changes against a reference dictionary. After each operation, it checks that the queue size matches the reference, extracted tasks have the true maximum priority, each parent's priority is at least as high as its children's, and the index dictionary matches the heap.

Checking the dictionary matters because incorrect positions could cause `increase_key` to modify the wrong task and damage the heap without immediately raising an error.

### 2.6 Scheduler Simulation

`simulate()` models one processor using **non-preemptive scheduling**. At each scheduling step, it inserts every task that has arrived. It then selects the highest-priority waiting task and runs it until completion. The clock advances by that task's duration. If no task is ready, the clock jumps to the next arrival time.

```text
  t=  0-2   task 2    priority 10  deadline 30   ok
  t=  2-6   task 6    priority 10  deadline 32   ok
  t=  6-8   task 9    priority 10  deadline 31   ok
  t=  8-9   task 0    priority 6   deadline 26   ok
  t=  9-10  task 8    priority 5   deadline 18   ok
  t= 10-14  task 4    priority 2   deadline 16   ok
  t= 14-17  task 1    priority 2   deadline 17   ok
  t= 17-19  task 7    priority 1   deadline 15   LATE
  t= 19-23  task 3    priority 1   deadline 27   ok
  t= 23-25  task 5    priority 1   deadline 17   LATE
```

Eight of ten tasks met their deadlines, and **all ten completed**. The other two finished late; they were not starved. Both had priority 1 and early deadlines. Task 7 had deadline 15 and finished at 19. Task 5 had deadline 17 and finished at 25. Higher-priority work was selected ahead of them.

The queue followed the chosen policy. Highest-priority-first uses priority to select tasks and does not use their deadlines. A low-priority task with an early deadline can therefore be delayed.

**Starvation** means that a task keeps waiting and never runs. It is a risk if higher-priority tasks keep arriving, but this fixed workload of ten tasks does not show starvation.

Two possible changes use the existing heap structure, each with a limitation.

First, a min-heap ordered by deadline gives **earliest-deadline-first (EDF)**. Its general optimality guarantee on one processor assumes **preemption**, under the required scheduling assumptions. Preemption lets the processor pause a running task to run another. This simulator is non-preemptive, so changing the key may improve deadline performance but does not provide that guarantee. A long task already running can still make a newly arrived task miss its deadline. Meeting deadlines without preemption is a harder scheduling problem.

Second, the max-heap can use **ageing**. Waiting tasks receive higher priorities as their deadlines approach, using the `increase_key` operation from Section 2.4. The policy still considers priority, but can reduce long delays. Preventing indefinite waiting requires a suitable ageing rule; its effectiveness depends on how quickly priorities increase and how new tasks are prioritized.

## Conclusion

Heapsort has an `O(n log n)` upper bound for every input and a `Θ(n log n)` worst case, using `O(1)` auxiliary space. The fixed heap height prevents any input ordering from exceeding that upper bound. A separate result gives a tight bound for distinct keys (Schaffer & Sedgewick, 1993). All-equal input takes only `Θ(n)` in this implementation.

Heapsort was slowest in all twelve measured configurations. At n = 20,000, it took 1.55 to 1.77 times as long as randomized Quicksort. Doubling the input from 10,000 to 20,000 increased its time by 2.16, 2.15, and 2.16 across the three distributions, close to the predicted 2.15 for `n log n` growth.

Timing alone does not answer every performance question. Heapsort's roughly 10% variation does not separate all input effects from measurement noise. Its fixed shape guarantees the upper bound, not identical work on every input. Comparison counts would measure comparison work, but would not fully explain elapsed-time differences or cache effects. Within the tested sizes, no distribution showed a clear change toward quadratic growth. Merge Sort showed the largest variation with input distribution, at nearly 60%.

Heapsort combines a worst-case time guarantee with constant extra space. Merge Sort needs `O(n)` extra space, while this Quicksort can take `O(n²)` time in the worst case.

The array-backed priority queue uses `O(n)` total storage. Under the expected and amortized cost assumptions described above, insertions, extract-max, and key changes take `O(log n)`, while peek and emptiness checks take `O(1)`. The index map avoids an `O(n)` task search during key changes. The 10,000-operation randomized test passed its checks of heap order and index-map consistency.

The scheduler showed how highest-priority-first can delay urgent low-priority tasks: two of ten tasks finished after their deadlines. Deadline-based scheduling and priority ageing are possible changes using the same heap structure. Neither gives this non-preemptive simulator EDF's general optimality guarantee; priority ageing also has no such guarantee simply because preemption is available.

## References

Cormen, T. H., Leiserson, C. E., Rivest, R. L., & Stein, C. (2022). *Introduction to algorithms* (4th ed.). MIT Press.

Schaffer, R., & Sedgewick, R. (1993). The analysis of heapsort. *Journal of Algorithms, 15*(1), 76–100.

Williams, J. W. J. (1964). Algorithm 232: Heapsort. *Communications of the ACM, 7*(6), 347–348.
