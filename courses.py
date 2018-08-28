#########
# Python 2.7 script to pull the unique courses, by year and not by year
# Usage: python courses.py INFILE
#########

import pandas as pd
import numpy as np
import sys

# error checking on usage
if len(sys.argv) != 2:
    print ("USAGE: courses.py INFILE\n")
    exit(1)

if sys.argv[1][-4:] != ".csv":
    print (sys.argv[1] +  " must be a .csv file\n")
    exit(2)

inf = open(sys.argv[1], "r")
if not inf:
    print ("Could not open " + sys.argv[1] + "\n")
    exit(3)
inf.close()

df = pd.read_csv(sys.argv[1])
if "course_id" not in list(df):
    print ("Must have column named \"course_id\"\n")
    exit(4)

# strip year information (so CS50 2016 and 2015 are considered the same)
def strip_year(row):
    course = row['course_id']
    s = course.rfind("/")
    course = course[:s]
    d = course.rfind(".")
    s = course.rfind("/")
    if d > s:
        course = course[:d]
    return course

def keep_year_strip_modules(row):
    course = row['course_id']
    s = course.rfind("/")
    acc = course[s:]
    course = course[:s]
    d = course.rfind(".")
    s = course.rfind("/")
    if d > s:
        course = course[:d]
    course += acc
    return course

# now get unique courses
courses = df['course_id'].unique()
courses = pd.DataFrame(courses)
courses.columns = ['course_id']
courses['course_id_no_module'] = courses.apply(lambda row: keep_year_strip_modules(row), axis = 1)
courses = courses['course_id_no_module'].unique()
courses = pd.DataFrame(courses)
courses.columns = ['course_id']
courses.to_csv('courses.csv', index = False)


courses['course_id_no_year'] = courses.apply(lambda row: strip_year(row), axis = 1)
courses_no_year = courses['course_id_no_year'].unique()
courses_no_year = pd.DataFrame(courses_no_year)
courses_no_year.columns = ['course_id_no_year']
courses_no_year.to_csv('courses_no_year.csv', index = False)

