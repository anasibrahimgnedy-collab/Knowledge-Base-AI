# Test Profile: Nour Fathy

**Scenario:** High-GPA senior eligible for the capstone: requests a Fall-only cloud course (rejected) and an advanced security course.

## 1. Student input

| Field | Value |
|---|---|
| Academic level | 4 |
| Upcoming term | Spring |
| GPA | 3.7 |
| Passed courses | CS101, MATH101, ENG101, HUM101, CS103, CS102, MATH102, CS201, MATH201, MATH202, CS205, CS204, CS202, CS203, CS301, CS303, CS303L, CS302, CS305, CS307 |
| Skills | python, networking, cryptography |
| Interests | cybersecurity, distributed systems, cloud computing |
| Goals | security engineer in a cloud company |
| Preferred credit load | 21 |
| Requested courses | CS404, CS405 |

## 2. Retrieved evidence from the Knowledge Base

### 2a. Course passages (retrieved per course)

**CS405 (RECOMMENDED)**
> **[kb/courses/CS405.md § Overview]** (sim 0.57) CS405 Advanced Cybersecurity is a 3-credit-hour elective course at academic level 4. It is offered in the Spring semester only. Registration requirements - prerequisites: CS305.
> **[kb/courses/CS405.md § Registration notes]** (sim 0.11) Standard registration rules apply; see the registration policies.

**CS403 (RECOMMENDED)**
> **[kb/courses/CS403.md § Overview]** (sim 0.58) CS403 Distributed Systems is a 3-credit-hour elective course at academic level 4. It is offered in the Spring semester only. Registration requirements - prerequisites: CS302, CS303.
> **[kb/courses/CS403.md § Registration notes]** (sim 0.42) Standard registration rules apply; see the registration policies.

**CS407 (RECOMMENDED)**
> **[kb/courses/CS407.md § Overview]** (sim 0.70) CS407 Professional Ethics and Law in Computing is a 3-credit-hour core course at academic level 4. It is offered in every semester (Fall and Spring). Registration requirements - at least 30 passed credit hours.

**CS401 (RECOMMENDED)**
> **[kb/courses/CS401.md § Overview]** (sim 0.61) CS401 Capstone Project I is a 4-credit-hour core course at academic level 4. It is offered in every semester (Fall and Spring). Registration requirements - prerequisites: CS205, CS301; at least 60 passed credit hours; cumulative GPA of at least 2.0.

**CS306 (RECOMMENDED)**
> **[kb/courses/CS306.md § Overview]** (sim 0.62) CS306 Mobile Application Development is a 3-credit-hour elective course at academic level 3. It is offered in the Spring semester only. Registration requirements - prerequisites: CS204.
> **[kb/courses/CS306.md § Description]** (sim 0.04) Designs and builds cross-platform mobile applications with attention to user interface, device sensors and cloud back ends.

**CS304 (RECOMMENDED)**
> **[kb/courses/CS304.md § Overview]** (sim 0.54) CS304 Machine Learning is a 3-credit-hour elective course at academic level 3. It is offered in the Spring semester only. Registration requirements - prerequisites: CS201, MATH201, MATH202.
> **[kb/courses/CS304.md § Description]** (sim 0.03) Introduces supervised and unsupervised learning: linear and logistic regression, decision trees, clustering, neural networks, model evaluation and overfitting, using Python libraries.

**CS404 (REJECTED)**
> **[kb/courses/CS404.md § Overview]** (sim 0.60) CS404 Cloud Computing is a 3-credit-hour elective course at academic level 4. It is offered in the Fall semester only. Registration requirements - prerequisites: CS303.

**CS206 (REJECTED)**
> **[kb/courses/CS206.md § Overview]** (sim 0.61) CS206 Computer Graphics is a 3-credit-hour elective course at academic level 2. It is offered in the Fall semester only. Registration requirements - prerequisites: CS201.

**CS402 (REJECTED)**
> **[kb/courses/CS402.md § Overview]** (sim 0.58) CS402 Deep Learning is a 3-credit-hour elective course at academic level 4. It is offered in the Spring semester only. Registration requirements - prerequisites: CS304; cumulative GPA of at least 2.5.

**CS406 (REJECTED)**
> **[kb/courses/CS406.md § Overview]** (sim 0.67) CS406 Natural Language Processing is a 3-credit-hour elective course at academic level 4. It is offered in the Spring semester only. Registration requirements - prerequisites: CS304.

### 2b. Policy passages (retrieved for the rules applied)

Credit limit for this student: 21 credit hours.

> **[kb/policies/credit_load_policy.md § Exceeding the limit]** (sim 0.38) A registration that would exceed the maximum credit hours is rejected. Exceptions are not granted by the advising system; students must petition the dean in writing.

> **[kb/policies/level_and_availability_policy.md § Semester availability]** (sim 0.58) Each course is offered in the Fall semester, the Spring semester, or both. A course can only be registered in a semester in which it is offered. Course overviews state the semesters in which the course is offered. A course offered only in Fall cannot be registered in the Spring semester.

> **[kb/policies/prerequisite_policy.md § Prerequisites]** (sim 0.52) A student may register for a course only if every prerequisite listed for that course has been passed. Prerequisites are cumulative: all listed prerequisites are required, not just one. A course that is currently in progress or was failed does not satisfy a prerequisite.

## 3. Accepted courses

| Course | Title | Credits | Reasons |
|---|---|---|---|
| CS405 | Advanced Cybersecurity | 3 | Requested by the student and passes every registration rule. Prerequisites satisfied: CS305 passed. Offered in Spring; level 4 is within student level 4. Matches your interests/goals: cybersecurity. |
| CS403 | Distributed Systems | 3 | Prerequisites satisfied: CS302, CS303 passed. Offered in Spring; level 4 is within student level 4. Matches your interests/goals: distributed systems, cloud computing. |
| CS407 | Professional Ethics and Law in Computing | 3 | No prerequisites required. Offered in Spring; level 4 is within student level 4. Core degree requirement. Matches your interests/goals: cloud computing. |
| CS401 | Capstone Project I | 4 | Prerequisites satisfied: CS205, CS301 passed. Offered in Spring; level 4 is within student level 4. Core degree requirement. |
| CS306 | Mobile Application Development | 3 | Prerequisites satisfied: CS204 passed. Offered in Spring; level 3 is within student level 4. |
| CS304 | Machine Learning | 3 | Prerequisites satisfied: CS201, MATH201, MATH202 passed. Offered in Spring; level 3 is within student level 4. Matches your interests/goals: python. |

## 4. Rejected courses and reasons

| Course | Title | Rule failed | Reason | Policy source |
|---|---|---|---|---|
| CS404 | Cloud Computing | NOT_OFFERED_THIS_TERM | CS404 is offered only in Fall, not in Spring. | kb/policies/level_and_availability_policy.md § Semester availability |
| CS206 | Computer Graphics | NOT_OFFERED_THIS_TERM | CS206 is offered only in Fall, not in Spring. | kb/policies/level_and_availability_policy.md § Semester availability |
| CS402 | Deep Learning | PREREQUISITE_UNMET | missing prerequisite(s): CS304. **Hint:** Take CS304 first (eligible now) to work towards CS402. | kb/policies/prerequisite_policy.md § Prerequisites |
| CS406 | Natural Language Processing | PREREQUISITE_UNMET | missing prerequisite(s): CS304. **Hint:** Take CS304 first (eligible now) to work towards CS406. | kb/policies/prerequisite_policy.md § Prerequisites |

## 5. Final recommendation

**Register for:** CS405, CS403, CS407, CS401, CS306, CS304  
**Total:** 19 credit hours (maximum allowed: 21, planned: 21)

