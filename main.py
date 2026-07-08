"""CLI demo script for the PawPal+ backend system."""

from pawpal_system import Owner, Pet, Priority, Scheduler, Task, format_time


def print_schedule(schedule: list[Task]) -> None:
    """Print the schedule in a readable terminal format."""
    print("Today's Schedule")
    print("----------------")

    for task in schedule:
        time_text = format_time(task.scheduled_time)
        priority_text = task.priority.name.title()
        status_text = "Complete" if task.completed else "Pending"

        print(
            f"{time_text} | {task.title} "
            f"({task.category}, {task.duration_minutes} min, "
            f"{priority_text}, {status_text})"
        )


def main() -> None:
    """Create sample PawPal+ data and print a daily schedule."""
    owner = Owner(
        name="Aamir",
        contact_info="aamir@example.com",
        preferences={"schedule_style": "morning-heavy"},
    )

    dog = Pet(
        name="Buddy",
        breed="Golden Retriever",
        age=4,
        dietary_needs="Grain-free food",
        medical_notes="Needs allergy medication",
    )

    cat = Pet(
        name="Milo",
        breed="Tabby",
        age=2,
        dietary_needs="Wet food preferred",
    )

    morning_walk = Task(
        title="Morning walk",
        category="Walk",
        duration_minutes=30,
        priority=Priority.HIGH,
        scheduled_time=480,  # 8:00 AM
        recurrence="daily",
    )

    breakfast = Task(
        title="Breakfast feeding",
        category="Feeding",
        duration_minutes=15,
        priority=Priority.HIGH,
        scheduled_time=540,  # 9:00 AM
        recurrence="daily",
    )

    medication = Task(
        title="Allergy medication",
        category="Medication",
        duration_minutes=5,
        priority=Priority.MEDIUM,
        scheduled_time=600,  # 10:00 AM
        recurrence="daily",
    )

    litter_cleaning = Task(
        title="Clean litter box",
        category="Cleaning",
        duration_minutes=10,
        priority=Priority.LOW,
        scheduled_time=660,  # 11:00 AM
        recurrence="daily",
    )

    dog.add_task(morning_walk)
    dog.add_task(breakfast)
    dog.add_task(medication)
    cat.add_task(litter_cleaning)

    owner.add_pet(dog)
    owner.add_pet(cat)

    scheduler = Scheduler(date="today")
    scheduler.load_from_owner(owner)

    schedule = scheduler.generate_daily_schedule()
    print_schedule(schedule)

    conflicts = scheduler.detect_conflicts()
    if conflicts:
        print("\nConflicts")
        print("---------")
        for conflict in conflicts:
            print(conflict)


if __name__ == "__main__":
    main()