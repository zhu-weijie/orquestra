import pytest

from orquestra.core import resolve_task_order
from orquestra.models import Task


# Helper to create dummy tasks
def T(name, deps=None):
    return Task(name=name, agent="dummy", instruction="dummy", depends_on=deps or [])


def test_linear_dependency():
    """Tests A -> B -> C"""
    task_a = T("A")
    task_b = T("B", deps=["A"])
    task_c = T("C", deps=["B"])
    plan = resolve_task_order([task_c, task_b, task_a])  # Order doesn't matter
    assert [[t.name for t in batch] for batch in plan] == [["A"], ["B"], ["C"]]


def test_parallel_tasks():
    """Tests A, B -> C"""
    task_a = T("A")
    task_b = T("B")
    task_c = T("C", deps=["A", "B"])
    plan = resolve_task_order([task_a, task_b, task_c])
    # A and B should be in the first batch, sorted alphabetically
    assert [[t.name for t in batch] for batch in plan] == [["A", "B"], ["C"]]


def test_no_dependencies():
    """Tests A, B, C (all independent)"""
    tasks = [T("C"), T("A"), T("B")]
    plan = resolve_task_order(tasks)
    assert len(plan) == 1
    assert sorted([t.name for t in plan[0]]) == ["A", "B", "C"]


def test_diamond_dependency():
    """Tests A -> B, A -> C, B -> D, C -> D"""
    task_a = T("A")
    task_b = T("B", deps=["A"])
    task_c = T("C", deps=["A"])
    task_d = T("D", deps=["B", "C"])
    plan = resolve_task_order([task_a, task_b, task_c, task_d])
    # B and C should be in the second batch, sorted
    assert [[t.name for t in batch] for batch in plan] == [["A"], ["B", "C"], ["D"]]


def test_circular_dependency_raises_error():
    """Tests A -> B -> A"""
    task_a = T("A", deps=["B"])
    task_b = T("B", deps=["A"])
    with pytest.raises(ValueError, match="Circular dependency detected"):
        resolve_task_order([task_a, task_b])


def test_missing_dependency_raises_error():
    """Tests A -> B, where B is not defined"""
    task_a = T("A", deps=["B"])
    with pytest.raises(ValueError, match="depends on non-existent task 'B'"):
        resolve_task_order([task_a])
