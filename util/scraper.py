import os
import sys
import urllib2 as urllib
import sqlite3 as sqlite
import BeautifulSoup as bs


# The BeautifulSoup class constructor accepts the HTML to parse, so we will alias
# the class to a new name to make it look like a function.
soupify = bs.BeautifulSoup


# Constant values for attendance field of courseattributes table.
attendance_required = 'required'
attendance_not_specified = 'not specified'
attendance_not_required = 'not required'


queries = {
    # Department information
    'initialize departments table': '''create table if not exists departments(
id integer primary key,
name varchar(32),
campus varchar(32)
)''',
    # Course information
    'initialize courses table': '''create table if not exists courses(
id integer primary key,
title varchar(64),
number integer,
description text
)''',
    # Relates courses to their prerequisite courses
    'initialize prerequisites table': '''create table if not exists prerequisites(
id integer primary key,
foreign key(course_id) references courses(id),
foreign key(prerequisite_id) references courses(id)
)''',
    # Relates courses to their corequisite courses
    'initialize corequisites table': '''create table if not exists corequisites(
id integer primary key,
foreign key(course_id) references courses(id),
foreign key(corequisite_id) references courses(id)
)''',
    # Relates courses to other courses that cannot also provide credit
    'initialize concurrent table': '''create table if not exists concurrent(
id integer primary key,
foreign key(course_id) references courses(id),
foreign key(concurrent_id) references courses(id)
)''',
    # Extra information about courses
    'initialize courseattributes table': '''create table if not exists courseattributes(
id integer primary key,
foreign key(course_id) references courses(id),
attendance varchar(16),
lecture_hours integer,
lab_hours integer,
notes text
)''',
    # Initialize a department
    'create department': 'insert into departments(name, campus) values(?,?)',
    # Insert course information
    'create course': 'insert into courses(title, number, description) values(?,?,?)',
    # Add a course (by id) as a prerequisite to another course (by id)
    'add prerequisite': 'insert into prerequisites(course_id, prerequisite_id) values(?,?)',
    # Add a course (by id) as a corequisite to another course (by id)
    'add corequisite': 'insert into corequisites(course_id, corequisite_id), values(?,?)',
    # Add concurrent course restriction information
    'add concurrent': 'insert into concurrent(course_id, concurrent_id) values(?,?)',
    # Set attributes of a course
    'set course attributes': 'insert into courseattributes(' +
    'course_id, attendance, lecture_hours, lab_hours, notes) values(?,?,?,?,?)',
    # Find a course by title and number
    'find course': 'select * from courses where title=? and number=?'
}


# High level department names as seen in the Table of Contents of the university calendar
# http://www.mun.ca/regoff/calendar/
# TODO: Add information about other campuses.
departments = {
    'Memorial University': [
        'Arts',
        'Business Administration',
        'Education',
        'Engineering and Applied Science',
        'Fisheries and Marine Institute',
        'Human Kinetics and Recreation',
        'Medicine',
        'Music',
        'Nursing',
        'Pharmacy',
        'Science',
        'Social Work'
    ]
}


def initialize_database(dbfile):
    'Initialize a new sqlite database file to store course information in'
    db = sqlite.connect(dbfile)
    db.execute(queries['initialize departments table'])
    db.execute(queries['initialize courses table'])
    db.execute(queries['initialize prerequisites table'])
    db.execute(queries['initialize corequisites table'])
    db.execute(queries['initialize concurrent table'])
    db.execute(queries['initialize courseattributes table'])
    for campus in departments.keys():
        for department in departments[campus]:
            db.execute(queries['create department'], (department, campus))
    db.commit()
    return db


def store_course_information(db, soup):
    'Store information parsed about courses'
    pass


def main():
    if len(sys.argv) != 5:
        print('Run as `python {0} <database file> <campus> <department> <course list URL>`'.format(
            sys.argv[0]))
        return
    dbfile, campus, department, url = sys.argv[1:5]
    dbfile = os.curdir + os.path.sep + dbfile
    if campus not in departments.kes() or department not in departments[campus]:
        print('Campus: {0}, Department: {1} not recognized.\nQuitting.'.format(campus, department))
        return
    try:
        source = urllib.urlopen(url).read()
    except Exception as ex:
        print('Could not open {0}\nError: {1}'.format(url, ex.message))
        return
    if not os.path.isfile(dbfile):
        db = initialize_database(dbfile)
    else:
        db = sqlite.connect(dbfile)
    soup = soupify(source)
    courses = soup.findAll('div', attrs={'class': 'course'})
    store_course_information(db, courses)


if __name__ == '__main__':
    main()
