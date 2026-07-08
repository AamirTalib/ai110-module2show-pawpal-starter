import datetime

import streamlit as st

from pawpal_system import Owner, Pet, Task, Scheduler, Priority, format_time

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

# Create the Owner once and keep it across Streamlit reruns.
if "owner" not in st.session_state:
    st.session_state.owner = Owner(name="", contact_info="")

owner = st.session_state.owner

# Map the UI's friendly priority labels to the backend Priority enum.
PRIORITY_OPTIONS = {"low": Priority.LOW, "medium": Priority.MEDIUM, "high": Priority.HIGH}

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to **PawPal+**, a pet care planning assistant. Enter your info, add a
pet, give it care tasks, then generate a daily schedule.
"""
)

with st.expander("Scenario", expanded=False):
    st.markdown(
        """
**PawPal+** helps a pet owner plan care tasks for their pet(s) based on
constraints like time and priority.
"""
    )

st.divider()

# --- Owner info ------------------------------------------------------------
st.subheader("Owner")
owner.name = st.text_input("Owner name", value=owner.name or "Jordan")
owner.contact_info = st.text_input("Contact info", value=owner.contact_info)

st.divider()

# --- Add a pet -------------------------------------------------------------
st.subheader("Pets")
col1, col2, col3 = st.columns(3)
with col1:
    pet_name = st.text_input("Pet name", value="Mochi")
with col2:
    pet_breed = st.text_input("Breed", value="")
with col3:
    pet_age = st.number_input("Age", min_value=0, max_value=40, value=1)

if st.button("Add pet"):
    if pet_name.strip():
        owner.add_pet(Pet(name=pet_name, breed=pet_breed, age=int(pet_age)))
        st.success(f"Added pet: {pet_name}")
    else:
        st.warning("Please enter a pet name.")

if owner.pets:
    st.write("Current pets:", ", ".join(p.name for p in owner.pets))
else:
    st.info("No pets yet. Add one above.")

st.divider()

# --- Add tasks to a pet ----------------------------------------------------
st.subheader("Tasks")

if owner.pets:
    pet_names = [p.name for p in owner.pets]
    selected_name = st.selectbox("Add task to pet", pet_names)
    selected_pet = owner.pets[pet_names.index(selected_name)]

    col1, col2 = st.columns(2)
    with col1:
        task_title = st.text_input("Task title", value="Morning walk")
    with col2:
        task_category = st.text_input("Category", value="general")

    col3, col4, col5 = st.columns(3)
    with col3:
        duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
    with col4:
        priority_label = st.selectbox("Priority", list(PRIORITY_OPTIONS.keys()), index=2)
    with col5:
        start_time = st.time_input("Start time", value=datetime.time(8, 0))

    if st.button("Add task"):
        task = Task(
            title=task_title,
            category=task_category,
            duration_minutes=int(duration),
            priority=PRIORITY_OPTIONS[priority_label],
            scheduled_time=start_time.hour * 60 + start_time.minute,
        )
        selected_pet.add_task(task)
        st.success(f"Added '{task_title}' to {selected_pet.name}")

    # Show the selected pet's current tasks.
    if selected_pet.tasks:
        st.write(f"Tasks for {selected_pet.name}:")
        st.table(
            [
                {
                    "Time": format_time(t.scheduled_time),
                    "Task": t.title,
                    "Category": t.category,
                    "Minutes": t.duration_minutes,
                    "Priority": t.priority.name,
                }
                for t in selected_pet.tasks
            ]
        )
    else:
        st.info(f"No tasks yet for {selected_pet.name}.")
else:
    st.info("Add a pet first, then you can add tasks for it.")

st.divider()

# --- Generate schedule -----------------------------------------------------
st.subheader("Build Schedule")

schedule_date = st.date_input("Schedule date", value=datetime.date.today())

if st.button("Generate schedule"):
    scheduler = owner.build_scheduler(str(schedule_date))
    plan = scheduler.generate_daily_schedule()

    if not plan:
        st.warning("No tasks to schedule yet. Add a pet and some tasks above.")
    else:
        st.markdown(f"### Daily plan for {schedule_date}")
        # Sorted plan shown as a clean table (time first, then priority).
        st.table(
            [
                {
                    "Time": format_time(task.scheduled_time),
                    "Task": task.title,
                    "Duration (min)": task.duration_minutes,
                    "Priority": task.priority.name.title(),
                    "Status": "Done" if task.completed else "Pending",
                }
                for task in plan
            ]
        )

        conflicts = scheduler.detect_conflicts()
        if conflicts:
            st.warning("Scheduling conflicts found:")
            for message in conflicts:
                st.write(f"- {message}")
        else:
            st.success("No scheduling conflicts. 🎉")
