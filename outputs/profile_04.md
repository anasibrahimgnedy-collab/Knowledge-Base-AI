# Test Profile: Youssef Adel

**Scenario:** UNMET PREREQUISITES: transfer student who skipped CS202 and MATH202 but asks for Operating Systems and Machine Learning.

## 1. Student input

| Field | Value |
|---|---|
| Academic level | 3 |
| Upcoming term | Spring |
| GPA | 3.0 |
| Passed courses | CS101, MATH101, ENG101, HUM101, CS103, CS102, MATH102, CS201, MATH201, CS205, CS203 |
| Skills | python, sql |
| Interests | operating systems, machine learning |
| Goals | work on systems software |
| Preferred credit load | 18 |
| Requested courses | CS302, CS304 |

## 2. Retrieved evidence from the Knowledge Base

### 2a. Course passages (retrieved per course)

**CS301 (RECOMMENDED)**
> **[kb/courses/CS301.md § Overview]** (sim 0.59) CS301 Design and Analysis of Algorithms is a 3-credit-hour core course at academic level 3. It is offered in every semester (Fall and Spring). Registration requirements - prerequisites: CS201, MATH102.

**MATH202 (RECOMMENDED)**
> **[kb/courses/MATH202.md § Overview]** (sim 0.63) MATH202 Linear Algebra is a 3-credit-hour core course at academic level 2. It is offered in every semester (Fall and Spring). Registration requirements - prerequisites: MATH101.
> **[kb/courses/MATH202.md § Description]** (sim 0.04) Covers vectors, matrices, linear systems, vector spaces, eigenvalues and applications to computing and data science.

**CS202 (RECOMMENDED)**
> **[kb/courses/CS202.md § Overview]** (sim 0.65) CS202 Computer Organization and Architecture is a 4-credit-hour core course at academic level 2. It is offered in the Spring semester only. Registration requirements - prerequisites: CS103.

**CS307 (RECOMMENDED)**
> **[kb/courses/CS307.md § Overview]** (sim 0.59) CS307 Artificial Intelligence is a 3-credit-hour elective course at academic level 3. It is offered in every semester (Fall and Spring). Registration requirements - prerequisites: CS201, MATH201.

**CS204 (RECOMMENDED)**
> **[kb/courses/CS204.md § Overview]** (sim 0.63) CS204 Web Application Development is a 3-credit-hour elective course at academic level 2. It is offered in every semester (Fall and Spring). Registration requirements - prerequisites: CS102.

**CS302 (REJECTED)**
> **[kb/courses/CS302.md § Overview]** (sim 0.59) CS302 Operating Systems is a 3-credit-hour core course at academic level 3. It is offered in the Spring semester only. Registration requirements - prerequisites: CS201, CS202.

**CS304 (REJECTED)**
> **[kb/courses/CS304.md § Overview]** (sim 0.54) CS304 Machine Learning is a 3-credit-hour elective course at academic level 3. It is offered in the Spring semester only. Registration requirements - prerequisites: CS201, MATH201, MATH202.

**CS206 (REJECTED)**
> **[kb/courses/CS206.md § Overview]** (sim 0.61) CS206 Computer Graphics is a 3-credit-hour elective course at academic level 2. It is offered in the Fall semester only. Registration requirements - prerequisites: CS201.

**CS303 (REJECTED)**
> **[kb/courses/CS303.md § Overview]** (sim 0.52) CS303 Computer Networks is a 3-credit-hour core course at academic level 3. It is offered in every semester (Fall and Spring). Registration requirements - prerequisites: CS202.

**CS303L (REJECTED)**
> **[kb/courses/CS303L.md § Overview]** (sim 0.58) CS303L Computer Networks Laboratory is a 1-credit-hour elective course at academic level 3. It is offered in every semester (Fall and Spring). Registration requirements - corequisite: CS303.

### 2b. Policy passages (retrieved for the rules applied)

Credit limit for this student: 21 credit hours.

> **[kb/policies/credit_load_policy.md § Exceeding the limit]** (sim 0.38) A registration that would exceed the maximum credit hours is rejected. Exceptions are not granted by the advising system; students must petition the dean in writing.

> **[kb/policies/prerequisite_policy.md § Prerequisites]** (sim 0.52) A student may register for a course only if every prerequisite listed for that course has been passed. Prerequisites are cumulative: all listed prerequisites are required, not just one. A course that is currently in progress or was failed does not satisfy a prerequisite.

> **[kb/policies/level_and_availability_policy.md § Semester availability]** (sim 0.58) Each course is offered in the Fall semester, the Spring semester, or both. A course can only be registered in a semester in which it is offered. Course overviews state the semesters in which the course is offered. A course offered only in Fall cannot be registered in the Spring semester.

> **[kb/policies/prerequisite_policy.md § Corequisites]** (sim 0.38) A corequisite must be passed before, or registered in the same semester as, the course that requires it. If the corequisite course is not passed, the student must register for both courses together, and both must be individually eligible.

> **[kb/policies/level_and_availability_policy.md § Academic level restriction]** (sim 0.47) Courses are numbered by academic level from 1 to 4. A student may register only for courses at or below the academic level recorded for the student by the registrar. A level 1 student may not register for level 2, 3 or 4 courses, and a level 2 student may not register for level 3 or 4 courses.

## 3. Accepted courses

| Course | Title | Credits | Reasons |
|---|---|---|---|
| CS301 | Design and Analysis of Algorithms | 3 | Prerequisites satisfied: CS201, MATH102 passed. Offered in Spring; level 3 is within student level 3. Core degree requirement. |
| MATH202 | Linear Algebra | 3 | Prerequisites satisfied: MATH101 passed. Offered in Spring; level 2 is within student level 3. Core degree requirement. |
| CS202 | Computer Organization and Architecture | 4 | Prerequisites satisfied: CS103 passed. Offered in Spring; level 2 is within student level 3. Core degree requirement. |
| CS307 | Artificial Intelligence | 3 | Prerequisites satisfied: CS201, MATH201 passed. Offered in Spring; level 3 is within student level 3. |
| CS204 | Web Application Development | 3 | Prerequisites satisfied: CS102 passed. Offered in Spring; level 2 is within student level 3. |

## 4. Rejected courses and reasons

| Course | Title | Rule failed | Reason | Policy source |
|---|---|---|---|---|
| CS302 | Operating Systems | PREREQUISITE_UNMET | missing prerequisite(s): CS202. **Hint:** Take CS202 first (eligible now) to work towards CS302. | kb/policies/prerequisite_policy.md § Prerequisites |
| CS304 | Machine Learning | PREREQUISITE_UNMET | missing prerequisite(s): MATH202. **Hint:** Take MATH202 first (eligible now) to work towards CS304. | kb/policies/prerequisite_policy.md § Prerequisites |
| CS206 | Computer Graphics | NOT_OFFERED_THIS_TERM | CS206 is offered only in Fall, not in Spring. | kb/policies/level_and_availability_policy.md § Semester availability |
| CS303 | Computer Networks | PREREQUISITE_UNMET | missing prerequisite(s): CS202. **Hint:** Take CS202 first (eligible now) to work towards CS303. | kb/policies/prerequisite_policy.md § Prerequisites |
| CS303L | Computer Networks Laboratory | COREQUISITE_UNAVAILABLE | corequisite CS303 cannot be registered (missing prerequisite(s): CS202). | kb/policies/prerequisite_policy.md § Corequisites |
| CS305 | Cybersecurity Fundamentals | PREREQUISITE_UNMET | missing prerequisite(s): CS202. **Hint:** Take CS202 first (eligible now) to work towards CS305. | kb/policies/prerequisite_policy.md § Prerequisites |
| CS306 | Mobile Application Development | PREREQUISITE_UNMET | missing prerequisite(s): CS204. **Hint:** Take CS204 first (eligible now) to work towards CS306. | kb/policies/prerequisite_policy.md § Prerequisites |
| CS407 | Professional Ethics and Law in Computing | LEVEL_RESTRICTION | CS407 is a level 4 course; student is level 3. | kb/policies/level_and_availability_policy.md § Academic level restriction |
| CS402 | Deep Learning | LEVEL_RESTRICTION, PREREQUISITE_UNMET | CS402 is a level 4 course; student is level 3; missing prerequisite(s): CS304. | kb/policies/level_and_availability_policy.md § Academic level restriction; kb/policies/prerequisite_policy.md § Prerequisites |
| CS403 | Distributed Systems | LEVEL_RESTRICTION, PREREQUISITE_UNMET | CS403 is a level 4 course; student is level 3; missing prerequisite(s): CS302, CS303. | kb/policies/level_and_availability_policy.md § Academic level restriction; kb/policies/prerequisite_policy.md § Prerequisites |
| CS405 | Advanced Cybersecurity | LEVEL_RESTRICTION, PREREQUISITE_UNMET | CS405 is a level 4 course; student is level 3; missing prerequisite(s): CS305. | kb/policies/level_and_availability_policy.md § Academic level restriction; kb/policies/prerequisite_policy.md § Prerequisites |
| CS406 | Natural Language Processing | LEVEL_RESTRICTION, PREREQUISITE_UNMET | CS406 is a level 4 course; student is level 3; missing prerequisite(s): CS304. | kb/policies/level_and_availability_policy.md § Academic level restriction; kb/policies/prerequisite_policy.md § Prerequisites |

_(2 further courses are also ineligible; see the JSON output for the full list.)_

## 5. Final recommendation

**Register for:** CS301, MATH202, CS202, CS307, CS204  
**Total:** 16 credit hours (maximum allowed: 21, planned: 18)

