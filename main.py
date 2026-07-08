"""CLI demo for the PawPal+ backend: sorting, filtering, recurring, conflicts."""

from datetime import date

from pawpal_system import Owner, Pet, Priority, Task, format_time


def print_schedule(schedule: list[Task]) -> None:
    """Print a schedule in a readable terminal format."""
    for task in schedule:
        time_text = format_time(task.scheduled_time)
        priority_text = task.priority.name.title()
        status_text = "Complete" if task.completed else "Pending"
        print(
            f"  {time_text} | {task.title} "
            f"({task.category}, {task.duration_minutes} min, "
            f"{priority_text}, {status_text})"
        )


def main() -> None:
    """Create sample PawPal+ data and demo each scheduling feature."""
    owner = Owner(
        name="Aamir",
        contact_info="aamir@example.com",
        preferences={"schedule_style": "morning-heavy"},
    )

    dog = Pet(name="Buddy", breed="Golden Retriever", age=4)
    cat = Pet(name="Milo", breed="Tabby", age=2)

    today = date(2026, 7, 7)

    # Tasks are created OUT OF ORDER on purpose to show sorting.
    medication = Task(
        title="Allergy medication", category="Medication", duration_minutes=5,
        priority=Priority.MEDIUM, scheduled_time=600, recurrence="daily", due_date=today,
    )
    morning_walk = Task(
        title="Morning walk", category="Walk", duration_minutes=30,
        priority=Priority.HIGH, scheduled_time=480, recurrence="daily", due_date=today,
    )
    breakfast = Task(
        title="Breakfast feeding", category="Feeding", duration_minutes=15,
        priority=Priority.HIGH, scheduled_time=540,
    )
    # Same time as breakfast (540) -> creates a conflict.
    vet_call = Task(
        title="Vet phone check-in", category="Admin", duration_minutes=10,
        priority=Priority.LOW, scheduled_time=540,
    )
    # No scheduled_time -> should sort to the end.
    grooming = Task(
        title="Grooming", category="Grooming", duration_minutes=20,
        priority=Priority.MEDIUM, recurrence="weekly", due_date=today,
    )

    for task in (medication, morning_walk, breakfast, vet_call):
        dog.add_task(task)
    cat.add_task(grooming)

    owner.add_pet(dog)
    owner.add_pet(cat)

    scheduler = owner.build_scheduler(str(today))

    # 1. Sorting -----------------------------------------------------------
    print("Sorted daily schedule")
    print("---------------------")
    print_schedule(scheduler.generate_daily_schedule())

    # 2. Filtering ---------------------------------------------------------
    breakfast.mark_complete()  # complete one task so status filtering is visible

    print("\nFilter by pet (Buddy)")
    print("---------------------")
    print_schedule(scheduler.filter_by_pet(owner, "Buddy"))

    print("\nFilter by status: completed")
    print("---------------------------")
    print_schedule(scheduler.filter_by_status(True))

    print("\nFilter by status: pending")
    print("-------------------------")
    print_schedule(scheduler.filter_by_status(False))

    # 3. Recurring next occurrence ----------------------------------------
    print("\nRecurring tasks")
    print("---------------")
    next_walk = morning_walk.complete_and_reschedule()  # daily -> +1 day
    next_grooming = grooming.complete_and_reschedule()  # weekly -> +7 days
    print(f"  '{morning_walk.title}' (daily) due {morning_walk.due_date} "
          f"-> next due {next_walk.due_date}")
    print(f"  '{grooming.title}' (weekly) due {grooming.due_date} "
          f"-> next due {next_grooming.due_date}")

    # 4. Conflict detection ------------------------------------------------
    print("\nConflicts")
    print("---------")
    conflicts = scheduler.detect_conflicts()
    if conflicts:
        for conflict in conflicts:
            print(f"  {conflict}")
    else:
        print("  None")


if __name__ == "__main__":
    main()
