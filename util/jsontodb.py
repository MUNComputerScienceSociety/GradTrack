'''This utility exists to convert the files that describe the courses in each
department at MUN into a SQLite database so that information can be easily
retrieved later.
Note that two sets of courses such as "Engineering One" and "Engineering Work Terms"
are treated as separate departments to make searching easier. Of course, they should
still share the same identifier, "ENGI" in this case, so they are stll related.
'''

import sqlite3 as sqlite
from json import loads as from_json
import sys
import os


# Attributes of courses that do not belong in the `attributes` table
special_attributes = [
    'courseTitle',
    'courseNumber',
    'courseDescription',
    'prerequisites',
    'corequisites',
    'concurrent'
]


queries = {
    # Department information | identifier is a string like "BIOL"
    'initialize departments table': '''create table if not exists departments(
id integer primary key,
name text,
identifier varchar(8)
)''',
    # Course information
    'initialize courses table': '''create table if not exists courses(
id integer primary key,
department_id integer,
identifier varchar(16),
title varchar(128),
number varchar(16),
description text,
foreign key(department_id) references departments(id)
)''',
    # Relates courses to their prerequisite courses
    'initialize prerequisites table': '''create table if not exists prerequisites(
id integer primary key,
course_id integer,
prerequisite_id integer,
foreign key(course_id) references courses(id),
foreign key(prerequisite_id) references courses(id)
)''',
    # Relates courses to their corequisite courses
    'initialize corequisites table': '''create table if not exists corequisites(
id integer primary key,
course_id integer,
corequisite_id integer,
foreign key(course_id) references courses(id),
foreign key(corequisite_id) references courses(id)
)''',
    # Relates courses to other courses that cannot also provide credit
    'initialize concurrent table': '''create table if not exists concurrent(
id integer primary key,
course_id integer,
concurrent_id integer,
foreign key(course_id) references courses(id),
foreign key(concurrent_id) references courses(id)
)''',
    # Extra information about courses
    'initialize attributes table': '''create table if not exists attributes(
id integer primary key,
course_id integer,
name varchar(4),
value text,
foreign key(course_id) references courses(id)
)''',
    # Initialize a department
    'create department': 'insert into departments(name, identifier) values(?, ?)',
    # Insert course information
    'create course': 'insert into courses(department_id, identifier, title, number, description) ' +
    'values(?,?,?,?,?)',
    # Add a course (by id) as a prerequisite to another course (by id)
    'add prerequisite': 'insert into prerequisites(course_id, prerequisite_id) values(?,?)',
    # Add a course (by id) as a corequisite to another course (by id)
    'add corequisite': 'insert into corequisites(course_id, corequisite_id) values(?,?)',
    # Add concurrent course restriction information
    'add concurrent': 'insert into concurrent(course_id, concurrent_id) values(?,?)',
    # Set an attribute of a course
    'set course attribute': 'insert into attributes(course_id, name, value) values(?,?,?)',
    # Find a course by identifier
    'find course by identifier': 'select * from courses where identifier=?',
    # Find a department by its name
    'find department by name': 'select * from departments where name=?',
    # Find a department by its identifier code
    'find department by identifier': 'select * from departments where identifier=?'
}


def initialize_database(dbfile):
    'Initialize a new sqlite database file to store course information in'
    db = sqlite.connect(dbfile)
    db.execute(queries['initialize departments table'])
    db.execute(queries['initialize courses table'])
    db.execute(queries['initialize prerequisites table'])
    db.execute(queries['initialize corequisites table'])
    db.execute(queries['initialize concurrent table'])
    db.execute(queries['initialize attributes table'])
    db.commit()
    return db


def store_department_information(db, name, identifier):
    'Stores information about a department'
    # Check if the department exists already
    res = db.execute(queries['find department by name'], (name,))
    department = res.fetchone()
    if department is None:
        db.execute(queries['create department'], (name, identifier))
        res = db.execute(queries['find department by name'], (name,))
        department = res.fetchone()
    deptid = department[0]
    return deptid


def store_course_information(db, department_id, identifier, course):
    'Stores information about a course with a given identifier'
    # Check if the course already exists
    res = db.execute(queries['find course by identifier'], (identifier,))
    course_data = res.fetchone()
    if course_data is None:
        db.execute(
            queries['create course'],
            (department_id, identifier, course['courseTitle'],
                course['courseNumber'], course['courseDescription']))
        res = db.execute(queries['find course by identifier'], (identifier,))
        course_data = res.fetchone()
    course_id = course_data[0]
    # Store course attributes other than established prereqs, coreqs, and concurrent courses
    for attr in course:
        if attr not in special_attributes:
            db.execute(queries['set course attribute'], (course_id, attr, course[attr]))


def store_information(db, filenames):
    'Store the information about courses in a list of json files'
    for filename in filenames:
        data = from_json(open(filename).read())
        dept_id = store_department_information(db, data['name'], data['identifier'])
        for identifier in data['courses']:
            store_course_information(db, dept_id, identifier, data['courses'][identifier])


def build_course_relations(db, filenames):
    'Create relations between courses and their prerequisites and so on'
    for filename in filenames:
        data = from_json(open(filename).read())
        for course_ident in data['courses']:
            res = db.execute(queries['find course by identifier'], (course_ident,))
            course_id = res.fetchone()[0]
            for prereq_ident in data['courses'][course_ident]['prerequisites']:
                res = db.execute(queries['find course by identifier'], (prereq_ident,))
                prereq = res.fetchone()
                if prereq is not None:
                    prereq_id = prereq[0]
                    db.execute(queries['add prerequisite'], (course_id, prereq_id))
            for coreq_ident in data['courses'][course_ident]['corequisites']:
                res = db.execute(queries['find course by identifier'], (coreq_ident,))
                coreq = res.fetchone()
                if coreq is not None:
                    coreq_id = coreq[0]
                    db.execute(queries['add corequisite'], (course_id, coreq_id))
            for concur_ident in data['courses'][course_ident]['concurrent']:
                res = db.execute(queries['find course by identifier'], (concur_ident,))
                concur = res.fetchone()
                if concur is not None:
                    concur_id = concur[0]
                    db.execute(queries['add concurrent'], (course_id, concur_id))


def main():
    if len(sys.argv) != 3:
        print 'Run as `python {0} <json file directory> <database file>`'.format(sys.argv[0])
        return
    directory, dbfile = sys.argv[1:3]
    if not os.path.isfile(dbfile):
        db = initialize_database(dbfile)
    else:
        db = sqlite.connect(dbfile)
    filenames = [os.path.sep.join([directory, fname])
                 for fname in os.listdir(directory) if fname.endswith('.json')]
    # Do one pass through the course files to add all the courses to the database
    print 'Adding course information to the database.'
    store_information(db, filenames)
    db.commit()
    # Do another pass to build associations between courses and pre/corequisites etc.
    print 'Building relations between courses.'
    build_course_relations(db, filenames)
    db.commit()
    db.close()
    print 'Done'


if __name__ == '__main__':
    main()
