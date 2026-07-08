"""PawPal+ backend system.

This module defines the core data model and scheduling skeleton for PawPal+.
It is translated directly from the UML draft in diagrams/uml_draft.mmd.

NOTE: This is a Phase 1 skeleton. Method bodies are intentionally left as
stubs (`pass` or simple returns) and will be implemented in later phases.
"""

from dataclasses import dataclass, field


@dataclass
class Task:
    """A single pet care task (e.g. a walk, feeding, or medication)."""

    title: str
    category: str
    duration_minutes: int
    priority: str
    scheduled_time: str = ""
    recurrence: str = "none"
    completed: bool = False

    def schedule(self, time: str) -> None:
        """Assign a scheduled time to this task."""
        pass

    def mark_complete(self) -> None:
        """Mark this task as completed."""
        pass

    def is_recurring(self) -> bool:
        """Return True if this task repeats (daily, weekly, etc.)."""
        pass


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
        """Add a care task for this pet."""
        pass

    def view_tasks(self) -> list[Task]:
        """Return the list of this pet's tasks."""
        pass

    def update_info(self, info: dict) -> None:
        """Update this pet's basic information."""
        pass


@dataclass
class Owner:
    """A pet owner with contact info, preferences, and one or more pets."""

    name: str
    contact_info: str = ""
    preferences: dict = field(default_factory=dict)
    pets: list[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        """Register a new pet under this owner."""
        pass

    def update_preferences(self, preferences: dict) -> None:
        """Update the owner's scheduling preferences."""
        pass

    def view_schedule(self) -> None:
        """Display the owner's schedule (to be defined in a later phase)."""
        pass


@dataclass
class Scheduler:
    """Builds a daily plan from a collection of tasks and time constraints."""

    tasks: list[Task] = field(default_factory=list)
    date: str = ""
    available_slots: list = field(default_factory=list)

    def generate_daily_schedule(self) -> list[Task]:
        """Produce an ordered daily plan based on constraints and priorities."""
        pass

    def sort_tasks(self) -> list[Task]:
        """Sort tasks (e.g. by priority and duration)."""
        pass

    def detect_conflicts(self) -> list:
        """Find overlapping or conflicting tasks in the schedule."""
        pass

    def handle_recurring_tasks(self) -> None:
        """Expand recurring tasks into concrete scheduled instances."""
        pass
