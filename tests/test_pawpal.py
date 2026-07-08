"""Tests for core PawPal+ behaviors.

Tests are grouped by feature: basics, sorting, recurrence, conflicts, and
edge cases. Each test follows an arrange / act / assert structure.
"""

from datetime import date

from pawpal_system import Owner, Pet, Priority, Scheduler, Task


# --- Basics ---------------------------------------------------------------

def test_mark_complete_changes_status():
    """Calling mark_complete() flips a task's completed flag to True."""
    # arrange
    task = Task("Morning walk", "exercise", 30)
    assert task.completed is False

    # act
    task.mark_complete()

    # assert
    assert task.completed is True


def test_add_task_increases_pet_task_count():
    """Adding a task to a Pet increases that pet's task count by one."""
    # arrange
    pet = Pet("Biscuit", "Golden Retriever", 3)
    assert len(pet.tasks) == 0

    # act
    pet.add_task(Task("Feeding", "food", 10))

    # assert
    assert len(pet.tasks) == 1


# --- Sorting --------------------------------------------------------------

def test_schedule_is_returned_in_chronological_order():
    """generate_daily_schedule() returns tasks ordered by scheduled_time."""
    # arrange: tasks created out of chronological order
    noon = Task("Noon", "c", 10, scheduled_time=720)      # 12:00
    morning = Task("Morning", "c", 10, scheduled_time=480)  # 08:00
    evening = Task("Evening", "c", 10, scheduled_time=1080)  # 18:00
    scheduler = Scheduler(tasks=[noon, evening, morning])

    # act
    ordered = scheduler.generate_daily_schedule()

    # assert
    assert [t.title for t in ordered] == ["Morning", "Noon", "Evening"]


def test_same_time_orders_higher_priority_first():
    """When two tasks share a time, the higher priority one comes first."""
    # arrange
    low = Task("Low", "c", 10, Priority.LOW, scheduled_time=480)
    high = Task("High", "c", 10, Priority.HIGH, scheduled_time=480)
    scheduler = Scheduler(tasks=[low, high])

    # act
    ordered = scheduler.sort_tasks()

    # assert
    assert [t.title for t in ordered] == ["High", "Low"]


def test_unscheduled_tasks_sort_to_the_end():
    """Tasks with no scheduled_time appear after scheduled ones."""
    # arrange
    scheduled = Task("Scheduled", "c", 10, scheduled_time=600)
    unscheduled = Task("Someday", "c", 10)
    scheduler = Scheduler(tasks=[unscheduled, scheduled])

    # act
    ordered = scheduler.sort_tasks()

    # assert
    assert [t.title for t in ordered] == ["Scheduled", "Someday"]


# --- Recurrence -----------------------------------------------------------

def test_daily_recurrence_creates_next_occurrence_one_day_later():
    """Completing a daily task creates a fresh occurrence due the next day."""
    # arrange
    task = Task("Walk", "walk", 30, recurrence="daily", due_date=date(2026, 7, 7))

    # act
    nxt = task.complete_and_reschedule()

    # assert
    assert task.completed is True          # original marked done
    assert nxt is not None                 # a new occurrence was created
    assert nxt.completed is False          # the new one starts pending
    assert nxt.due_date == date(2026, 7, 8)


def test_weekly_recurrence_advances_due_date_by_seven_days():
    """A weekly task's next occurrence is due seven days later."""
    # arrange
    task = Task("Grooming", "groom", 20, recurrence="weekly", due_date=date(2026, 7, 7))

    # act
    nxt = task.next_occurrence()

    # assert
    assert nxt.due_date == date(2026, 7, 14)


def test_non_recurring_task_has_no_next_occurrence():
    """A non-recurring task returns None for its next occurrence."""
    # arrange
    task = Task("One-off", "c", 10, due_date=date(2026, 7, 7))

    # act / assert
    assert task.next_occurrence() is None


# --- Conflicts ------------------------------------------------------------

def test_detect_conflicts_flags_same_scheduled_time():
    """detect_conflicts returns a readable message for tasks at the same time."""
    # arrange
    feeding = Task("Feeding", "food", 15, scheduled_time=540)   # 09:00
    vet_call = Task("Vet call", "admin", 10, scheduled_time=540)  # 09:00
    walk = Task("Walk", "walk", 30, scheduled_time=480)          # 08:00
    scheduler = Scheduler(tasks=[feeding, vet_call, walk])

    # act
    conflicts = scheduler.detect_conflicts()

    # assert
    assert len(conflicts) == 1
    assert "09:00" in conflicts[0]
    assert "Feeding" in conflicts[0] and "Vet call" in conflicts[0]


def test_no_conflicts_when_times_differ():
    """detect_conflicts returns an empty list when no times collide."""
    # arrange
    a = Task("A", "c", 10, scheduled_time=480)
    b = Task("B", "c", 10, scheduled_time=540)
    scheduler = Scheduler(tasks=[a, b])

    # act
    conflicts = scheduler.detect_conflicts()

    # assert
    assert conflicts == []


# --- Filtering ------------------------------------------------------------

def test_filter_by_status_splits_completed_and_pending():
    """filter_by_status returns only tasks matching the requested status."""
    # arrange
    done = Task("Done", "c", 10)
    done.mark_complete()
    pending = Task("Pending", "c", 10)
    scheduler = Scheduler(tasks=[done, pending])

    # act / assert
    assert scheduler.filter_by_status(True) == [done]
    assert scheduler.filter_by_status(False) == [pending]


def test_filter_by_pet_returns_only_that_pets_tasks():
    """filter_by_pet returns the named pet's tasks (empty list if not found)."""
    # arrange
    dog = Pet("Buddy", "Lab", 4)
    dog.add_task(Task("Walk", "walk", 30))
    cat = Pet("Milo", "Tabby", 2)
    cat.add_task(Task("Litter", "clean", 10))
    owner = Owner("Sam", pets=[dog, cat])
    scheduler = owner.build_scheduler("today")

    # act / assert
    assert scheduler.filter_by_pet(owner, "Buddy") == dog.tasks
    assert scheduler.filter_by_pet(owner, "Nobody") == []


# --- Edge cases -----------------------------------------------------------

def test_pet_with_no_tasks_returns_empty_list():
    """A pet that has had no tasks added returns an empty task list."""
    # arrange
    pet = Pet("Newbie", "Poodle", 1)

    # act / assert
    assert pet.view_tasks() == []


def test_owner_with_multiple_pets_returns_all_tasks():
    """view_schedule() gathers the tasks of every pet the owner has."""
    # arrange
    dog = Pet("Buddy", "Lab", 4)
    dog.add_task(Task("Walk", "walk", 30))
    dog.add_task(Task("Feeding", "food", 15))
    cat = Pet("Milo", "Tabby", 2)
    cat.add_task(Task("Litter", "clean", 10))
    owner = Owner("Sam", pets=[dog, cat])

    # act
    all_tasks = owner.view_schedule()

    # assert
    assert len(all_tasks) == 3
    titles = [t.title for t in all_tasks]
    assert titles == ["Walk", "Feeding", "Litter"]
