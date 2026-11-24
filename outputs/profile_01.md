# Test Profile: Amira Hassan

**Scenario:** New level-1 student starting in Spring with no history: availability (Fall-only CS103) and prerequisite chain rules apply.

## 1. Student input

| Field | Value |
|---|---|
| Academic level | 1 |
| Upcoming term | Spring |
| GPA | none (first semester) |
| Passed courses | none |
| Skills | basic computer use |
| Interests | programming, problem solving |
| Goals | become a software developer |
| Preferred credit load | 15 |
| Requested courses | - |

## 2. Retrieved evidence from the Knowledge Base

### 2a. Course passages (retrieved per course)

**CS101 (RECOMMENDED)**
> **[kb/courses/CS101.md § Overview]** (sim 0.59) CS101 Introduction to Programming is a 4-credit-hour core course at academic level 1. It is offered in every semester (Fall and Spring). There are no prerequisites or other registration requirements.
> **[kb/courses/CS101.md § Registration notes]** (sim 0.42) Standard registration rules apply; see the registration policies.

**MATH101 (RECOMMENDED)**
> **[kb/courses/MATH101.md § Overview]** (sim 0.55) MATH101 Calculus I is a 3-credit-hour core course at academic level 1. It is offered in every semester (Fall and Spring). There are no prerequisites or other registration requirements.
> **[kb/courses/MATH101.md § Description]** (sim 0.05) Covers limits, continuity, derivatives and basic integration of single-variable functions, with applications to optimisation and rates of change.

**ENG101 (RECOMMENDED)**
> **[kb/courses/ENG101.md § Overview]** (sim 0.72) ENG101 Technical Writing and Communication is a 3-credit-hour core course at academic level 1. It is offered in every semester (Fall and Spring). There are no prerequisites or other registration requirements.

**HUM101 (RECOMMENDED)**
> **[kb/courses/HUM101.md § Overview]** (sim 0.69) HUM101 Critical Thinking and Society is a 3-credit-hour general education course at academic level 1. It is offered in every semester (Fall and Spring). There are no prerequisites or other registration requirements.

**CS102 (REJECTED)**
> **[kb/courses/CS102.md § Overview]** (sim 0.68) CS102 Object-Oriented Programming is a 3-credit-hour core course at academic level 1. It is offered in the Spring semester only. Registration requirements - prerequisites: CS101.

**CS103 (REJECTED)**
> **[kb/courses/CS103.md § Overview]** (sim 0.66) CS103 Digital Logic Design is a 3-credit-hour core course at academic level 1. It is offered in the Fall semester only. There are no prerequisites or other registration requirements.

**MATH102 (REJECTED)**
> **[kb/courses/MATH102.md § Overview]** (sim 0.62) MATH102 Discrete Mathematics is a 3-credit-hour core course at academic level 1. It is offered in the Spring semester only. Registration requirements - prerequisites: MATH101.

**CS202 (REJECTED)**
> **[kb/courses/CS202.md § Overview]** (sim 0.65) CS202 Computer Organization and Architecture is a 4-credit-hour core course at academic level 2. It is offered in the Spring semester only. Registration requirements - prerequisites: CS103.

**CS303L (REJECTED)**
> **[kb/courses/CS303L.md § Overview]** (sim 0.58) CS303L Computer Networks Laboratory is a 1-credit-hour elective course at academic level 3. It is offered in every semester (Fall and Spring). Registration requirements - corequisite: CS303.

### 2b. Policy passages (retrieved for the rules applied)

Credit limit for this student: 18 credit hours.

> **[kb/policies/credit_load_policy.md § Exceeding the limit]** (sim 0.38) A registration that would exceed the maximum credit hours is rejected. Exceptions are not granted by the advising system; students must petition the dean in writing.

> **[kb/policies/prerequisite_policy.md § Prerequisites]** (sim 0.52) A student may register for a course only if every prerequisite listed for that course has been passed. Prerequisites are cumulative: all listed prerequisites are required, not just one. A course that is currently in progress or was failed does not satisfy a prerequisite.

> **[kb/policies/level_and_availability_policy.md § Semester availability]** (sim 0.58) Each course is offered in the Fall semester, the Spring semester, or both. A course can only be registered in a semester in which it is offered. Course overviews state the semesters in which the course is offered. A course offered only in Fall cannot be registered in the Spring semester.

> **[kb/policies/level_and_availability_policy.md § Academic level restriction]** (sim 0.47) Courses are numbered by academic level from 1 to 4. A student may register only for courses at or below the academic level recorded for the student by the registrar. A level 1 student may not register for level 2, 3 or 4 courses, and a level 2 student may not register for level 3 or 4 courses.

> **[kb/policies/prerequisite_policy.md § Corequisites]** (sim 0.38) A corequisite must be passed before, or registered in the same semester as, the course that requires it. If the corequisite course is not passed, the student must register for both courses together, and both must be individually eligible.

## 3. Accepted courses

| Course | Title | Credits | Reasons |
|---|---|---|---|
| CS101 | Introduction to Programming | 4 | No prerequisites required. Offered in Spring; level 1 is within student level 1. Core degree requirement. Matches your interests/goals: programming, problem solving. |
| MATH101 | Calculus I | 3 | No prerequisites required. Offered in Spring; level 1 is within student level 1. Core degree requirement. |
| ENG101 | Technical Writing and Communication | 3 | No prerequisites required. Offered in Spring; level 1 is within student level 1. Core degree requirement. |
| HUM101 | Critical Thinking and Society | 3 | No prerequisites required. Offered in Spring; level 1 is within student level 1. |

## 4. Rejected courses and reasons

| Course | Title | Rule failed | Reason | Policy source |
|---|---|---|---|---|
| CS102 | Object-Oriented Programming | PREREQUISITE_UNMET | missing prerequisite(s): CS101. **Hint:** Take CS101 first (eligible now) to work towards CS102. | kb/policies/prerequisite_policy.md § Prerequisites |
| CS103 | Digital Logic Design | NOT_OFFERED_THIS_TERM | CS103 is offered only in Fall, not in Spring. | kb/policies/level_and_availability_policy.md § Semester availability |
| MATH102 | Discrete Mathematics | PREREQUISITE_UNMET | missing prerequisite(s): MATH101. **Hint:** Take MATH101 first (eligible now) to work towards MATH102. | kb/policies/prerequisite_policy.md § Prerequisites |
| CS202 | Computer Organization and Architecture | LEVEL_RESTRICTION, PREREQUISITE_UNMET | CS202 is a level 2 course; student is level 1; missing prerequisite(s): CS103. | kb/policies/level_and_availability_policy.md § Academic level restriction; kb/policies/prerequisite_policy.md § Prerequisites |
| CS303L | Computer Networks Laboratory | LEVEL_RESTRICTION, COREQUISITE_UNAVAILABLE | CS303L is a level 3 course; student is level 1; corequisite CS303 cannot be registered (CS303 is a level 3 course; student is level 1; missing prerequisite(s): CS202). | kb/policies/level_and_availability_policy.md § Academic level restriction; kb/policies/prerequisite_policy.md § Corequisites |
| CS301 | Design and Analysis of Algorithms | LEVEL_RESTRICTION, PREREQUISITE_UNMET | CS301 is a level 3 course; student is level 1; missing prerequisite(s): CS201, MATH102. | kb/policies/level_and_availability_policy.md § Academic level restriction; kb/policies/prerequisite_policy.md § Prerequisites |
| CS204 | Web Application Development | LEVEL_RESTRICTION, PREREQUISITE_UNMET | CS204 is a level 2 course; student is level 1; missing prerequisite(s): CS102. | kb/policies/level_and_availability_policy.md § Academic level restriction; kb/policies/prerequisite_policy.md § Prerequisites |
| CS302 | Operating Systems | LEVEL_RESTRICTION, PREREQUISITE_UNMET | CS302 is a level 3 course; student is level 1; missing prerequisite(s): CS201, CS202. | kb/policies/level_and_availability_policy.md § Academic level restriction; kb/policies/prerequisite_policy.md § Prerequisites |
| CS303 | Computer Networks | LEVEL_RESTRICTION, PREREQUISITE_UNMET | CS303 is a level 3 course; student is level 1; missing prerequisite(s): CS202. | kb/policies/level_and_availability_policy.md § Academic level restriction; kb/policies/prerequisite_policy.md § Prerequisites |
| CS201 | Data Structures | LEVEL_RESTRICTION, PREREQUISITE_UNMET | CS201 is a level 2 course; student is level 1; missing prerequisite(s): CS102. | kb/policies/level_and_availability_policy.md § Academic level restriction; kb/policies/prerequisite_policy.md § Prerequisites |

_(16 further courses are also ineligible; see the JSON output for the full list.)_

## 5. Final recommendation

**Register for:** CS101, MATH101, ENG101, HUM101  
**Total:** 13 credit hours (maximum allowed: 18, planned: 15)

