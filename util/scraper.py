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
name varchar(32),
campus varchar(32)
)''',
    # Course information
    'initialize courses table': '''create table if not exists courses(
title varchar(64),
number integer,
description text
)''',
    # Relates courses to their prerequisite courses
    'initialize prerequisites table': '''create table if not exists prerequisites(
foreign key(course_id) references courses(id),
foreign key(prerequisite_id) references courses(id)
)''',
    # Relates courses to their corequisite courses
    'initialize corequisites table': '''create table if not exists corequisites(
foreign key(course_id) references courses(id),
foreign key(corequisite_id) references courses(id)
)''',
    # Relates courses to other courses that cannot also provide credit
    'initialize concurrent table': '''create table if not exists concurrent(
foreign key(course_id) references courses(id),
foreign key(corequisite_id) references courses(id)
)''',
    # Extra information about courses
    'initialize courseattributes table': '''create table if not exists courseattributes(
foreign key(course_id) references courses(id),
attendance varchar(16),
lecture_hours integer,
lab_hours integer,
notes text
)''',
    # Initialize a department
    'create department': 'insert into departments values(?,?)'
}


# High level department names as seen in the Table of Contents of the university calendar
# http://www.mun.ca/regoff/calendar/
mun_departments = [
    "Arts",
    "Business Administration",
    "Education",
    "Engineering and Applied Science",
    "Fisheries and Marine Institute",
    "Human Kinetics and Recreation",
    "Medicine",
    "Music",
    "Nursing",
    "Pharmacy",
    "Science",
    "Social Work"
]


def initialize_database(dbfile):
    "Initialize a new sqlite database file to store course information in"
    db = sqlite.connect(dbfile)
    db.execute(queries['initialize departments table'])
    db.execute(queries['initialize courses table'])
    db.execute(queries['initialize prerequisites table'])
    db.execute(queries['initialize corequisites table'])
    db.execute(queries['initialize concurrent table'])
    db.execute(queries['initialize courseattributes table'])
    for department in mun_departments:
        db.execute(queries['create department'], (department, 'Memorial University'))
    # TODO: Extend this to include Grenfell and other departments
    db.commit()
    return db


def main():
    if len(sys.argv) != 4:
        print('Run as `python {0} <database file> <faculty> <course list URL>`'.format(sys.argv[0]))
        return
    dbfile, faculty, url = sys.argv[1], sys.argv[2], sys.argv[3]
    try:
        source = urllib.urlopen(url).read()
    except Exception as ex:
        print('Could not open {0}\nError: {1}'.format(url, ex.message))
        return
    soup = soupify(source)
    courses = soup.findAll('div', attrs={'class': 'course'})
    return courses