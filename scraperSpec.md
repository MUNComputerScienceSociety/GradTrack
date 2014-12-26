**From the README:**

>A mechanism will have to be created to, ideally automatically, fetch course information en masse.
>Course information and graduation requirements should be updated fairly regularly and be easily
>accessible from the main application. To accomplish this, a 
>[web scraper](http://en.wikipedia.org/wiki/Web_scraping) should be implemented in the
>[Python (version 2.7)](https://wiki.python.org/moin/BeginnersGuide/Programmers) programming language,
>which is used in a number of courses at Memorial University.

# Requirements

1. Parse course information to associate courses with their attributes
    1. Break apart blocks of HTML into relevant sections
    2. Associate attribute codes (AR, PR, CO, ...) with attribute names
    3. Prevent unnecessary overwriting of existing data
    4. Create course and attribute relation instances
2. Build relations between courses that are prerequisites, corequisites, or concurrent
    1. Parse the list of requisite course identifiers
    2. Translate common names (e.g. Chemistry) into identifiers (e.g. CHEM)
    3. Create relations between new courses and their requisite courses
        1. Ask for the page containing information about courses not already in the database
        2. It may also be possible to simple follow course links to get information
3. Organize couse information into the database for convenient retrieval

# Relevant information

Field         | Example
--------------|------------------------------------
Title         | General Physics II
Department    | PHYS
Number        | 1051
Description   | A calculus based introduction to...
Lecture Hours | 3
Lab Hours     | 3
Attendance    | Not Required
Other Hours   | 0
Prerequisites | PHYS 1050, MATH 1001
Corequisites  | MATH 1001
Concurrent    | None
Notes         | None

# Explanation

The phrase *concurrent course* refers to a course for which a student cannot earn credit for as well as a given course. Certain departments have their own equivalent of courses taught in other departments, and students cannot earn credit for both.

A *corequisite* for a course is a course that contains content required for the given course but which can be taken at the same time rather than strictly before it.

A *prerequisite* for a course is a course that must be successfully completed before the course in question.

Many course listings do not contain information about all of the fields listed above, so the scraper must supply default values in such cases.