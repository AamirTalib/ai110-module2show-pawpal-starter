"""PawPal+ backend system.

This module defines the core data model and scheduling logic for PawPal+.
It is translated from the UML draft in diagrams/uml_draft.mmd.

The four main classes are Owner, Pet, Task, and Scheduler.
"""

from dataclasses import dataclass, field, replace
from datetime import date, timedelta
from enum import IntEnum


class Priority(IntEnum):
    """Task priority. Higher value = more important, so it sorts naturally."""

    LOW = 1
    MEDIUM = 2
    HIGH = 3


def format_time(minutes: int | None) -> str:
    """Turn minutes-since-midnight into a readable 'HH:MM' string."""
    if minutes is None:
        return "unscheduled"
    hours, mins = divmod(minutes, 60)
    return f"{hours:02d}:{mins:02d}"


@dataclass
class Task:
    """A single pet care task (e.g. a walk, feeding, or medication)."""

    title: str
    category: str
    duration_minutes: int
    priority: Priority = Priority.MEDIUM
    # Minutes since midnight (e.g. 8:00 AM -> 480). None means "not yet placed".
    # Storing an int lets the scheduler compare times and compute end times
    # (end = scheduled_time + duration_minutes).
    scheduled_time: int | None = None
    recurrence: str = "none"
    due_date: date | None = None
    completed: bool = False

    def schedule(self, time: int) -> None:
        """Assign a start time (minutes since midnight) to this task."""
        self.scheduled_time = time

    def mark_complete(self) -> None:
        """Mark this task as completed."""
        self.completed = True

    def is_recurring(self) -> bool:
        """Return True if this task repeats (recurrence is set and not 'none')."""
        return self.recurrence not in ("", "none")

    def next_occurrence(self) -> "Task | None":
        """Return a fresh copy of this task on its next due date, or None."""
        steps = {"daily": timedelta(days=1), "weekly": timedelta(days=7)}
        step = steps.get(self.recurrence)
        if step is None or self.due_date is None:
            return None
        return replace(self, due_date=self.due_date + step, completed=False)

    def complete_and_reschedule(self) -> "Task | None":
        """Mark this task complete and return its next occurrence (if recurring)."""
        self.mark_complete()
        return self.next_occurrence()


@dataclass
class Pet:
    """A pet belonging to an owner, along with its care tasks."""

    name: str
    breed: str
    age: int
    dietary_needs: str = ""
    medical_notes: str = ""
    tasks: list[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Add a care task to this pet's task list."""
        self.tasks.append(task)

    def view_tasks(self) -> list[Task]:
        """Return this pet's list of tasks."""
        return self.tasks

    def update_info(self, info: dict) -> None:
        """Update this pet's basic info from a dict of valid attributes."""
        allowed = ("name", "breed", "age", "dietary_needs", "medical_notes")
        for key, value in info.items():
            if key in allowed:
                setattr(self, key, value)


@dataclass
class Owner:
    """A pet owner with contact info, preferences, and one or more pets."""

    name: str
    contact_info: str = ""
    preferences: dict = field(default_factory=dict)
    pets: list[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to this owner's pet list."""
        self.pets.append(pet)

    def update_preferences(self, preferences: dict) -> None:
        """Merge new values into the owner's preferences dictionary."""
        self.preferences.update(preferences)

    def build_scheduler(self, date: str) -> "Scheduler":
        """Create a Scheduler for `date`, loaded with all of this owner's tasks."""
        # Tasks are passed by reference, so completing a task in the plan is
        # reflected on the pet.
        scheduler = Scheduler(date=date)
        scheduler.load_from_owner(self)
        return scheduler

    def view_schedule(self) -> list[Task]:
        """Return all tasks from all of this owner's pets."""
        all_tasks: list[Task] = []
        for pet in self.pets:
            all_tasks.extend(pet.view_tasks())
        return all_tasks


@dataclass
class Scheduler:
    """Builds a daily plan from a collection of tasks and time constraints."""

    tasks: list[Task] = field(default_factory=list)
    date: str = ""
    available_slots: list = field(default_factory=list)

    def add_tasks(self, tasks: list[Task]) -> None:
        """Load tasks (by reference) that this scheduler should plan."""
        self.tasks.extend(tasks)

    def load_from_owner(self, owner: Owner) -> None:
        """Retrieve all tasks from an owner's pets into this scheduler."""
        self.add_tasks(owner.view_schedule())

    def sort_tasks(self) -> list[Task]:
        """Return tasks sorted by scheduled_time first, then priority (high first)."""
        # Unscheduled tasks (scheduled_time is None) sort to the end.
        # Negating priority puts HIGH before MEDIUM before LOW.
        return sorted(
            self.tasks,
            key=lambda t: (
                t.scheduled_time if t.scheduled_time is not None else float("inf"),
                -t.priority,
            ),
        )

    def generate_daily_schedule(self) -> list[Task]:
        """Return the day's tasks in a clear, sorted order."""
        return self.sort_tasks()

    def filter_by_status(self, completed: bool) -> list[Task]:
        """Return tasks matching the given completed status."""
        return [task for task in self.tasks if task.completed == completed]

    def filter_by_pet(self, owner: Owner, pet_name: str) -> list[Task]:
        """Return the tasks belonging to the named pet, or [] if not found."""
        for pet in owner.pets:
            if pet.name == pet_name:
                return pet.view_tasks()
        return []

    def detect_conflicts(self) -> list[str]:
        """Return messages for any tasks that share the same scheduled_time."""
        conflicts: list[str] = []
        seen: dict[int, Task] = {}
        for task in self.tasks:
            if task.scheduled_time is None:
                continue
            if task.scheduled_time in seen:
                other = seen[task.scheduled_time]
                conflicts.append(
                    f"Conflict at {format_time(task.scheduled_time)}: "
                    f"'{other.title}' and '{task.title}'"
                )
            else:
                seen[task.scheduled_time] = task
        return conflicts

    def handle_recurring_tasks(self) -> list[Task]:
        """Return the tasks that are recurring."""
        return [task for task in self.tasks if task.is_recurring()]
