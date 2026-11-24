# Test Profile: Omar Khaled

**Scenario:** Level-1 student who asks for a level-2 web course: level restriction must reject it and the remaining level-1 courses fill the plan.

## 1. Student input

| Field | Value |
|---|---|
| Academic level | 1 |
| Upcoming term | Spring |
| GPA | 3.2 |
| Passed courses | CS101, MATH101, CS103 |
| Skills | python |
| Interests | object oriented programming, web development |
| Goals | build web applications |
| Preferred credit load | 15 |
| Requested courses | CS204 |

## 2. Retrieved evidence from the Knowledge Base

### 2a. Course passages (retrieved per course)

**CS102 (RECOMMENDED)**
> **[kb/courses/CS102.md § Overview]** (sim 0.68) CS102 Object-Oriented Programming is a 3-credit-hour core course at academic level 1. It is offered in the Spring semester only. Registration requirements - prerequisites: CS101.
> **[kb/courses/CS102.md § Registration notes]** (sim 0.49) Standard registration rules apply; see the registration policies.

**ENG101 (RECOMMENDED)**
> **[kb/courses/ENG101.md § Overview]** (sim 0.72) ENG101 Technical Writing and Communication is a 3-credit-hour core course at academic level 1. It is offered in every semester (Fall and Spring). There are no prerequisites or other registration requirements.

**MATH102 (RECOMMENDED)**
> **[kb/courses/MATH102.md § Overview]** (sim 0.62) MATH102 Discrete Mathematics is a 3-credit-hour core course at academic level 1. It is offered in the Spring semester only. Registration requirements - prerequisites: MATH101.

**HUM101 (RECOMMENDED)**
> **[kb/courses/HUM101.md § Overview]** (sim 0.69) HUM101 Critical Thinking and Society is a 3-credit-hour general education course at academic level 1. It is offered in every semester (Fall and Spring). There are no prerequisites or other registration requirements.

**CS204 (REJECTED)**
> **[kb/courses/CS204.md § Overview]** (sim 0.63) CS204 Web Application Development is a 3-credit-hour elective course at academic level 2. It is offered in every semester (Fall and Spring). Registration requirements - prerequisites: CS102.

**MATH202 (REJECTED)**
> **[kb/courses/MATH202.md § Overview]** (sim 0.63) MATH202 Linear Algebra is a 3-credit-hour core course at academic level 2. It is offered in every semester (Fall and Spring). Registration requirements - prerequisites: MATH101.

**CS202 (REJECTED)**
> **[kb/courses/CS202.md § Overview]** (sim 0.65) CS202 Computer Organization and Architecture is a 4-credit-hour core course at academic level 2. It is offered in the Spring semester only. Registration requirements - prerequisites: CS103.

**MATH201 (REJECTED)**
> **[kb/courses/MATH201.md § Overview]** (sim 0.64) MATH201 Probability and Statistics is a 3-credit-hour core course at academic level 2. It is offered in every semester (Fall and Spring). Registration requirements - prerequisites: MATH101.

**CS306 (REJECTED)**
> **[kb/courses/CS306.md § Overview]** (sim 0.62) CS306 Mobile Application Development is a 3-credit-hour elective course at academic level 3. It is offered in the Spring semester only. Registration requirements - prerequisites: CS204.

### 2b. Policy passages (retrieved for the rules applied)

Credit limit for this student: 21 credit hours.

> **[kb/policies/credit_load_policy.md § Exceeding the limit]** (sim 0.38) A registration that would exceed the maximum credit hours is rejected. Exceptions are not granted by the advising system; students must petition the dean in writing.

> **[kb/policies/level_and_availability_policy.md § Academic level restriction]** (sim 0.47) Courses are numbered by academic level from 1 to 4. A student may register only for courses at or below the academic level recorded for the student by the registrar. A level 1 student may not register for level 2, 3 or 4 courses, and a level 2 student may not register for level 3 or 4 courses.

> **[kb/policies/prerequisite_policy.md § Prerequisites]** (sim 0.52) A student may register for a course only if every prerequisite listed for that course has been passed. Prerequisites are cumulative: all listed prerequisites are required, not just one. A course that is currently in progress or was failed does not satisfy a prerequisite.

> **[kb/policies/prerequisite_policy.md § Corequisites]** (sim 0.38) A corequisite must be passed before, or registered in the same semester as, the course that requires it. If the corequisite course is not passed, the student must register for both courses together, and both must be individually eligible.

## 3. Accepted courses

| Course | Title | Credits | Reasons |
|---|---|---|---|
| CS102 | Object-Oriented Programming | 3 | Prerequisites satisfied: CS101 passed. Offered in Spring; level 1 is within student level 1. Core degree requirement. Matches your interests/goals: object oriented programming. |
| ENG101 | Technical Writing and Communication | 3 | No prerequisites required. Offered in Spring; level 1 is within student level 1. Core degree requirement. |
| MATH102 | Discrete Mathematics | 3 | Prerequisites satisfied: MATH101 passed. Offered in Spring; level 1 is within student level 1. Core degree requirement. |
| HUM101 | Critical Thinking and Society | 3 | No prerequisites required. Offered in Spring; level 1 is within student level 1. |

## 4. Rejected courses and reasons

| Course | Title | Rule failed | Reason | Policy source |
|---|---|---|---|---|
| CS204 | Web Application Development | LEVEL_RESTRICTION, PREREQUISITE_UNMET | CS204 is a level 2 course; student is level 1; missing prerequisite(s): CS102. **Hint:** Take CS102 first (eligible now) to work towards CS204. | kb/policies/level_and_availability_policy.md § Academic level restriction; kb/policies/prerequisite_policy.md § Prerequisites |
| MATH202 | Linear Algebra | LEVEL_RESTRICTION | MATH202 is a level 2 course; student is level 1. | kb/policies/level_and_availability_policy.md § Academic level restriction |
| CS202 | Computer Organization and Architecture | LEVEL_RESTRICTION | CS202 is a level 2 course; student is level 1. | kb/policies/level_and_availability_policy.md § Academic level restriction |
| MATH201 | Probability and Statistics | LEVEL_RESTRICTION | MATH201 is a level 2 course; student is level 1. | kb/policies/level_and_availability_policy.md § Academic level restriction |
| CS306 | Mobile Application Development | LEVEL_RESTRICTION, PREREQUISITE_UNMET | CS306 is a level 3 course; student is level 1; missing prerequisite(s): CS204. | kb/policies/level_and_availability_policy.md § Academic level restriction; kb/policies/prerequisite_policy.md § Prerequisites |
| CS305 | Cybersecurity Fundamentals | LEVEL_RESTRICTION, PREREQUISITE_UNMET | CS305 is a level 3 course; student is level 1; missing prerequisite(s): CS202. | kb/policies/level_and_availability_policy.md § Academic level restriction; kb/policies/prerequisite_policy.md § Prerequisites |
| CS301 | Design and Analysis of Algorithms | LEVEL_RESTRICTION, PREREQUISITE_UNMET | CS301 is a level 3 course; student is level 1; missing prerequisite(s): CS201, MATH102. **Hint:** Take MATH102 first (eligible now) to work towards CS301. | kb/policies/level_and_availability_policy.md § Academic level restriction; kb/policies/prerequisite_policy.md § Prerequisites |
| CS303L | Computer Networks Laboratory | LEVEL_RESTRICTION, COREQUISITE_UNAVAILABLE | CS303L is a level 3 course; student is level 1; corequisite CS303 cannot be registered (CS303 is a level 3 course; student is level 1; missing prerequisite(s): CS202). | kb/policies/level_and_availability_policy.md § Academic level restriction; kb/policies/prerequisite_policy.md § Corequisites |
| CS304 | Machine Learning | LEVEL_RESTRICTION, PREREQUISITE_UNMET | CS304 is a level 3 course; student is level 1; missing prerequisite(s): CS201, MATH201, MATH202. | kb/policies/level_and_availability_policy.md § Academic level restriction; kb/policies/prerequisite_policy.md § Prerequisites |
| CS302 | Operating Systems | LEVEL_RESTRICTION, PREREQUISITE_UNMET | CS302 is a level 3 course; student is level 1; missing prerequisite(s): CS201, CS202. | kb/policies/level_and_availability_policy.md § Academic level restriction; kb/policies/prerequisite_policy.md § Prerequisites |
| CS201 | Data Structures | LEVEL_RESTRICTION, PREREQUISITE_UNMET | CS201 is a level 2 course; student is level 1; missing prerequisite(s): CS102. **Hint:** Take CS102 first (eligible now) to work towards CS201. | kb/policies/level_and_availability_policy.md § Academic level restriction; kb/policies/prerequisite_policy.md § Prerequisites |

_(12 further courses are also ineligible; see the JSON output for the full list.)_

## 5. Final recommendation

**Register for:** CS102, ENG101, MATH102, HUM101  
**Total:** 12 credit hours (maximum allowed: 21, planned: 15)

