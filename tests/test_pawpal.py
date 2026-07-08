"""Tests for core PawPal+ behaviors."""

from pawpal_system import Pet, Task


def test_mark_complete_changes_status():
    """Calling mark_complete() flips a task's completed flag to True."""
    task = Task("Morning walk", "exercise", 30)
    assert task.completed is False

    task.mark_complete()

    assert task.completed is True


def test_add_task_increases_pet_task_count():
    """Adding a task to a Pet increases that pet's task count by one."""
    pet = Pet("Biscuit", "Golden Retriever", 3)
    assert len(pet.tasks) == 0

    pet.add_task(Task("Feeding", "food", 10))

    assert len(pet.tasks) == 1
