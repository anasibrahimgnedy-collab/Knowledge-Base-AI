# Test Profile: Karim Samir

**Scenario:** EDGE CASES: probation GPA (limit 12), only 29 passed credits (capstone needs 60, ethics needs 30), GPA below capstone minimum, and a request to repeat a passed course.

## 1. Student input

| Field | Value |
|---|---|
| Academic level | 4 |
| Upcoming term | Spring |
| GPA | 1.8 |
| Passed courses | CS101, MATH101, ENG101, CS103, CS102, MATH102, CS201, CS205, CS301 |
| Skills | java |
| Interests | software engineering, project management |
| Goals | finish the degree and start the capstone |
| Preferred credit load | 18 |
| Requested courses | CS401, CS407, CS101 |

## 2. Retrieved evidence from the Knowledge Base

### 2a. Course passages (retrieved per course)

**CS203 (RECOMMENDED)**
> **[kb/courses/CS203.md § Overview]** (sim 0.56) CS203 Database Systems is a 3-credit-hour core course at academic level 2. It is offered in the Spring semester only. Registration requirements - prerequisites: CS102.

**MATH201 (RECOMMENDED)**
> **[kb/courses/MATH201.md § Overview]** (sim 0.64) MATH201 Probability and Statistics is a 3-credit-hour core course at academic level 2. It is offered in every semester (Fall and Spring). Registration requirements - prerequisites: MATH101.

**MATH202 (RECOMMENDED)**
> **[kb/courses/MATH202.md § Overview]** (sim 0.63) MATH202 Linear Algebra is a 3-credit-hour core course at academic level 2. It is offered in every semester (Fall and Spring). Registration requirements - prerequisites: MATH101.

**HUM101 (RECOMMENDED)**
> **[kb/courses/HUM101.md § Overview]** (sim 0.69) HUM101 Critical Thinking and Society is a 3-credit-hour general education course at academic level 1. It is offered in every semester (Fall and Spring). There are no prerequisites or other registration requirements.

**CS407 (REJECTED)**
> **[kb/courses/CS407.md § Overview]** (sim 0.70) CS407 Professional Ethics and Law in Computing is a 3-credit-hour core course at academic level 4. It is offered in every semester (Fall and Spring). Registration requirements - at least 30 passed credit hours.

**CS401 (REJECTED)**
> **[kb/courses/CS401.md § Overview]** (sim 0.61) CS401 Capstone Project I is a 4-credit-hour core course at academic level 4. It is offered in every semester (Fall and Spring). Registration requirements - prerequisites: CS205, CS301; at least 60 passed credit hours; cumulative GPA of at least 2.0.

**CS302 (REJECTED)**
> **[kb/courses/CS302.md § Overview]** (sim 0.59) CS302 Operating Systems is a 3-credit-hour core course at academic level 3. It is offered in the Spring semester only. Registration requirements - prerequisites: CS201, CS202.

**CS405 (REJECTED)**
> **[kb/courses/CS405.md § Overview]** (sim 0.57) CS405 Advanced Cybersecurity is a 3-credit-hour elective course at academic level 4. It is offered in the Spring semester only. Registration requirements - prerequisites: CS305.

**CS304 (REJECTED)**
> **[kb/courses/CS304.md § Overview]** (sim 0.54) CS304 Machine Learning is a 3-credit-hour elective course at academic level 3. It is offered in the Spring semester only. Registration requirements - prerequisites: CS201, MATH201, MATH202.

### 2b. Policy passages (retrieved for the rules applied)

Credit limit for this student: 12 credit hours.

> **[kb/policies/credit_load_policy.md § Exceeding the limit]** (sim 0.38) A registration that would exceed the maximum credit hours is rejected. Exceptions are not granted by the advising system; students must petition the dean in writing.

> **[kb/policies/level_and_availability_policy.md § Minimum passed credit hours]** (sim 0.52) Senior courses may require a minimum number of passed credit hours, stated in the course overview. The Capstone Project requires 60 passed credit hours. Professional Ethics and Law in Computing requires 30 passed credit hours.

> **[kb/policies/prerequisite_policy.md § Additional requirements]** (sim 0.39) Some courses require a minimum number of passed credit hours or a minimum cumulative GPA. These requirements are stated in the course overview and must be satisfied at the time of registration.

> **[kb/policies/prerequisite_policy.md § Prerequisites]** (sim 0.52) A student may register for a course only if every prerequisite listed for that course has been passed. Prerequisites are cumulative: all listed prerequisites are required, not just one. A course that is currently in progress or was failed does not satisfy a prerequisite.

> **[kb/policies/level_and_availability_policy.md § Semester availability]** (sim 0.58) Each course is offered in the Fall semester, the Spring semester, or both. A course can only be registered in a semester in which it is offered. Course overviews state the semesters in which the course is offered. A course offered only in Fall cannot be registered in the Spring semester.

> **[kb/policies/prerequisite_policy.md § Corequisites]** (sim 0.38) A corequisite must be passed before, or registered in the same semester as, the course that requires it. If the corequisite course is not passed, the student must register for both courses together, and both must be individually eligible.

## 3. Accepted courses

| Course | Title | Credits | Reasons |
|---|---|---|---|
| CS203 | Database Systems | 3 | Prerequisites satisfied: CS102 passed. Offered in Spring; level 2 is within student level 4. Core degree requirement. |
| MATH201 | Probability and Statistics | 3 | Prerequisites satisfied: MATH101 passed. Offered in Spring; level 2 is within student level 4. Core degree requirement. |
| MATH202 | Linear Algebra | 3 | Prerequisites satisfied: MATH101 passed. Offered in Spring; level 2 is within student level 4. Core degree requirement. |
| HUM101 | Critical Thinking and Society | 3 | No prerequisites required. Offered in Spring; level 1 is within student level 4. |

## 4. Rejected courses and reasons

| Course | Title | Rule failed | Reason | Policy source |
|---|---|---|---|---|
| CS407 | Professional Ethics and Law in Computing | MIN_PASSED_CREDITS | requires 30 passed credit hours; student has 29. | kb/policies/level_and_availability_policy.md § Minimum passed credit hours |
| CS401 | Capstone Project I | MIN_PASSED_CREDITS, MIN_GPA | requires 60 passed credit hours; student has 29; requires GPA >= 2.0; student GPA is 1.80. | kb/policies/level_and_availability_policy.md § Minimum passed credit hours; kb/policies/prerequisite_policy.md § Additional requirements |
| CS302 | Operating Systems | PREREQUISITE_UNMET | missing prerequisite(s): CS202. **Hint:** Take CS202 first (eligible now) to work towards CS302. | kb/policies/prerequisite_policy.md § Prerequisites |
| CS405 | Advanced Cybersecurity | PREREQUISITE_UNMET | missing prerequisite(s): CS305. | kb/policies/prerequisite_policy.md § Prerequisites |
| CS304 | Machine Learning | PREREQUISITE_UNMET | missing prerequisite(s): MATH201, MATH202. **Hint:** Take MATH201, MATH202 first (eligible now) to work towards CS304. | kb/policies/prerequisite_policy.md § Prerequisites |
| CS306 | Mobile Application Development | PREREQUISITE_UNMET | missing prerequisite(s): CS204. **Hint:** Take CS204 first (eligible now) to work towards CS306. | kb/policies/prerequisite_policy.md § Prerequisites |
| CS206 | Computer Graphics | NOT_OFFERED_THIS_TERM | CS206 is offered only in Fall, not in Spring. | kb/policies/level_and_availability_policy.md § Semester availability |
| CS303 | Computer Networks | PREREQUISITE_UNMET | missing prerequisite(s): CS202. **Hint:** Take CS202 first (eligible now) to work towards CS303. | kb/policies/prerequisite_policy.md § Prerequisites |
| CS303L | Computer Networks Laboratory | COREQUISITE_UNAVAILABLE | corequisite CS303 cannot be registered (missing prerequisite(s): CS202). | kb/policies/prerequisite_policy.md § Corequisites |
| CS305 | Cybersecurity Fundamentals | PREREQUISITE_UNMET | missing prerequisite(s): CS202. **Hint:** Take CS202 first (eligible now) to work towards CS305. | kb/policies/prerequisite_policy.md § Prerequisites |
| CS307 | Artificial Intelligence | PREREQUISITE_UNMET | missing prerequisite(s): MATH201. **Hint:** Take MATH201 first (eligible now) to work towards CS307. | kb/policies/prerequisite_policy.md § Prerequisites |
| CS403 | Distributed Systems | PREREQUISITE_UNMET | missing prerequisite(s): CS302, CS303. | kb/policies/prerequisite_policy.md § Prerequisites |

_(3 further courses are also ineligible; see the JSON output for the full list.)_

Eligible but not selected (would exceed the planned load):
CS202 (4 cr), CS204 (3 cr)

## 5. Final recommendation

**Register for:** CS203, MATH201, MATH202, HUM101  
**Total:** 12 credit hours (maximum allowed: 12, planned: 12)

- WARNING: Preferred load of 18 credit hours exceeds the maximum of 12 allowed for this student (GPA 1.80 < 2.0 (probation limit)); the plan is capped at 12.
