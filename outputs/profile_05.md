# Test Profile: Sara Nabil

**Scenario:** EXCEEDS CREDIT LIMIT: GPA 2.4 allows 18 credit hours but the student wants 24 and requests 22 hours of courses.

## 1. Student input

| Field | Value |
|---|---|
| Academic level | 3 |
| Upcoming term | Spring |
| GPA | 2.4 |
| Passed courses | CS101, MATH101, ENG101, HUM101, CS103, CS102, MATH102, CS201, MATH201, MATH202, CS205, CS202, CS203 |
| Skills | python, java |
| Interests | networking, security, artificial intelligence |
| Goals | graduate on time with broad skills |
| Preferred credit load | 24 |
| Requested courses | CS301, CS302, CS303, CS303L, CS304, CS305, CS307, CS204 |

## 2. Retrieved evidence from the Knowledge Base

### 2a. Course passages (retrieved per course)

**CS307 (RECOMMENDED)**
> **[kb/courses/CS307.md § Overview]** (sim 0.59) CS307 Artificial Intelligence is a 3-credit-hour elective course at academic level 3. It is offered in every semester (Fall and Spring). Registration requirements - prerequisites: CS201, MATH201.
> **[kb/courses/CS307.md § Registration notes]** (sim 0.38) Standard registration rules apply; see the registration policies.

**CS303 (RECOMMENDED)**
> **[kb/courses/CS303.md § Overview]** (sim 0.52) CS303 Computer Networks is a 3-credit-hour core course at academic level 3. It is offered in every semester (Fall and Spring). Registration requirements - prerequisites: CS202.
> **[kb/courses/CS303.md § Registration notes]** (sim 0.07) Standard registration rules apply; see the registration policies.

**CS301 (RECOMMENDED)**
> **[kb/courses/CS301.md § Overview]** (sim 0.59) CS301 Design and Analysis of Algorithms is a 3-credit-hour core course at academic level 3. It is offered in every semester (Fall and Spring). Registration requirements - prerequisites: CS201, MATH102.

**CS302 (RECOMMENDED)**
> **[kb/courses/CS302.md § Overview]** (sim 0.59) CS302 Operating Systems is a 3-credit-hour core course at academic level 3. It is offered in the Spring semester only. Registration requirements - prerequisites: CS201, CS202.

**CS305 (RECOMMENDED)**
> **[kb/courses/CS305.md § Overview]** (sim 0.58) CS305 Cybersecurity Fundamentals is a 3-credit-hour elective course at academic level 3. It is offered in the Spring semester only. Registration requirements - prerequisites: CS202.
> **[kb/courses/CS305.md § Registration notes]** (sim 0.10) Standard registration rules apply; see the registration policies.

**CS303L (RECOMMENDED)**
> **[kb/courses/CS303L.md § Overview]** (sim 0.58) CS303L Computer Networks Laboratory is a 1-credit-hour elective course at academic level 3. It is offered in every semester (Fall and Spring). Registration requirements - corequisite: CS303.
> **[kb/courses/CS303L.md § Registration notes]** (sim 0.07) Standard registration rules apply; see the registration policies.

**CS204 (REJECTED)**
> **[kb/courses/CS204.md § Overview]** (sim 0.63) CS204 Web Application Development is a 3-credit-hour elective course at academic level 2. It is offered in every semester (Fall and Spring). Registration requirements - prerequisites: CS102.

**CS304 (REJECTED)**
> **[kb/courses/CS304.md § Overview]** (sim 0.54) CS304 Machine Learning is a 3-credit-hour elective course at academic level 3. It is offered in the Spring semester only. Registration requirements - prerequisites: CS201, MATH201, MATH202.

**CS206 (REJECTED)**
> **[kb/courses/CS206.md § Overview]** (sim 0.61) CS206 Computer Graphics is a 3-credit-hour elective course at academic level 2. It is offered in the Fall semester only. Registration requirements - prerequisites: CS201.

**CS306 (REJECTED)**
> **[kb/courses/CS306.md § Overview]** (sim 0.62) CS306 Mobile Application Development is a 3-credit-hour elective course at academic level 3. It is offered in the Spring semester only. Registration requirements - prerequisites: CS204.

**CS407 (REJECTED)**
> **[kb/courses/CS407.md § Overview]** (sim 0.70) CS407 Professional Ethics and Law in Computing is a 3-credit-hour core course at academic level 4. It is offered in every semester (Fall and Spring). Registration requirements - at least 30 passed credit hours.

### 2b. Policy passages (retrieved for the rules applied)

Credit limit for this student: 18 credit hours.

> **[kb/policies/credit_load_policy.md § Exceeding the limit]** (sim 0.38) A registration that would exceed the maximum credit hours is rejected. Exceptions are not granted by the advising system; students must petition the dean in writing.

> **[kb/policies/level_and_availability_policy.md § Semester availability]** (sim 0.58) Each course is offered in the Fall semester, the Spring semester, or both. A course can only be registered in a semester in which it is offered. Course overviews state the semesters in which the course is offered. A course offered only in Fall cannot be registered in the Spring semester.

> **[kb/policies/prerequisite_policy.md § Prerequisites]** (sim 0.52) A student may register for a course only if every prerequisite listed for that course has been passed. Prerequisites are cumulative: all listed prerequisites are required, not just one. A course that is currently in progress or was failed does not satisfy a prerequisite.

> **[kb/policies/level_and_availability_policy.md § Academic level restriction]** (sim 0.47) Courses are numbered by academic level from 1 to 4. A student may register only for courses at or below the academic level recorded for the student by the registrar. A level 1 student may not register for level 2, 3 or 4 courses, and a level 2 student may not register for level 3 or 4 courses.

> **[kb/policies/level_and_availability_policy.md § Minimum passed credit hours]** (sim 0.52) Senior courses may require a minimum number of passed credit hours, stated in the course overview. The Capstone Project requires 60 passed credit hours. Professional Ethics and Law in Computing requires 30 passed credit hours.

> **[kb/policies/prerequisite_policy.md § Additional requirements]** (sim 0.39) Some courses require a minimum number of passed credit hours or a minimum cumulative GPA. These requirements are stated in the course overview and must be satisfied at the time of registration.

## 3. Accepted courses

| Course | Title | Credits | Reasons |
|---|---|---|---|
| CS307 | Artificial Intelligence | 3 | Requested by the student and passes every registration rule. Prerequisites satisfied: CS201, MATH201 passed. Offered in Spring; level 3 is within student level 3. Matches your interests/goals: artificial intelligence. |
| CS303 | Computer Networks | 3 | Corequisite of CS303L; must be registered together. Requested by the student and passes every registration rule. Prerequisites satisfied: CS202 passed. Offered in Spring; level 3 is within student level 3. Core degree requirement. Matches your interests/goals: networking. |
| CS301 | Design and Analysis of Algorithms | 3 | Requested by the student and passes every registration rule. Prerequisites satisfied: CS201, MATH102 passed. Offered in Spring; level 3 is within student level 3. Core degree requirement. |
| CS302 | Operating Systems | 3 | Requested by the student and passes every registration rule. Prerequisites satisfied: CS201, CS202 passed. Offered in Spring; level 3 is within student level 3. Core degree requirement. |
| CS305 | Cybersecurity Fundamentals | 3 | Requested by the student and passes every registration rule. Prerequisites satisfied: CS202 passed. Offered in Spring; level 3 is within student level 3. Matches your interests/goals: security. |
| CS303L | Computer Networks Laboratory | 1 | Requested by the student and passes every registration rule. No prerequisites required. Offered in Spring; level 3 is within student level 3. Matches your interests/goals: networking. |

## 4. Rejected courses and reasons

| Course | Title | Rule failed | Reason | Policy source |
|---|---|---|---|---|
| CS204 | Web Application Development | CREDIT_LIMIT_EXCEEDED | adding CS204 (3 credit hours) would bring the load to 19, above the maximum of 18. | kb/policies/credit_load_policy.md § Exceeding the limit |
| CS304 | Machine Learning | CREDIT_LIMIT_EXCEEDED | adding CS304 (3 credit hours) would bring the load to 19, above the maximum of 18. | kb/policies/credit_load_policy.md § Exceeding the limit |
| CS206 | Computer Graphics | NOT_OFFERED_THIS_TERM | CS206 is offered only in Fall, not in Spring. | kb/policies/level_and_availability_policy.md § Semester availability |
| CS306 | Mobile Application Development | PREREQUISITE_UNMET | missing prerequisite(s): CS204. **Hint:** Take CS204 first (eligible now) to work towards CS306. | kb/policies/prerequisite_policy.md § Prerequisites |
| CS407 | Professional Ethics and Law in Computing | LEVEL_RESTRICTION | CS407 is a level 4 course; student is level 3. | kb/policies/level_and_availability_policy.md § Academic level restriction |
| CS405 | Advanced Cybersecurity | LEVEL_RESTRICTION, PREREQUISITE_UNMET | CS405 is a level 4 course; student is level 3; missing prerequisite(s): CS305. **Hint:** Take CS305 first (eligible now) to work towards CS405. | kb/policies/level_and_availability_policy.md § Academic level restriction; kb/policies/prerequisite_policy.md § Prerequisites |
| CS403 | Distributed Systems | LEVEL_RESTRICTION, PREREQUISITE_UNMET | CS403 is a level 4 course; student is level 3; missing prerequisite(s): CS302, CS303. **Hint:** Take CS302, CS303 first (eligible now) to work towards CS403. | kb/policies/level_and_availability_policy.md § Academic level restriction; kb/policies/prerequisite_policy.md § Prerequisites |
| CS406 | Natural Language Processing | LEVEL_RESTRICTION, PREREQUISITE_UNMET | CS406 is a level 4 course; student is level 3; missing prerequisite(s): CS304. **Hint:** Take CS304 first (eligible now) to work towards CS406. | kb/policies/level_and_availability_policy.md § Academic level restriction; kb/policies/prerequisite_policy.md § Prerequisites |
| CS401 | Capstone Project I | LEVEL_RESTRICTION, PREREQUISITE_UNMET, MIN_PASSED_CREDITS | CS401 is a level 4 course; student is level 3; missing prerequisite(s): CS301; requires 60 passed credit hours; student has 42. **Hint:** Take CS301 first (eligible now) to work towards CS401. | kb/policies/level_and_availability_policy.md § Academic level restriction; kb/policies/level_and_availability_policy.md § Minimum passed credit hours; kb/policies/prerequisite_policy.md § Prerequisites |
| CS402 | Deep Learning | LEVEL_RESTRICTION, PREREQUISITE_UNMET, MIN_GPA | CS402 is a level 4 course; student is level 3; missing prerequisite(s): CS304; requires GPA >= 2.5; student GPA is 2.40. **Hint:** Take CS304 first (eligible now) to work towards CS402. | kb/policies/level_and_availability_policy.md § Academic level restriction; kb/policies/prerequisite_policy.md § Additional requirements; kb/policies/prerequisite_policy.md § Prerequisites |
| CS404 | Cloud Computing | NOT_OFFERED_THIS_TERM, LEVEL_RESTRICTION, PREREQUISITE_UNMET | CS404 is offered only in Fall, not in Spring; CS404 is a level 4 course; student is level 3; missing prerequisite(s): CS303. **Hint:** Take CS303 first (eligible now) to work towards CS404. | kb/policies/level_and_availability_policy.md § Academic level restriction; kb/policies/level_and_availability_policy.md § Semester availability; kb/policies/prerequisite_policy.md § Prerequisites |

## 5. Final recommendation

**Register for:** CS307, CS303, CS301, CS302, CS305, CS303L  
**Total:** 16 credit hours (maximum allowed: 18, planned: 18)

- WARNING: Preferred load of 24 credit hours exceeds the maximum of 18 allowed for this student (GPA 2.40 (standard limit)); the plan is capped at 18.
