from flask import Flask, render_template, redirect, request
import requests
from difflib import HtmlDiff
from pathlib import Path
import os
import sqlite3

database = sqlite3.connect("database.sqlite3")

# database.execute("DROP TABLE graded_submissions;") # for easy table death
database.execute("CREATE TABLE IF NOT EXISTS graded_submissions (name TEXT);")

app = Flask(__name__)

pathList = []
subFilePath = Path()
for filename in os.scandir(os.path.join(subFilePath.resolve(), 'submissionFileFolder')):
    # print(filename.name)
    pathList.append(filename.name)
pathListIndex = 0
pathListSize = len(pathList)

database.row_factory = lambda cursor, row: row[0]
cursor = database.cursor()
cursor.execute("SELECT name from graded_submissions;")
gradedList = cursor.fetchall()
print(gradedList)
database.commit()
database.close()

# initial_run_check = True

source_file = 'assignment_key.txt'
submission_file = pathList[0]

for i in range(0, pathListSize): #Function for skip to next ungraded student, comment out to disable
    if pathList[i] not in gradedList:
        submission_file = pathList[i]
        pathListIndex = i
        break

# submission_file = 'testFileFolder/' + current_file

@app.route('/')
# def hello():
#     return 'Hello, World!'
def index():
    global source_file
    global submission_file
    global gradedList
    print(gradedList)
    file_1 = open(source_file, 'r')
    file_2 = open('submissionFileFolder/' + submission_file, 'r')
    
    differ = HtmlDiff() 
    diffTable = differ.make_table(file_1, file_2, fromdesc='Provided Assignment Key', todesc=('Student Submission: ' + submission_file), context=True, numlines=2)

    file_1.close() 
    file_2.close() 
    if (all(e in gradedList for e in pathList)):
        return render_template('index.html', diff=diffTable, graded_verifier='All submissions graded! unless something went horribly wrong')
    else:
        return render_template('index.html', diff=diffTable)


@app.route('/diffSubmissionPrev', methods=['POST'])
def prev():
    global submission_file
    global pathList
    global pathListIndex
    # global pathListSize
    if pathListIndex > 0:
        pathListIndex -= 1
        submission_file = pathList[pathListIndex]

    return redirect('/')

@app.route('/diffSubmissionNext', methods=['POST'])
def next():
    global submission_file
    global pathList
    global pathListIndex
    global pathListSize
    if pathListIndex < (pathListSize - 1):
        pathListIndex += 1
        submission_file = pathList[pathListIndex]

    return redirect('/')

@app.route('/postGrade100', methods=['POST'])
def grade100():
    global submission_file
    global gradedList
    database = sqlite3.connect("database.sqlite3")
    
    database.execute(f"INSERT INTO graded_submissions (name) VALUES ('{submission_file}');")
    gradedList.append(submission_file)

    database.commit()
    database.close()

    grade_dict = {
    'problem_key' : 123456789, #default
    'username' : 'poiu1234', #default, needs to read and scrape from submission_file name
    'grade' : 100, #hardcode
    'comments' : "", #hardcode
    }
    print("grade 100!")

    r = requests.post('https://staging.csci3403.com/api/grade/', data=grade_dict)
    
    # print (
    #     r,
    #     r.text,
    #     r.status_code,
    #     r.headers['content-type'],
    # )

    next()
    return redirect('/')

@app.route('/postGradePartial', methods=['POST'])
def gradePartial():
    global submission_file
    global gradedList
    database = sqlite3.connect("database.sqlite3")
    
    database.execute(f"INSERT INTO graded_submissions (name) VALUES ('{submission_file}');")
    gradedList.append(submission_file)

    database.commit()
    database.close()

    grade_dict = {
    'problem_key' : 123456789, #default
    'username' : 'poiu1234', #default
    'grade' : request.form['gradeValue'], #hardcode
    'comments' : request.form['feedbackValue'], #hardcode
    }
    print("partial grade", request.form['gradeValue'])
    print(request.form['feedbackValue'])

    r = requests.post('https://staging.csci3403.com/api/grade/', data=grade_dict)
    
    # print (
    #     r,
    #     r.text,
    #     r.status_code,
    #     r.headers['content-type'],
    # )

    next()
    return redirect('/')
