# PawPal+ Project Reflection

## 1. System Design
The user should be able to perfrom the following actions: 
- Enter their pets information as well as their own 
- Genenate a pet care schedule/plan for the user to follow 
- Have preferences for how they want their grooming schedule to be 

**a. Initial design**

- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?

My initial UML design includes 4 classes: Owner, Pet, Task, Scheduler. 
The Owner class stroes information such as Name, contact info, pets 
The Pet class stores information such as Breed, age, medical and dietary needs 
The Task class stores information such as walk, feed, groom, give medicine 
and Lastly The Scheduler class stores info such as recurring tasks, priotity, availability conflicts 

**b. Design changes**

- Did your design change during implementation? 

Yes my design did change during implementation 

- If yes, describe at least one change and why you made it.

1. Priority was a string with no sort order, it now has a 1,2, or 3 rating to signify priority. 
2. Schedule time was a string and has now been changed to an int.
3. Owner and Schedule were disconnected, they now have build_scheduler and add_tasks, which gather each pet's tasks by reference and hand them to the scheduler.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?

Considers Time, priority, completion status, recurring tasks, and conflicts

- How did you decide which constraints mattered most?

Scheduled time definitely matters the most because the plan needs to be shown in the correct order that the User intended.


**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

One tradeoff it makes is that it can detect if two tasks are both scheduled at 9:00, but it does not fully calculate 
whether a 30 min 9:00 task overlaps with a 9:15 task. The traddeoff is reasonable because exact time conflict 
detection is simpler and easier to test

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?

I used AI for scaffolding the class skeletons, implementing backend logic, connecting the backend to Streamlit, and improving documentation to name few. 

- What kinds of prompts or questions were most helpful?

The most helpful prompts were the specific prompts that mentioned what should not be changed along with what should.

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

I did not accept an AI suggestion as is when extra tool specific folders and files were created. 
Instead of committing them, I kept the submitted project clean by ignoring those files.

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

I tested task completion, adding tasks to pets, sorting tasks in chronological order, priority ordering when tasks share the same time, recurring task behavior, conflict detection, pets with no tasks, and owners with multiple pets. These tests were important because they verified the main behaviors that the scheduler and UI depend on.


**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

I am about like 80% confident that teh scheduler works correctly for the project requirements. 
If I had more time, I would test overlapping task durations, invalid time inputs and editing existing tasks.


---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?
    
    I am most satisfied with how the project moved from a UML design into a working backend system. 

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

    If I had another iteration, I would improve the scheduler so it could detect overlapping time ranges instead of 
    only exact same time conflicts and a more polished UI.


**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?

    One important thing I learned is that while AI is helpful for the legwork, I still am the lead architect/designer. 
    AI helped generate code and validation tests but I had to decide what worked best for the app and verified that it worked correctly and collelctively. 
