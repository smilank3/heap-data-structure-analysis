"""
Priority queue using a binary max-heap and a task scheduler.

Run:  python priority_queue.py
"""

import random


class Task:
    """A task that needs to be scheduled.

    Attributes:
        task_id:      unique ID for the task
        priority:     higher number means higher priority
        arrival_time: time when the task becomes available
        deadline:     time when the task should be finished
        duration:     how long the task takes to finish
    """

    def __init__(self, task_id, priority, arrival_time, deadline, duration=1):
        self.task_id = task_id
        self.priority = priority
        self.arrival_time = arrival_time
        self.deadline = deadline
        self.duration = duration

    def __repr__(self):
        return (f"Task(id={self.task_id}, priority={self.priority}, "
                f"arrival={self.arrival_time}, deadline={self.deadline})")


class MaxPriorityQueue:
    """A max-heap that stores Task objects based on priority.

    The heap is stored in a Python list.
    For an item at index i:
        parent   = (i - 1) // 2
        children = 2i + 1, 2i + 2

    These positions let us find parents and children without using pointers.
    A dictionary stores each task's position in the heap.

    The dictionary helps us find a task quickly when changing its priority.
    Without it, we would have to search the whole heap, which would take O(n).
    """

    def __init__(self):
        self._heap = []        # list of Task objects
        self._index = {}       # task_id -> position in the heap

    # ---------------- internal helpers ----------------

    def _swap(self, i, j):
        self._heap[i], self._heap[j] = self._heap[j], self._heap[i]
        self._index[self._heap[i].task_id] = i
        self._index[self._heap[j].task_id] = j

    def _sift_up(self, i):
        """Move an item up if its priority is higher than its parent. O(log n)."""
        while i > 0:
            parent = (i - 1) // 2
            if self._heap[i].priority <= self._heap[parent].priority:
                return
            self._swap(i, parent)
            i = parent

    def _sift_down(self, i):
        """Move an item down if a child has a higher priority. O(log n)."""
        size = len(self._heap)
        while True:
            left, right = 2 * i + 1, 2 * i + 2
            largest = i
            if left < size and self._heap[left].priority > self._heap[largest].priority:
                largest = left
            if right < size and self._heap[right].priority > self._heap[largest].priority:
                largest = right
            if largest == i:
                return
            self._swap(i, largest)
            i = largest

    # ---------------- public operations ----------------

    def insert(self, task):
        """Add a task to the queue. O(log n)."""
        if task.task_id in self._index:
            raise ValueError(f"duplicate task_id: {task.task_id}")
        self._heap.append(task)
        self._index[task.task_id] = len(self._heap) - 1
        self._sift_up(len(self._heap) - 1)

    def extract_max(self):
        """Remove and return the task with the highest priority. O(log n).

        The highest-priority task is at the root.
        Move the last item to the root and move it down to fix the heap.
        """
        if not self._heap:
            raise IndexError("extract_max from an empty priority queue")

        top = self._heap[0]
        last = self._heap.pop()
        del self._index[top.task_id]

        if self._heap:                      # the queue still has tasks
            self._heap[0] = last
            self._index[last.task_id] = 0
            self._sift_down(0)

        return top

    def peek(self):
        """Return the highest-priority task without removing it. O(1)."""
        if not self._heap:
            raise IndexError("peek on an empty priority queue")
        return self._heap[0]

    def change_priority(self, task_id, new_priority):
        """Change a task's priority and fix the heap. O(log n).

        If the priority increases, move the task up.
        If the priority decreases, move the task down.
        The index dictionary lets us find the task in O(1) time.
        """
        if task_id not in self._index:
            raise KeyError(f"no such task: {task_id}")

        i = self._index[task_id]
        old = self._heap[i].priority
        self._heap[i].priority = new_priority

        if new_priority > old:
            self._sift_up(i)
        elif new_priority < old:
            self._sift_down(i)

    def increase_key(self, task_id, new_priority):
        """Increase a task's priority. O(log n)."""
        if new_priority < self._heap[self._index[task_id]].priority:
            raise ValueError("new priority is lower than the current one")
        self.change_priority(task_id, new_priority)

    def decrease_key(self, task_id, new_priority):
        """Decrease a task's priority. O(log n)."""
        if new_priority > self._heap[self._index[task_id]].priority:
            raise ValueError("new priority is higher than the current one")
        self.change_priority(task_id, new_priority)

    def is_empty(self):
        """Return True if there are no tasks. O(1)."""
        return len(self._heap) == 0

    def __len__(self):
        return len(self._heap)


# ----------------------------------------------------------------------
# Scheduler simulation
# ----------------------------------------------------------------------

def simulate(tasks, verbose=True):
    """Run tasks on one processor, always choosing the highest priority.

    At each time step, add all tasks that have arrived.
    Then run the highest-priority waiting task until it is finished.

    A running task cannot be stopped by a new task.
    """
    pending = sorted(tasks, key=lambda t: t.arrival_time)
    queue = MaxPriorityQueue()
    clock = 0
    next_arrival = 0
    completed = []

    while next_arrival < len(pending) or not queue.is_empty():
        # Add all tasks that have arrived.
        while next_arrival < len(pending) and pending[next_arrival].arrival_time <= clock:
            queue.insert(pending[next_arrival])
            next_arrival += 1

        if queue.is_empty():
            clock = pending[next_arrival].arrival_time   # Wait for the next task.
            continue

        task = queue.extract_max()
        start = clock
        clock += task.duration
        late = clock > task.deadline
        completed.append((task, start, clock, late))

        if verbose:
            flag = "LATE" if late else "ok"
            print(f"  t={start:>3}-{clock:<3} task {task.task_id:<4} "
                  f"priority {task.priority:<3} deadline {task.deadline:<4} {flag}")

    return completed


def run_tests():
    """Test that the priority queue works correctly."""
    failures = []

    def check(cond, msg):
        if not cond:
            failures.append(msg)

    def invariants_hold(pq):
        """Check that the heap and index dictionary are correct."""
        for i in range(1, len(pq._heap)):
            if pq._heap[(i - 1) // 2].priority < pq._heap[i].priority:
                return False
        if len(pq._index) != len(pq._heap):
            return False
        return all(pq._heap[pos].task_id == tid for tid, pos in pq._index.items())

    # --- test empty queue ---
    pq = MaxPriorityQueue()
    check(pq.is_empty(), "a new queue should be empty")
    check(len(pq) == 0, "a new queue should have length 0")
    for op in (pq.extract_max, pq.peek):
        try:
            op()
            failures.append(f"{op.__name__} on an empty queue should raise")
        except IndexError:
            pass

    pq.insert(Task("solo", 5, 0, 10))
    check(not pq.is_empty(), "queue with one task is not empty")
    check(pq.extract_max().task_id == "solo", "single extract")
    check(pq.is_empty(), "queue empty again after extracting the only task")

    # --- test duplicate and unknown task IDs ---
    pq = MaxPriorityQueue()
    pq.insert(Task("X", 1, 0, 10))
    try:
        pq.insert(Task("X", 2, 0, 10))
        failures.append("duplicate task_id should raise")
    except ValueError:
        pass
    try:
        pq.change_priority("missing", 5)
        failures.append("unknown task_id should raise")
    except KeyError:
        pass
    try:
        pq.increase_key("X", 0)
        failures.append("increase_key to a lower value should raise")
    except ValueError:
        pass
    try:
        pq.decrease_key("X", 99)
        failures.append("decrease_key to a higher value should raise")
    except ValueError:
        pass

    # --- test tasks with the same priority ---
    pq = MaxPriorityQueue()
    for i in range(20):
        pq.insert(Task(i, 5, arrival_time=i, deadline=100))
    drained = {pq.extract_max().task_id for _ in range(20)}
    check(drained == set(range(20)), "all equal-priority tasks must be returned")

    # --- test the queue with random tasks ---
    rng = random.Random(123)
    pq = MaxPriorityQueue()
    reference = {}          # task_id -> priority
    next_id = 0

    for step in range(10000):
        roll = rng.random()

        if roll < 0.45 or not reference:
            pq.insert(Task(next_id, rng.randint(0, 1000), 0, 100))
            reference[next_id] = pq._heap[pq._index[next_id]].priority
            next_id += 1
        elif roll < 0.75:
            task = pq.extract_max()
            expected = max(reference.values())
            if task.priority != expected:
                failures.append(f"step {step}: extracted {task.priority}, "
                                f"highest was {expected}")
                break
            del reference[task.task_id]
        else:
            tid = rng.choice(list(reference))
            new_p = rng.randint(0, 1000)
            pq.change_priority(tid, new_p)
            reference[tid] = new_p

        if len(pq) != len(reference):
            failures.append(f"step {step}: size {len(pq)} != {len(reference)}")
            break
        if not invariants_hold(pq):
            failures.append(f"step {step}: heap or index-map invariant broken")
            break

    check(invariants_hold(pq), "invariants must hold at the end of the workload")

    print(f"Correctness: {'all checks passed' if not failures else 'FAILURES'}")
    for f in failures:
        print("  FAIL:", f)
    print()
    return not failures


def run_demo():
    print("PRIORITY QUEUE OPERATIONS\n")
    pq = MaxPriorityQueue()
    print(f"  is_empty on a new queue: {pq.is_empty()}")

    for tid, pr in [("A", 3), ("B", 7), ("C", 5), ("D", 1), ("E", 9)]:
        pq.insert(Task(tid, pr, arrival_time=0, deadline=20))
    print(f"  after 5 inserts: size {len(pq)}, highest priority "
          f"{pq.peek().task_id} ({pq.peek().priority})")

    pq.increase_key("D", 10)
    print(f"  increase_key(D, 10) -> highest is now "
          f"{pq.peek().task_id} ({pq.peek().priority})")

    pq.decrease_key("D", 2)
    print(f"  decrease_key(D, 2)  -> highest is now "
          f"{pq.peek().task_id} ({pq.peek().priority})")

    order = []
    while not pq.is_empty():
        t = pq.extract_max()
        order.append(f"{t.task_id}({t.priority})")
    print(f"  extraction order: {' > '.join(order)}")
    print(f"  is_empty after draining: {pq.is_empty()}\n")

    print("SCHEDULER SIMULATION\n")
    rng = random.Random(7)
    tasks = [
        Task(task_id=i,
             priority=rng.randint(1, 10),
             arrival_time=rng.randint(0, 12),
             deadline=rng.randint(14, 32),
             duration=rng.randint(1, 4))
        for i in range(10)
    ]
    for t in sorted(tasks, key=lambda t: t.arrival_time):
        print(f"  {t} duration={t.duration}")
    print()

    completed = simulate(tasks)
    late = sum(1 for *_, l in completed if l)
    print(f"\n  {len(completed)} tasks completed, {late} missed their deadline")


if __name__ == "__main__":
    print()
    if run_tests():
        run_demo()
