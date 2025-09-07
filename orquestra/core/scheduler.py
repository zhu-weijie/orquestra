from collections import deque
from typing import Dict, List, Set

from orquestra.models import Task


def resolve_task_order(tasks: List[Task]) -> List[List[Task]]:
    """
    Resolves the execution order of tasks based on their dependencies using
    a topological sort algorithm.

    Args:
        tasks: A list of Task objects.

    Returns:
        A list of lists, where each inner list is a "batch" of tasks
        that can be executed in parallel.

    Raises:
        ValueError: If a circular dependency is detected in the tasks.
    """
    # Create a mapping of task names to task objects for easy lookup
    task_map: Dict[str, Task] = {task.name: task for task in tasks}

    # Build the adjacency list and in-degree map
    adj: Dict[str, Set[str]] = {name: set() for name in task_map}
    in_degree: Dict[str, int] = {name: 0 for name in task_map}

    for task in tasks:
        for dep in task.depends_on:
            if dep not in task_map:
                raise ValueError(
                    f"Task '{task.name}' depends on non-existent task '{dep}'."
                )
            # A depends on B means an edge from B to A
            adj[dep].add(task.name)
            in_degree[task.name] += 1

    # Initialize the queue with all tasks that have no dependencies
    queue: deque[str] = deque(
        [name for name, degree in in_degree.items() if degree == 0]
    )

    execution_plan: List[List[Task]] = []
    resolved_tasks_count = 0

    while queue:
        batch_size = len(queue)
        current_batch: List[Task] = []

        for _ in range(batch_size):
            task_name = queue.popleft()
            current_batch.append(task_map[task_name])
            resolved_tasks_count += 1

            for neighbor_name in sorted(
                list(adj[task_name])
            ):  # sort for deterministic order
                in_degree[neighbor_name] -= 1
                if in_degree[neighbor_name] == 0:
                    queue.append(neighbor_name)

        # Sort the batch by name for deterministic output
        current_batch.sort(key=lambda t: t.name)
        execution_plan.append(current_batch)

    if resolved_tasks_count != len(tasks):
        raise ValueError("Circular dependency detected in the workflow tasks.")

    return execution_plan
