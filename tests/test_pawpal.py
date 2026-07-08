"""Tests for core PawPal+ behaviors."""

from datetime import date

from pawpal_system import Owner, Pet, Priority, Scheduler, Task


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


def test_sort_orders_by_time_then_priority_with_unscheduled_last():
    """Tasks sort by scheduled_time, ties break on priority, unscheduled last."""
    late = Task("Late", "c", 10, Priority.LOW, scheduled_time=600)
    early_low = Task("Early low", "c", 10, Priority.LOW, scheduled_time=480)
    early_high = Task("Early high", "c", 10, Priority.HIGH, scheduled_time=480)
    unscheduled = Task("Someday", "c", 10, Priority.HIGH)

    scheduler = Scheduler(tasks=[late, early_low, unscheduled, early_high])
    titles = [t.title for t in scheduler.sort_tasks()]

    assert titles == ["Early high", "Early low", "Late", "Someday"]


def test_filter_by_status_splits_completed_and_pending():
    """filter_by_status returns only tasks matching the requested status."""
    done = Task("Done", "c", 10)
    done.mark_complete()
    pending = Task("Pending", "c", 10)
    scheduler = Scheduler(tasks=[done, pending])

    assert scheduler.filter_by_status(True) == [done]
    assert scheduler.filter_by_status(False) == [pending]


def test_filter_by_pet_returns_only_that_pets_tasks():
    """filter_by_pet returns the named pet's tasks (empty list if not found)."""
    dog = Pet("Buddy", "Lab", 4)
    dog.add_task(Task("Walk", "walk", 30))
    cat = Pet("Milo", "Tabby", 2)
    cat.add_task(Task("Litter", "clean", 10))
    owner = Owner("Sam", pets=[dog, cat])
    scheduler = owner.build_scheduler("today")

    assert scheduler.filter_by_pet(owner, "Buddy") == dog.tasks
    assert scheduler.filter_by_pet(owner, "Nobody") == []


def test_daily_recurrence_advances_due_date_by_one_day():
    """Completing a daily task returns a fresh occurrence due one day later."""
    task = Task("Walk", "walk", 30, recurrence="daily", due_date=date(2026, 7, 7))

    nxt = task.complete_and_reschedule()

    assert task.completed is True
    assert nxt.completed is False
    assert nxt.due_date == date(2026, 7, 8)


def test_weekly_recurrence_advances_due_date_by_seven_days():
    """A weekly task's next occurrence is due seven days later."""
    task = Task("Grooming", "groom", 20, recurrence="weekly", due_date=date(2026, 7, 7))

    nxt = task.next_occurrence()

    assert nxt.due_date == date(2026, 7, 14)


def test_non_recurring_task_has_no_next_occurrence():
    """A non-recurring task returns None for its next occurrence."""
    task = Task("One-off", "c", 10, due_date=date(2026, 7, 7))

    assert task.next_occurrence() is None


def test_detect_conflicts_flags_same_scheduled_time():
    """detect_conflicts returns a message when two tasks share a start time."""
    a = Task("Feeding", "food", 15, scheduled_time=540)
    b = Task("Vet call", "admin", 10, scheduled_time=540)
    solo = Task("Walk", "walk", 30, scheduled_time=480)
    scheduler = Scheduler(tasks=[a, b, solo])

    conflicts = scheduler.detect_conflicts()

    assert len(conflicts) == 1
    assert "09:00" in conflicts[0]
